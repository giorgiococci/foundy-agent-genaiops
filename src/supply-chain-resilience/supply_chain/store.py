"""SQLite persistence for the synthetic planning and approved-transfer records."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing, contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Iterator
from uuid import uuid4

from .domain import (
    OPTIONS, DemoActor, DemoRole, Snapshot, ToolError,
    assess_transfers, quote_transfer, transfer_violations,
)


DECISION_FIELDS = (
    "proposal_id", "snapshot_version", "snapshot_digest", "policy_version", "option", "quantity",
    "cost", "arrival_day", "completion_day", "source", "destination", "component",
)


def _fingerprint(value: object) -> str:
    content = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class DemoStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    @contextmanager
    def _connection(self, *, write: bool = False) -> Iterator[sqlite3.Connection]:
        uri = self.path.resolve().as_uri() + "?mode=rw"
        with closing(sqlite3.connect(uri, uri=True, timeout=5)) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            with connection:
                connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
                yield connection

    def initialize(self, snapshot: Snapshot | None = None) -> dict[str, object]:
        initial = snapshot if snapshot is not None else Snapshot()
        try:
            with self.path.open("xb"):
                pass
        except FileExistsError as error:
            raise ToolError("already_exists", "Refusing to overwrite an existing database.") from error
        with self._connection(write=True) as connection:
            connection.execute(
                "CREATE TABLE scenario (id INTEGER PRIMARY KEY CHECK(id = 1), "
                "version INTEGER NOT NULL, local_stock INTEGER NOT NULL, "
                "source_stock INTEGER NOT NULL, source_reserved INTEGER NOT NULL, "
                "cost_cap INTEGER, policy_version TEXT NOT NULL)"
            )
            connection.execute(
                "CREATE TABLE proposals (proposal_id TEXT PRIMARY KEY, "
                "snapshot_version INTEGER NOT NULL, snapshot_digest TEXT NOT NULL, policy_version TEXT NOT NULL, "
                "option TEXT NOT NULL, quantity INTEGER NOT NULL, cost INTEGER NOT NULL, "
                "arrival_day INTEGER NOT NULL, completion_day INTEGER NOT NULL, "
                "source TEXT NOT NULL, destination TEXT NOT NULL, component TEXT NOT NULL, "
                "approved_by TEXT, approval_digest TEXT)"
            )
            connection.execute(
                "CREATE TABLE requests (request_id TEXT PRIMARY KEY, "
                "proposal_id TEXT NOT NULL UNIQUE REFERENCES proposals(proposal_id), "
                "result_json TEXT NOT NULL)"
            )
            connection.execute(
                "INSERT INTO scenario VALUES (1, ?, ?, ?, ?, ?, ?)",
                (initial.version, initial.local_stock, initial.source_stock,
                 initial.source_reserved, initial.cost_cap, initial.policy_version),
            )
        return {"status": "initialized", "database": str(self.path)}

    @staticmethod
    def _snapshot(connection: sqlite3.Connection) -> Snapshot:
        row = connection.execute("SELECT * FROM scenario WHERE id = 1").fetchone()
        if row is None:
            raise ToolError("invalid_database", "The initialized scenario is missing.")
        return Snapshot(
            version=row["version"], local_stock=row["local_stock"],
            source_stock=row["source_stock"], source_reserved=row["source_reserved"],
            cost_cap=row["cost_cap"], policy_version=row["policy_version"],
        )

    @staticmethod
    def _proposal(connection: sqlite3.Connection, proposal_id: str) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)
        ).fetchone()
        if row is None:
            raise ToolError("not_found", "The proposal does not exist.")
        return row

    @staticmethod
    def _decision(row: sqlite3.Row) -> dict[str, object]:
        return {field: row[field] for field in DECISION_FIELDS}

    @classmethod
    def _digest(cls, row: sqlite3.Row) -> str:
        return _fingerprint(cls._decision(row))

    @staticmethod
    def _request(connection: sqlite3.Connection, proposal_id: str) -> dict[str, object] | None:
        row = connection.execute(
            "SELECT result_json FROM requests WHERE proposal_id = ?", (proposal_id,)
        ).fetchone()
        if row is None:
            return None
        try:
            payload: object = json.loads(row["result_json"])
        except json.JSONDecodeError as error:
            raise ToolError("invalid_database", "The stored request outcome is not valid JSON.") from error
        if not isinstance(payload, dict) or payload.get("status") != "requested":
            raise ToolError("invalid_database", "The stored request outcome is invalid.")
        return payload

    def read_snapshot(self, actor: DemoActor) -> dict[str, object]:
        actor.require(DemoRole.PLANNER, DemoRole.APPROVER, DemoRole.VIEWER)
        with self._connection() as connection:
            data = self._snapshot(connection).planning_data()
            data["pending_request_count"] = connection.execute(
                "SELECT COUNT(*) FROM requests"
            ).fetchone()[0]
            return data

    def read_policy(self, actor: DemoActor) -> dict[str, object]:
        actor.require(DemoRole.PLANNER, DemoRole.APPROVER, DemoRole.VIEWER)
        with self._connection() as connection:
            return self._snapshot(connection).policy_data()

    def _assessment(self, connection: sqlite3.Connection) -> dict[str, object]:
        pending = connection.execute("SELECT proposal_id FROM requests LIMIT 1").fetchone()
        if pending is not None:
            return {
                "status": "transfer_pending", "options": [],
                "request": self._request(connection, pending["proposal_id"]),
                "reason": "An existing request covers this recovery; stock is not yet received.",
            }
        return assess_transfers(self._snapshot(connection))

    def compare_options(self, actor: DemoActor) -> dict[str, object]:
        actor.require(DemoRole.PLANNER, DemoRole.APPROVER, DemoRole.VIEWER)
        with self._connection() as connection:
            return self._assessment(connection)

    def create_proposal(self, actor: DemoActor, option: str) -> dict[str, object]:
        actor.require(DemoRole.PLANNER)
        if option not in OPTIONS:
            raise ToolError("invalid_argument", "Choose STANDARD or EXPRESS explicitly.")
        with self._connection(write=True) as connection:
            assessment = self._assessment(connection)
            if assessment["status"] != "options_available":
                raise ToolError(str(assessment["status"]), "No new transfer proposal is available.")
            snapshot = self._snapshot(connection)
            quote = quote_transfer(snapshot, option)
            if transfer_violations(snapshot, quote):
                raise ToolError("infeasible", "The selected option violates stock or cost constraints.")
            proposal_id = str(uuid4())
            connection.execute(
                "INSERT INTO proposals (proposal_id, snapshot_version, snapshot_digest, policy_version, "
                "option, quantity, cost, arrival_day, completion_day, source, destination, component) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'W-B', 'W-A', 'BOARD-1')",
                (proposal_id, snapshot.version, _fingerprint(asdict(snapshot)), snapshot.policy_version,
                 option, quote["quantity"], quote["cost"], quote["arrival_day"], quote["completion_day"]),
            )
            return {"status": "proposed", **self._decision(self._proposal(connection, proposal_id))}

    def _validate_current(self, connection: sqlite3.Connection, row: sqlite3.Row) -> Snapshot:
        snapshot = self._snapshot(connection)
        if (row["snapshot_version"] != snapshot.version
                or row["policy_version"] != snapshot.policy_version
                or row["snapshot_digest"] != _fingerprint(asdict(snapshot))):
            raise ToolError("stale_proposal", "Planning facts changed; refresh and obtain new approval.")
        quote = quote_transfer(snapshot, row["option"])
        expected = (
            quote["quantity"], quote["cost"], quote["arrival_day"],
            quote["completion_day"], "W-B", "W-A", "BOARD-1",
        )
        actual = tuple(row[field] for field in (
            "quantity", "cost", "arrival_day", "completion_day", "source", "destination", "component",
        ))
        if actual != expected:
            raise ToolError("invalid_proposal", "The proposal no longer matches the planning facts.")
        if transfer_violations(snapshot, quote):
            raise ToolError("infeasible", "The current stock, timing or cost constraints reject this action.")
        return snapshot

    def approve(self, actor: DemoActor, proposal_id: str) -> dict[str, object]:
        """Human-only control path; intentionally absent from the model tool list."""
        actor.require(DemoRole.APPROVER)
        with self._connection(write=True) as connection:
            row = self._proposal(connection, proposal_id)
            if self._request(connection, proposal_id) is not None:
                raise ToolError("already_requested", "The approved action has already executed.")
            self._validate_current(connection, row)
            digest = self._digest(row)
            if row["approval_digest"] is not None and row["approval_digest"] != digest:
                raise ToolError("approval_mismatch", "The approved proposal was changed.")
            if row["approval_digest"] is None:
                connection.execute(
                    "UPDATE proposals SET approved_by = ?, approval_digest = ? WHERE proposal_id = ?",
                    (actor.name, digest, proposal_id),
                )
            approved = self._proposal(connection, proposal_id)
            return {"status": "approved", **self._decision(approved), "approved_by": approved["approved_by"]}

    def execute(self, actor: DemoActor, proposal_id: str) -> dict[str, object]:
        actor.require(DemoRole.PLANNER)
        with self._connection(write=True) as connection:
            row = self._proposal(connection, proposal_id)
            existing = self._request(connection, proposal_id)
            if existing is not None:
                return {**existing, "status": "already_requested"}
            if row["approval_digest"] is None:
                raise ToolError("approval_required", "An authorized human must approve this exact proposal.")
            if row["approval_digest"] != self._digest(row):
                raise ToolError("approval_mismatch", "Approval does not match the proposal.")
            snapshot = self._validate_current(connection, row)
            reserved = snapshot.source_reserved + row["quantity"]
            result: dict[str, object] = {
                "status": "requested", "request_id": str(uuid4()),
                "proposal": self._decision(row), "approved_by": row["approved_by"],
                "reservation": {"warehouse": "W-B", "component": "BOARD-1", "quantity": row["quantity"]},
                "inventory_after": {
                    "source_on_hand": snapshot.source_stock, "source_reserved": reserved,
                    "source_available": snapshot.source_stock - reserved,
                    "destination_on_hand": snapshot.local_stock,
                },
                "movement": "Not shipped or received.",
            }
            connection.execute(
                "UPDATE scenario SET source_reserved = ?, version = version + 1 WHERE id = 1",
                (reserved,),
            )
            connection.execute(
                "INSERT INTO requests VALUES (?, ?, ?)",
                (result["request_id"], proposal_id, json.dumps(result, sort_keys=True)),
            )
            return result

    def read_result(self, actor: DemoActor, proposal_id: str) -> dict[str, object]:
        actor.require(DemoRole.PLANNER, DemoRole.APPROVER, DemoRole.VIEWER)
        with self._connection() as connection:
            row = self._proposal(connection, proposal_id)
            existing = self._request(connection, proposal_id)
            if existing is not None:
                return existing
            if row["approval_digest"] is not None:
                if row["approval_digest"] != self._digest(row):
                    raise ToolError("approval_mismatch", "The approved proposal was changed.")
                self._validate_current(connection, row)
            return {
                "status": "approved" if row["approval_digest"] is not None else "proposed",
                **self._decision(row),
            }
