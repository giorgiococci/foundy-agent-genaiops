"""Managed-agent definitions and source provenance, not execution or deployment."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from azure.ai.projects.models import FunctionTool, PromptAgentDefinition

from ...domain import ToolError
from .tools import FUNCTION_TOOL_SPECS


PROMPTS = Path(__file__).parent / "prompts"
READ_TOOL_NAMES = frozenset({
    "read_planning_snapshot", "read_transfer_policy", "compare_transfer_options",
})


def instructions(name: str) -> str:
    if name not in ("readonly", "walkthrough", "advisor"):
        raise ToolError("unknown_prompt", "Select an explicit bundled instruction asset.")
    text = (PROMPTS / f"{name}.txt").read_text(encoding="utf-8")
    if not text.strip():
        raise ToolError("empty_prompt", "Agent instructions must not be empty.")
    return text


def definition(deployment: str) -> PromptAgentDefinition:
    if not deployment.strip():
        raise ToolError("missing_deployment", "An explicit model deployment is required.")
    return PromptAgentDefinition(
        model=deployment, instructions=instructions("advisor"),
        tools=[FunctionTool(**spec) for spec in FUNCTION_TOOL_SPECS],
    )


def fingerprint(value: object) -> str:
    content = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def provenance(deployment: str) -> dict[str, str]:
    candidate = definition(deployment).as_dict()
    return {
        "profile": "advisor", "publication": "local-candidate",
        "instructions_sha256": hashlib.sha256(instructions("advisor").encode("utf-8")).hexdigest(),
        "tool_schema_sha256": fingerprint(FUNCTION_TOOL_SPECS),
        "definition_sha256": fingerprint(candidate),
        "deployment": deployment,
    }
