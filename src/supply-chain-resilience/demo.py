"""Manual tool walkthrough only: no LLM, Foundry connection or real authentication."""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
from pathlib import Path

from supply_chain import DemoActor, DemoRole, DemoStore, FUNCTION_TOOL_SPECS, Snapshot, ToolError, ToolSession


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path(__file__).with_name("demo.sqlite3"))
    parser.add_argument("--role", choices=[role.value for role in DemoRole], default="planner",
                        help="Demo role fixture only, NOT authentication.")
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init")
    initialize.add_argument("--scenario", choices=[
        "baseline", "no-impact", "insufficient-stock", "ceiling-92", "ceiling-80", "missing-policy",
    ], default="baseline")
    commands.add_parser("tools")
    commands.add_parser("snapshot")
    commands.add_parser("policy")
    commands.add_parser("compare")
    proposal = commands.add_parser("propose")
    proposal.add_argument("option", choices=["STANDARD", "EXPRESS"])
    approval = commands.add_parser("approve")
    approval.add_argument("proposal_id")
    approval.add_argument("--confirm", action="store_true", help="Explicit human confirmation of this proposal.")
    for command in ("execute", "result"):
        commands.add_parser(command).add_argument("proposal_id")
    args = parser.parse_args(argv)
    store = DemoStore(args.db)
    actor = DemoActor(f"demo-{args.role}", DemoRole(args.role))
    session = ToolSession(store, actor)
    try:
        if args.command == "init":
            scenarios = {
                "baseline": Snapshot(), "no-impact": Snapshot(local_stock=60),
                "insufficient-stock": Snapshot(source_stock=60),
                "ceiling-92": Snapshot(cost_cap=92), "ceiling-80": Snapshot(cost_cap=80),
                "missing-policy": Snapshot(cost_cap=None),
            }
            result: object = store.initialize(scenarios[args.scenario])
        elif args.command == "tools":
            result = FUNCTION_TOOL_SPECS
        elif args.command == "approve":
            if not args.confirm:
                raise ToolError("confirmation_required", "Inspect the exact proposal, then explicitly use --confirm.")
            result = store.approve(actor, args.proposal_id)
        else:
            calls = {
                "snapshot": ("read_planning_snapshot", {}),
                "policy": ("read_transfer_policy", {}),
                "compare": ("compare_transfer_options", {}),
            }
            if args.command == "propose":
                name, arguments = "create_transfer_proposal", {"option": args.option}
            elif args.command in ("execute", "result"):
                name = "execute_approved_transfer" if args.command == "execute" else "read_transfer_result"
                arguments = {"proposal_id": args.proposal_id}
            else:
                name, arguments = calls[args.command]
            result = session.dispatch(name, json.dumps(arguments))
    except ToolError as error:
        result = {"status": "error", "error": {"code": error.code, "message": str(error)}}
    except (sqlite3.Error, OSError):
        logging.exception("Local walkthrough failed.")
        result = {"status": "error", "error": {"code": "storage_error", "message": "Local storage operation failed."}}
    if isinstance(result, dict) and result.get("status") == "error":
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
