"""Offline native-framework tracing, per-agent isolation and export lifecycle checks."""

from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from agent_framework.observability import enable_instrumentation
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import Connection
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, SpanExportResult
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.agents.resilience_advisor.conversation import AdvisorConversation
from supply_chain.agents.resilience_advisor.definition import definition
from supply_chain.observability import (
    AgentSampler, CorrelationProcessor, PAYLOAD_ATTRIBUTES, PolicyExporter,
    TelemetryPolicy, Tracing, agent_trace, capture_content, linked_insights_connection_string, traced_tool,
)
from supply_chain.runtime import Pricing
from supply_chain.session import CandidateSession
from tests.runtime_tests import OfflineFoundry, response
from advisor_demo import chat


class ObservabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.memory = InMemorySpanExporter()
        self.exporter = PolicyExporter(self.memory)
        self.provider = TracerProvider(
            sampler=AgentSampler(), shutdown_on_exit=False,
            resource=Resource({"service.name": "offline-test"}),
        )
        self.provider.add_span_processor(CorrelationProcessor())
        self.provider.add_span_processor(SimpleSpanProcessor(self.exporter))
        self.addCleanup(self.provider.shutdown)
        lookup = patch("opentelemetry.trace.get_tracer_provider", return_value=self.provider)
        lookup.start()
        self.addCleanup(lookup.stop)
        enable_instrumentation(enable_sensitive_data=False, enable_message_events=False, force=True)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)

    def scope(self, mode="metadata", *, run_id="run-test"):
        return agent_trace(
            TelemetryPolicy(mode), agent_name="synthetic-advisor", agent_id="advisor:3",
            run_id=run_id, conversation_id="conv_offline",
        )

    def native_turn(self, mode):
        store = DemoStore(self.directory / "planning.sqlite3")
        store.initialize()
        service = MagicMock()
        offline = OfflineFoundry(self, service)
        advisor = AdvisorConversation(
            ToolSession(store, DemoActor("demo-viewer", DemoRole.VIEWER)),
            pricing=Pricing(Decimal("5"), Decimal("20"), "offline fixture"),
            telemetry_policy=TelemetryPolicy(mode),
        )
        service.responses.create.side_effect = [
            response((("read_planning_snapshot", "trace-tool-1", "{}"),
                      ("read_transfer_policy", "trace-tool-2", "{}"),
                      ("compare_transfer_options", "trace-tool-3", "{}"))),
            response(text=json.dumps({
                "message": "Synthetic advisor answer: no stock has moved.",
                "evidence": [store.compare_options(DemoActor("demo-viewer", DemoRole.VIEWER))],
            })),
        ]
        result = offline.run(advisor, "Synthetic planner question.")
        return result, self.memory.get_finished_spans()

    def test_native_agent_model_and_tool_spans_share_trace_and_identity(self):
        result, spans = self.native_turn("metadata")
        operations = {(span.attributes or {}).get("gen_ai.operation.name") for span in spans}
        self.assertIn("invoke_agent", operations)
        self.assertIn("chat", operations)
        self.assertIn("execute_tool", operations)
        self.assertEqual(len({span.context.trace_id for span in spans}), 1)
        self.assertEqual(result["telemetry"]["trace_id"], format(spans[0].context.trace_id, "032x"))
        for span in spans:
            self.assertEqual(span.attributes["gen_ai.agent.id"], "supply-chain-resilience-advisor:3")
            self.assertEqual(span.attributes["gen_ai.conversation.id"], "conv_offline")
            self.assertFalse(PAYLOAD_ATTRIBUTES & set(span.attributes))
        self.assertEqual(sum(span.attributes.get("gen_ai.usage.input_tokens", 0) for span in spans
                             if span.attributes.get("gen_ai.operation.name") == "chat"), 200)

    def test_content_captures_synthetic_turn_and_native_tool_arguments_and_result(self):
        result, spans = self.native_turn("content")
        root = next(span for span in spans if span.name == "supply_chain.turn")
        self.assertIn("Synthetic planner question.", root.attributes["gen_ai.input.messages"])
        self.assertIn("Synthetic advisor answer", root.attributes["gen_ai.output.messages"])
        tools = [span for span in spans if span.attributes.get("gen_ai.operation.name") == "execute_tool"]
        self.assertEqual(len(tools), 3)
        for tool in tools:
            self.assertEqual(json.loads(tool.attributes["gen_ai.tool.call.arguments"]), {})
            self.assertIsInstance(json.loads(tool.attributes["gen_ai.tool.call.result"]), dict)
        self.assertEqual(result["status"], "completed")
        self.assertTrue(all("gen_ai.system_instructions" not in span.attributes for span in spans))

    def test_disabled_native_agent_emits_no_spans(self):
        result, spans = self.native_turn("off")
        self.assertEqual(spans, ())
        self.assertNotIn("telemetry", result)

    def test_batch_flush_preserves_all_native_spans_outside_the_agent_context(self):
        memory = InMemorySpanExporter()
        self.provider.add_span_processor(BatchSpanProcessor(
            PolicyExporter(memory), schedule_delay_millis=60_000,
        ))
        result, immediate = self.native_turn("content")
        self.assertTrue(self.provider.force_flush(timeout_millis=5000))
        batched = memory.get_finished_spans()
        self.assertEqual(len(immediate), 7)
        self.assertEqual(len(batched), 7)
        self.assertEqual(
            {span.context.span_id for span in immediate}, {span.context.span_id for span in batched},
        )
        self.assertTrue(all(
            format(span.context.trace_id, "032x") == result["telemetry"]["trace_id"] for span in batched
        ))

    def test_concurrent_agent_policies_do_not_leak_content_or_enable_disabled_agent(self):
        async def run(mode):
            with self.scope(mode, run_id=mode):
                capture_content("gen_ai.input.messages", f"private-{mode}")
                await asyncio.sleep(0)
                with trace.get_tracer("test").start_as_current_span("child"):
                    capture_content("gen_ai.output.messages", f"private-{mode}")
                    await asyncio.sleep(0)

        async def together():
            await asyncio.gather(run("metadata"), run("content"), run("off"))

        asyncio.run(together())
        spans = self.memory.get_finished_spans()
        self.assertEqual(len(spans), 4)
        for span in spans:
            mode = span.attributes["supply_chain.run.id"]
            serialized = str(span.attributes)
            self.assertNotIn("private-metadata", serialized)
            self.assertNotIn("private-off", serialized)
            self.assertEqual(bool(PAYLOAD_ATTRIBUTES & set(span.attributes)), mode == "content")
        self.assertEqual(len({span.context.trace_id for span in spans}), 2)

    def test_unscoped_activity_is_not_exported(self):
        with trace.get_tracer("test").start_as_current_span("outside-agent"):
            pass
        self.assertEqual(self.memory.get_finished_spans(), ())

    def test_metadata_drops_payloads_exception_text_events_and_unknown_attributes(self):
        with self.scope() as span:
            span.set_attribute("gen_ai.input.messages", "private-message")
            span.set_attribute("unrecognized", "private-unknown")
            span.set_attribute("supply_chain.unrecognized", "private-custom")
            span.record_exception(RuntimeError("private-error"))
            span.set_status(trace.Status(trace.StatusCode.ERROR, "private-status"))
            span.add_event("private-event", {"value": "private-event-value"})
        exported = self.memory.get_finished_spans()[0]
        self.assertNotIn("private-", str(exported.attributes))
        self.assertFalse(exported.events)
        self.assertIsNone(exported.status.description)
        self.assertEqual(exported.status.status_code, trace.StatusCode.ERROR)

    def test_content_redacts_known_credentials_and_limits_payload_size(self):
        with self.scope("content"):
            capture_content("gen_ai.input.messages", {
                "password": "do-not-export", "nested": {"api_key": "do-not-export"},
                "message": "Bearer do-not-export InstrumentationKey=do-not-export",
            })
            with trace.get_tracer("test").start_as_current_span("large"):
                capture_content("gen_ai.output.messages", "x" * 20_000)
        spans = self.memory.get_finished_spans()
        self.assertNotIn("do-not-export", str([span.attributes for span in spans]))
        self.assertTrue(json.loads(spans[0].attributes["gen_ai.output.messages"])["truncated"])
        self.assertLess(len(spans[0].attributes["gen_ai.output.messages"]), 6000)

    def test_tool_error_is_not_swallowed_and_turn_context_is_reset(self):
        def broken(**arguments: object) -> dict[str, object]:
            raise ToolError("fixture_error", "private-tool-error")

        with self.assertRaises(ToolError):
            with self.scope("content"):
                traced_tool(broken)(password="private")
        with trace.get_tracer("test").start_as_current_span("after-error"):
            pass
        spans = self.memory.get_finished_spans()
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].attributes["error.type"], "ToolError")
        self.assertNotIn("private", str(spans[0].attributes))

    def test_export_failure_is_reported_at_flush_and_shutdown_still_runs(self):
        underlying = MagicMock()
        underlying.export.return_value = SpanExportResult.FAILURE
        exporter = PolicyExporter(underlying)
        provider = TracerProvider(sampler=AgentSampler(), shutdown_on_exit=False)
        provider.add_span_processor(CorrelationProcessor())
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        with self.scope():
            with provider.get_tracer("failure-test").start_as_current_span("export-failure"):
                pass
        with self.assertRaises(ToolError) as caught:
            Tracing(provider, exporter).close()
        self.assertEqual(caught.exception.code, "telemetry_export_failed")
        underlying.shutdown.assert_called_once()

    def test_flush_timeout_shuts_down_and_is_explicit(self):
        provider = MagicMock()
        provider.force_flush.return_value = False
        with self.assertRaises(ToolError):
            Tracing(provider, self.exporter).close()
        provider.shutdown.assert_called_once()

    def test_export_exception_is_explicit_without_logging_its_sensitive_message(self):
        destination = MagicMock()
        destination.export.side_effect = RuntimeError("private-export-error")
        exporter = PolicyExporter(destination)
        with self.scope():
            pass
        with self.assertLogs("supply_chain.observability", level="ERROR") as logged:
            result = exporter.export(self.memory.get_finished_spans())
        self.assertEqual(result, SpanExportResult.FAILURE)
        self.assertTrue(exporter.failed)
        self.assertNotIn("private-export-error", str(logged.output))
        provider = MagicMock()
        provider.force_flush.return_value = True
        with self.assertRaises(ToolError):
            Tracing(provider, exporter).close()

    def test_lower_live_limits_survive_session_save_and_reload(self):
        candidate = CandidateSession.initialize(
            self.directory / "bounded", "test", model_request_limit=5, tool_call_limit=10,
            total_token_limit=30_000, spend_eur_limit=2,
        )
        restored = CandidateSession.load(candidate.directory)
        self.assertEqual(restored.advisor.safety.limits.model_requests, 5)
        self.assertEqual(restored.advisor.safety.limits.tool_calls, 10)
        self.assertEqual(restored.advisor.safety.limits.total_tokens, 30_000)
        self.assertEqual(restored.advisor.safety.limits.spend_eur, Decimal("2"))

    def test_cli_flushes_after_both_native_success_and_validation_error(self):
        for succeeds in (True, False):
            with self.subTest(succeeds=succeeds):
                candidate = CandidateSession.initialize(self.directory / str(succeeds), "test")
                service = MagicMock()
                offline = OfflineFoundry(self, service)
                candidate.framework_session = offline.session
                project = offline.project
                project.agents.get_version = AsyncMock(return_value=SimpleNamespace(
                    version="3", definition=definition("test"),
                ))
                service.responses.create.return_value = response(
                    text='{"message":"Synthetic answer.","evidence":[]}' if succeeds else "invalid JSON",
                )
                with patch("advisor_demo.AzureCliCredential"), patch("advisor_demo.AIProjectClient") as factory:
                    factory.return_value.__aenter__.return_value = project
                    with patch("advisor_demo.start_azure_tracing") as start, patch(
                        "advisor_demo.linked_insights_connection_string",
                        new_callable=AsyncMock, return_value="offline-destination-not-exported",
                    ) as discover:
                        if succeeds:
                            result = asyncio.run(chat(
                                candidate, "Synthetic question.", "https://example.invalid", "tenant", "3",
                                telemetry="content",
                            ))
                            self.assertEqual(result["telemetry"]["mode"], "content")
                        else:
                            with self.assertRaises(ToolError):
                                asyncio.run(chat(
                                    candidate, "Synthetic question.", "https://example.invalid", "tenant", "3",
                                    telemetry="content",
                                ))
                        start.assert_called_once_with("offline-destination-not-exported")
                        discover.assert_awaited_once_with(project)
                        start.return_value.close.assert_called_once()

    def test_cli_off_does_not_discover_destination_or_export_with_an_existing_provider(self):
        candidate = CandidateSession.initialize(self.directory / "cli-off", "test")
        service = MagicMock()
        offline = OfflineFoundry(self, service)
        candidate.framework_session = offline.session
        offline.project.agents.get_version = AsyncMock(return_value=SimpleNamespace(
            version="3", definition=definition("test"),
        ))
        service.responses.create.return_value = response(text='{"message":"Synthetic answer.","evidence":[]}')
        with patch("advisor_demo.AzureCliCredential"), patch("advisor_demo.AIProjectClient") as factory:
            factory.return_value.__aenter__.return_value = offline.project
            with patch("advisor_demo.start_azure_tracing") as start, patch(
                "advisor_demo.linked_insights_connection_string", new_callable=AsyncMock,
            ) as discover:
                result = asyncio.run(chat(
                    candidate, "Synthetic question.", "https://example.invalid", "tenant", "3",
                ))
                start.assert_not_called()
                discover.assert_not_awaited()
        self.assertNotIn("telemetry", result)
        self.assertEqual(self.memory.get_finished_spans(), ())

    def test_linked_destination_supports_api_key_and_observed_project_identity_layout(self):
        for credentials, metadata in (
            ({"type": "ApiKey", "key": "offline-key-value"}, {}),
            ({"type": "ProjectManagedIdentity"}, {"ApplicationInsightsConnectionString": "offline-key-value"}),
        ):
            with self.subTest(layout=credentials["type"]):
                connection = Connection({
                    "name": "offline-insights", "id": "offline-connection", "type": "AppInsights",
                    "target": "/subscriptions/offline/providers/microsoft.insights/components/offline",
                    "isDefault": True, "credentials": credentials, "metadata": metadata,
                })

                async def connections(**kwargs):
                    yield connection

                project = MagicMock(spec=AIProjectClient)
                project.connections = MagicMock()
                project.connections.list.side_effect = connections
                project.connections.get = AsyncMock(return_value=connection)
                value = asyncio.run(linked_insights_connection_string(project))
                self.assertEqual(value, "offline-key-value")
                project.connections.get.assert_awaited_once_with(
                    name="offline-insights", include_credentials=True,
                )

    def test_missing_ambiguous_or_unsupported_linked_destination_fails_closed(self):
        for count, credentials, metadata in (
            (0, {"type": "ApiKey", "key": "fixture"}, {}),
            (2, {"type": "ApiKey", "key": "fixture"}, {}),
            (1, {"type": "unexpected-layout"}, {"ApplicationInsightsConnectionString": "do-not-use"}),
            (1, {"type": "ProjectManagedIdentity"}, {}),
        ):
            with self.subTest(count=count, layout=credentials["type"]):
                connection = Connection({
                    "name": "offline-insights", "id": "offline-connection", "type": "AppInsights",
                    "target": "offline", "isDefault": True, "credentials": credentials, "metadata": metadata,
                })

                async def connections(**kwargs):
                    for _ in range(count):
                        yield connection

                project = MagicMock(spec=AIProjectClient)
                project.connections = MagicMock()
                project.connections.list.side_effect = connections
                project.connections.get = AsyncMock(return_value=connection)
                with self.assertRaises(ToolError):
                    asyncio.run(linked_insights_connection_string(project))


if __name__ == "__main__":
    unittest.main()
