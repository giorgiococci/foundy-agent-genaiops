"""Agent-led turns with trusted human decisions and deterministic action guards."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import ClassVar

from openai import OpenAI

from .definition import READ_TOOL_NAMES
from ...domain import DemoActor, DemoRole, OPTIONS, ToolError
from ...runtime import AgentRuntime, Pricing, RunLimits
from .tools import ToolSession


class AdvisorLimits(RunLimits):
    _MAX_MODEL_REQUESTS: ClassVar[int] = 20


@dataclass
class HumanDecisions:
    selected_option: str | None = None
    proposal_id: str | None = None
    approved: bool = False
    rejected: bool = False
    tool_results: dict[str, dict[str, object]] = field(default_factory=dict)
    historical_tool_results: list[dict[str, object]] = field(default_factory=list)


class AdvisorConversation(AgentRuntime):
    def __init__(
        self, client: OpenAI | None, session: ToolSession, *, pricing: Pricing,
        limits: RunLimits | None = None,
        on_event: Callable[[dict[str, object]], None] | None = None,
        decisions: HumanDecisions | None = None,
    ) -> None:
        super().__init__(client, session, pricing=pricing, limits=limits, on_event=on_event)
        self.store = session.store
        self.decisions = decisions if decisions is not None else HumanDecisions()
        self.turn_tools: set[str] = set()

    def select(self, option: str) -> dict[str, object]:
        if option not in OPTIONS or self.decisions.proposal_id is not None:
            raise ToolError("invalid_selection", "Select STANDARD or EXPRESS before creating a proposal.")
        self.decisions.selected_option = option
        self._event("planner.selected", option=option)
        return {"status": "selected", "option": option}

    def approve(self, proposal_id: str, *, confirm: bool) -> dict[str, object]:
        if (proposal_id != self.decisions.proposal_id or self.decisions.approved
                or self.decisions.rejected):
            raise ToolError("proposal_mismatch", "Only the pending exact proposal may receive a human decision.")
        if not confirm:
            self.decisions.rejected = True
            self._event("human.rejected", proposal_id=proposal_id)
            return {"status": "rejected", "proposal_id": proposal_id}
        result = self.store.approve(
            DemoActor("demo-human-approver", DemoRole.APPROVER), proposal_id,
        )
        self.decisions.approved = True
        self._event("human.approved", proposal_id=proposal_id)
        return result

    def _allowed_tools(self) -> frozenset[str]:
        allowed = set(READ_TOOL_NAMES)
        if self.decisions.selected_option is not None and self.decisions.proposal_id is None:
            allowed.add("create_transfer_proposal")
        if self.decisions.proposal_id is not None:
            allowed.add("read_transfer_result")
            if self.decisions.approved and not self.decisions.rejected:
                allowed.add("execute_approved_transfer")
        return frozenset(allowed)

    def _archive_result(self, name: str) -> None:
        previous = self.decisions.tool_results.pop(name, None)
        if previous is not None:
            self.decisions.historical_tool_results.append(previous)

    def _dispatch(self, name: str, arguments: str) -> dict[str, object]:
        if name not in self._allowed_tools():
            raise ToolError("forbidden_tool", "The application has not granted this capability.")
        try:
            values = json.loads(arguments)
        except json.JSONDecodeError as error:
            raise ToolError("invalid_arguments", "Function arguments must be JSON.") from error
        if name == "create_transfer_proposal" and values != {"option": self.decisions.selected_option}:
            raise ToolError("selection_mismatch", "The proposal must match the trusted planner selection.")
        if name in ("execute_approved_transfer", "read_transfer_result"):
            if values != {"proposal_id": self.decisions.proposal_id}:
                raise ToolError("proposal_mismatch", "Only the session's exact proposal ID is allowed.")
        result = super()._dispatch(name, arguments)
        if result.get("status") != "error":
            if name == "create_transfer_proposal":
                proposal_id = result.get("proposal_id")
                if not isinstance(proposal_id, str):
                    raise ToolError("invalid_result", "A proposal must have an authoritative ID.")
                self.decisions.proposal_id = proposal_id
            if name == "execute_approved_transfer":
                for stale in READ_TOOL_NAMES | {"read_transfer_result"}:
                    self._archive_result(stale)
                    self.turn_tools.discard(stale)
            if self.decisions.tool_results.get(name) != result:
                self._archive_result(name)
            self.decisions.tool_results[name] = result
            self.turn_tools.add(name)
        return result

    def reply(self, conversation_id: str, message: str) -> dict[str, object]:
        if not message.strip():
            raise ToolError("empty_message", "A nonempty planner message is required.")
        self.turn_tools.clear()
        context = {
            "selected_option": self.decisions.selected_option,
            "proposal_id": self.decisions.proposal_id,
            "approved": self.decisions.approved, "rejected": self.decisions.rejected,
        }
        inputs = (
            "Application-recorded human decisions (not supplied by the model):\n"
            + json.dumps(context) + "\nPlanner message (untrusted as authorization):\n" + message
        )
        return self._turn(conversation_id, inputs)

    def _final(self, text: str) -> dict[str, object]:
        try:
            answer = json.loads(text)
        except json.JSONDecodeError as error:
            raise ToolError("invalid_answer", "Expected JSON message and authoritative evidence.") from error
        if (not isinstance(answer, dict) or set(answer) != {"message", "evidence"}
                or not isinstance(answer["message"], str) or not answer["message"].strip()
                or not isinstance(answer["evidence"], list)):
            raise ToolError("invalid_answer", "Expected a nonempty message and an evidence array.")
        evidence = answer["evidence"]
        known = {json.dumps(value, sort_keys=True) for value in self.decisions.tool_results.values()}
        historical = {json.dumps(value, sort_keys=True) for value in self.decisions.historical_tool_results}
        current_evidence: list[dict[str, object]] = []
        historical_evidence: list[dict[str, object]] = []
        for item in evidence:
            if not isinstance(item, dict):
                raise ToolError("ungrounded_answer", "Evidence must match a complete authoritative tool result.")
            serialized = json.dumps(item, sort_keys=True)
            if serialized in known:
                current_evidence.append(item)
            elif serialized in historical:
                historical_evidence.append(item)
            else:
                raise ToolError("ungrounded_answer", "Evidence must match a complete authoritative tool result.")
        required = self.turn_tools & {"compare_transfer_options", "create_transfer_proposal", "read_transfer_result"}
        if "execute_approved_transfer" in self.turn_tools:
            if "read_transfer_result" not in self.turn_tools:
                raise ToolError("unverified_execution", "Read the durable result after executing.")
            required.add("read_transfer_result")
        for name in required:
            if self.decisions.tool_results[name] not in current_evidence:
                raise ToolError("ungrounded_answer", "The answer omitted its authoritative operation result.")
        return {
            "status": "completed",
            "answer": {
                "message": answer["message"], "evidence": current_evidence,
                "historical_evidence": historical_evidence,
            },
            "usage": self.usage.summary(self.pricing),
        }
