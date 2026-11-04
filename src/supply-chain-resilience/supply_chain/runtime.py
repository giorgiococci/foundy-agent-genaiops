"""Agent Framework middleware for cumulative budgets and fail-closed tool execution."""

from __future__ import annotations

import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from decimal import Decimal
from time import perf_counter
from agent_framework import (
    ChatContext, ChatMiddleware, ChatResponse, Content, FunctionInvocationContext,
    FunctionMiddleware, MiddlewareFailure,
)
from openai.types.responses import Response

from .domain import ToolError


LOGGER = logging.getLogger(__name__)


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
        if (self.model_requests > 20 or self.tool_calls > 20 or self.total_tokens > 100_000
                or not self.spend_eur.is_finite() or not 0 < self.spend_eur <= 10):
            raise ToolError("invalid_limits", "The requested limits exceed the permitted demo bounds.")


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


class RunSafety(ChatMiddleware):
    def __init__(
        self, *, pricing: Pricing, validate_call: Callable[[str, str], object],
        limits: RunLimits | None = None,
        usage: RunUsage | None = None, seen_call_ids: set[str] | None = None,
        on_event: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.pricing = pricing
        self.validate_call = validate_call
        self.limits = limits if limits is not None else RunLimits()
        self.usage = usage if usage is not None else RunUsage()
        self.seen_call_ids = seen_call_ids if seen_call_ids is not None else set()
        self.on_event = on_event
        self.pending_calls: dict[str, str] = {}
        self.failure: ToolError | None = None

    def event(self, name: str, **fields: object) -> None:
        if self.on_event is not None:
            self.on_event({"event": name, **fields})

    async def process(self, context: ChatContext, call_next: Callable[[], Awaitable[None]]) -> None:
        # Also blocks the framework's best-effort settlement request after a fatal tool error.
        if self.failure is not None:
            raise self.failure
        if context.stream:
            raise ToolError("unsupported_stream", "This demo currently validates complete non-streaming responses.")
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
        self.event("model.started", request_number=self.usage.model_requests)
        started = perf_counter()
        await call_next()
        result = context.result
        if not isinstance(result, ChatResponse) or not isinstance(result.raw_representation, Response):
            raise ToolError("invalid_response", "Expected an auditable Foundry Responses result; usage remains uncertain.")
        response = result.raw_representation
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
        self.event(
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
        calls = [item for item in response.output if item.type == "function_call"]
        if self.usage.tool_calls + len(calls) > self.limits.tool_calls:
            raise ToolError("tool_limit", "The function batch exceeds the remaining tool-call allowance.")
        pending: dict[str, str] = {}
        for call in calls:
            self.validate_call(call.name, call.arguments)
            if not call.call_id or call.call_id in self.seen_call_ids or call.call_id in pending:
                raise ToolError("invalid_call_id", "Empty or repeated function call ID.")
            pending[call.call_id] = call.name
        self.pending_calls = pending


class ToolSafety(FunctionMiddleware):
    def __init__(self, safety: RunSafety) -> None:
        self.safety = safety

    async def process(
        self, context: FunctionInvocationContext, call_next: Callable[[], Awaitable[None]],
    ) -> None:
        safety = self.safety
        name = context.function.name
        call_id = context.metadata.get("call_id")
        started = perf_counter()
        if safety.failure is not None:
            raise MiddlewareFailure(str(safety.failure)) from safety.failure
        try:
            if (not isinstance(call_id, str) or safety.pending_calls.get(call_id) != name
                    or call_id in safety.seen_call_ids):
                raise ToolError("invalid_call_id", "Function invocation lacks a validated, unused model call ID.")
            safety.seen_call_ids.add(call_id)
            safety.usage.tool_calls += 1
            safety.event("tool.started", tool=name, call_id=call_id)
            await call_next()
            contents = context.result
            if (not isinstance(contents, list) or len(contents) != 1
                    or not isinstance(contents[0], Content) or contents[0].type != "text"
                    or not isinstance(contents[0].text, str)):
                raise ToolError("invalid_result", "Expected a serialized authoritative tool result.")
            try:
                result = json.loads(contents[0].text)
            except json.JSONDecodeError as error:
                raise ToolError("invalid_result", "Tool result text is not authoritative JSON.") from error
            if not isinstance(result, dict):
                raise ToolError("invalid_result", "Expected an authoritative result object.")
            if result.get("status") == "error":
                raise ToolError("tool_failed", f"{name} failed: {json.dumps(result['error'])}")
            safety.event(
                "tool.completed", tool=name, call_id=call_id, status=result.get("status"),
                duration_ms=round((perf_counter() - started) * 1000, 3),
            )
        except Exception as error:
            # Ordinary function exceptions are recoverable in the framework, but not in this guarded demo.
            failure = error if isinstance(error, ToolError) else ToolError(
                "tool_exception", f"{name} failed unexpectedly; inspect the chained error without retrying.",
            )
            safety.failure = failure
            LOGGER.exception("Tool execution aborted: %s (%s).", name, failure.code)
            safety.event("tool.failed", tool=name, call_id=call_id, code=failure.code)
            raise MiddlewareFailure(str(failure)) from error
