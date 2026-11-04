"""Real Agent Framework execution with an offline service boundary and SDK responses."""

from __future__ import annotations

import json
import asyncio
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from agent_framework import AgentSession
from agent_framework.exceptions import AgentFrameworkException
from azure.ai.projects.aio import AIProjectClient
from openai import AsyncOpenAI
from openai.types.responses import Response

from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.agents.resilience_advisor.agent import create_agent
from supply_chain.agents.resilience_advisor.conversation import AdvisorConversation
from supply_chain.agents.resilience_advisor.definition import READ_TOOL_NAMES, definition
from supply_chain.runtime import Pricing, RunLimits


def response(
    calls: tuple[tuple[str, str, str], ...] = (), *, text: str | None = None,
    status: str = "completed", input_tokens: int = 100, output_tokens: int = 20,
    conversation_id: str = "conv_offline",
) -> Response:
    output: list[dict[str, object]] = [
        {"type": "function_call", "name": name, "call_id": call_id, "arguments": arguments}
        for name, call_id, arguments in calls
    ]
    if text is not None:
        output.append({
            "type": "message", "id": "message-test", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": text, "annotations": []}],
        })
    return Response.model_validate({
        "id": "response-test", "object": "response", "created_at": 0,
        "model": "gpt-6.1-sol", "parallel_tool_calls": False, "tool_choice": "auto",
        "tools": [], "output": output, "status": status,
        "conversation": {"id": conversation_id},
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens,
                  "total_tokens": input_tokens + output_tokens,
                  "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0},
                  "output_tokens_details": {"reasoning_tokens": 0}},
    })


class OfflineFoundry:
    def __init__(self, case: unittest.TestCase, service: MagicMock) -> None:
        def unexpected_request(request: httpx.Request) -> httpx.Response:
            raise AssertionError(f"Unexpected offline HTTP request: {request.method} {request.url}")

        self.client = AsyncOpenAI(
            api_key="offline-test-only", base_url="https://example.invalid", max_retries=0,
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(unexpected_request)),
        )
        self.client.with_options = MagicMock(return_value=self.client)

        async def create(**kwargs):
            value = service.responses.create(**kwargs)
            return SimpleNamespace(headers={}, parse=lambda: value)

        self.client.responses.with_raw_response.create = AsyncMock(side_effect=create)
        self.project = MagicMock(spec=AIProjectClient)
        self.project.agents = MagicMock()
        self.project.get_openai_client.return_value = self.client
        self.session = AgentSession(service_session_id="conv_offline")
        case.addCleanup(lambda: asyncio.run(self.client.close()))

    def run(self, advisor: AdvisorConversation, message: str = "Explain the delay."):
        agent = create_agent(self.project, "3", conversation=advisor)
        return asyncio.run(advisor.reply(agent, self.session, message))


class RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.store = DemoStore(Path(temporary.name) / "runtime.sqlite3")
        self.store.initialize()
        self.actor = DemoActor("demo-viewer", DemoRole.VIEWER)
        self.session = ToolSession(self.store, self.actor)
        self.client = MagicMock()
        self.offline = OfflineFoundry(self, self.client)
        self.pricing = Pricing(Decimal("2"), Decimal("10"), "offline test fixture, not a live rate")
        self.loop = self.new_loop()

    def new_loop(self, **limits) -> AdvisorConversation:
        return AdvisorConversation(self.session, pricing=self.pricing, limits=RunLimits(**limits))

    def final_answer(self) -> str:
        return json.dumps({
            "message": "EXPRESS costs five more for one extra day of margin. No stock has moved.",
            "evidence": [self.store.compare_options(self.actor)],
        })

    def successful_responses(self) -> list[Response]:
        return [
            response((("read_planning_snapshot", "call-1", "{}"),
                      ("read_transfer_policy", "call-2", "{}"))),
            response((("compare_transfer_options", "call-3", "{}"),)),
            response(text=self.final_answer()),
        ]

    def assert_run_error(self, code: str) -> None:
        with self.assertRaises(ToolError) as caught:
            self.offline.run(self.loop)
        self.assertEqual(caught.exception.code, code)

    def test_sdk_definition_exposes_exactly_six_strict_advisor_tools(self) -> None:
        agent = definition("deployment-test")
        self.assertEqual(agent.kind, "prompt")
        self.assertEqual(agent.model, "deployment-test")
        self.assertEqual({tool.name for tool in agent.tools}, READ_TOOL_NAMES | {
            "create_transfer_proposal", "execute_approved_transfer", "read_transfer_result",
        })
        for tool in agent.tools:
            self.assertTrue(tool.strict)
            self.assertFalse(tool.parameters["additionalProperties"])

    def test_sdk_call_ids_continue_same_conversation_without_stock_effects(self) -> None:
        before = self.store.read_snapshot(self.actor)
        self.client.responses.create.side_effect = self.successful_responses()
        result = self.offline.run(self.loop)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(self.loop.turn_tools, READ_TOOL_NAMES)
        self.assertEqual(self.loop.safety.usage.model_requests, 3)
        self.assertEqual(self.loop.safety.usage.tool_calls, 3)
        self.assertEqual(self.loop.safety.usage.total_tokens, 360)
        self.assertEqual(self.store.read_snapshot(self.actor), before)
        requests = self.client.responses.create.call_args_list
        self.assertEqual([request.kwargs["conversation"] for request in requests], ["conv_offline"] * 3)
        outputs = requests[1].kwargs["input"]
        self.assertEqual([item["call_id"] for item in outputs], ["call-1", "call-2"])
        self.assertEqual([item["type"] for item in outputs], ["function_call_output"] * 2)
        self.assertEqual(json.loads(outputs[0]["output"])["source"]["available"], 50)
        self.assertEqual(requests[2].kwargs["input"][0]["call_id"], "call-3")
        for request in requests:
            self.assertEqual(request.kwargs["max_output_tokens"], 4096)
            self.assertNotIn("tools", request.kwargs)
            self.assertEqual(request.kwargs["extra_body"]["agent_reference"], {
                "type": "agent_reference", "name": "supply-chain-resilience-advisor", "version": "3",
            })
            self.assertEqual(request.kwargs["truncation"], "disabled")
        self.client.responses.input_tokens.count.assert_not_called()

    def test_forbidden_tool_stops_entire_batch_before_dispatch(self) -> None:
        self.client.responses.create.return_value = response((
            ("read_planning_snapshot", "safe", "{}"),
            ("execute_approved_transfer", "forbidden", '{"proposal_id":"injected"}'),
        ))
        with patch.object(self.session, "dispatch", wraps=self.session.dispatch) as dispatch:
            self.assert_run_error("forbidden_tool")
        dispatch.assert_not_called()

    def test_intermediate_assistant_text_does_not_corrupt_final_json(self) -> None:
        responses = self.successful_responses()
        responses[0] = response((
            ("read_planning_snapshot", "call-1", "{}"),
            ("read_transfer_policy", "call-2", "{}"),
        ), text="I will investigate the stock and policy.")
        self.client.responses.create.side_effect = responses
        self.assertEqual(self.offline.run(self.loop)["status"], "completed")

    def test_batch_tool_limit_stops_before_any_dispatch(self) -> None:
        self.loop = self.new_loop(tool_calls=1)
        self.client.responses.create.return_value = self.successful_responses()[0]
        with patch.object(self.session, "dispatch") as dispatch:
            self.assert_run_error("tool_limit")
        dispatch.assert_not_called()

    def test_invalid_arguments_in_later_call_stop_entire_batch(self) -> None:
        self.client.responses.create.return_value = response((
            ("read_planning_snapshot", "safe", "{}"),
            ("read_transfer_policy", "bad", '{"actor":"untrusted"}'),
        ))
        with patch.object(self.session, "dispatch", wraps=self.session.dispatch) as dispatch:
            self.assert_run_error("invalid_arguments")
        dispatch.assert_not_called()

    def test_fatal_tool_error_stops_siblings_and_settlement_before_network(self) -> None:
        self.client.responses.create.return_value = self.successful_responses()[0]
        failure = {"status": "error", "error": {"code": "database_error", "message": "offline failure"}}
        with patch.object(self.session, "dispatch", return_value=failure) as dispatch:
            self.assert_run_error("tool_failed")
            dispatch.assert_called_once_with("read_planning_snapshot", "{}")
        self.assertEqual(self.loop.safety.usage.tool_calls, 1)
        self.assertEqual(self.loop.safety.seen_call_ids, {"call-1"})
        self.assertFalse(self.loop.safety.usage.usage_unreconciled)
        self.assert_run_error("tool_failed")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_real_openai_http_serialization_uses_version_pinned_managed_agent(self) -> None:
        requests = []
        results = iter(self.successful_responses())

        def service(request: httpx.Request) -> httpx.Response:
            requests.append(json.loads(request.content))
            return httpx.Response(200, json=next(results).model_dump(mode="json"))

        async def run():
            async with AsyncOpenAI(
                api_key="offline-test-only", base_url="https://example.invalid", max_retries=2,
                http_client=httpx.AsyncClient(transport=httpx.MockTransport(service)),
            ) as client:
                project = MagicMock(spec=AIProjectClient)
                project.get_openai_client.return_value = client
                async with create_agent(project, "3", conversation=self.loop) as agent:
                    self.assertEqual(agent.client.client.max_retries, 0)
                    return await self.loop.reply(agent, self.offline.session, "Explain the delay.")

        self.assertEqual(asyncio.run(run())["status"], "completed")
        self.assertEqual(len(requests), 3)
        for request in requests:
            self.assertEqual(request["agent_reference"], {
                "type": "agent_reference", "name": "supply-chain-resilience-advisor", "version": "3",
            })
            self.assertEqual(request["conversation"], "conv_offline")
            self.assertNotIn("tools", request)
        self.assertEqual([item["call_id"] for item in requests[1]["input"]], ["call-1", "call-2"])

    def test_unexpected_tool_exception_is_fatal_not_a_recoverable_model_result(self) -> None:
        self.client.responses.create.return_value = self.successful_responses()[0]
        with patch.object(self.session, "dispatch", side_effect=RuntimeError("offline callback failure")) as dispatch:
            self.assert_run_error("tool_exception")
        dispatch.assert_called_once()
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_real_sdk_transient_http_error_is_not_retried(self) -> None:
        requests = []

        def unavailable(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(503, json={"error": {"message": "offline unavailable", "type": "server_error"}})

        async def run():
            async with AsyncOpenAI(
                api_key="offline-test-only", base_url="https://example.invalid", max_retries=2,
                http_client=httpx.AsyncClient(transport=httpx.MockTransport(unavailable)),
            ) as client:
                project = MagicMock(spec=AIProjectClient)
                project.get_openai_client.return_value = client
                async with create_agent(project, "3", conversation=self.loop) as agent:
                    await self.loop.reply(agent, self.offline.session, "Explain the delay.")

        with self.assertRaises(AgentFrameworkException):
            asyncio.run(run())
        self.assertEqual(len(requests), 1)
        self.assertTrue(self.loop.safety.usage.usage_unreconciled)

    def test_repeated_and_empty_call_ids_are_rejected(self) -> None:
        for ids in (("same", "same"), ("", "second")):
            with self.subTest(ids=ids):
                self.loop = self.new_loop()
                self.client.responses.create.return_value = response((
                    ("read_planning_snapshot", ids[0], "{}"),
                    ("read_transfer_policy", ids[1], "{}"),
                ))
                self.assert_run_error("invalid_call_id")

    def test_call_ids_cannot_be_reused_in_later_response(self) -> None:
        self.client.responses.create.side_effect = [
            response((("read_planning_snapshot", "same", "{}"),)),
            response((("read_transfer_policy", "same", "{}"),)),
        ]
        self.assert_run_error("invalid_call_id")

    def test_tool_error_is_explicit_and_no_fallback_answer_is_requested(self) -> None:
        self.client.responses.create.return_value = response((
            ("read_planning_snapshot", "bad-arguments", '{"actor":"injected"}'),
        ))
        self.assert_run_error("invalid_arguments")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_token_threshold_is_checked_after_actual_usage(self) -> None:
        self.loop = self.new_loop(total_tokens=119)
        self.client.responses.create.return_value = response(text="{}")
        self.assert_run_error("token_limit")
        self.assertEqual(self.client.responses.create.call_count, 1)
        self.assertEqual(self.loop.safety.usage.total_tokens, 120)

    def test_cost_threshold_is_checked_after_actual_usage(self) -> None:
        for ceiling, expected in ((Decimal("0.00119"), "spend_limit"), (Decimal("0.00120"), "invalid_answer")):
            with self.subTest(ceiling=ceiling):
                self.loop = self.new_loop(spend_eur=ceiling)
                self.client.responses.create.return_value = response(text="{}")
                self.assert_run_error(expected)

    def test_aggregate_token_limit_includes_prior_response_usage(self) -> None:
        self.loop = self.new_loop(total_tokens=120)
        self.client.responses.create.return_value = response((("read_planning_snapshot", "one", "{}"),))
        self.assert_run_error("token_limit")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_request_limit_stops_the_loop(self) -> None:
        self.loop = self.new_loop(model_requests=1)
        self.client.responses.create.return_value = self.successful_responses()[0]
        self.assert_run_error("request_limit")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_unsupported_token_count_is_never_called(self) -> None:
        self.client.responses.input_tokens.count.side_effect = TimeoutError("count unavailable")
        self.client.responses.create.side_effect = self.successful_responses()
        self.assertEqual(self.offline.run(self.loop)["status"], "completed")
        self.client.responses.input_tokens.count.assert_not_called()

    def test_unreconciled_usage_is_explicit_and_stops_before_request(self) -> None:
        self.loop.safety.usage.usage_unreconciled = True
        self.assertTrue(self.loop.safety.usage.summary(self.pricing)["usage_unreconciled"])
        self.assert_run_error("uncertain_request")
        self.client.responses.create.assert_not_called()

    def test_lost_response_marks_usage_unknown_and_cannot_retry(self) -> None:
        self.client.responses.create.side_effect = TimeoutError("lost response")
        with self.assertRaisesRegex(AgentFrameworkException, "lost response"):
            self.offline.run(self.loop)
        self.assertTrue(self.loop.safety.usage.usage_unreconciled)
        self.assertEqual(self.loop.safety.usage.model_requests, 1)
        self.assert_run_error("uncertain_request")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_missing_usage_remains_unreconciled(self) -> None:
        result = response(text="{}")
        result.usage = None
        self.client.responses.create.return_value = result
        self.assert_run_error("missing_usage")
        self.assertTrue(self.loop.safety.usage.usage_unreconciled)

    def test_invalid_usage_remains_unreconciled(self) -> None:
        result = response(text="{}")
        result.usage.total_tokens += 1
        self.client.responses.create.return_value = result
        self.assert_run_error("invalid_usage")
        self.assertTrue(self.loop.safety.usage.usage_unreconciled)

    def test_incomplete_response_stops_and_accounts_for_usage(self) -> None:
        self.client.responses.create.return_value = response(status="incomplete", text="{}")
        self.assert_run_error("response_failed")
        self.assertEqual(self.loop.safety.usage.total_tokens, 120)

    def test_output_maximum_violation_stops_further_inference(self) -> None:
        self.client.responses.create.return_value = response(output_tokens=4097, text="{}")
        self.assert_run_error("usage_bound_mismatch")
        self.assertEqual(self.loop.safety.usage.total_tokens, 4197)
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_hallucinated_grounding_without_tools_is_not_a_success(self) -> None:
        self.client.responses.create.return_value = response(text=self.final_answer())
        self.assert_run_error("ungrounded_answer")

    def test_invalid_final_shapes_are_rejected(self) -> None:
        for text in ("not json", "[]", '{"options":[],"explanation":"invented"}'):
            with self.subTest(text=text):
                self.loop = self.new_loop()
                self.client.responses.create.side_effect = self.successful_responses()[:-1] + [response(text=text)]
                self.assert_run_error("invalid_answer")

    def test_changed_numeric_or_boolean_evidence_is_rejected(self) -> None:
        for field, value in (("feasible", 1), ("cost", 91)):
            with self.subTest(field=field):
                self.loop = self.new_loop()
                answer = json.loads(self.final_answer())
                answer["evidence"][0]["options"][0][field] = value
                self.client.responses.create.side_effect = self.successful_responses()[:-1] + [
                    response(text=json.dumps(answer)),
                ]
                self.assert_run_error("ungrounded_answer")

    def test_invalid_limits_and_unverified_prices_are_rejected(self) -> None:
        for fields in ({"model_requests": 21}, {"tool_calls": 21}, {"total_tokens": 100001},
                       {"total_tokens": True}, {"spend_eur": Decimal("NaN")}, {"spend_eur": Decimal("11")}):
            with self.subTest(fields=fields), self.assertRaises(ToolError):
                RunLimits(**fields)
        for rate in (Decimal("NaN"), Decimal("Infinity"), Decimal("0"), Decimal("-1")):
            with self.subTest(rate=rate), self.assertRaises(ToolError):
                Pricing(rate, Decimal("10"), "test")
        with self.assertRaises(ToolError):
            Pricing(Decimal("2"), Decimal("10"), "")
