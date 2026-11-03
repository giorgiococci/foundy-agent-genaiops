"""One bounded read-only managed Foundry agent; no provisioning or cleanup."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.core.exceptions import AzureError
from azure.identity import AzureCliCredential
from openai import OpenAIError

from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.foundry import Pricing, ReadOnlyAgentLoop, agent_definition


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["preflight", "run"])
    parser.add_argument("--endpoint", default=os.environ.get("FOUNDRY_PROJECT_ENDPOINT"))
    parser.add_argument("--deployment", default=os.environ.get("FOUNDRY_MODEL_DEPLOYMENT"))
    parser.add_argument("--tenant", default=os.environ.get("FOUNDRY_TENANT_ID"))
    parser.add_argument("--agent-name", default="supply-chain-resilience-advisor")
    parser.add_argument("--agent-version", default="1")
    parser.add_argument("--input-eur-per-million")
    parser.add_argument("--output-eur-per-million")
    parser.add_argument("--price-source")
    args = parser.parse_args(argv)
    if not args.endpoint or not args.deployment or not args.tenant:
        parser.error("Explicit project endpoint, deployment and tenant configuration are required.")
    loop: ReadOnlyAgentLoop | None = None
    resources: dict[str, str] = {}
    try:
        pricing: Pricing | None = None
        if args.command == "run":
            if not args.input_eur_per_million or not args.output_eur_per_million or not args.price_source:
                raise ToolError("unverified_pricing", "Run requires verified EUR rates and a price-source reference.")
            try:
                pricing = Pricing(
                    Decimal(args.input_eur_per_million), Decimal(args.output_eur_per_million),
                    args.price_source,
                )
            except InvalidOperation as error:
                raise ToolError("invalid_pricing", "EUR rates must be finite positive decimal numbers.") from error
        with AzureCliCredential(tenant_id=args.tenant, process_timeout=60) as credential:
            with AIProjectClient(
                endpoint=args.endpoint, credential=credential, retry_total=0,
            ) as project:
                deployment = project.deployments.get(args.deployment)
                metadata = deployment.as_dict()
                if args.command == "preflight":
                    print(json.dumps({"status": "preflight_ok", "deployment": metadata}, indent=2))
                    return 0
                if pricing is None:
                    raise ToolError("unverified_pricing", "Pricing must be verified before creating an agent.")
                agent = project.agents.get_version(args.agent_name, args.agent_version)
                if agent.definition.as_dict() != agent_definition(args.deployment).as_dict():
                    raise ToolError("agent_mismatch", "The existing agent definition differs from this read-only demo.")
                active = project.agents.get(args.agent_name)
                if active.versions.latest.version != agent.version:
                    raise ToolError("agent_mismatch", "The named endpoint uses a different latest version; do not invoke it as the read-only version.")
                resources.update(agent_name=agent.name, agent_version=agent.version)
                print(json.dumps({"agent_reference": resources}), file=sys.stderr, flush=True)
                with project.get_openai_client(
                    agent_name=agent.name, max_retries=0, timeout=60,
                ) as client:
                    conversation = client.conversations.create()
                    resources["conversation_id"] = conversation.id
                    print(json.dumps({"created_resources": resources}), file=sys.stderr, flush=True)
                    with tempfile.TemporaryDirectory(prefix="supply-chain-foundry-") as directory:
                        store = DemoStore(Path(directory) / "baseline.sqlite3")
                        store.initialize()
                        viewer = DemoActor("demo-foundry-viewer", DemoRole.VIEWER)
                        baseline = store.read_snapshot(viewer)
                        loop = ReadOnlyAgentLoop(client, ToolSession(store, viewer), pricing=pricing)
                        result = loop.run(conversation.id)
                        if store.read_snapshot(viewer) != baseline:
                            raise ToolError("state_changed", "The read-only live slice changed the baseline.")
                        result["resources"] = resources
                        result["baseline_unchanged"] = True
                        result["deployment"] = metadata
                        print(json.dumps(result, indent=2))
                        return 0
    except (ToolError, AzureError, OpenAIError, OSError) as error:
        logging.error("%s: %s", type(error).__name__, error)
        failure: dict[str, object] = {
            "status": "error",
            "error": {"code": error.code if isinstance(error, ToolError) else type(error).__name__,
                      "message": str(error)},
            "created_resources": resources,
        }
        if loop is not None:
            failure["usage"] = loop.usage.summary(loop.pricing)
        print(json.dumps(failure, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
