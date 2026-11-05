"""Agent-led candidate CLI; init/inspect/decisions are local, chat requires publication."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys

from pathlib import Path

from agent_framework.exceptions import AgentFrameworkException
from azure.ai.projects.aio import AIProjectClient
from azure.core.exceptions import AzureError
from azure.identity.aio import AzureCliCredential
from openai import OpenAIError

from supply_chain.agents.resilience_advisor.definition import definition, provenance
from supply_chain.domain import ToolError
from supply_chain.session import CandidateSession
from supply_chain.service import managed_agent
from supply_chain.observability import Mode, TelemetryPolicy, linked_insights_connection_string, start_azure_tracing


async def chat(
    candidate: CandidateSession, message: str | None, endpoint: str, tenant: str,
    agent_version: str, *, telemetry: Mode = "off",
) -> dict[str, object]:
    candidate.ensure_ready()
    if message is not None and not message.strip():
        raise ToolError("empty_message", "A nonempty planner message is required.")
    record = candidate.record
    candidate.advisor.telemetry_policy = TelemetryPolicy(telemetry)
    if record.agent_version is not None and (record.agent_version != agent_version or record.endpoint != endpoint):
        raise ToolError("agent_mismatch", "The session is bound to another published version or project.")
    async with AzureCliCredential(tenant_id=tenant, process_timeout=60) as credential:
        async with AIProjectClient(endpoint=endpoint, credential=credential, retry_total=0) as project:
            async with managed_agent(project, candidate, endpoint, agent_version) as agent:
                tracing = start_azure_tracing(
                    await linked_insights_connection_string(project)
                ) if telemetry != "off" else None
                try:
                    return await candidate.reply(agent, message)
                finally:
                    if tracing is not None:
                        tracing.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["definition", "init", "inspect", "select", "approve", "reject", "chat", "resume"])
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--deployment", default=os.environ.get("FOUNDRY_MODEL_DEPLOYMENT"))
    parser.add_argument("--option", choices=["STANDARD", "EXPRESS"])
    parser.add_argument("--proposal-id")
    parser.add_argument("--tool-call-id")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--message")
    parser.add_argument("--endpoint", default=os.environ.get("FOUNDRY_PROJECT_ENDPOINT"))
    parser.add_argument("--tenant", default=os.environ.get("FOUNDRY_TENANT_ID"))
    parser.add_argument("--agent-version")
    parser.add_argument("--telemetry", choices=["off", "metadata", "content"], default="off",
                        help="Export selected per-agent traces to linked Insights; content is for synthetic data only.")
    parser.add_argument("--model-request-limit", type=int, choices=range(1, 21), default=10,
                        help="Initial candidate allowance; does not change an existing session.")
    parser.add_argument("--tool-call-limit", type=int, default=20)
    parser.add_argument("--total-token-limit", type=int, default=100_000)
    parser.add_argument("--spend-eur-limit", type=int, default=10)
    args = parser.parse_args(argv)
    try:
        if args.command in ("definition", "init") and not args.deployment:
            raise ToolError("missing_deployment", "Supply the explicit candidate deployment.")
        if args.command == "definition":
            print(json.dumps({"definition": definition(args.deployment).as_dict(),
                              "provenance": provenance(args.deployment)}, indent=2))
            return 0
        if args.directory is None:
            raise ToolError("missing_directory", "Supply a dedicated new or existing candidate directory.")
        directory = args.directory.resolve()
        if args.command == "init":
            candidate = CandidateSession.initialize(
                directory, args.deployment, model_request_limit=args.model_request_limit,
                tool_call_limit=args.tool_call_limit, total_token_limit=args.total_token_limit,
                spend_eur_limit=args.spend_eur_limit,
            )
            result = candidate.inspect()
        else:
            candidate = CandidateSession.load(directory)
            with candidate.locked():
                candidate = CandidateSession.load(directory)
                if args.command == "inspect":
                    result = candidate.inspect()
                elif args.command in ("chat", "resume"):
                    if not all((args.endpoint, args.tenant, args.agent_version)) or (args.command == "chat" and not args.message):
                        raise ToolError("missing_configuration", "Chat needs message, explicit endpoint/tenant and a published agent version.")
                    result = asyncio.run(chat(
                        candidate, args.message if args.command == "chat" else None,
                        args.endpoint, args.tenant, args.agent_version,
                        telemetry=args.telemetry,
                    ))
                else:
                    candidate.ensure_ready()
                    conversation = candidate.advisor
                    if not args.tool_call_id:
                        raise ToolError("human_request_mismatch", "Supply the exact pending native --tool-call-id.")
                    if args.command == "select":
                        if args.option is None:
                            raise ToolError("selection_required", "Supply the planner's explicit option.")
                        result = conversation.respond(args.tool_call_id, option=args.option)
                    else:
                        if not args.proposal_id or (args.command == "approve" and not args.confirm):
                            raise ToolError("confirmation_required", "Supply the exact proposal ID and --confirm for approval.")
                        result = conversation.respond(args.tool_call_id, proposal_id=args.proposal_id,
                                                      confirm=args.command == "approve")
                    candidate.save()
        print(json.dumps(result, indent=2))
        return 0
    except (ToolError, AgentFrameworkException, AzureError, OpenAIError, OSError, json.JSONDecodeError) as error:
        logging.error("%s: %s", type(error).__name__, error)
        print(json.dumps({"status": "error", "error": {
            "code": error.code if isinstance(error, ToolError) else type(error).__name__,
            "message": str(error),
        }}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
