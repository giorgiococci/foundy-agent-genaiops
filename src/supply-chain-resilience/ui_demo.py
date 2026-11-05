"""Start the real Foundry chat; Send and actual human-tool responses start inference."""

import argparse
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

from supply_chain.ui import UIConfig, create_app


def main() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parents[2] / "artifacts" / "local" / "ui")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--deployment", default=os.environ.get("FOUNDRY_MODEL_DEPLOYMENT", "gpt-6.1-sol"))
    parser.add_argument("--endpoint", default=os.environ.get("FOUNDRY_PROJECT_ENDPOINT", ""))
    parser.add_argument("--tenant", default=os.environ.get("FOUNDRY_TENANT_ID", ""))
    parser.add_argument("--agent-version", default=os.environ.get("FOUNDRY_AGENT_VERSION", ""))
    parser.add_argument("--model-request-limit", type=int, default=10)
    parser.add_argument("--tool-call-limit", type=int, default=20)
    parser.add_argument("--total-token-limit", type=int, default=100_000)
    parser.add_argument("--spend-eur-limit", type=int, default=10)
    parser.add_argument("--telemetry", choices=["off", "metadata", "content"], default="off")
    args = parser.parse_args()
    app = create_app(UIConfig(
        directory=args.directory, deployment=args.deployment, endpoint=args.endpoint,
        tenant=args.tenant, agent_version=args.agent_version,
        telemetry=args.telemetry, model_request_limit=args.model_request_limit,
        tool_call_limit=args.tool_call_limit, total_token_limit=args.total_token_limit,
        spend_eur_limit=args.spend_eur_limit,
    ))
    uvicorn.run(app, host="127.0.0.1", port=args.port, workers=1, log_level="info")


if __name__ == "__main__":
    main()
