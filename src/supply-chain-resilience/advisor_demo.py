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

from supply_chain.agents.resilience_advisor.agent import create_agent
from supply_chain.agents.resilience_advisor.definition import definition, provenance
from supply_chain.domain import ToolError
from supply_chain.session import CandidateSession


async def chat(candidate: CandidateSession, message: str, endpoint: str, tenant: str, agent_version: str) -> dict[str, object]:
    candidate.ensure_ready()
    if not message.strip():
        raise ToolError("empty_message", "A nonempty planner message is required.")
    record = candidate.record
    if record.agent_version is not None and (record.agent_version != agent_version or record.endpoint != endpoint):
        raise ToolError("agent_mismatch", "The session is bound to another published version or project.")
    async with AzureCliCredential(tenant_id=tenant, process_timeout=60) as credential:
        async with AIProjectClient(endpoint=endpoint, credential=credential, retry_total=0) as project:
            published = await project.agents.get_version(
                agent_name="supply-chain-resilience-advisor", agent_version=agent_version,
            )
            if (published.version != agent_version
                    or published.definition.as_dict() != definition(record.deployment).as_dict()):
                raise ToolError("candidate_unpublished", "The exact published version does not match this candidate; no inference is permitted.")
            async with create_agent(project, agent_version, conversation=candidate.advisor) as agent:
                if candidate.framework_session is None:
                    record.endpoint = endpoint
                    record.agent_version = agent_version
                    record.running = True
                    candidate.save()
                    candidate.framework_session = await agent.create_conversation(session_id=record.run_id)
                    record.running = False
                    candidate.save()
                return await candidate.reply(agent, message)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["definition", "init", "inspect", "select", "approve", "reject", "chat"])
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--deployment", default=os.environ.get("FOUNDRY_MODEL_DEPLOYMENT"))
    parser.add_argument("--option", choices=["STANDARD", "EXPRESS"])
    parser.add_argument("--proposal-id")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--message")
    parser.add_argument("--endpoint", default=os.environ.get("FOUNDRY_PROJECT_ENDPOINT"))
    parser.add_argument("--tenant", default=os.environ.get("FOUNDRY_TENANT_ID"))
    parser.add_argument("--agent-version")
    parser.add_argument("--model-request-limit", type=int, choices=[10, 20], default=10,
                        help="Initial candidate allowance; does not change an existing session.")
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
            )
            result = candidate.inspect()
        else:
            candidate = CandidateSession.load(directory)
            with candidate.locked():
                candidate = CandidateSession.load(directory)
                if args.command == "inspect":
                    result = candidate.inspect()
                elif args.command == "chat":
                    if not all((args.message, args.endpoint, args.tenant, args.agent_version)):
                        raise ToolError("missing_configuration", "Chat needs message, explicit endpoint/tenant and a published agent version.")
                    result = asyncio.run(chat(candidate, args.message, args.endpoint, args.tenant, args.agent_version))
                else:
                    candidate.ensure_ready()
                    conversation = candidate.advisor
                    if args.command == "select":
                        if args.option is None:
                            raise ToolError("selection_required", "Supply the planner's explicit option.")
                        result = conversation.select(args.option)
                    else:
                        if not args.proposal_id or (args.command == "approve" and not args.confirm):
                            raise ToolError("confirmation_required", "Supply the exact proposal ID and --confirm for approval.")
                        result = conversation.approve(args.proposal_id, confirm=args.command == "approve")
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
