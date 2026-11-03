from __future__ import annotations

import contextlib
import io
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from demo import main
from supply_chain import (
    DemoActor, DemoRole, DemoStore, FUNCTION_TOOL_SPECS, ToolError, ToolSession,
)


PLANNER = DemoActor("demo-planner", DemoRole.PLANNER)
APPROVER = DemoActor("demo-approver", DemoRole.APPROVER)
VIEWER = DemoActor("demo-viewer", DemoRole.VIEWER)


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "scenario.sqlite3"
        self.store = DemoStore(self.path)
        self.store.initialize()
        self.session = ToolSession(self.store, PLANNER)

    def sql(self, statement: str, values: tuple[object, ...] = ()) -> None:
        with contextlib.closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute(statement, values)

    def counts(self) -> tuple[int, int]:
        with contextlib.closing(sqlite3.connect(self.path)) as connection:
            return (connection.execute("SELECT COUNT(*) FROM proposals").fetchone()[0],
                    connection.execute("SELECT COUNT(*) FROM requests").fetchone()[0])

    def proposal(self, option: str = "STANDARD") -> str:
        result = self.store.create_proposal(PLANNER, option)
        proposal_id = result["proposal_id"]
        self.assertIsInstance(proposal_id, str)
        return str(proposal_id)

    def approved(self, option: str = "STANDARD") -> str:
        proposal_id = self.proposal(option)
        self.store.approve(APPROVER, proposal_id)
        return proposal_id

    def assert_error(self, code: str, name: str, arguments: dict[str, object]) -> None:
        result = self.session.dispatch(name, json.dumps(arguments))
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"]["code"], code)

    def test_cli_walkthrough_persists_across_processes(self) -> None:
        path = Path(self.temporary.name) / "process walkthrough.sqlite3"
        script = Path(__file__).resolve().parents[1] / "demo.py"

        def cli(*arguments: str, expected_code: int = 0) -> dict[str, object]:
            completed = subprocess.run(
                [sys.executable, "-B", str(script), "--db", str(path), *arguments],
                capture_output=True, text=True, timeout=10, check=False,
            )
            self.assertEqual(completed.returncode, expected_code, completed.stderr)
            self.assertEqual(completed.stdout if expected_code else completed.stderr, "")
            payload: object = json.loads(completed.stderr if expected_code else completed.stdout)
            if not isinstance(payload, dict):
                raise AssertionError("Expected a JSON object from the CLI.")
            return payload

        cli("init")
        comparison = cli("compare")
        self.assertEqual(comparison["status"], "options_available")
        self.assertEqual([(option["option"], option["quantity"], option["cost"])
                          for option in comparison["options"]],
                         [("STANDARD", 40, 90), ("EXPRESS", 40, 95)])
        proposal = cli("propose", "EXPRESS")
        proposal_id = proposal["proposal_id"]
        assert isinstance(proposal_id, str)
        refused = cli("execute", proposal_id, expected_code=1)
        self.assertEqual(refused["error"]["code"], "approval_required")
        unconfirmed = cli("--role", "approver", "approve", proposal_id, expected_code=1)
        self.assertEqual(unconfirmed["error"]["code"], "confirmation_required")
        approval = cli("--role", "approver", "approve", proposal_id, "--confirm")
        self.assertEqual(approval["status"], "approved")
        outcome = cli("execute", proposal_id)
        self.assertEqual(outcome["status"], "requested")
        self.assertEqual(cli("execute", proposal_id), {**outcome, "status": "already_requested"})
        self.assertEqual(cli("result", proposal_id), outcome)
        snapshot = cli("snapshot")
        self.assertEqual(snapshot["snapshot_version"], 2)
        self.assertEqual(snapshot["source"], {
            "warehouse": "W-B", "on_hand": 80, "reserved": 70, "available": 10,
        })
        self.assertEqual(snapshot["local"], {"warehouse": "W-A", "on_hand": 20})
        self.assertEqual(cli("compare")["status"], "transfer_pending")

    def test_initialization_never_overwrites(self) -> None:
        proposal_id = self.proposal()
        with self.assertRaises(ToolError) as caught:
            self.store.initialize()
        self.assertEqual(caught.exception.code, "already_exists")
        self.assertEqual(self.store.read_result(VIEWER, proposal_id)["status"], "proposed")
        self.assertEqual(self.counts(), (1, 0))

    def test_store_with_spaces_in_path(self) -> None:
        path = Path(self.temporary.name) / "synthetic planning.sqlite3"
        store = DemoStore(path)
        store.initialize()
        self.assertEqual(store.read_snapshot(VIEWER)["source"]["available"], 50)

    def test_comparison_does_not_create_proposals_or_choose(self) -> None:
        result = self.session.dispatch("compare_transfer_options", "{}")
        self.assertEqual(result["status"], "options_available")
        self.assertEqual(self.counts(), (0, 0))
        self.assertIn("Human choice required", result["selection"])
        self.assert_error("invalid_arguments", "create_transfer_proposal", {})
        self.assertEqual(self.counts(), (0, 0))

    def test_selected_feasible_option_is_required(self) -> None:
        self.sql("UPDATE scenario SET cost_cap = 92")
        self.assert_error("infeasible", "create_transfer_proposal", {"option": "EXPRESS"})
        self.assertEqual(self.store.create_proposal(PLANNER, "STANDARD")["cost"], 90)
        self.assert_error("invalid_argument", "create_transfer_proposal", {"option": "fastest"})

    def test_no_proposals_for_incomplete_noimpact_or_infeasible_data(self) -> None:
        for update, code in (
            ("UPDATE scenario SET local_stock = 60", "no_impact"),
            ("UPDATE scenario SET local_stock = 20, cost_cap = NULL", "insufficient_data"),
            ("UPDATE scenario SET cost_cap = 80", "infeasible"),
            ("UPDATE scenario SET cost_cap = 100, source_stock = 60", "infeasible"),
        ):
            with self.subTest(code=code):
                self.sql(update)
                self.assert_error(code, "create_transfer_proposal", {"option": "STANDARD"})
        self.assertEqual(self.counts(), (0, 0))

    def test_proposal_and_approval_do_not_move_stock(self) -> None:
        proposal_id = self.proposal("EXPRESS")
        self.assertEqual(self.store.read_snapshot(VIEWER)["source"]["reserved"], 30)
        approved = self.store.approve(APPROVER, proposal_id)
        self.assertEqual((approved["option"], approved["cost"]), ("EXPRESS", 95))
        self.assertEqual(self.store.read_snapshot(VIEWER)["source"]["reserved"], 30)
        self.assertEqual(self.store.read_result(VIEWER, proposal_id)["status"], "approved")

    def test_no_action_without_approval(self) -> None:
        proposal_id = self.proposal()
        self.assert_error("approval_required", "execute_approved_transfer", {"proposal_id": proposal_id})
        self.assertEqual(self.store.read_snapshot(VIEWER)["source"]["reserved"], 30)
        self.assertEqual(self.counts(), (1, 0))

    def test_human_approval_is_not_a_tool(self) -> None:
        self.assertNotIn("approve", {tool["name"] for tool in FUNCTION_TOOL_SPECS})
        self.assert_error("unknown_tool", "approve", {"proposal_id": self.proposal()})
        with self.assertRaises(ToolError) as caught:
            self.store.approve(PLANNER, self.proposal())
        self.assertEqual(caught.exception.code, "unauthorized")

    def test_model_cannot_supply_identity_or_approval(self) -> None:
        proposal_id = self.proposal()
        for extra in ({"actor": "approver"}, {"role": "approver"}, {"approved": True},
                      {"approved_by": "demo-approver"}, {"quantity": 1}):
            with self.subTest(extra=extra):
                self.assert_error("invalid_arguments", "execute_approved_transfer",
                                  {"proposal_id": proposal_id, **extra})
        self.assertEqual(self.counts(), (1, 0))

    def test_unauthorized_writes_and_authorized_reads(self) -> None:
        for actor in (VIEWER, APPROVER):
            session = ToolSession(self.store, actor)
            self.assertEqual(session.dispatch("read_planning_snapshot", "{}")["status"], "ok")
            for name, arguments in (
                ("create_transfer_proposal", {"option": "STANDARD"}),
                ("execute_approved_transfer", {"proposal_id": self.approved()}),
            ):
                result = session.dispatch(name, json.dumps(arguments))
                self.assertEqual(result["error"]["code"], "unauthorized")
        self.assertEqual(self.counts()[1], 0)

    def test_execution_persists_exact_reservation_without_receipt(self) -> None:
        proposal_id = self.approved("EXPRESS")
        result = self.store.execute(PLANNER, proposal_id)
        self.assertEqual(result["status"], "requested")
        self.assertEqual(result["reservation"], {"warehouse": "W-B", "component": "BOARD-1", "quantity": 40})
        self.assertEqual(result["inventory_after"], {
            "source_on_hand": 80, "source_reserved": 70, "source_available": 10, "destination_on_hand": 20,
        })
        snapshot = DemoStore(self.path).read_snapshot(VIEWER)
        self.assertEqual(snapshot["source"], {"warehouse": "W-B", "on_hand": 80, "reserved": 70, "available": 10})
        self.assertEqual(snapshot["local"]["on_hand"], 20)
        self.assertEqual(snapshot["snapshot_version"], 2)
        self.assertEqual(snapshot["pending_request_count"], 1)

    def test_repeated_and_concurrent_execution_is_idempotent(self) -> None:
        proposal_id = self.approved()
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda _: self.store.execute(PLANNER, proposal_id), range(12)))
        self.assertEqual(sum(result["status"] == "requested" for result in results), 1)
        self.assertEqual(sum(result["status"] == "already_requested" for result in results), 11)
        self.assertEqual(len({result["request_id"] for result in results}), 1)
        self.assertEqual(self.counts(), (1, 1))
        self.assertEqual(self.store.read_snapshot(VIEWER)["source"]["reserved"], 70)

    def test_approval_is_bound_to_exact_proposal(self) -> None:
        first = self.approved("STANDARD")
        second = self.proposal("EXPRESS")
        self.assert_error("approval_required", "execute_approved_transfer", {"proposal_id": second})
        self.assertEqual(self.store.read_result(VIEWER, first)["status"], "approved")
        self.assertEqual(self.counts(), (2, 0))

    def test_changed_selection_invalidates_approval(self) -> None:
        proposal_id = self.approved()
        self.sql("UPDATE proposals SET option = 'EXPRESS', cost = 95, arrival_day = 1, completion_day = 2")
        self.assert_error("approval_mismatch", "execute_approved_transfer", {"proposal_id": proposal_id})
        self.assert_error("approval_mismatch", "read_transfer_result", {"proposal_id": proposal_id})
        self.assertEqual(self.counts(), (1, 0))

    def test_changed_facts_or_policy_reject_approval_even_without_version_bump(self) -> None:
        proposal_id = self.approved()
        for statement, restore in (
            ("UPDATE scenario SET source_reserved = 31", "UPDATE scenario SET source_reserved = 30"),
            ("UPDATE scenario SET cost_cap = 95", "UPDATE scenario SET cost_cap = 100"),
            ("UPDATE scenario SET policy_version = 'P-1:2'", "UPDATE scenario SET policy_version = 'P-1:1'"),
            ("UPDATE scenario SET version = 2", "UPDATE scenario SET version = 1"),
        ):
            with self.subTest(statement=statement):
                self.sql(statement)
                self.assert_error("stale_proposal", "execute_approved_transfer", {"proposal_id": proposal_id})
                self.assert_error("stale_proposal", "read_transfer_result", {"proposal_id": proposal_id})
                self.sql(restore)
        self.assertEqual(self.counts(), (1, 0))

    def test_stale_proposal_cannot_be_approved(self) -> None:
        proposal_id = self.proposal()
        self.sql("UPDATE scenario SET local_stock = 21")
        with self.assertRaises(ToolError) as caught:
            self.store.approve(APPROVER, proposal_id)
        self.assertEqual(caught.exception.code, "stale_proposal")

    def test_first_action_invalidates_other_approved_proposal(self) -> None:
        first = self.approved()
        second = self.approved("EXPRESS")
        self.store.execute(PLANNER, first)
        self.assert_error("stale_proposal", "execute_approved_transfer", {"proposal_id": second})
        self.assertEqual(self.counts(), (2, 1))

    def test_pending_request_prevents_new_recovery(self) -> None:
        self.store.execute(PLANNER, self.approved())
        self.assertEqual(self.store.compare_options(PLANNER)["status"], "transfer_pending")
        self.assert_error("transfer_pending", "create_transfer_proposal", {"option": "STANDARD"})
        self.assertEqual(self.counts(), (1, 1))

    def test_lost_response_is_reconciled_from_durable_result(self) -> None:
        proposal_id = self.approved()
        self.store.execute(PLANNER, proposal_id)  # Simulate the caller losing this return value.
        recovered = DemoStore(self.path).read_result(PLANNER, proposal_id)
        self.assertEqual(recovered["status"], "requested")
        duplicate = DemoStore(self.path).execute(PLANNER, proposal_id)
        self.assertEqual(duplicate["request_id"], recovered["request_id"])
        self.assertEqual(duplicate["status"], "already_requested")
        self.assertEqual(self.counts(), (1, 1))

    def test_request_insert_failure_rolls_back_inventory(self) -> None:
        proposal_id = self.approved()
        self.sql("CREATE TRIGGER reject_request BEFORE INSERT ON requests "
                 "BEGIN SELECT RAISE(ABORT, 'injected request failure'); END")
        with self.assertLogs("supply_chain", level="ERROR"):
            self.assert_error("database_error", "execute_approved_transfer", {"proposal_id": proposal_id})
        self.assertEqual(self.store.read_snapshot(VIEWER)["source"]["reserved"], 30)
        self.assertEqual(self.store.read_snapshot(VIEWER)["snapshot_version"], 1)
        self.assertEqual(self.store.read_result(VIEWER, proposal_id)["status"], "approved")
        self.assertEqual(self.counts(), (1, 0))

    def test_invalid_arguments_and_unknown_ids_are_explicit_errors(self) -> None:
        for arguments in ("not json", "[]", "null", '{"option":1}', '{"option":""}',
                          '{"option":"STANDARD","role":"approver"}'):
            with self.subTest(arguments=arguments):
                result = self.session.dispatch("create_transfer_proposal", arguments)
                self.assertEqual(result["error"]["code"], "invalid_arguments")
        for name in ("read_transfer_result", "execute_approved_transfer"):
            self.assert_error("not_found", name, {"proposal_id": "missing"})
        self.assert_error("unknown_tool", "delete_database", {})

    def test_function_contracts_match_dispatcher(self) -> None:
        names = [tool["name"] for tool in FUNCTION_TOOL_SPECS]
        self.assertEqual(len(names), len(set(names)))
        for tool in FUNCTION_TOOL_SPECS:
            parameters = tool["parameters"]
            self.assertTrue(tool["strict"])
            self.assertFalse(parameters["additionalProperties"])
            self.assertEqual(set(parameters["required"]), set(parameters["properties"]))
            self.assertNotIn("role", parameters["properties"])
            self.assertNotIn("approved", parameters["properties"])
            arguments = {key: ("STANDARD" if key == "option" else "missing")
                         for key in parameters["required"]}
            result = self.session.dispatch(tool["name"], json.dumps(arguments))
            if result["status"] == "error":
                self.assertNotIn(result["error"]["code"], ("unknown_tool", "invalid_arguments"))
            self.assert_error("invalid_arguments", tool["name"], {**arguments, "unexpected": True})

    def test_missing_database_does_not_create_a_fallback(self) -> None:
        path = Path(self.temporary.name) / "absent.sqlite3"
        session = ToolSession(DemoStore(path), PLANNER)
        with self.assertLogs("supply_chain", level="ERROR"):
            result = session.dispatch("read_planning_snapshot", "{}")
        self.assertEqual(result["error"]["code"], "database_error")
        self.assertFalse(path.exists())

    def test_invalid_stored_outcome_is_not_a_successful_fallback(self) -> None:
        proposal_id = self.approved()
        self.store.execute(PLANNER, proposal_id)
        for value in ("not json", "[]", '{"status":"approved"}'):
            with self.subTest(value=value):
                self.sql("UPDATE requests SET result_json = ?", (value,))
                self.assert_error("invalid_database", "read_transfer_result", {"proposal_id": proposal_id})
                self.assert_error("invalid_database", "execute_approved_transfer", {"proposal_id": proposal_id})
        self.assertEqual(self.counts(), (1, 1))
        self.assertEqual(self.store.read_snapshot(VIEWER)["source"]["reserved"], 70)

    def test_cli_walkthrough_and_human_confirmation(self) -> None:
        def invoke(*arguments: str) -> tuple[int, dict[str, object]]:
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = main(["--db", str(self.path), *arguments])
            return code, json.loads(stdout.getvalue() or stderr.getvalue())

        code, proposal = invoke("propose", "EXPRESS")
        self.assertEqual(code, 0)
        proposal_id = str(proposal["proposal_id"])
        code, result = invoke("execute", proposal_id)
        self.assertEqual((code, result["error"]["code"]), (1, "approval_required"))
        code, result = invoke("--role", "approver", "approve", proposal_id)
        self.assertEqual((code, result["error"]["code"]), (1, "confirmation_required"))
        code, result = invoke("--role", "approver", "approve", proposal_id, "--confirm")
        self.assertEqual((code, result["status"]), (0, "approved"))
        code, result = invoke("execute", proposal_id)
        self.assertEqual((code, result["status"]), (0, "requested"))
        code, result = invoke("result", proposal_id)
        self.assertEqual((code, result["status"]), (0, "requested"))
        self.assertEqual(self.counts(), (1, 1))

    def test_cli_initialization_variants_and_tool_listing(self) -> None:
        path = Path(self.temporary.name) / "variant.sqlite3"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["--db", str(path), "init", "--scenario", "ceiling-92"]), 0)
        store = DemoStore(path)
        self.assertEqual(store.read_policy(VIEWER)["cost_cap"], 92)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["tools"]), 0)
        self.assertEqual(json.loads(output.getvalue()), FUNCTION_TOOL_SPECS)

    def test_cli_reports_storage_error_with_nonzero_exit(self) -> None:
        with patch.object(DemoStore, "initialize", side_effect=PermissionError("injected")):
            with self.assertLogs(level="ERROR"), contextlib.redirect_stderr(io.StringIO()) as stderr:
                code = main(["init"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(stderr.getvalue())["error"]["code"], "storage_error")


if __name__ == "__main__":
    unittest.main()
