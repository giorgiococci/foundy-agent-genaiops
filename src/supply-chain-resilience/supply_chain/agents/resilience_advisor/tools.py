"""Advisor-owned function schemas and dispatcher; no HTTP, MCP or SDK dependency."""

from __future__ import annotations

import json
import logging
import sqlite3

from ...domain import DemoActor, ToolError
from ...store import DemoStore


LOGGER = logging.getLogger(__name__)


def _tool(name: str, description: str, properties: dict[str, object]) -> dict[str, object]:
    return {
        "name": name, "description": description, "strict": True,
        "parameters": {
            "type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False,
        },
    }


FUNCTION_TOOL_SPECS = [
    _tool("read_planning_snapshot", "Read authoritative synthetic stock, orders and receipt facts.", {}),
    _tool("read_transfer_policy", "Read the versioned demo policy and cost ceiling.", {}),
    _tool("compare_transfer_options", "Compare feasible transfers; do not assume the planner's preference.", {}),
    _tool("create_transfer_proposal", "Create a proposal for the explicitly selected option; no stock changes.", {
        "option": {"type": "string", "enum": ["STANDARD", "EXPRESS"]},
    }),
    _tool("execute_approved_transfer", "Request and reserve only an exact human-approved transfer; no shipment.", {
        "proposal_id": {"type": "string"},
    }),
    _tool("read_transfer_result", "Read the durable outcome before retrying an uncertain request.", {
        "proposal_id": {"type": "string"},
    }),
]


class ToolSession:
    def __init__(self, store: DemoStore, actor: DemoActor) -> None:
        self.store = store
        self.actor = actor

    def dispatch(self, name: str, arguments_json: str) -> dict[str, object]:
        try:
            return self._dispatch(name, arguments_json)
        except ToolError as error:
            return {"status": "error", "error": {"code": error.code, "message": str(error)}}
        except sqlite3.Error:
            LOGGER.exception("Local demo database operation failed.")
            return {
                "status": "error",
                "error": {"code": "database_error", "message": "Database failure; no successful outcome is claimed."},
            }

    def _dispatch(self, name: str, arguments_json: str) -> dict[str, object]:
        expected = {
            "read_planning_snapshot": (), "read_transfer_policy": (),
            "compare_transfer_options": (), "create_transfer_proposal": ("option",),
            "execute_approved_transfer": ("proposal_id",), "read_transfer_result": ("proposal_id",),
        }
        if name not in expected:
            raise ToolError("unknown_tool", "The requested tool is not exposed.")
        try:
            arguments: object = json.loads(arguments_json)
        except json.JSONDecodeError as error:
            raise ToolError("invalid_arguments", "Tool arguments must be valid JSON.") from error
        if not isinstance(arguments, dict) or set(arguments) != set(expected[name]):
            raise ToolError("invalid_arguments", "Unexpected or missing tool arguments.")
        values: dict[str, str] = {}
        for key in expected[name]:
            value = arguments[key]
            if not isinstance(value, str) or not value.strip():
                raise ToolError("invalid_arguments", f"{key} must be a nonempty string.")
            values[key] = value
        if name == "read_planning_snapshot":
            return self.store.read_snapshot(self.actor)
        if name == "read_transfer_policy":
            return self.store.read_policy(self.actor)
        if name == "compare_transfer_options":
            return self.store.compare_options(self.actor)
        if name == "create_transfer_proposal":
            return self.store.create_proposal(self.actor, values["option"])
        if name == "execute_approved_transfer":
            return self.store.execute(self.actor, values["proposal_id"])
        return self.store.read_result(self.actor, values["proposal_id"])
