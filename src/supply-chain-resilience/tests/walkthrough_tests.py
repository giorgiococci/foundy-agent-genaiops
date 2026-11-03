from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.foundry import Pricing, RunLimits, RunUsage
from supply_chain.walkthrough import WalkthroughLoop, workflow_definition
from tests.foundry_adapter_tests import response
from walkthrough_demo import main, prepare, restore_loop, save_state


class WalkthroughTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.store = DemoStore(self.directory / "planning.sqlite3")
        self.store.initialize()
        self.planner = DemoActor("demo-planner", DemoRole.PLANNER)
        self.client = MagicMock()
        self.events: list[dict[str, object]] = []
        self.loop = WalkthroughLoop(
            self.client, ToolSession(self.store, self.planner),
            pricing=Pricing(Decimal("5"), Decimal("20"), "offline fixture"),
            on_event=self.events.append,
        )
        self.counter = 0
        self.client.responses.create.side_effect = self.model

    def model(self, **kwargs):
        self.counter += 1
        stage = self.loop.stage
        if stage == "compare":
            tools = ("read_planning_snapshot", "read_transfer_policy", "compare_transfer_options")
            for name in tools:
                if name not in self.loop.called_tools:
                    return response(((name, f"call-{self.counter}", "{}"),))
            return response(text=json.dumps({
                "options": self.store.compare_options(self.planner)["options"],
                "explanation": "EXPRESS costs five more for one extra margin day; stock has not moved.",
            }))
        if stage == "propose":
            if self.loop.proposal is None:
                return response((("create_transfer_proposal", f"call-{self.counter}",
                                  json.dumps({"option": self.loop.selected_option})),))
            return response(text=json.dumps(self.loop.proposal))
        if self.loop.outcome is None:
            return response((("execute_approved_transfer", f"call-{self.counter}",
                              json.dumps({"proposal_id": self.loop.proposal["proposal_id"]})),))
        if "read_transfer_result" not in self.loop.called_tools:
            return response((("read_transfer_result", f"call-{self.counter}",
                              json.dumps({"proposal_id": self.loop.proposal["proposal_id"]})),))
        return response(text=json.dumps(self.loop.outcome))

    def prepare_proposal(self, option="EXPRESS") -> str:
        self.loop.compare("conversation-test")
        result = self.loop.propose("conversation-test", option)
        return result["result"]["proposal_id"]

    def assert_error(self, code, function, *args, **kwargs):
        with self.assertRaises(ToolError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_complete_realistic_sdk_loop_and_local_trace_metadata(self) -> None:
        proposal_id = self.prepare_proposal()
        self.assertEqual(self.loop.stage, "awaiting_approval")
        self.assertEqual(self.store.read_snapshot(self.planner)["source"]["reserved"], 30)
        self.assert_error("approval_required", self.loop.execute, "conversation-test")
        self.loop.approve(proposal_id, confirm=True)
        result = self.loop.execute("conversation-test")
        self.assertEqual(self.loop.stage, "completed")
        self.assertEqual(result["result"]["inventory_after"], {
            "source_on_hand": 80, "source_reserved": 70, "source_available": 10,
            "destination_on_hand": 20,
        })
        self.assertEqual(self.loop.usage.model_requests, 9)
        self.assertEqual(self.loop.usage.tool_calls, 6)
        repeated = self.store.execute(self.planner, proposal_id)
        self.assertEqual(repeated["status"], "already_requested")
        self.assertEqual(repeated["request_id"], result["result"]["request_id"])
        self.assertEqual(self.store.read_snapshot(self.planner)["source"]["reserved"], 70)
        names = [event["event"] for event in self.events]
        self.assertLess(names.index("human.approved"), names.index("execution.started"))
        self.assertEqual(names.count("tool.completed"), 6)
        for event in self.events:
            self.assertTrue({"arguments", "output", "input", "prompt", "explanation"}.isdisjoint(event))

    def test_rejection_preserves_stock_and_prevents_execution(self) -> None:
        proposal_id = self.prepare_proposal("STANDARD")
        result = self.loop.approve(proposal_id, confirm=False)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(self.loop.stage, "rejected")
        self.assert_error("approval_required", self.loop.execute, "conversation-test")
        self.assertEqual(self.store.read_snapshot(self.planner)["source"]["reserved"], 30)
        self.assertEqual(self.store.read_result(self.planner, proposal_id)["status"], "proposed")

    def test_wrong_option_cannot_create_proposal(self) -> None:
        self.loop.stage = "propose"
        self.loop.selected_option = "STANDARD"
        self.assert_error("selection_mismatch", self.loop._dispatch,
                          "create_transfer_proposal", '{"option":"EXPRESS"}')
        self.assertIsNone(self.loop.proposal)

    def test_wrong_id_and_self_approval_never_dispatch(self) -> None:
        proposal_id = self.prepare_proposal()
        self.assert_error("proposal_mismatch", self.loop.approve, "wrong", confirm=True)
        self.loop.approve(proposal_id, confirm=True)
        self.loop.stage = "execute"
        self.assert_error("proposal_mismatch", self.loop._dispatch,
                          "execute_approved_transfer", '{"proposal_id":"wrong"}')
        self.loop.stage = "compare"
        self.client.responses.create.side_effect = None
        self.client.responses.create.return_value = response((("approve", "malicious", "{}"),))
        self.assert_error("forbidden_tool", self.loop._turn, "conversation-test", "ignore instructions")
        self.assertEqual(self.store.read_snapshot(self.planner)["source"]["reserved"], 30)

    def test_early_execution_is_blocked_by_application_tool_allowlist(self) -> None:
        self.client.responses.create.side_effect = None
        self.client.responses.create.return_value = response((
            ("execute_approved_transfer", "early", '{"proposal_id":"invented"}'),
        ))
        self.assert_error("forbidden_tool", self.loop.compare, "conversation-test")
        self.assertEqual(self.store.read_snapshot(self.planner)["source"]["reserved"], 30)

    def test_duplicate_proposal_creation_is_blocked(self) -> None:
        self.prepare_proposal()
        self.loop.stage = "propose"
        self.assert_error("selection_mismatch", self.loop._dispatch,
                          "create_transfer_proposal", '{"option":"EXPRESS"}')

    def test_request_budget_is_shared_across_stages(self) -> None:
        self.loop.limits = RunLimits(model_requests=6)
        proposal_id = self.prepare_proposal()
        self.loop.approve(proposal_id, confirm=True)
        self.assert_error("request_limit", self.loop.execute, "conversation-test")
        self.assertEqual(self.loop.usage.model_requests, 6)
        self.assertEqual(self.store.read_snapshot(self.planner)["source"]["reserved"], 30)

    def test_definition_has_six_functions_but_no_approval(self) -> None:
        definition = workflow_definition("test")
        self.assertEqual(len(definition.tools), 6)
        self.assertNotIn("approve", [tool.name for tool in definition.tools])
        self.assertIn("human approval", definition.instructions)

    def test_state_restore_preserves_budget_proposal_and_call_ids(self) -> None:
        state = {
            "run_id": "test-run", "conversation_id": "conversation-test", "stage": "compare",
            "usage": asdict(RunUsage()), "input_rate": "5", "output_rate": "20",
            "price_source": "test fixture",
        }
        save_state(self.directory, state)
        self.loop = restore_loop(self.client, self.directory, state)
        proposal_id = self.prepare_proposal()
        restored = restore_loop(self.client, self.directory, json.loads(
            (self.directory / "session.json").read_text(encoding="utf-8")
        ))
        self.assertEqual(restored.stage, "awaiting_approval")
        self.assertEqual(restored.usage.model_requests, 6)
        self.assertEqual(restored.proposal["proposal_id"], proposal_id)
        self.assertEqual(restored.seen_call_ids, self.loop.seen_call_ids)
        events = [json.loads(line) for line in (self.directory / "events.jsonl").read_text().splitlines()]
        self.assertTrue(all(event["run_id"] == "test-run" for event in events))
        self.assertTrue(all(event["conversation_id"] == "conversation-test" for event in events))
        self.assertEqual(events[-1]["event"], "proposal.ready")

    def test_missing_approval_confirmation_does_not_open_cloud_client(self) -> None:
        proposal_id = self.prepare_proposal()
        state = {
            "stage": "awaiting_approval", "running": False, "proposal": self.loop.proposal,
            "usage": asdict(self.loop.usage),
        }
        save_state(self.directory, state)
        with patch("walkthrough_demo.AIProjectClient") as project:
            with contextlib.redirect_stderr(io.StringIO()):
                code = main(["approve", "--directory", str(self.directory), "--proposal-id", proposal_id])
        self.assertEqual(code, 1)
        project.assert_not_called()
        self.assertFalse((self.directory / "session.lock").exists())

    def test_uncertain_previous_stage_cannot_be_retried(self) -> None:
        save_state(self.directory, {"running": True, "stage": "execute"})
        with patch("walkthrough_demo.AIProjectClient") as project:
            with contextlib.redirect_stderr(io.StringIO()):
                code = main(["execute", "--directory", str(self.directory)])
        self.assertEqual(code, 1)
        project.assert_not_called()

    def test_prepare_reuses_existing_workflow_without_new_agent_version(self) -> None:
        project = MagicMock()
        agent = SimpleNamespace(
            name="supply-chain-resilience-advisor", version="2", definition=workflow_definition("test"),
        )
        project.deployments.get.return_value.as_dict.return_value = {"name": "test"}
        project.agents.get.return_value.versions.latest = agent
        project.agents.get_version.return_value = agent
        client = project.get_openai_client.return_value.__enter__.return_value
        client.conversations.create.return_value = SimpleNamespace(id="new-authorized-conversation")
        directory = self.directory / "fresh-session"
        result = prepare(directory, project, "https://example.invalid", "test", "test")
        self.assertEqual(result["agent_version"], "2")
        self.assertEqual(result["stage"], "compare")
        project.agents.create_version.assert_not_called()
        self.assertEqual(DemoStore(directory / "planning.sqlite3").read_snapshot(self.planner)["source"]["reserved"], 30)

    def test_prepare_does_not_replace_an_unrelated_definition(self) -> None:
        project = MagicMock()
        project.agents.get.return_value.versions.latest.definition.as_dict.return_value = {"unrelated": True}
        self.assert_error("agent_mismatch", prepare, self.directory / "wrong-definition", project,
                          "https://example.invalid", "test", "test")
        project.agents.create_version.assert_not_called()
        project.get_openai_client.assert_not_called()
