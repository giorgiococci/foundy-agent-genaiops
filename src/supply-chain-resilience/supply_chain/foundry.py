"""Read-only managed-agent adapter; the local business tools remain SDK-free."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from time import perf_counter

from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from openai import OpenAI
from openai.types.responses import Response
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

from .domain import ToolError
from .tools import FUNCTION_TOOL_SPECS, ToolSession


READ_TOOL_NAMES = frozenset({
    "read_planning_snapshot", "read_transfer_policy", "compare_transfer_options",
})
INSTRUCTIONS = """You are the supply-chain learning demo's managed Foundry agent.
Use only the supplied synthetic facts. First read the planning snapshot and
transfer policy, then compare the transfer options using the provided tools.
Do not invent data, probabilities, stock movements or an optimal choice.
Explain the extra cost versus delivery-margin trade-off; the planner decides.
Do not create a proposal, approve anything or execute a transfer.
Return a JSON object with exactly two keys: options and explanation.
options must copy the complete options array from compare_transfer_options,
including quantity, cost, arrival_day, completion_day, delivery_margin_days,
feasible and reasons. explanation must be a nonempty English string explaining
the trade-off and the fact that no stock has moved. Do not use Markdown fences.
"""
PROMPT = (
    "The controller-board supplier receipt has been delayed. Read the current "
    "planning facts and policy, compare STANDARD and EXPRESS for both customer "
    "commitments, and explain the trade-off without choosing for the planner."
)


def agent_definition(deployment: str) -> PromptAgentDefinition:
    tools = [FunctionTool(**spec) for spec in FUNCTION_TOOL_SPECS
             if spec["name"] in READ_TOOL_NAMES]
    return PromptAgentDefinition(model=deployment, instructions=INSTRUCTIONS, tools=tools)


@dataclass(frozen=True)
class RunLimits:
    model_requests: int = 10
    tool_calls: int = 20
    total_tokens: int = 100_000
    output_tokens_per_request: int = 4096
    spend_eur: Decimal = Decimal("10")

    def __post_init__(self) -> None:
        for value in (self.model_requests, self.tool_calls, self.total_tokens,
                      self.output_tokens_per_request):
            if type(value) is not int or value < 1:
                raise ToolError("invalid_limits", "Run limits must be positive integers.")
        if (self.model_requests > 10 or self.tool_calls > 20 or self.total_tokens > 100_000
                or not self.spend_eur.is_finite() or not 0 < self.spend_eur <= 10):
            raise ToolError("invalid_limits", "This demo cannot exceed the S-020 approved limits.")


@dataclass(frozen=True)
class Pricing:
    """Operator-verified conservative EUR rates, not a quotation or billing API."""

    input_eur_per_million: Decimal
    output_eur_per_million: Decimal
    source: str

    def __post_init__(self) -> None:
        rates = (self.input_eur_per_million, self.output_eur_per_million)
        if any(not rate.is_finite() or rate <= 0 for rate in rates) or not self.source.strip():
            raise ToolError("unverified_pricing", "Positive verified EUR rates and their source are required.")

    def upper_cost(self, tokens: int) -> Decimal:
        return Decimal(tokens) * max(
            self.input_eur_per_million, self.output_eur_per_million
        ) / Decimal(1_000_000)


@dataclass
class RunUsage:
    model_requests: int = 0
    tool_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    usage_unreconciled: bool = False

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def summary(self, pricing: Pricing) -> dict[str, object]:
        return {
            "model_requests": self.model_requests, "tool_calls": self.tool_calls,
            "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "usage_unreconciled": self.usage_unreconciled,
            "budget_enforcement": "post_response_monitoring",
            "conservative_model_cost_eur": str(pricing.upper_cost(self.total_tokens)),
        }


class ReadOnlyAgentLoop:
    def __init__(
        self, client: OpenAI, session: ToolSession, *, pricing: Pricing,
        limits: RunLimits | None = None,
        on_event: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.client = client
        self.session = session
        self.pricing = pricing
        self.limits = limits if limits is not None else RunLimits()
        self.usage = RunUsage()
        self.seen_call_ids: set[str] = set()
        self.called_tools: set[str] = set()
        self.comparison: dict[str, object] | None = None
        self.on_event = on_event

    def _event(self, name: str, **fields: object) -> None:
        if self.on_event is not None:
            self.on_event({"event": name, **fields})

    def _request(
        self, conversation_id: str, inputs: str | ResponseInputParam,
    ) -> Response:
        if self.usage.usage_unreconciled:
            raise ToolError("uncertain_request", "An uncertain request cannot be retried automatically.")
        if self.usage.model_requests >= self.limits.model_requests:
            raise ToolError("request_limit", "The model-request limit has been reached.")
        if self.usage.total_tokens >= self.limits.total_tokens:
            raise ToolError("token_limit", "Reported usage reached the aggregate token monitoring threshold.")
        if self.pricing.upper_cost(self.usage.total_tokens) >= self.limits.spend_eur:
            raise ToolError("spend_limit", "Reported usage reached the estimated EUR monitoring threshold.")
        self.usage.usage_unreconciled = True
        self.usage.model_requests += 1
        self._event("model.started", request_number=self.usage.model_requests)
        started = perf_counter()
        response = self.client.responses.create(
            conversation=conversation_id, input=inputs,
            max_output_tokens=self.limits.output_tokens_per_request,
            parallel_tool_calls=False, truncation="disabled",
        )
        usage = response.usage
        if usage is None:
            raise ToolError("missing_usage", "No usage returned; request cost is unknown. Stop without retrying.")
        if (type(usage.input_tokens) is not int or usage.input_tokens < 0
                or type(usage.output_tokens) is not int or usage.output_tokens < 0
                or type(usage.total_tokens) is not int
                or usage.total_tokens != usage.input_tokens + usage.output_tokens):
            raise ToolError("invalid_usage", "The service returned invalid usage; stop without retrying.")
        self.usage.input_tokens += usage.input_tokens
        self.usage.output_tokens += usage.output_tokens
        self.usage.usage_unreconciled = False
        self._event(
            "model.completed", response_id=response.id, status=response.status,
            duration_ms=round((perf_counter() - started) * 1000, 3),
            input_tokens=usage.input_tokens, output_tokens=usage.output_tokens,
        )
        if usage.output_tokens > self.limits.output_tokens_per_request:
            raise ToolError("usage_bound_mismatch", "Actual output exceeded the requested maximum; stop and investigate.")
        if self.usage.total_tokens > self.limits.total_tokens:
            raise ToolError("token_limit", "Reported usage exceeded the token monitoring threshold; stop.")
        if self.pricing.upper_cost(self.usage.total_tokens) > self.limits.spend_eur:
            raise ToolError("spend_limit", "Reported usage exceeded the estimated EUR monitoring threshold; stop.")
        if response.status != "completed" or response.error is not None:
            raise ToolError("response_failed", f"Model response did not complete successfully: {response.status}.")
        return response

    def run(self, conversation_id: str) -> dict[str, object]:
        if self.usage.model_requests:
            raise ToolError("already_started", "Use a fresh loop for a separately authorized run.")
        return self._turn(conversation_id, PROMPT)

    def _allowed_tools(self) -> frozenset[str]:
        return READ_TOOL_NAMES

    def _dispatch(self, name: str, arguments: str) -> dict[str, object]:
        return self.session.dispatch(name, arguments)

    def _turn(
        self, conversation_id: str, inputs: str | ResponseInputParam,
    ) -> dict[str, object]:
        while True:
            response = self._request(conversation_id, inputs)
            calls = [item for item in response.output if item.type == "function_call"]
            if not calls:
                return self._final(response.output_text)
            if self.usage.tool_calls + len(calls) > self.limits.tool_calls:
                raise ToolError("tool_limit", "The function batch exceeds the remaining tool-call allowance.")
            batch_ids: set[str] = set()
            for call in calls:
                if call.name not in self._allowed_tools():
                    raise ToolError("forbidden_tool", "This tool is not allowed in the current application stage.")
                if not call.call_id or call.call_id in self.seen_call_ids or call.call_id in batch_ids:
                    raise ToolError("invalid_call_id", "Empty or repeated function call ID.")
                batch_ids.add(call.call_id)
            outputs: ResponseInputParam = []
            for call in calls:
                self.seen_call_ids.add(call.call_id)
                self.usage.tool_calls += 1
                self._event("tool.started", tool=call.name, call_id=call.call_id)
                started = perf_counter()
                result = self._dispatch(call.name, call.arguments)
                self._event(
                    "tool.completed", tool=call.name, call_id=call.call_id,
                    status=result.get("status"), duration_ms=round((perf_counter() - started) * 1000, 3),
                )
                if result.get("status") == "error":
                    raise ToolError("tool_failed", f"{call.name} failed: {json.dumps(result['error'])}")
                self.called_tools.add(call.name)
                if call.name == "compare_transfer_options":
                    self.comparison = result
                outputs.append(FunctionCallOutput(
                    type="function_call_output", call_id=call.call_id,
                    output=json.dumps(result),
                ))
            inputs = outputs

    def _final(self, text: str) -> dict[str, object]:
        if self.called_tools != READ_TOOL_NAMES or self.comparison is None:
            raise ToolError("ungrounded_answer", "The real agent did not call all three required fact tools.")
        try:
            answer: object = json.loads(text)
        except json.JSONDecodeError as error:
            raise ToolError("invalid_answer", "The final answer is not the required JSON object.") from error
        if (not isinstance(answer, dict) or set(answer) != {"options", "explanation"}
                or json.dumps(answer["options"], sort_keys=True) != json.dumps(
                    self.comparison.get("options"), sort_keys=True
                )
                or not isinstance(answer["explanation"], str) or not answer["explanation"].strip()):
            raise ToolError("invalid_answer", "The answer must preserve the tool's exact options and explain them.")
        return {
            "status": "completed", "answer": answer,
            "called_tools": sorted(self.called_tools), "usage": self.usage.summary(self.pricing),
        }
