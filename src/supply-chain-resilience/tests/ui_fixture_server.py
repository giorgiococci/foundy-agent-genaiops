"""Browser-test service only: actual framework/AG-UI with explicitly offline SDK responses."""

import argparse
from pathlib import Path

import uvicorn

from supply_chain.ui import UIConfig, create_app
from tests.ui_tests import SyntheticUIService


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--invalid-final", action="store_true")
    args = parser.parse_args()
    service = SyntheticUIService()
    service.terminal_delay = 1.5
    service.invalid_final = args.invalid_final
    app = create_app(UIConfig(directory=args.directory, deployment="test"),
                     agent_factory=service.agent)
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="warning")
