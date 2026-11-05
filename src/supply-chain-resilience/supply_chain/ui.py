"""Loopback CopilotKit chat backed by the real managed Foundry agent."""

from __future__ import annotations

import asyncio
import json
import logging
import secrets
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from dataclasses import asdict, dataclass
from decimal import Decimal
from importlib.metadata import version
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

from ag_ui.core import CustomEvent, RunAgentInput, RunErrorEvent, RunFinishedEvent
from ag_ui.encoder import EventEncoder
from agent_framework.foundry import FoundryAgent
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict

from .domain import ToolError
from .observability import Mode, TelemetryPolicy, linked_insights_connection_string, start_azure_tracing
from .service import managed_agent
from .runtime import RunLimits
from .session import CandidateSession, ROOT, frontend_fingerprint
from .ui_stream import AdvisorUIBinding
from .agents.resilience_advisor.tools import HUMAN_TOOL_NAMES


LOGGER = logging.getLogger(__name__)
FRONTEND = ROOT / "frontend" / "dist"
AgentFactory = Callable[[CandidateSession], AbstractAsyncContextManager[FoundryAgent]]


@dataclass(frozen=True)
class UIConfig:
    directory: Path
    deployment: str
    endpoint: str = ""
    tenant: str = ""
    agent_version: str = "3"
    telemetry: Mode = "off"
    model_request_limit: int = 10
    tool_call_limit: int = 20
    total_token_limit: int = 100_000
    spend_eur_limit: int = 10

    def __post_init__(self) -> None:
        if not self.deployment.strip():
            raise ToolError("missing_deployment", "Specify the deployment for new synthetic cases.")
        TelemetryPolicy(self.telemetry)
        RunLimits(model_requests=self.model_request_limit, tool_calls=self.tool_call_limit,
                  total_tokens=self.total_token_limit, spend_eur=Decimal(self.spend_eur_limit))


class HumanAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["select", "approve", "reject"]
    option: Literal["STANDARD", "EXPRESS"] | None = None
    proposal_id: str | None = None
    confirm: bool = False
    tool_call_id: str | None = None


def _case_path(config: UIConfig, case_id: str) -> Path:
    try:
        canonical = str(UUID(case_id))
    except ValueError as error:
        raise ToolError("invalid_case", "A server-created case ID is required.") from error
    if canonical != case_id:
        raise ToolError("invalid_case", "Use the canonical server-created case ID.")
    path = config.directory.resolve() / canonical
    if path.is_symlink() or not (path / "advisor-session.json").is_file():
        raise ToolError("unknown_case", "No such local UI case.")
    return path


def _history(candidate: CandidateSession) -> list[dict[str, object]]:
    path = candidate.directory / "ui-history.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def _save_history(candidate: CandidateSession, history: list[dict[str, object]]) -> None:
    temporary = candidate.directory / "ui-history.next.json"
    temporary.write_text(json.dumps(history, ensure_ascii=True), encoding="utf-8")
    temporary.replace(candidate.directory / "ui-history.json")


def _interaction(
    candidate: CandidateSession, history: list[dict[str, object]], snapshot: object, *, blocked: bool,
) -> dict[str, object] | None:
    pending = candidate.record.decisions.pending
    if blocked or pending is None or pending.receipt is not None or pending.consumed:
        return None
    for index in range(len(history) - 1, -1, -1):
        result = history[index].get("result")
        if isinstance(result, dict) and result.get("human_request", {}).get("call_id") == pending.call_id:
            return {
                "kind": "select" if pending.name == "request_transfer_choice" else "approve",
                "history_index": index, "evidence": pending.evidence, "tool_call_id": pending.call_id,
            }
    return None


def case_view(candidate: CandidateSession) -> dict[str, object]:
    inspection = candidate.inspect()
    events_path = candidate.directory / "events.jsonl"
    events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()] if events_path.exists() else []
    record = candidate.record
    drift = None
    try:
        candidate.ensure_ready()
    except ToolError as error:
        drift = {"code": error.code, "message": str(error)}
    history = _history(candidate)
    return {
        "id": candidate.directory.name, "run_id": record.run_id,
        "conversation_id": candidate.framework_session.service_session_id if candidate.framework_session else None,
        "running": record.running, "blocked": drift,
        "decisions": {
            "selected_option": record.decisions.selected_option,
            "proposal_id": record.decisions.proposal_id,
            "approved": record.decisions.approved, "rejected": record.decisions.rejected,
        },
        "snapshot": inspection["snapshot"], "result": inspection["result"],
        "usage": record.usage.summary(candidate.advisor.safety.pricing),
        "limits": {
            "requests": record.model_request_limit, "tools": record.tool_call_limit,
            "tokens": record.total_token_limit, "spend_eur": record.spend_eur_limit,
        },
        "history": history, "events": events[-100:],
        "pending_human": asdict(record.decisions.pending) if record.decisions.pending is not None else None,
        "interaction": _interaction(candidate, history, inspection["snapshot"], blocked=drift is not None),
    }


def create_app(config: UIConfig, *, agent_factory: AgentFactory | None = None) -> FastAPI:
    if agent_factory is None and not (config.endpoint.startswith("https://") and config.tenant and config.agent_version):
        raise ToolError("missing_configuration", "Set FOUNDRY_PROJECT_ENDPOINT (HTTPS) and FOUNDRY_TENANT_ID; specify the exact agent version.")
    frontend_fingerprint()
    token = secrets.token_urlsafe(32)

    @asynccontextmanager
    async def cloud_agent(candidate: CandidateSession) -> AsyncIterator[FoundryAgent]:
        async with AzureCliCredential(tenant_id=config.tenant, process_timeout=60) as credential:
            async with AIProjectClient(endpoint=config.endpoint, credential=credential, retry_total=0) as project:
                async with managed_agent(project, candidate, config.endpoint, config.agent_version) as agent:
                    yield agent

    factory = agent_factory or cloud_agent

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        config.directory.mkdir(parents=True, exist_ok=True)
        tracing = None
        if config.telemetry != "off":
            async with AzureCliCredential(tenant_id=config.tenant, process_timeout=60) as credential:
                async with AIProjectClient(endpoint=config.endpoint, credential=credential, retry_total=0) as project:
                    tracing = start_azure_tracing(await linked_insights_connection_string(project))
        try:
            yield
        finally:
            if tracing is not None:
                tracing.close()

    app = FastAPI(title="Supply Chain Resilience Lab", lifespan=lifespan, docs_url=None, redoc_url=None)

    @app.middleware("http")
    async def local_boundary(request: Request, call_next):
        host = request.url.hostname
        origin = request.headers.get("origin")
        allowed_origin = f"{request.url.scheme}://{request.headers.get('host', '')}"
        if (host not in ("127.0.0.1", "localhost", "::1")
                or request.headers.get("sec-fetch-site") == "cross-site"
                or (origin is not None and origin != allowed_origin)):
            return JSONResponse({"error": {"code": "local_origin_required"}}, status_code=403)
        if request.method not in ("GET", "HEAD") and not secrets.compare_digest(
            request.headers.get("x-local-token", ""), token,
        ):
            return JSONResponse({"error": {"code": "local_action_token_required"}}, status_code=403)
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        )
        return response

    @app.exception_handler(ToolError)
    async def tool_error(request: Request, error: ToolError):
        LOGGER.warning("UI operation refused (%s): %s", error.code, error)
        return JSONResponse({"error": {"code": error.code, "message": str(error)}}, status_code=409)

    @app.exception_handler(FileExistsError)
    async def busy(request: Request, error: FileExistsError):
        LOGGER.warning("UI case is locked by another command.")
        return JSONResponse({"error": {"code": "case_busy", "message": "Another case operation is active."}}, status_code=409)

    @app.get("/")
    async def index():
        return FileResponse(FRONTEND / "index.html")

    app.mount("/assets", StaticFiles(directory=FRONTEND / "assets"), name="frontend-assets")

    @app.get("/api/bootstrap")
    async def bootstrap():
        cases = []
        if config.directory.exists():
            for path in sorted(config.directory.iterdir()):
                if path.is_dir() and not path.is_symlink():
                    try:
                        canonical = str(UUID(path.name))
                    except ValueError:
                        continue
                    if path.name == canonical and (path / "advisor-session.json").is_file():
                        cases.append(canonical)
        return {
            "action_token": token, "cases": cases,
            "inference_enabled": True,
            "service_mode": "offline-test-fixture" if agent_factory is not None else "managed-foundry",
            "agent_version": config.agent_version, "deployment": config.deployment,
            "telemetry": config.telemetry,
        }

    @app.post("/api/cases")
    async def new_case(request: Request):
        body = await request.body()
        if body not in (b"", b"{}"):
            raise ToolError("invalid_request", "Case configuration is server-owned.")
        candidate = CandidateSession.initialize(
            config.directory / str(uuid4()), config.deployment,
            model_request_limit=config.model_request_limit, tool_call_limit=config.tool_call_limit,
            total_token_limit=config.total_token_limit, spend_eur_limit=config.spend_eur_limit,
        )
        candidate.record.ui_frontend_sha256 = frontend_fingerprint()
        candidate.record.ui_sdk_versions = {
            name: version(name) for name in ("agent-framework-ag-ui", "ag-ui-protocol", "fastapi", "uvicorn")
        }
        candidate.save()
        return case_view(candidate)

    @app.get("/api/cases/{case_id}")
    async def inspect_case(case_id: str):
        return case_view(CandidateSession.load(_case_path(config, case_id)))

    @app.post("/api/cases/{case_id}/actions")
    async def human_action(case_id: str, action: HumanAction):
        path = _case_path(config, case_id)
        candidate = CandidateSession.load(path)
        with candidate.locked():
            candidate = CandidateSession.load(path)
            candidate.ensure_ready()
            pending = candidate.record.decisions.pending
            if pending is None:
                raise ToolError("decision_not_available", "Wait for a validated native human request.")
            if action.tool_call_id != pending.call_id:
                raise ToolError("human_request_mismatch", "Supply the exact pending native tool-call ID.")
            if action.action == "select":
                if action.option is None or action.proposal_id is not None or action.confirm:
                    raise ToolError("invalid_selection", "Supply only an explicit option for selection.")
                candidate.advisor.respond(action.tool_call_id, option=action.option)
            else:
                if action.proposal_id is None or action.option is not None:
                    raise ToolError("confirmation_required", "Supply the exact pending proposal ID.")
                if action.action == "approve" and not action.confirm:
                    raise ToolError("confirmation_required", "Explicit exact-proposal confirmation is required.")
                if action.action == "reject" and action.confirm:
                    raise ToolError("invalid_request", "A rejection cannot confirm approval.")
                candidate.advisor.respond(
                    action.tool_call_id, proposal_id=action.proposal_id, confirm=action.action == "approve",
                )
            candidate.save()
        return case_view(candidate)

    @app.post("/api/cases/{case_id}/run")
    async def run_case(case_id: str, request: Request):
        path = _case_path(config, case_id)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 65_536:
                raise ToolError("invalid_request", "AG-UI request exceeds the local size bound.")
        try:
            data = RunAgentInput.model_validate_json(body)
        except ValueError as error:
            raise ToolError("invalid_request", "Invalid AG-UI run input.") from error
        props = data.forwarded_props or {}
        if (data.thread_id != case_id or not data.run_id or len(data.run_id) > 100
                or data.state or any(tool.name not in HUMAN_TOOL_NAMES for tool in data.tools)
                or len({tool.name for tool in data.tools}) != len(data.tools) or data.context
                or set(props) - {"__copilotkitRequestId"}
                or any(not isinstance(value, str) or not 0 < len(value) <= 100 for value in props.values())
                or data.resume or data.parent_run_id or len(data.messages) != 1):
            raise ToolError("untrusted_state", "Only a user turn or a correlated human-tool result is accepted.")
        message = data.messages[0]
        if message.role not in ("user", "tool") or not isinstance(message.content, str) or not 0 < len(message.content.strip()) <= 8000:
            raise ToolError("invalid_request", "One plain-text user message or human receipt is required.")
        encoder = EventEncoder()

        async def stream_events():
            candidate = CandidateSession.load(path)
            try:
                with candidate.locked():
                    candidate = CandidateSession.load(path)
                    candidate.ensure_ready()
                    history = _history(candidate)
                    if message.role == "user" and any(entry.get("request_id") == data.run_id for entry in history):
                        raise ToolError("duplicate_run", "This AG-UI run ID was already submitted; no operation was replayed.")
                    pending = candidate.record.decisions.pending
                    if message.role == "user":
                        if pending is not None and not pending.consumed:
                            raise ToolError("human_input_pending", "Respond to the current native human request first.")
                        native_input = message.content
                        trusted_message = {"id": str(uuid4()), "role": "user", "content": message.content}
                    else:
                        if (pending is None or pending.consumed or pending.receipt is None
                                or message.tool_call_id != pending.call_id):
                            raise ToolError("invalid_continuation", "No matching saved human receipt is awaiting continuation.")
                        try:
                            receipt = json.loads(message.content)
                        except json.JSONDecodeError as error:
                            raise ToolError("invalid_continuation", "A structured human receipt is required.") from error
                        if receipt != pending.receipt:
                            raise ToolError("untrusted_receipt", "Only the exact server-recorded human result is accepted.")
                        trusted_message = {
                            "id": str(uuid4()), "role": "tool", "toolCallId": pending.call_id,
                            "content": json.dumps(pending.receipt),
                        }
                    trusted_messages = [trusted_message]
                    if message.role == "tool":
                        trusted_messages.insert(0, {
                            "id": pending.call_id, "role": "assistant", "toolCalls": [{
                                "id": pending.call_id, "type": "function",
                                "function": {"name": pending.name, "arguments": json.dumps(pending.arguments)},
                            }],
                        })
                    trusted = {
                        "threadId": case_id, "runId": data.run_id, "messages": trusted_messages,
                        "state": {}, "tools": [], "context": [], "forwardedProps": {},
                    }
                    candidate.advisor.telemetry_policy = TelemetryPolicy(config.telemetry)
                    async with factory(candidate) as agent:
                        if candidate.framework_session is None or not candidate.framework_session.service_session_id:
                            raise ToolError("missing_conversation", "No server-bound managed conversation.")
                        candidate.record.running = True
                        candidate.save()
                        if message.role == "tool":
                            native_input = candidate.advisor.continuation()
                        history.append({
                            "role": message.role, "content": trusted_message["content"], "request_id": data.run_id,
                            **({"tool_call_id": message.tool_call_id} if message.role == "tool" else {}),
                        })
                        _save_history(candidate, history)
                        binding = AdvisorUIBinding(candidate, agent, native_input)
                        finished = None
                        events = binding.adapter().run(trusted)
                        try:
                            async for event in events:
                                if isinstance(event, RunErrorEvent):
                                    raise ToolError("stream_failed", "AG-UI reported failure; inspect local state before another operation.")
                                if isinstance(event, RunFinishedEvent):
                                    finished = event
                                else:
                                    yield encoder.encode(event)
                        finally:
                            await events.aclose()
                        if finished is None or binding.answer is None:
                            raise ToolError("incomplete_stream", "Stream ended without validated completion.")
                    history.append({"role": "assistant", "result": binding.answer})
                    _save_history(candidate, history)
                    candidate.record.running = False
                    candidate.save()
                    yield encoder.encode(CustomEvent(
                        name="validated_pause" if binding.answer["status"] == "awaiting_human" else "validated_answer",
                        value=binding.answer,
                    ))
                    yield encoder.encode(finished)
            except asyncio.CancelledError:
                LOGGER.warning("UI stream disconnected; durable case state is retained without replay.")
                raise
            except Exception as error:
                code = error.code if isinstance(error, ToolError) else (
                    "case_busy" if isinstance(error, FileExistsError) else type(error).__name__
                )
                LOGGER.error("UI streamed operation failed (%s); durable state retained.", code)
                yield encoder.encode(RunErrorEvent(
                    code=code, message="Operation failed. Inspect case state and local server logs; do not retry an uncertain turn.",
                ))

        return StreamingResponse(
            stream_events(), media_type="text/event-stream",
            headers={"X-Accel-Buffering": "no", "Cache-Control": "no-store"},
        )

    return app
