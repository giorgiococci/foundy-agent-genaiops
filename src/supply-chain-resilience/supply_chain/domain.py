"""Synthetic planning facts and business rules, independent of storage and SDKs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, timedelta
from enum import Enum


DEMAND = 60
OPTIONS = {
    "STANDARD": {"fixed_cost": 10, "unit_cost": 2, "arrival_day": 2},
    "EXPRESS": {"fixed_cost": 15, "unit_cost": 2, "arrival_day": 1},
}


class ToolError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class DemoRole(str, Enum):
    PLANNER = "planner"
    APPROVER = "approver"
    VIEWER = "viewer"


@dataclass(frozen=True)
class DemoActor:
    """Local role fixture, not authentication or a model-supplied argument."""

    name: str
    role: DemoRole

    def require(self, *roles: DemoRole) -> None:
        if not self.name or self.role not in roles:
            raise ToolError("unauthorized", "The demo actor cannot perform this action.")


@dataclass(frozen=True)
class PlanningContext:
    day_one: str
    currency: str
    labels: dict[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.day_one, str):
            raise ToolError("invalid_context", "The scenario day-one date must be an ISO calendar date.")
        try:
            parsed = date.fromisoformat(self.day_one)
        except ValueError as error:
            raise ToolError("invalid_context", "The scenario day-one date must be an ISO calendar date.") from error
        if parsed.isoformat() != self.day_one:
            raise ToolError("invalid_context", "Use YYYY-MM-DD for the scenario day-one date.")
        if (not isinstance(self.currency, str) or len(self.currency) != 3
                or not self.currency.isascii() or not self.currency.isalpha()
                or not self.currency.isupper()):
            raise ToolError("invalid_context", "Supply an explicit three-letter uppercase currency code.")
        if (not isinstance(self.labels, dict) or not self.labels
                or any(not isinstance(key, str) or not key.strip()
                       or not isinstance(value, str) or not value.strip()
                       for key, value in self.labels.items())):
            raise ToolError("invalid_context", "Entity labels must map nonempty IDs to nonempty names.")

    @classmethod
    def from_data(cls, value: object) -> PlanningContext:
        if not isinstance(value, dict) or set(value) != {"day_one", "currency", "labels"}:
            raise ToolError("invalid_context", "Supply day_one, currency and labels explicitly.")
        return cls(**value)

    def date_for(self, day: int) -> str:
        if type(day) is not int or day < 1:
            raise ToolError("invalid_context", "Scenario day slots must be positive integers.")
        try:
            return (date.fromisoformat(self.day_one) + timedelta(days=day - 1)).isoformat()
        except OverflowError as error:
            raise ToolError("invalid_context", "The scenario day is outside the supported calendar.") from error

    def data(self) -> dict[str, object]:
        return {**asdict(self), "day_unit": "calendar_day"}

    def transfer_data(self, arrival_day: int, completion_day: int) -> dict[str, object]:
        return {
            "context": self.data(),
            "arrival_date": self.date_for(arrival_day),
            "completion_date": self.date_for(completion_day),
        }


@dataclass(frozen=True)
class Snapshot:
    version: int = 1
    local_stock: int = 20
    source_stock: int = 80
    source_reserved: int = 30
    cost_cap: int | None = 100
    policy_version: str = "P-1:1"
    context: PlanningContext | None = None

    def __post_init__(self) -> None:
        values = (self.version, self.local_stock, self.source_stock, self.source_reserved)
        if any(type(value) is not int or value < 0 for value in values):
            raise ToolError("invalid_snapshot", "Versions and stock must be nonnegative integers.")
        if self.version < 1 or self.source_reserved > self.source_stock:
            raise ToolError("invalid_snapshot", "Invalid version or over-reserved source stock.")
        if self.cost_cap is not None and (type(self.cost_cap) is not int or self.cost_cap < 0):
            raise ToolError("invalid_snapshot", "The cost ceiling must be a nonnegative integer.")
        if not isinstance(self.policy_version, str) or not self.policy_version.strip():
            raise ToolError("invalid_snapshot", "A policy version is required.")
        if self.context is not None and not isinstance(self.context, PlanningContext):
            raise ToolError("invalid_snapshot", "Planning context must be explicitly validated.")

    @property
    def available(self) -> int:
        return self.source_stock - self.source_reserved

    def planning_data(self) -> dict[str, object]:
        return {
            "status": "ok",
            **({"context": self.context.data()} if self.context is not None else {}),
            "snapshot_version": self.version,
            "product": "HUB-1",
            "component": "BOARD-1",
            "boards_per_hub": 1,
            "local": {"warehouse": "W-A", "on_hand": self.local_stock},
            "source": {
                "warehouse": "W-B", "on_hand": self.source_stock,
                "reserved": self.source_reserved, "available": self.available,
            },
            "orders": [
                {"id": name, "quantity": quantity, "due_day": day,
                 **({"due_date": self.context.date_for(day)} if self.context is not None else {})}
                for name, quantity, day in (("C-1", 40, 3), ("C-2", 20, 4))
            ],
            "supplier_receipt": {
                "quantity": 40, "original_day": 1, "delayed_day": 6,
                **({"original_date": self.context.date_for(1), "delayed_date": self.context.date_for(6)}
                   if self.context is not None else {}),
            },
            "assembly_days": 1,
            "policy_version": self.policy_version,
        }

    def policy_data(self) -> dict[str, object]:
        return {
            "status": "insufficient_data" if self.cost_cap is None else "ok",
            **({"context": self.context.data()} if self.context is not None else {}),
            "policy_version": self.policy_version,
            "cost_cap": self.cost_cap,
            "rules": [
                "Protect both customer commitments within the cost ceiling.",
                "Never consume stock reserved for unrelated commitments.",
                "The planner chooses cost versus schedule margin.",
                "A request reserves source stock; it does not receive stock at W-A.",
                "Only a human-approved exact proposal may execute.",
            ],
            "assumptions": [
                "All data and relative day slots are synthetic.",
                "Day slots use consecutive calendar days, not a business-day calendar.",
                "Other components and assembly capacity are sufficient.",
                "No physical shipping, supplier purchasing or factory scheduling.",
            ],
        }


def quote_transfer(snapshot: Snapshot, name: str) -> dict[str, int]:
    option = OPTIONS.get(name)
    if option is None:
        raise ToolError("invalid_argument", "Choose STANDARD or EXPRESS explicitly.")
    quantity = max(0, DEMAND - snapshot.local_stock)
    return {
        "quantity": quantity, "cost": option["fixed_cost"] + option["unit_cost"] * quantity,
        "arrival_day": option["arrival_day"], "completion_day": option["arrival_day"] + 1,
    }


def transfer_violations(snapshot: Snapshot, quote: dict[str, int]) -> list[str]:
    reasons: list[str] = []
    if quote["quantity"] == 0:
        reasons.append("no_transfer_needed")
    if quote["quantity"] > snapshot.available:
        reasons.append("insufficient_available_stock")
    if snapshot.cost_cap is None:
        reasons.append("missing_cost_cap")
    elif quote["cost"] > snapshot.cost_cap:
        reasons.append("over_cost_cap")
    if quote["completion_day"] > 3:
        reasons.append("misses_customer_commitment")
    return reasons


def assess_transfers(snapshot: Snapshot) -> dict[str, object]:
    shortage = max(0, DEMAND - snapshot.local_stock)
    result: dict[str, object] = {
        "snapshot_version": snapshot.version, "policy_version": snapshot.policy_version,
        "demand": DEMAND, "shortage": shortage, "source_available": snapshot.available,
        "component": "BOARD-1",
        **({"context": snapshot.context.data()} if snapshot.context is not None else {}),
    }
    if shortage == 0:
        return {**result, "status": "no_impact", "options": []}
    if snapshot.cost_cap is None:
        return {
            **result, "status": "insufficient_data", "options": [],
            "reason": "The spending ceiling is missing.",
        }
    candidates: list[dict[str, object]] = []
    for name in OPTIONS:
        quote = quote_transfer(snapshot, name)
        reasons = transfer_violations(snapshot, quote)
        candidates.append({
            "option": name, **quote,
            **({"arrival_date": snapshot.context.date_for(quote["arrival_day"]),
                "completion_date": snapshot.context.date_for(quote["completion_day"])}
               if snapshot.context is not None else {}),
            "delivery_margin_days": {
                "C-1": 3 - quote["completion_day"], "C-2": 4 - quote["completion_day"],
            },
            "feasible": not reasons, "reasons": reasons,
        })
    return {
        **result,
        "status": "options_available" if any(item["feasible"] for item in candidates) else "infeasible",
        "cost_cap": snapshot.cost_cap,
        "options": candidates,
        "selection": "Human choice required; no cost-versus-margin priority is assumed.",
    }
