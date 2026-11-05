"""Shared trace export with explicit, task-local per-agent content policy."""

from __future__ import annotations

import json
import logging
import os
import re
from collections.abc import Callable, Generator, Mapping, Sequence
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Literal

from agent_framework.observability import enable_instrumentation
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import ApiKeyCredentials, ConnectionType
from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, Span, SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.sdk.trace.sampling import Decision, Sampler, SamplingResult
from opentelemetry.trace import SpanKind, Status
from opentelemetry.trace import Link, TraceState
from opentelemetry.util.types import Attributes

from .domain import ToolError


LOGGER = logging.getLogger(__name__)
Mode = Literal["off", "metadata", "content"]
PAYLOAD_ATTRIBUTES = frozenset({
    "gen_ai.input.messages", "gen_ai.output.messages",
    "gen_ai.tool.call.arguments", "gen_ai.tool.call.result",
})
METADATA_ATTRIBUTES = frozenset({
    "gen_ai.operation.name", "gen_ai.agent.id", "gen_ai.agent.name",
    "gen_ai.conversation.id", "gen_ai.provider.name", "gen_ai.system",
    "gen_ai.request.model", "gen_ai.response.model", "gen_ai.response.id",
    "gen_ai.response.finish_reasons", "gen_ai.tool.name", "gen_ai.tool.type",
    "gen_ai.tool.call.id", "error.type", "server.address",
    "supply_chain.run.id", "supply_chain.telemetry.mode",
    "supply_chain.service.conversation.id",
    "gen_ai.usage.input_tokens", "gen_ai.usage.output_tokens",
})
_SECRET_KEY = re.compile(r"password|secret|token|credential|authorization|connection.?string|api.?key", re.I)
_SECRET_TEXT = re.compile(
    r"(?i)\bBearer\s+\S+|(?:InstrumentationKey|SharedAccessKey|AccountKey|api[_-]?key)\s*=\s*[^;\s]+"
)


@dataclass(frozen=True)
class TelemetryPolicy:
    mode: Mode = "metadata"

    def __post_init__(self) -> None:
        if self.mode not in ("off", "metadata", "content"):
            raise ToolError("invalid_telemetry_policy", "Choose off, metadata or content explicitly.")


@dataclass(frozen=True)
class TraceScope:
    policy: TelemetryPolicy
    attributes: Mapping[str, str]


_SCOPE: ContextVar[TraceScope | None] = ContextVar("supply_chain_trace_scope", default=None)


def _content(value: object) -> str:
    def redact(item: object) -> object:
        if isinstance(item, dict):
            return {str(key): "[REDACTED]" if _SECRET_KEY.search(str(key)) else redact(val)
                    for key, val in item.items()}
        if isinstance(item, (list, tuple)):
            return [redact(val) for val in item]
        if isinstance(item, str):
            return _SECRET_TEXT.sub("[REDACTED]", item)
        return item

    text = json.dumps(redact(value), ensure_ascii=True)
    if len(text) > 6000:
        return json.dumps({"truncated": True, "preview": text[:4000]})
    return text


def capture_content(attribute: str, value: object) -> None:
    scope = _SCOPE.get()
    if scope is not None and scope.policy.mode == "content" and attribute in PAYLOAD_ATTRIBUTES:
        trace.get_current_span().set_attribute(attribute, _content(value))


def traced_tool(function: Callable[..., dict[str, object]]) -> Callable[..., dict[str, object]]:
    def invoke(**arguments: object) -> dict[str, object]:
        capture_content("gen_ai.tool.call.arguments", arguments)
        result = function(**arguments)
        capture_content("gen_ai.tool.call.result", result)
        return result

    return invoke


class AgentSampler(Sampler):
    def should_sample(
        self, parent_context: Context | None, trace_id: int, name: str,
        kind: SpanKind | None = None, attributes: Attributes = None,
        links: Sequence[Link] | None = None, trace_state: TraceState | None = None,
    ) -> SamplingResult:
        scope = _SCOPE.get()
        enabled = scope is not None and scope.policy.mode != "off"
        return SamplingResult(
            Decision.RECORD_AND_SAMPLE if enabled else Decision.DROP,
            attributes=attributes, trace_state=trace_state,
        )

    def get_description(self) -> str:
        return "Explicit per-agent trace scope"


class CorrelationProcessor(SpanProcessor):
    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        scope = _SCOPE.get()
        if scope is not None:
            span.set_attributes(scope.attributes)
            span.set_attribute("supply_chain.telemetry.mode", scope.policy.mode)


class PolicyExporter(SpanExporter):
    """Export allowlisted attributes only; never export exception text or arbitrary events."""

    def __init__(self, exporter: SpanExporter) -> None:
        self.exporter = exporter
        self.failed = False

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        filtered = []
        for span in spans:
            attributes = span.attributes or {}
            mode = attributes.get("supply_chain.telemetry.mode")
            if mode not in ("metadata", "content"):
                continue
            allowed = METADATA_ATTRIBUTES | (PAYLOAD_ATTRIBUTES if mode == "content" else frozenset())
            selected = {key: value for key, value in attributes.items() if key in allowed}
            # AG-UI uses its local thread ID for native telemetry; retain the managed service identity.
            if attributes.get("supply_chain.service.conversation.id"):
                selected["gen_ai.conversation.id"] = attributes["supply_chain.service.conversation.id"]
            filtered.append(ReadableSpan(
                name=span.name, context=span.context, parent=span.parent,
                resource=span.resource, kind=span.kind, start_time=span.start_time,
                end_time=span.end_time, instrumentation_scope=span.instrumentation_scope,
                status=Status(span.status.status_code),
                attributes=selected,
            ))
        if not filtered:
            return SpanExportResult.SUCCESS
        try:
            result = self.exporter.export(filtered)
        except Exception as error:
            self.failed = True
            LOGGER.error("Trace export raised %s; telemetry delivery is not confirmed.", type(error).__name__)
            return SpanExportResult.FAILURE
        if result != SpanExportResult.SUCCESS:
            self.failed = True
            LOGGER.error("Trace exporter reported failure; telemetry delivery is not confirmed.")
        return result

    def shutdown(self) -> None:
        self.exporter.shutdown()


@dataclass
class Tracing:
    provider: TracerProvider
    exporter: PolicyExporter

    def close(self) -> None:
        try:
            flushed = self.provider.force_flush(timeout_millis=30_000)
        finally:
            self.provider.shutdown()
        if not flushed or self.exporter.failed:
            raise ToolError("telemetry_export_failed", "Trace delivery failed or timed out; do not retry the model operation.")


async def linked_insights_connection_string(project: AIProjectClient) -> str:
    connections = [connection async for connection in project.connections.list(
        connection_type=ConnectionType.APPLICATION_INSIGHTS,
    )]
    if len(connections) != 1:
        raise ToolError("invalid_telemetry_destination", "Exactly one linked Application Insights connection is required.")
    connection = await project.connections.get(name=connections[0].name, include_credentials=True)
    if connection.type != ConnectionType.APPLICATION_INSIGHTS:
        raise ToolError("invalid_telemetry_destination", "The selected connection is not Application Insights.")
    if isinstance(connection.credentials, ApiKeyCredentials):
        value = connection.credentials.api_key
    elif connection.credentials.type == "ProjectManagedIdentity":
        # This service layout is not supported by the SDK 2.7 telemetry convenience method.
        value = (connection.metadata or {}).get("ApplicationInsightsConnectionString")
    else:
        raise ToolError("unsupported_telemetry_connection", "The linked telemetry credential layout is unsupported.")
    if not isinstance(value, str) or not value.strip():
        raise ToolError("missing_telemetry_destination", "The linked Insights connection has no connection string.")
    return value


def start_azure_tracing(connection_string: str) -> Tracing:
    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

    if not connection_string.strip():
        raise ToolError("missing_telemetry_destination", "The project has no linked Application Insights connection.")
    if not isinstance(trace.get_tracer_provider(), trace.ProxyTracerProvider):
        raise ToolError("telemetry_already_configured", "Configure the shared tracing provider only once at process startup.")
    # Export only to the linked destination, without auxiliary background exporters.
    for setting in ("APPLICATIONINSIGHTS_STATSBEAT_DISABLED_ALL",
                    "APPLICATIONINSIGHTS_SDKSTATS_DISABLED", "APPLICATIONINSIGHTS_CONTROLPLANE_DISABLED"):
        os.environ[setting] = "true"
    try:
        destination = AzureMonitorTraceExporter(
            connection_string=connection_string, disable_offline_storage=True, timeout=10, retry_total=0,
        )
    except ValueError as error:
        raise ToolError("invalid_telemetry_destination", "The linked telemetry destination is invalid; its value is not logged.") from error
    exporter = PolicyExporter(destination)
    provider = TracerProvider(
        sampler=AgentSampler(), shutdown_on_exit=False,
        resource=Resource({
            "service.name": "supply-chain-resilience", "microsoft.agent-framework": "True",
        }),
    )
    provider.add_span_processor(CorrelationProcessor())
    provider.add_span_processor(BatchSpanProcessor(exporter))
    # Never toggle process-global sensitive recording for an individual agent.
    enable_instrumentation(enable_sensitive_data=False, enable_message_events=False, force=True)
    trace.set_tracer_provider(provider)
    return Tracing(provider, exporter)


@contextmanager
def agent_trace(
    policy: TelemetryPolicy, *, agent_name: str, agent_id: str,
    run_id: str, conversation_id: str | None,
) -> Generator[trace.Span]:
    attributes = {
        "gen_ai.agent.name": agent_name, "gen_ai.agent.id": agent_id,
        "supply_chain.run.id": run_id,
    }
    if conversation_id:
        attributes["gen_ai.conversation.id"] = conversation_id
        attributes["supply_chain.service.conversation.id"] = conversation_id
    token = _SCOPE.set(TraceScope(policy, attributes))
    try:
        with trace.get_tracer(__name__).start_as_current_span(
            "supply_chain.turn", attributes=attributes, record_exception=False,
            set_status_on_exception=False,
        ) as span:
            try:
                yield span
            except Exception as error:
                span.set_status(trace.StatusCode.ERROR)
                span.set_attribute("error.type", type(error).__name__)
                raise
    finally:
        _SCOPE.reset(token)
