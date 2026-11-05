"""Versioned synthetic scenario input, independent of Foundry and SQLite."""

from __future__ import annotations

import json
from pathlib import Path

from .domain import PlanningContext, Snapshot, ToolError


SCENARIO = Path(__file__).parent.parent / "data" / "scenario.json"


def load_snapshot(path: Path = SCENARIO) -> Snapshot:
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or set(data) != {"id", "version", "business_model", "snapshot", "context"}
            or data["id"] != "controller-board-delay" or type(data["version"]) is not int
            or data["version"] != 2 or data["business_model"] != "HUB-1-BOARD-1-two-orders-v1"):
        raise ToolError("invalid_scenario", "Unsupported synthetic scenario identity or version.")
    fields = data["snapshot"]
    if not isinstance(fields, dict) or set(fields) != {
        "version", "local_stock", "source_stock", "source_reserved", "cost_cap", "policy_version",
    }:
        raise ToolError("invalid_scenario", "The scenario must explicitly supply all snapshot fields.")
    return Snapshot(**fields, context=PlanningContext.from_data(data["context"]))
