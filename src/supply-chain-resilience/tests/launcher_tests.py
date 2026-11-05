"""Local dotenv loading and explicit configuration precedence, without inference."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import ui_demo
from supply_chain.domain import ToolError
from supply_chain.ui import create_app


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.env = self.directory / ".env"
        self.env.write_text(
            "FOUNDRY_PROJECT_ENDPOINT=https://example.test/api/projects/demo\n"
            "FOUNDRY_TENANT_ID=dotenv-tenant\n"
            "FOUNDRY_AGENT_VERSION=4\n"
            "FOUNDRY_MODEL_DEPLOYMENT=dotenv-model\n",
            encoding="utf-8",
        )
        self.enterContext(patch.dict(os.environ, {}, clear=True))
        self.enterContext(patch.object(ui_demo, "__file__", str(self.directory / "ui_demo.py")))
        self.create_app = self.enterContext(patch.object(ui_demo, "create_app"))
        self.run = self.enterContext(patch.object(ui_demo.uvicorn, "run"))

    def launch(self, *arguments):
        with patch("sys.argv", ["ui_demo.py", *arguments]):
            ui_demo.main()
        self.run.assert_called_once_with(
            self.create_app.return_value, host="127.0.0.1", port=8080,
            workers=1, log_level="info",
        )
        return self.create_app.call_args.args[0]

    def test_loads_env_beside_launcher_not_working_directory(self):
        self.assertNotEqual(Path.cwd(), self.directory)
        config = self.launch()
        self.assertEqual(config.endpoint, "https://example.test/api/projects/demo")
        self.assertEqual(config.tenant, "dotenv-tenant")
        self.assertEqual(config.agent_version, "4")
        self.assertEqual(config.deployment, "dotenv-model")

    def test_process_environment_overrides_dotenv(self):
        os.environ["FOUNDRY_AGENT_VERSION"] = "environment-version"
        self.assertEqual(self.launch().agent_version, "environment-version")

    def test_cli_overrides_environment_and_dotenv(self):
        os.environ["FOUNDRY_AGENT_VERSION"] = "environment-version"
        self.assertEqual(
            self.launch("--agent-version", "cli-version").agent_version, "cli-version",
        )

    def test_missing_env_preserves_explicit_configuration(self):
        self.env.unlink()
        config = self.launch(
            "--endpoint", "https://explicit.test", "--tenant", "explicit-tenant",
            "--agent-version", "4",
        )
        self.assertEqual(config.endpoint, "https://explicit.test")
        self.assertEqual(config.tenant, "explicit-tenant")

    def test_missing_configuration_still_fails_without_starting_server(self):
        self.env.unlink()
        self.create_app.side_effect = create_app
        with patch("sys.argv", ["ui_demo.py"]), self.assertRaises(ToolError) as raised:
            ui_demo.main()
        self.assertEqual(raised.exception.code, "missing_configuration")
        self.run.assert_not_called()
