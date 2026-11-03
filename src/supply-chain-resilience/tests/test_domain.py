from __future__ import annotations

import unittest

from supply_chain import Snapshot, ToolError, assess_transfers


class ArithmeticTests(unittest.TestCase):
    def test_exact_baseline(self) -> None:
        result = assess_transfers(Snapshot())
        self.assertEqual((result["status"], result["shortage"], result["source_available"]),
                         ("options_available", 40, 50))
        self.assertEqual(result["options"], [
            {"option": "STANDARD", "quantity": 40, "cost": 90, "arrival_day": 2,
             "completion_day": 3, "delivery_margin_days": {"C-1": 0, "C-2": 1},
             "feasible": True, "reasons": []},
            {"option": "EXPRESS", "quantity": 40, "cost": 95, "arrival_day": 1,
             "completion_day": 2, "delivery_margin_days": {"C-1": 1, "C-2": 2},
             "feasible": True, "reasons": []},
        ])

    def test_no_impact(self) -> None:
        result = assess_transfers(Snapshot(local_stock=60))
        self.assertEqual((result["status"], result["shortage"], result["options"]), ("no_impact", 0, []))

    def test_insufficient_source(self) -> None:
        result = assess_transfers(Snapshot(source_stock=60))
        self.assertEqual((result["status"], result["source_available"]), ("infeasible", 30))
        for option in result["options"]:
            self.assertFalse(option["feasible"])
            self.assertIn("insufficient_available_stock", option["reasons"])

    def test_cost_thresholds_including_equality(self) -> None:
        for ceiling, expected in ((100, [True, True]), (95, [True, True]),
                                  (92, [True, False]), (90, [True, False]), (80, [False, False])):
            with self.subTest(ceiling=ceiling):
                result = assess_transfers(Snapshot(cost_cap=ceiling))
                self.assertEqual([option["feasible"] for option in result["options"]], expected)

    def test_missing_policy_is_not_a_default(self) -> None:
        result = assess_transfers(Snapshot(cost_cap=None))
        self.assertEqual((result["status"], result["options"]), ("insufficient_data", []))
        self.assertEqual(Snapshot(cost_cap=None).policy_data()["status"], "insufficient_data")

    def test_invalid_fixtures_are_rejected(self) -> None:
        for fields in ({"version": 0}, {"source_reserved": 81}, {"local_stock": -1},
                       {"cost_cap": -1}, {"cost_cap": True}, {"source_stock": 2.5},
                       {"policy_version": ""}):
            with self.subTest(fields=fields), self.assertRaises(ToolError):
                Snapshot(**fields)
