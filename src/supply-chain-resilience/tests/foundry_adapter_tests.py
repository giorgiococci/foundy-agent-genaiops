"""Offline SDK adapter tests; run with the project-local Foundry environment."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from openai.types.responses import Response

from foundry_demo import main
from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.foundry import (
    READ_TOOL_NAMES, Pricing, ReadOnlyAgentLoop, RunLimits, agent_definition,
)


def response(
    calls: tuple[tuple[str, str, str], ...] = (), *, text: str | None = None,
    status: str = "completed", input_tokens: int = 100, output_tokens: int = 20,
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
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens,
                  "total_tokens": input_tokens + output_tokens,
                  "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0},
                  "output_tokens_details": {"reasoning_tokens": 0}},
    })


class FoundryAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.store = DemoStore(Path(temporary.name) / "baseline.sqlite3")
        self.store.initialize()
        self.actor = DemoActor("demo-viewer", DemoRole.VIEWER)
        self.session = ToolSession(self.store, self.actor)
        self.client = MagicMock()
        self.client.responses.input_tokens.count.return_value = SimpleNamespace(input_tokens=100)
        self.pricing = Pricing(Decimal("2"), Decimal("10"), "offline test fixture, not a live rate")
        self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing)

    def final_answer(self) -> str:
        return json.dumps({
            "options": self.store.compare_options(self.actor)["options"],
            "explanation": "EXPRESS costs five more for one extra day of margin. No stock has moved.",
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
            self.loop.run("conversation-test")
        self.assertEqual(caught.exception.code, code)

    def test_sdk_definition_exposes_exactly_three_read_tools(self) -> None:
        definition = agent_definition("deployment-test")
        self.assertEqual(definition.kind, "prompt")
        self.assertEqual(definition.model, "deployment-test")
        self.assertIsNotNone(definition.tools)
        self.assertEqual({tool.name for tool in definition.tools}, READ_TOOL_NAMES)
        for tool in definition.tools:
            self.assertTrue(tool.strict)
            self.assertFalse(tool.parameters["additionalProperties"])

    def test_real_sdk_response_objects_and_call_ids_continue_same_conversation(self) -> None:
        before = self.store.read_snapshot(self.actor)
        self.client.responses.create.side_effect = self.successful_responses()
        result = self.loop.run("conversation-test")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["called_tools"], sorted(READ_TOOL_NAMES))
        self.assertEqual(self.loop.usage.model_requests, 3)
        self.assertEqual(self.loop.usage.tool_calls, 3)
        self.assertEqual(self.loop.usage.total_tokens, 360)
        self.assertEqual(self.store.read_snapshot(self.actor), before)
        requests = self.client.responses.create.call_args_list
        self.assertEqual([request.kwargs["conversation"] for request in requests],
                         ["conversation-test"] * 3)
        outputs = requests[1].kwargs["input"]
        self.assertEqual([item["call_id"] for item in outputs], ["call-1", "call-2"])
        self.assertEqual([item["type"] for item in outputs], ["function_call_output"] * 2)
        self.assertEqual(json.loads(outputs[0]["output"])["source"]["available"], 50)
        self.assertEqual(requests[2].kwargs["input"][0]["call_id"], "call-3")
        for request in requests:
            self.assertEqual(request.kwargs["max_output_tokens"], 4096)
            self.assertFalse(request.kwargs["parallel_tool_calls"])
            self.assertEqual(request.kwargs["truncation"], "disabled")
        self.client.responses.input_tokens.count.assert_not_called()

    def test_forbidden_tool_stops_before_dispatch(self) -> None:
        self.client.responses.create.return_value = response((
            ("read_planning_snapshot", "safe", "{}"),
            ("execute_approved_transfer", "forbidden", '{"proposal_id":"injected"}'),
        ))
        with patch.object(self.session, "dispatch", wraps=self.session.dispatch) as dispatch:
            self.assert_run_error("forbidden_tool")
        dispatch.assert_not_called()

    def test_batch_tool_limit_stops_before_any_dispatch(self) -> None:
        self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing,
                                     limits=RunLimits(tool_calls=1))
        self.client.responses.create.return_value = self.successful_responses()[0]
        with patch.object(self.session, "dispatch") as dispatch:
            self.assert_run_error("tool_limit")
        dispatch.assert_not_called()

    def test_repeated_and_empty_call_ids_are_rejected(self) -> None:
        for ids in (("same", "same"), ("", "second")):
            with self.subTest(ids=ids):
                self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing)
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
        self.assert_run_error("tool_failed")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_token_threshold_is_checked_after_actual_usage(self) -> None:
        self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing,
                                     limits=RunLimits(total_tokens=119))
        self.client.responses.create.return_value = response(text="{}")
        self.assert_run_error("token_limit")
        self.assertEqual(self.client.responses.create.call_count, 1)
        self.assertEqual(self.loop.usage.total_tokens, 120)

    def test_cost_threshold_is_checked_after_actual_usage(self) -> None:
        for ceiling, expected in ((Decimal("0.00119"), "spend_limit"),
                                  (Decimal("0.00120"), "ungrounded_answer")):
            with self.subTest(ceiling=ceiling):
                self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing,
                                             limits=RunLimits(spend_eur=ceiling))
                self.client.responses.create.return_value = response(text="{}")
                self.assert_run_error(expected)

    def test_aggregate_token_limit_includes_prior_response_usage(self) -> None:
        self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing,
                                     limits=RunLimits(total_tokens=120))
        self.client.responses.create.return_value = response((
            ("read_planning_snapshot", "one", "{}"),
        ))
        self.assert_run_error("token_limit")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_request_limit_stops_the_loop(self) -> None:
        self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing,
                                     limits=RunLimits(model_requests=1))
        self.client.responses.create.return_value = self.successful_responses()[0]
        self.assert_run_error("request_limit")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_unsupported_token_count_is_never_called(self) -> None:
        self.client.responses.input_tokens.count.side_effect = TimeoutError("count unavailable")
        self.client.responses.create.side_effect = self.successful_responses()
        self.assertEqual(self.loop.run("conversation-test")["status"], "completed")
        self.client.responses.input_tokens.count.assert_not_called()

    def test_unreconciled_usage_is_explicit_in_summary(self) -> None:
        self.loop.usage.usage_unreconciled = True
        self.assertTrue(self.loop.usage.summary(self.pricing)["usage_unreconciled"])
        self.assert_run_error("uncertain_request")
        self.client.responses.create.assert_not_called()

    def test_lost_response_marks_usage_unknown_and_cannot_retry(self) -> None:
        self.client.responses.create.side_effect = TimeoutError("lost response")
        with self.assertRaisesRegex(TimeoutError, "lost response"):
            self.loop.run("conversation-test")
        self.assertTrue(self.loop.usage.usage_unreconciled)
        self.assertEqual(self.loop.usage.model_requests, 1)
        self.assert_run_error("already_started")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_missing_usage_remains_unreconciled(self) -> None:
        result = response(text="{}")
        result.usage = None
        self.client.responses.create.return_value = result
        self.assert_run_error("missing_usage")
        self.assertTrue(self.loop.usage.usage_unreconciled)

    def test_incomplete_response_stops_and_accounts_for_usage(self) -> None:
        self.client.responses.create.return_value = response(status="incomplete", text="{}")
        self.assert_run_error("response_failed")
        self.assertEqual(self.loop.usage.total_tokens, 120)

    def test_output_maximum_violation_stops_further_inference(self) -> None:
        self.client.responses.create.return_value = response(output_tokens=4097, text="{}")
        self.assert_run_error("usage_bound_mismatch")
        self.assertEqual(self.loop.usage.total_tokens, 4197)
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_hallucinated_or_missing_grounding_is_not_a_success(self) -> None:
        self.client.responses.create.return_value = response(text=self.final_answer())
        self.assert_run_error("ungrounded_answer")

    def test_invalid_final_shapes_are_rejected(self) -> None:
        numeric_boolean = json.loads(self.final_answer())
        numeric_boolean["options"][0]["feasible"] = 1
        wrong_cost = json.loads(self.final_answer())
        wrong_cost["options"][0]["cost"] = 91
        for text in ("not json", "[]", '{"options":[],"explanation":"invented"}',
                     json.dumps(numeric_boolean), json.dumps(wrong_cost)):
            with self.subTest(text=text):
                self.loop = ReadOnlyAgentLoop(self.client, self.session, pricing=self.pricing)
                responses = self.successful_responses()
                responses[-1] = response(text=text)
                self.client.responses.create.side_effect = responses
                self.assert_run_error("invalid_answer")

    def test_invalid_limits_and_unverified_prices_are_rejected(self) -> None:
        for fields in ({"model_requests": 11}, {"tool_calls": 21}, {"total_tokens": 100001},
                       {"total_tokens": True}, {"spend_eur": Decimal("NaN")},
                       {"spend_eur": Decimal("11")}):
            with self.subTest(fields=fields), self.assertRaises(ToolError):
                RunLimits(**fields)
        for rate in (Decimal("NaN"), Decimal("Infinity"), Decimal("0"), Decimal("-1")):
            with self.subTest(rate=rate), self.assertRaises(ToolError):
                Pricing(rate, Decimal("10"), "test")
        with self.assertRaises(ToolError):
            Pricing(Decimal("2"), Decimal("10"), "")

    def test_cli_run_without_pricing_stops_before_any_azure_client(self) -> None:
        with patch("foundry_demo.AIProjectClient") as project:
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                code = main(["run", "--endpoint", "https://example.invalid/api/projects/demo",
                             "--deployment", "test", "--tenant", "test"])
        self.assertEqual(code, 1)
        self.assertIn("unverified_pricing", stderr.getvalue())
        project.assert_not_called()

    def test_cli_reuses_named_version_without_creating_an_agent(self) -> None:
        with patch("foundry_demo.AzureCliCredential"), patch("foundry_demo.AIProjectClient") as factory:
            project = factory.return_value.__enter__.return_value
            project.deployments.get.return_value.as_dict.return_value = {"name": "test"}
            project.agents.get_version.return_value = SimpleNamespace(
                name="supply-chain-resilience-advisor", version="1",
                definition=agent_definition("test"),
            )
            project.agents.get.return_value.versions.latest.version = "1"
            client = project.get_openai_client.return_value.__enter__.return_value
            client.conversations.create.return_value = SimpleNamespace(id="conversation-offline")
            with patch("foundry_demo.ReadOnlyAgentLoop") as loop_factory:
                loop_factory.return_value.run.return_value = {"status": "completed"}
                with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                    code = main([
                        "run", "--endpoint", "https://example.invalid/api/projects/demo",
                        "--deployment", "test", "--tenant", "test",
                        "--input-eur-per-million", "5", "--output-eur-per-million", "20",
                        "--price-source", "offline fixture",
                    ])
        self.assertEqual(code, 0)
        project.agents.get_version.assert_called_once_with("supply-chain-resilience-advisor", "1")
        project.agents.create_version.assert_not_called()

    def test_cli_stops_before_inference_if_named_endpoint_version_changed(self) -> None:
        with patch("foundry_demo.AzureCliCredential"), patch("foundry_demo.AIProjectClient") as factory:
            project = factory.return_value.__enter__.return_value
            project.deployments.get.return_value.as_dict.return_value = {"name": "test"}
            project.agents.get_version.return_value = SimpleNamespace(
                name="supply-chain-resilience-advisor", version="1", definition=agent_definition("test"),
            )
            project.agents.get.return_value.versions.latest.version = "2"
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([
                    "run", "--endpoint", "https://example.invalid/api/projects/demo",
                    "--deployment", "test", "--tenant", "test",
                    "--input-eur-per-million", "5", "--output-eur-per-million", "20",
                    "--price-source", "offline fixture",
                ])
        self.assertEqual(code, 1)
        project.get_openai_client.assert_not_called()
