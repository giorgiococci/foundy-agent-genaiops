"""Agent-led turns with trusted human decisions and deterministic action guards."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Callable
from dataclasses import asdict, dataclass, field

from agent_framework import AgentResponse, AgentResponseUpdate, AgentSession, Content, Message, MiddlewareFailure
from agent_framework.foundry import FoundryAgent

from .definition import READ_TOOL_NAMES
from ...domain import DemoActor, DemoRole, OPTIONS, ToolError
from ...runtime import Pricing, RunLimits, RunSafety, RunUsage
from ...observability import TelemetryPolicy, agent_trace, capture_content
from .tools import HUMAN_TOOL_NAMES, ToolSession, human_arguments


DEFAULT_TELEMETRY_POLICY = TelemetryPolicy("content")


@dataclass
class HumanRequest:
    call_id: str
    name: str
    arguments: dict[str, str]
    evidence: dict[str, object]
    receipt: dict[str, object] | None = None
    consumed: bool = False


@dataclass
class HumanDecisions:
    selected_option: str | None = None
    proposal_id: str | None = None
    approved: bool = False
    rejected: bool = False
    tool_results: dict[str, dict[str, object]] = field(default_factory=dict)
    historical_tool_results: list[dict[str, object]] = field(default_factory=list)
    pending: HumanRequest | None = None
    human_history: list[HumanRequest] = field(default_factory=list)


class AdvisorConversation:
    def __init__(
        self, session: ToolSession, *, pricing: Pricing,
        limits: RunLimits | None = None,
        on_event: Callable[[dict[str, object]], None] | None = None,
        decisions: HumanDecisions | None = None,
        usage: RunUsage | None = None, seen_call_ids: set[str] | None = None,
        telemetry_policy: TelemetryPolicy = DEFAULT_TELEMETRY_POLICY,
    ) -> None:
        self.session = session
        self.store = session.store
        self.decisions = decisions if decisions is not None else HumanDecisions()
        self.turn_tools: set[str] = set()
        self.telemetry_policy = telemetry_policy
        self.safety = RunSafety(
            pricing=pricing, limits=limits, validate_call=self._validate_call,
            usage=usage, seen_call_ids=seen_call_ids, on_event=on_event,
            human_tool_names=HUMAN_TOOL_NAMES,
        )

    def _human_evidence(self, name: str, arguments: dict[str, str]) -> dict[str, object]:
        state = self.decisions
        if state.pending is not None and not state.pending.consumed:
            raise ToolError("human_input_pending", "Resolve the current native human request first.")
        if name == "request_transfer_choice":
            value = state.tool_results.get("compare_transfer_options")
            valid = (state.selected_option is None and state.proposal_id is None and value is not None
                     and value.get("status") == "options_available")
        else:
            value = state.tool_results.get("create_transfer_proposal")
            valid = (state.proposal_id == arguments["proposal_id"] and value is not None
                     and value.get("status") == "proposed" and not state.approved and not state.rejected)
        snapshot = self.store.read_snapshot(self.session.actor)
        if (not valid or value is None
                or value.get("snapshot_version") != snapshot["snapshot_version"]
                or value.get("policy_version") != snapshot["policy_version"]):
            raise ToolError("decision_not_available", "A current authoritative comparison/proposal is required.")
        return value

    def respond(self, call_id: str, *, option: str | None = None,
                proposal_id: str | None = None, confirm: bool | None = None) -> dict[str, object]:
        pending = self.decisions.pending
        if pending is None:
            raise ToolError("decision_not_available", "There is no native human request.")
        if pending.call_id != call_id:
            raise ToolError("human_request_mismatch", "The response belongs to another native request.")
        expected = ({"status": "selected", "option": option} if pending.name == "request_transfer_choice"
                    else {"status": "approved" if confirm else "rejected", "proposal_id": proposal_id})
        if pending.receipt is not None:
            if pending.consumed or any(pending.receipt.get(key) != value for key, value in expected.items()):
                raise ToolError("human_response_conflict", "This native request already received a different or consumed response.")
            return pending.receipt
        snapshot = self.store.read_snapshot(self.session.actor)
        if any(pending.evidence.get(key) != snapshot[key] for key in ("snapshot_version", "policy_version")):
            raise ToolError("stale_human_request", "Facts changed since this question; no decision was recorded.")
        if pending.name == "request_transfer_choice":
            if option is None or proposal_id is not None or confirm is not None:
                raise ToolError("invalid_selection", "Supply only a feasible option.")
            options = pending.evidence.get("options")
            if (not isinstance(options, list) or not any(
                isinstance(item, dict) and item.get("option") == option and item.get("feasible") is True
                for item in options
            )):
                raise ToolError("invalid_selection", "Select an authoritative feasible option.")
            result = self.select(option)
        else:
            if (option is not None or confirm is None
                    or proposal_id != pending.arguments["proposal_id"]):
                raise ToolError("proposal_mismatch", "An explicit decision on the exact proposal is required.")
            result = self.approve(proposal_id, confirm=confirm)
        pending.receipt = {**result, "tool_call_id": call_id}
        self.safety.event("human.responded", call_id=call_id, status=pending.receipt["status"])
        return pending.receipt

    def continuation(self) -> Message:
        pending = self.decisions.pending
        if pending is None or pending.receipt is None or pending.consumed:
            raise ToolError("invalid_continuation", "A saved, unconsumed human response is required.")
        pending.consumed = True
        self.turn_tools.clear()
        self.safety.event("human.continuation", call_id=pending.call_id)
        return Message("tool", [Content.from_function_result(
            pending.call_id, result=json.dumps(pending.receipt),
        )])

    def _complete(self, result: AgentResponse) -> dict[str, object]:
        requests = [content for message in result.messages for content in message.contents
                    if content.type == "function_call" and content.user_input_request]
        if requests:
            if len(requests) != 1:
                raise ToolError("invalid_human_batch", "Expected one native human request.")
            call = requests[0]
            if (call.name not in HUMAN_TOOL_NAMES or not call.call_id
                    or self.safety.pending_calls.get(call.call_id) != call.name
                    or call.call_id in self.safety.seen_call_ids):
                raise ToolError("invalid_call_id", "Unvalidated native human request.")
            arguments = human_arguments(call.name, call.arguments if isinstance(call.arguments, str)
                                        else json.dumps(call.arguments))
            evidence = self._human_evidence(call.name, arguments)
            if self.decisions.pending is not None:
                self.decisions.human_history.append(self.decisions.pending)
            self.decisions.pending = HumanRequest(call.call_id, call.name, arguments, evidence)
            self.safety.seen_call_ids.add(call.call_id)
            self.safety.usage.tool_calls += 1
            self.safety.event("human.requested", call_id=call.call_id, tool=call.name)
            return {
                "status": "awaiting_human",
                "answer": {"message": arguments["question"], "evidence": [evidence], "historical_evidence": []},
                "human_request": asdict(self.decisions.pending),
                "usage": self.safety.usage.summary(self.safety.pricing),
            }
        if not result.messages or result.messages[-1].role != "assistant":
            raise ToolError("invalid_answer", "Expected a final assistant answer or native human request.")
        return self._final(result.messages[-1].text)

    def invoke_tool(self, name: str, **arguments: object) -> dict[str, object]:
        return self._dispatch(name, json.dumps(arguments))

    def select(self, option: str) -> dict[str, object]:
        if option not in OPTIONS or self.decisions.proposal_id is not None:
            raise ToolError("invalid_selection", "Select STANDARD or EXPRESS before creating a proposal.")
        self.decisions.selected_option = option
        self.safety.event("planner.selected", option=option)
        return {"status": "selected", "option": option}

    def approve(self, proposal_id: str, *, confirm: bool) -> dict[str, object]:
        if (proposal_id != self.decisions.proposal_id or self.decisions.approved
                or self.decisions.rejected):
            raise ToolError("proposal_mismatch", "Only the pending exact proposal may receive a human decision.")
        if not confirm:
            self.decisions.rejected = True
            self.safety.event("human.rejected", proposal_id=proposal_id)
            return {"status": "rejected", "proposal_id": proposal_id}
        result = self.store.approve(
            DemoActor("demo-human-approver", DemoRole.APPROVER), proposal_id,
        )
        self.decisions.approved = True
        self.safety.event("human.approved", proposal_id=proposal_id)
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

    def _validate_call(self, name: str, arguments: str) -> None:
        if name in HUMAN_TOOL_NAMES:
            self._human_evidence(name, human_arguments(name, arguments))
            return
        if name not in self._allowed_tools():
            raise ToolError("forbidden_tool", "The application has not granted this capability.")
        values = self.session.validate_arguments(name, arguments)
        if name == "create_transfer_proposal" and values != {"option": self.decisions.selected_option}:
            raise ToolError("selection_mismatch", "The proposal must match the trusted planner selection.")
        if name in ("execute_approved_transfer", "read_transfer_result"):
            if values != {"proposal_id": self.decisions.proposal_id}:
                raise ToolError("proposal_mismatch", "Only the session's exact proposal ID is allowed.")

    def _dispatch(self, name: str, arguments: str) -> dict[str, object]:
        self._validate_call(name, arguments)
        result = self.session.dispatch(name, arguments)
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

    def inputs(self, message: str) -> str:
        if self.decisions.pending is not None and not self.decisions.pending.consumed:
            raise ToolError("human_input_pending", "Resolve the native human request before sending a new question.")
        if not message.strip():
            raise ToolError("empty_message", "A nonempty planner message is required.")
        self.turn_tools.clear()
        context = {
            "selected_option": self.decisions.selected_option,
            "proposal_id": self.decisions.proposal_id,
            "approved": self.decisions.approved, "rejected": self.decisions.rejected,
        }
        return (
            "Application-recorded human decisions (not supplied by the model):\n"
            + json.dumps(context) + "\nPlanner message (untrusted as authorization):\n" + message
        )
    async def stream(
        self, agent: FoundryAgent, framework_session: AgentSession, message: str | Message,
        completed: Callable[[dict[str, object]], None],
        *, native_completed: Callable[[AgentResponse], None] | None = None,
    ) -> AsyncIterator[AgentResponseUpdate]:
        inputs = self.inputs(message) if isinstance(message, str) else message
        with agent_trace(
            self.telemetry_policy, agent_name=agent.name, agent_id=agent.id,
            run_id=framework_session.session_id, conversation_id=framework_session.service_session_id,
        ) as span:
            if span.is_recording():
                self.safety.event(
                    "telemetry.started", trace_id=format(span.get_span_context().trace_id, "032x"),
                    mode=self.telemetry_policy.mode,
                )
            capture_content("gen_ai.input.messages", [
                {"role": "user", "content": inputs} if isinstance(inputs, str) else inputs.to_dict(),
            ])
            try:
                async with agent.run(inputs, session=framework_session, stream=True) as updates:
                    async for update in updates:
                        yield update
                    result = await updates.get_final_response()
                answer = self._complete(result)
                capture_content("gen_ai.output.messages", [{"role": "assistant", "content": answer["answer"]}])
                if span.is_recording():
                    answer["telemetry"] = {
                        "trace_id": format(span.get_span_context().trace_id, "032x"),
                        "mode": self.telemetry_policy.mode,
                    }
                if native_completed is not None:
                    native_completed(result)
                completed(answer)
            except MiddlewareFailure as error:
                if self.safety.failure is not None:
                    raise self.safety.failure from error
                raise

    async def reply(self, agent: FoundryAgent, framework_session: AgentSession, message: str | Message) -> dict[str, object]:
        inputs = self.inputs(message) if isinstance(message, str) else message
        with agent_trace(
            self.telemetry_policy, agent_name=agent.name, agent_id=agent.id,
            run_id=framework_session.session_id, conversation_id=framework_session.service_session_id,
        ) as span:
            if span.is_recording():
                self.safety.event(
                    "telemetry.started", trace_id=format(span.get_span_context().trace_id, "032x"),
                    mode=self.telemetry_policy.mode,
                )
            capture_content("gen_ai.input.messages", [
                {"role": "user", "content": inputs} if isinstance(inputs, str) else inputs.to_dict(),
            ])
            try:
                result = await agent.run(inputs, session=framework_session)
            except MiddlewareFailure as error:
                if self.safety.failure is not None:
                    raise self.safety.failure from error
                raise
            answer = self._complete(result)
            capture_content("gen_ai.output.messages", [{"role": "assistant", "content": answer["answer"]}])
            if span.is_recording():
                answer["telemetry"] = {
                    "trace_id": format(span.get_span_context().trace_id, "032x"),
                    "mode": self.telemetry_policy.mode,
                }
            return answer

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
            "usage": self.safety.usage.summary(self.safety.pricing),
        }
