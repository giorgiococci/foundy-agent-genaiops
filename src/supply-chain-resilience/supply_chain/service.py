"""Shared exact-version binding for CLI and local UI transports."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from agent_framework.foundry import FoundryAgent
from azure.ai.projects.aio import AIProjectClient

from .agents.resilience_advisor.agent import create_agent
from .agents.resilience_advisor.definition import definition
from .domain import ToolError
from .session import CandidateSession


@asynccontextmanager
async def managed_agent(
    project: AIProjectClient, candidate: CandidateSession, endpoint: str, agent_version: str,
) -> AsyncIterator[FoundryAgent]:
    candidate.ensure_ready()
    record = candidate.record
    if record.agent_version is not None and (record.agent_version != agent_version or record.endpoint != endpoint):
        raise ToolError("agent_mismatch", "The session is bound to another published version or project.")
    published = await project.agents.get_version(
        agent_name="supply-chain-resilience-advisor", agent_version=agent_version,
    )
    if published.version != agent_version or published.definition.as_dict() != definition(record.deployment).as_dict():
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
        yield agent
