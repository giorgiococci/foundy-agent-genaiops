"""Compose the managed resilience advisor with local functions and safety middleware."""

from __future__ import annotations

import json
from functools import partial

from agent_framework import FunctionTool
from agent_framework.foundry import FoundryAgent, RawFoundryAgentChatClient
from azure.ai.projects.aio import AIProjectClient

from ...domain import ToolError
from ...runtime import ToolSafety
from .conversation import AdvisorConversation
from .tools import FUNCTION_TOOL_SPECS


def create_agent(
    project: AIProjectClient, agent_version: str, *, conversation: AdvisorConversation,
) -> FoundryAgent:
    tools = [
        FunctionTool(
            name=spec["name"], description=spec["description"],
            input_model=spec["parameters"], func=partial(conversation.invoke_tool, spec["name"]),
            result_parser=json.dumps,
        )
        for spec in FUNCTION_TOOL_SPECS
    ]
    safety = conversation.safety
    agent = FoundryAgent(
        project_client=project, agent_name="supply-chain-resilience-advisor",
        agent_version=agent_version, allow_preview=False, tools=tools,
        middleware=[safety, ToolSafety(safety)], timeout=60,
        function_invocation_configuration={
            "max_iterations": safety.limits.model_requests,
            "allow_concurrent_invocation": False, "terminate_on_unknown_calls": True,
        },
        default_options={
            "max_tokens": safety.limits.output_tokens_per_request, "truncation": "disabled",
        },
    )
    if not isinstance(agent.client, RawFoundryAgentChatClient):
        raise ToolError("invalid_client", "Expected the managed Foundry Agent Framework client.")
    agent.client.client.max_retries = 0
    return agent
