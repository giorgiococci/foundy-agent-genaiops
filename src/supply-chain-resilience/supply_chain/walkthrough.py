"""Human-gated live demo stages sharing the bounded managed-agent loop."""

from __future__ import annotations

import json

from azure.ai.projects.models import FunctionTool, PromptAgentDefinition

from .domain import DemoActor, DemoRole, ToolError
from .foundry import INSTRUCTIONS, PROMPT, READ_TOOL_NAMES, ReadOnlyAgentLoop
from .tools import FUNCTION_TOOL_SPECS


WORKFLOW_INSTRUCTIONS = INSTRUCTIONS.replace(
    "Do not create a proposal, approve anything or execute a transfer.",
    """During comparison do not create or execute anything.
After the planner explicitly selects an option, call create_transfer_proposal
once with that exact option. Return the complete tool result as JSON, unchanged.
Stop for human approval outside the model. Never claim or create approval.
Only after the application says human approval is recorded, call
execute_approved_transfer for that exact proposal ID, then read_transfer_result
for the same ID. Return the complete read_transfer_result JSON unchanged.
For proposal and execution stages, the JSON tool result replaces the
options/explanation answer format below. Do not retry failed writes.""",
)


def workflow_definition(deployment: str) -> PromptAgentDefinition:
    return PromptAgentDefinition(
        model=deployment, instructions=WORKFLOW_INSTRUCTIONS,
        tools=[FunctionTool(**spec) for spec in FUNCTION_TOOL_SPECS],
    )


class WalkthroughLoop(ReadOnlyAgentLoop):
    stage: str = "compare"
    selected_option: str | None = None
    proposal: dict[str, object] | None = None
    outcome: dict[str, object] | None = None

    def _allowed_tools(self) -> frozenset[str]:
        if self.stage == "compare":
            return READ_TOOL_NAMES
        if self.stage == "propose":
            return frozenset({"create_transfer_proposal"})
        if self.stage == "execute":
            return frozenset({"execute_approved_transfer", "read_transfer_result"})
        return frozenset()

    def _dispatch(self, name: str, arguments: str) -> dict[str, object]:
        try:
            values: object = json.loads(arguments)
        except json.JSONDecodeError as error:
            raise ToolError("invalid_arguments", "Function arguments must be JSON.") from error
        if self.stage == "propose":
            if values != {"option": self.selected_option} or self.proposal is not None:
                raise ToolError("selection_mismatch", "Only one proposal for the exact human selection is permitted.")
        if self.stage == "execute":
            if self.proposal is None or values != {"proposal_id": self.proposal["proposal_id"]}:
                raise ToolError("proposal_mismatch", "Only the human-approved proposal ID is permitted.")
            if name == "read_transfer_result" and self.outcome is None:
                raise ToolError("execution_required", "Execute the approved request before confirming its result.")
        result = super()._dispatch(name, arguments)
        if result.get("status") != "error":
            if name == "create_transfer_proposal":
                self.proposal = result
            elif name == "execute_approved_transfer":
                self.outcome = result
        return result

    def _final(self, text: str) -> dict[str, object]:
        if self.stage == "compare":
            return super()._final(text)
        expected = self.proposal if self.stage == "propose" else self.outcome
        required = "create_transfer_proposal" if self.stage == "propose" else "read_transfer_result"
        if expected is None or required not in self.called_tools:
            raise ToolError("ungrounded_answer", "The required application tool was not called.")
        try:
            answer: object = json.loads(text)
        except json.JSONDecodeError as error:
            raise ToolError("invalid_answer", "Expected the exact JSON tool result.") from error
        if json.dumps(answer, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise ToolError("invalid_answer", "The model answer differs from the authoritative tool result.")
        return {"status": "completed", "result": expected, "usage": self.usage.summary(self.pricing)}

    def compare(self, conversation_id: str) -> dict[str, object]:
        if self.stage != "compare" or self.usage.model_requests:
            raise ToolError("invalid_stage", "Comparison can run only once in a fresh walkthrough.")
        result = self._turn(conversation_id, PROMPT)
        self.stage = "awaiting_selection"
        self._event("comparison.ready")
        return result

    def propose(self, conversation_id: str, option: str) -> dict[str, object]:
        if self.stage != "awaiting_selection" or option not in ("STANDARD", "EXPRESS"):
            raise ToolError("invalid_stage", "Select STANDARD or EXPRESS after comparison.")
        self.selected_option = option
        self.stage = "propose"
        self._event("planner.selected", option=option)
        result = self._turn(
            conversation_id,
            f"The human planner selected {option}. Create exactly one proposal for "
            "that option using create_transfer_proposal and return its complete JSON unchanged. "
            "Do not execute; human approval has not been given.",
        )
        self.stage = "awaiting_approval"
        self._event("proposal.ready", proposal_id=self.proposal["proposal_id"] if self.proposal else None)
        return result

    def approve(self, proposal_id: str, *, confirm: bool) -> dict[str, object]:
        if (self.stage != "awaiting_approval" or self.proposal is None
                or proposal_id != self.proposal["proposal_id"]):
            raise ToolError("proposal_mismatch", "Inspect and approve the current exact proposal.")
        if not confirm:
            self.stage = "rejected"
            self._event("human.rejected", proposal_id=proposal_id)
            return {"status": "rejected", "proposal_id": proposal_id}
        result = self.session.store.approve(DemoActor("demo-human-approver", DemoRole.APPROVER), proposal_id)
        self.stage = "approved"
        self._event("human.approved", proposal_id=proposal_id)
        return result

    def execute(self, conversation_id: str) -> dict[str, object]:
        if self.stage != "approved" or self.proposal is None:
            raise ToolError("approval_required", "Human approval must precede the execution stage.")
        proposal_id = self.proposal["proposal_id"]
        if self.session.store.read_result(self.session.actor, str(proposal_id))["status"] != "approved":
            raise ToolError("approval_required", "Durable approval is required.")
        self.stage = "execute"
        self._event("execution.started", proposal_id=proposal_id)
        result = self._turn(
            conversation_id,
            f"The application recorded explicit human approval for proposal {proposal_id}. "
            "Call execute_approved_transfer with that ID, then read_transfer_result "
            "with the same ID. Return the complete read_transfer_result JSON unchanged. "
            "This is a request/reservation, not a shipment or receipt.",
        )
        self.stage = "completed"
        self._event("execution.completed", proposal_id=proposal_id)
        return result
