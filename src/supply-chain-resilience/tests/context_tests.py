"""Authoritative scenario presentation, independent of the advisor's wording."""

from dataclasses import asdict, replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from supply_chain.agents.resilience_advisor.definition import instructions
from supply_chain.data import SCENARIO, load_snapshot
from supply_chain.domain import DemoActor, DemoRole, PlanningContext, Snapshot, ToolError, assess_transfers
from supply_chain.store import DemoStore


PLANNER = DemoActor("planner", DemoRole.PLANNER)
APPROVER = DemoActor("approver", DemoRole.APPROVER)


class ContextTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.snapshot = load_snapshot()
        self.store = DemoStore(self.directory / "planning.sqlite3")
        self.store.initialize(self.snapshot)

    def error(self, code, function, *args):
        with self.assertRaises(ToolError) as raised:
            function(*args)
        self.assertEqual(raised.exception.code, code)

    def test_calendar_dates_and_currency_come_from_explicit_scenario(self):
        facts = self.store.read_snapshot(PLANNER)
        self.assertEqual(facts["context"]["day_one"], "2026-11-09")
        self.assertEqual(facts["context"]["day_unit"], "calendar_day")
        self.assertEqual(facts["context"]["currency"], "EUR")
        self.assertEqual(facts["context"]["labels"]["W-B"], "Reserve warehouse")
        self.assertEqual([order["due_date"] for order in facts["orders"]], ["2026-11-11", "2026-11-12"])
        self.assertEqual(facts["supplier_receipt"], {
            "quantity": 40, "original_day": 1, "delayed_day": 6,
            "original_date": "2026-11-09", "delayed_date": "2026-11-14",
        })
        compared = self.store.compare_options(PLANNER)
        self.assertEqual(
            [(option["arrival_date"], option["completion_date"]) for option in compared["options"]],
            [("2026-11-10", "2026-11-11"), ("2026-11-09", "2026-11-10")],
        )
        self.assertEqual(self.store.read_policy(PLANNER)["context"], facts["context"])

    def test_alternate_calendar_currency_and_names_do_not_change_business_rules(self):
        context = PlanningContext("2032-02-28", "USD", {"BOARD-1": "Alternate component", "W-B": "Depot East"})
        alternate = replace(self.snapshot, context=context)
        compared = assess_transfers(alternate)
        baseline = assess_transfers(Snapshot())
        self.assertEqual(compared["context"]["currency"], "USD")
        self.assertEqual(compared["context"]["labels"]["W-B"], "Depot East")
        self.assertEqual(
            [(option["arrival_date"], option["completion_date"]) for option in compared["options"]],
            [("2032-02-29", "2032-03-01"), ("2032-02-28", "2032-02-29")],
        )
        for option, expected in zip(compared["options"], baseline["options"], strict=True):
            self.assertEqual({key: value for key, value in option.items()
                              if key not in {"arrival_date", "completion_date"}}, expected)
        for key in ("shortage", "demand", "source_available", "cost_cap", "status"):
            self.assertEqual(compared[key], baseline[key])

    def test_missing_context_does_not_invent_dates_names_or_currency(self):
        facts = Snapshot().planning_data()
        self.assertNotIn("context", facts)
        self.assertNotIn("due_date", facts["orders"][0])
        self.assertNotIn("arrival_date", assess_transfers(Snapshot())["options"][0])
        self.assertNotIn("context", Snapshot().policy_data())

    def test_context_is_explicit_and_validated(self):
        values = json.loads(SCENARIO.read_text(encoding="utf-8"))["context"]
        for changes in (
            {"day_one": "2026-02-30"}, {"day_one": "20261109"}, {"day_one": None},
            {"currency": "eur"}, {"currency": "\u20ac"}, {"labels": {}},
            {"labels": {"W-A": ""}}, {"labels": {"W-A": 4}},
        ):
            with self.subTest(changes=changes):
                self.error("invalid_context", PlanningContext.from_data, {**values, **changes})
        self.error("invalid_context", PlanningContext.from_data, {"day_one": "2026-11-09"})
        self.error("invalid_context", PlanningContext.from_data, {**values, "extra": True})
        context = PlanningContext.from_data(values)
        for day in (0, -1, True, 1.5):
            self.error("invalid_context", context.date_for, day)
        self.error("invalid_context", PlanningContext("9999-12-31", "EUR", {"x": "X"}).date_for, 2)

    def test_scenario_rejects_missing_presentation_instead_of_defaulting(self):
        values = json.loads(SCENARIO.read_text(encoding="utf-8"))
        del values["context"]
        path = self.directory / "missing.json"
        path.write_text(json.dumps(values), encoding="utf-8")
        self.error("invalid_scenario", load_snapshot, path)

    def test_exact_proposal_persists_context_through_approval_and_readback(self):
        proposal = self.store.create_proposal(PLANNER, "EXPRESS")
        self.assertEqual(proposal["arrival_date"], "2026-11-09")
        self.assertEqual(proposal["completion_date"], "2026-11-10")
        self.assertEqual(proposal["context"], self.snapshot.context.data())
        restored = DemoStore(self.store.path)
        self.assertEqual(restored.read_result(PLANNER, proposal["proposal_id"]), proposal)
        approved = restored.approve(APPROVER, proposal["proposal_id"])
        result = restored.execute(PLANNER, proposal["proposal_id"])
        self.assertEqual(result["proposal"]["context"], approved["context"])
        self.assertEqual(result["proposal"]["completion_date"], approved["completion_date"])
        self.assertEqual(restored.read_result(PLANNER, proposal["proposal_id"]), result)
        self.assertEqual(restored.read_snapshot(PLANNER)["source"]["reserved"], 70)

    def test_changed_context_requires_new_approval_even_without_version_bump(self):
        proposal = self.store.create_proposal(PLANNER, "STANDARD")
        self.store.approve(APPROVER, proposal["proposal_id"])
        changed = asdict(replace(self.snapshot.context, currency="USD"))
        with self.store._connection(write=True) as connection:
            connection.execute("UPDATE scenario SET context_json = ?", (json.dumps(changed),))
        self.error("stale_proposal", self.store.execute, PLANNER, proposal["proposal_id"])
        self.assertEqual(self.store.read_snapshot(PLANNER)["source"]["reserved"], 30)

    def test_tampered_proposal_context_cannot_be_approved(self):
        proposal = self.store.create_proposal(PLANNER, "STANDARD")
        changed = asdict(replace(self.snapshot.context, day_one="2030-01-01"))
        with self.store._connection(write=True) as connection:
            connection.execute("UPDATE proposals SET context_json = ?", (json.dumps(changed),))
        self.error("invalid_proposal", self.store.approve, APPROVER, proposal["proposal_id"])

    def test_tampered_approved_context_cannot_execute(self):
        proposal = self.store.create_proposal(PLANNER, "STANDARD")
        self.store.approve(APPROVER, proposal["proposal_id"])
        changed = asdict(replace(self.snapshot.context, currency="USD"))
        with self.store._connection(write=True) as connection:
            connection.execute("UPDATE proposals SET context_json = ?", (json.dumps(changed),))
        self.error("approval_mismatch", self.store.execute, PLANNER, proposal["proposal_id"])

    def test_corrupt_persisted_context_is_an_explicit_error(self):
        with self.store._connection(write=True) as connection:
            connection.execute("UPDATE scenario SET context_json = 'not-json'")
        self.error("invalid_database", self.store.read_snapshot, PLANNER)

    def test_prompt_uses_writing_principles_not_fixture_values(self):
        prompt = instructions("advisor")
        for value in ("HUB-1", "BOARD-1", "W-A", "W-B", "C-1", "C-2", "2026-11-09", "EUR"):
            self.assertNotIn(value, prompt)
        self.assertIn("not a mandatory script", prompt)
        self.assertIn("never invent dates, currency, names", prompt)
        self.assertIn("no buffer", prompt)
