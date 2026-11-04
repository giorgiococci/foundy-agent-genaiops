"""Durable candidate sessions; never publish an agent or reset uncertain work."""

from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from importlib.metadata import version
from pathlib import Path
from collections.abc import Generator
from uuid import uuid4

from agent_framework import AgentSession
from agent_framework.foundry import FoundryAgent

from .agents.resilience_advisor.definition import fingerprint, provenance
from .agents.resilience_advisor.conversation import AdvisorConversation, HumanDecisions
from .agents.resilience_advisor.tools import ToolSession
from .data import SCENARIO, load_snapshot
from .domain import DemoActor, DemoRole, ToolError
from .runtime import Pricing, RunLimits, RunUsage
from .store import DemoStore


ROOT = Path(__file__).parent.parent
EVALUATIONS = ROOT / "evals" / "resilience_advisor" / "cases.json"
SDK_PACKAGES = (
    "agent-framework-core", "agent-framework-foundry", "agent-framework-openai",
    "azure-ai-projects", "azure-identity", "openai",
)


def source_fingerprint() -> str:
    paths = sorted((ROOT / "supply_chain").rglob("*.py")) + [ROOT / "advisor_demo.py"]
    return fingerprint({str(path.relative_to(ROOT)): path.read_text(encoding="utf-8") for path in paths})


def asset_fingerprint(path: Path) -> str:
    return fingerprint(json.loads(path.read_text(encoding="utf-8")))


@dataclass
class SessionRecord:
    deployment: str
    provenance: dict[str, str]
    source_sha256: str
    scenario_sha256: str
    evaluation_sha256: str
    sdk_versions: dict[str, str]
    model_request_limit: int = 10
    format: str = "supply-chain-framework-1"
    run_id: str = field(default_factory=lambda: str(uuid4()))
    running: bool = False
    agent_version: str | None = None
    framework_session: dict[str, object] | None = None
    endpoint: str | None = None
    usage: RunUsage = field(default_factory=RunUsage)
    decisions: HumanDecisions = field(default_factory=HumanDecisions)
    seen_call_ids: list[str] = field(default_factory=list)


class CandidateSession:
    def __init__(self, directory: Path, record: SessionRecord) -> None:
        self.directory = directory
        self.record = record
        self.store = DemoStore(directory / "planning.sqlite3")
        self.framework_session = (
            AgentSession.from_dict(record.framework_session) if record.framework_session is not None else None
        )
        self.advisor = AdvisorConversation(
            ToolSession(self.store, DemoActor("demo-planner", DemoRole.PLANNER)),
            pricing=Pricing(Decimal("5"), Decimal("20"), "Conservative demo estimate; not an invoice"),
            limits=RunLimits(model_requests=record.model_request_limit), decisions=record.decisions,
            usage=record.usage, seen_call_ids=set(record.seen_call_ids), on_event=self._event,
        )

    @classmethod
    def initialize(
        cls, directory: Path, deployment: str, *, model_request_limit: int = 10,
    ) -> CandidateSession:
        RunLimits(model_requests=model_request_limit)
        snapshot = load_snapshot()
        record = SessionRecord(
            deployment=deployment, provenance=provenance(deployment),
            source_sha256=source_fingerprint(), scenario_sha256=asset_fingerprint(SCENARIO),
            evaluation_sha256=asset_fingerprint(EVALUATIONS),
            sdk_versions={name: version(name) for name in SDK_PACKAGES},
            model_request_limit=model_request_limit,
        )
        directory.mkdir(parents=True, exist_ok=False)
        candidate = cls(directory, record)
        candidate.store.initialize(snapshot)
        candidate.save()
        return candidate

    @classmethod
    def load(cls, directory: Path) -> CandidateSession:
        path = directory / "advisor-session.json"
        if not path.exists() and (directory / "session.json").exists():
            raise ToolError("incompatible_session", "Historical state is read-only; inspect its recorded JSON/SQLite separately. No migration is performed.")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("format") != "supply-chain-framework-1":
            raise ToolError("incompatible_session", "A new Agent Framework session is required. Historical artifacts remain read-only; no migration is performed.")
        try:
            data["usage"] = RunUsage(**data["usage"])
            data["decisions"] = HumanDecisions(**data["decisions"])
            return cls(directory, SessionRecord(**data))
        except (KeyError, TypeError) as error:
            raise ToolError("invalid_session", "Candidate state fields are missing or incompatible.") from error

    def save(self) -> None:
        self.record.framework_session = self.framework_session.to_dict() if self.framework_session is not None else None
        self.record.seen_call_ids = sorted(self.advisor.safety.seen_call_ids)
        temporary = self.directory / "advisor-session.next.json"
        temporary.write_text(json.dumps(asdict(self.record), indent=2), encoding="utf-8")
        temporary.replace(self.directory / "advisor-session.json")

    @contextmanager
    def locked(self) -> Generator[None]:
        lock = self.directory / "advisor.lock"
        with lock.open("x", encoding="utf-8") as stream:
            stream.write("Exclusive candidate command in progress.\n")
        try:
            yield
        finally:
            lock.unlink()

    def ensure_ready(self) -> None:
        if self.record.running or self.record.usage.usage_unreconciled:
            raise ToolError("uncertain_turn", "Inspect durable state; an interrupted turn cannot retry automatically.")
        current_sdks = {name: version(name) for name in SDK_PACKAGES}
        if (self.record.provenance != provenance(self.record.deployment)
                or self.record.source_sha256 != source_fingerprint()
                or self.record.scenario_sha256 != asset_fingerprint(SCENARIO)
                or self.record.evaluation_sha256 != asset_fingerprint(EVALUATIONS)
                or self.record.sdk_versions != current_sdks):
            raise ToolError("candidate_drift", "Code, instructions, tools, data, evaluations or SDKs changed; do not resume silently.")

    def _event(self, fields: dict[str, object]) -> None:
        self.save()
        trace = {
            "time": datetime.now(timezone.utc).isoformat(),
            "run_id": self.record.run_id,
            "conversation_id": self.framework_session.service_session_id if self.framework_session is not None else None,
            "definition_sha256": self.record.provenance["definition_sha256"], **fields,
        }
        with (self.directory / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(trace) + "\n")

    async def reply(self, agent: FoundryAgent, message: str) -> dict[str, object]:
        self.ensure_ready()
        if not message.strip():
            raise ToolError("empty_message", "A nonempty planner message is required.")
        if (self.framework_session is None or not isinstance(self.framework_session.service_session_id, str)
                or not self.framework_session.service_session_id.strip()):
            raise ToolError("missing_conversation", "Bind an explicitly verified managed-agent conversation first.")
        self.record.running = True
        self.save()
        result = await self.advisor.reply(agent, self.framework_session, message)
        self.record.running = False
        self.save()
        return result

    def inspect(self) -> dict[str, object]:
        viewer = DemoActor("demo-viewer", DemoRole.VIEWER)
        return {
            "session": asdict(self.record), "snapshot": self.store.read_snapshot(viewer),
            "result": self.store.read_result(viewer, self.record.decisions.proposal_id)
            if self.record.decisions.proposal_id else None,
        }
