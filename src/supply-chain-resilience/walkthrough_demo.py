"""Staged synthetic walkthrough with durable state and local metadata-only events."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from azure.ai.projects import AIProjectClient
from azure.core.exceptions import AzureError
from azure.identity import AzureCliCredential
from openai import OpenAIError

from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.foundry import Pricing, RunUsage, agent_definition
from supply_chain.walkthrough import WalkthroughLoop, workflow_definition


def save_state(directory: Path, state: dict[str, object]) -> None:
    temporary = directory / "session.next.json"
    temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temporary.replace(directory / "session.json")


def restore_loop(client, directory: Path, state: dict) -> WalkthroughLoop:
    store = DemoStore(directory / "planning.sqlite3")
    pricing = Pricing(Decimal(state["input_rate"]), Decimal(state["output_rate"]), state["price_source"])
    loop = WalkthroughLoop(
        client, ToolSession(store, DemoActor("demo-planner", DemoRole.PLANNER)), pricing=pricing,
    )
    loop.usage = RunUsage(**state["usage"])
    loop.stage = state["stage"]
    loop.selected_option = state.get("selected_option")
    loop.proposal = state.get("proposal")
    loop.outcome = state.get("outcome")
    loop.comparison = state.get("comparison")
    loop.called_tools = set(state.get("called_tools", []))
    loop.seen_call_ids = set(state.get("seen_call_ids", []))

    def event(fields: dict[str, object]) -> None:
        state.update(
            stage=loop.stage, usage=asdict(loop.usage), selected_option=loop.selected_option,
            proposal=loop.proposal, outcome=loop.outcome, comparison=loop.comparison,
            called_tools=sorted(loop.called_tools), seen_call_ids=sorted(loop.seen_call_ids),
        )
        save_state(directory, state)
        record = {
            "time": datetime.now(timezone.utc).isoformat(), "run_id": state["run_id"],
            "conversation_id": state["conversation_id"], "stage": loop.stage, **fields,
        }
        with (directory / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record) + "\n")

    loop.on_event = event
    return loop


def prepare(directory: Path, project: AIProjectClient, endpoint: str, deployment: str, tenant: str) -> dict:
    directory.mkdir(parents=True, exist_ok=False)
    state = {
        "run_id": str(uuid4()), "endpoint": endpoint, "deployment": deployment, "tenant": tenant,
        "agent_name": "supply-chain-resilience-advisor", "stage": "preparing",
        "usage": asdict(RunUsage()), "running": False,
        "input_rate": "5", "output_rate": "20",
        "price_source": "Azure OpenAI Global Sol both context tiers and ECB 2026-11-02; conservative EUR estimates",
    }
    save_state(directory, state)
    metadata = project.deployments.get(deployment).as_dict()
    existing = project.agents.get(state["agent_name"])
    if existing.versions.latest.definition.as_dict() == workflow_definition(deployment).as_dict():
        agent = existing.versions.latest
    elif existing.versions.latest.definition.as_dict() == agent_definition(deployment).as_dict():
        agent = project.agents.create_version(
            agent_name=state["agent_name"], definition=workflow_definition(deployment),
            metadata={"demo": "supply-chain-resilience", "step": "S-022", "mode": "human-gated"},
        )
    else:
        raise ToolError("agent_mismatch", "The current agent is neither the baseline nor this workflow; stop before changing it.")
    state["agent_version"] = agent.version
    save_state(directory, state)
    verified = project.agents.get_version(agent.name, agent.version)
    if verified.definition.as_dict() != workflow_definition(deployment).as_dict():
        raise ToolError("agent_mismatch", "The created workflow definition does not match.")
    DemoStore(directory / "planning.sqlite3").initialize()
    with project.get_openai_client(agent_name=agent.name, max_retries=0, timeout=60) as client:
        conversation = client.conversations.create()
    state.update(conversation_id=conversation.id, stage="compare", deployment_metadata=metadata)
    save_state(directory, state)
    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "compare", "propose", "approve", "reject", "execute", "result"])
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--option", choices=["STANDARD", "EXPRESS"])
    parser.add_argument("--proposal-id")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv)
    directory = args.directory.resolve()
    loop: WalkthroughLoop | None = None
    state: dict = {}
    lock: Path | None = None
    try:
        if args.command == "prepare":
            endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
            deployment = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT")
            tenant = os.environ.get("FOUNDRY_TENANT_ID")
            if not endpoint or not deployment or not tenant:
                raise ToolError("missing_configuration", "Explicit project, deployment and tenant configuration is required.")
            if directory.exists():
                raise ToolError("already_exists", "Refusing to overwrite an existing walkthrough directory.")
            with AzureCliCredential(tenant_id=tenant, process_timeout=60) as credential:
                with AIProjectClient(endpoint=endpoint, credential=credential, retry_total=0) as project:
                    state = prepare(directory, project, endpoint, deployment, tenant)
            print(json.dumps(state, indent=2))
            return 0
        state = json.loads((directory / "session.json").read_text(encoding="utf-8"))
        candidate = directory / "session.lock"
        with candidate.open("x", encoding="utf-8") as stream:
            stream.write("Exclusive walkthrough command in progress.\n")
        lock = candidate
        if args.command == "result":
            store = DemoStore(directory / "planning.sqlite3")
            actor = DemoActor("demo-viewer", DemoRole.VIEWER)
            result = {
                "stage": state["stage"], "usage": state["usage"],
                "snapshot": store.read_snapshot(actor),
                "result": store.read_result(actor, state["proposal"]["proposal_id"]) if state.get("proposal") else None,
            }
        elif args.command in ("approve", "reject"):
            if state["running"]:
                raise ToolError("uncertain_stage", "A previous stage did not finish; reconcile its durable state first.")
            if not args.proposal_id:
                raise ToolError("missing_proposal", "Supply the exact proposal ID after inspection.")
            if args.command == "approve" and not args.confirm:
                raise ToolError("confirmation_required", "Human approval requires --confirm.")
            loop = restore_loop(None, directory, state)
            result = loop.approve(args.proposal_id, confirm=args.command == "approve")
        else:
            if state["running"]:
                raise ToolError("uncertain_stage", "Previous model stage did not finish; do not retry automatically.")
            expected_stage = {"compare": "compare", "propose": "awaiting_selection", "execute": "approved"}[args.command]
            if state["stage"] != expected_stage:
                raise ToolError("invalid_stage", f"{args.command} requires stage {expected_stage}.")
            if args.command == "propose" and args.option is None:
                raise ToolError("selection_required", "Supply the planner's explicit --option selection.")
            with AzureCliCredential(tenant_id=state["tenant"], process_timeout=60) as credential:
                with AIProjectClient(endpoint=state["endpoint"], credential=credential, retry_total=0) as project:
                    current = project.agents.get(state["agent_name"])
                    if (current.versions.latest.version != state["agent_version"]
                            or current.versions.latest.definition.as_dict()
                            != workflow_definition(state["deployment"]).as_dict()):
                        raise ToolError("agent_mismatch", "The active named-agent version changed; stop before inference.")
                    with project.get_openai_client(agent_name=state["agent_name"], max_retries=0, timeout=60) as client:
                        loop = restore_loop(client, directory, state)
                        state["running"] = True
                        save_state(directory, state)
                        if args.command == "compare":
                            result = loop.compare(state["conversation_id"])
                        elif args.command == "propose":
                            result = loop.propose(state["conversation_id"], args.option)
                        else:
                            result = loop.execute(state["conversation_id"])
                        state["running"] = False
                        save_state(directory, state)
        print(json.dumps(result, indent=2))
        return 0
    except (ToolError, AzureError, OpenAIError, OSError, json.JSONDecodeError) as error:
        logging.error("%s: %s", type(error).__name__, error)
        if loop is not None:
            loop._event("stage.failed", error_type=type(error).__name__,
                        error_code=error.code if isinstance(error, ToolError) else None)
        print(json.dumps({
            "status": "error", "error": {
                "code": error.code if isinstance(error, ToolError) else type(error).__name__,
                "message": str(error),
            },
            "stage": state.get("stage"), "usage": state.get("usage"),
        }, indent=2), file=sys.stderr)
        return 1
    finally:
        if lock is not None:
            lock.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
