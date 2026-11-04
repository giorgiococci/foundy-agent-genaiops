---
title: "Supply Chain Resilience Agent"
description: "Agent-led Foundry conversation, explicit prompt assets, Python function tools and human-approved synthetic reservations."
ms.date: "2026-11-04"
---

## What Runs Today

One managed Foundry prompt agent investigates a delayed component receipt,
compares recovery options and conducts a conversation with the planner.
The agent chooses its tools and reasoning order. Python executes the tools,
records human decisions and enforces stock/approval safeguards; it does not
prescribe compare/propose/execute reasoning stages.

Microsoft Agent Framework `FoundryAgent` now owns model/tool continuation.
There is one runtime path, not a framework wrapper around the old loop.
The framework migration is verified offline and by one bounded live
STANDARD case in S-032 on 2026-11-04.

The published agent is `supply-chain-resilience-advisor`, version `3`.
S-026 exercised actual investigation, STANDARD choice, exact human approval,
one reservation and post-write read-back. Its final answer failed a local
evidence check because it also included genuine pre-write facts.
S-027 corrects that handoff locally by separating current and historical
evidence, with regression tests. The published prompt/schema/definition did
not change. S-032 now verifies that correction through Agent Framework:
the final answer separates genuine pre-write facts from the current durable
reservation result and passes validation. Exactly one proposal/request
exists; W-B ends at 80 on hand / 70 reserved / 10 available, W-A remains 20.
This is a successful synthetic case, not a general model-quality certification.
See the [implementation log](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md).

## Source Layout

| Surface | Responsibility |
| ------- | -------------- |
| [advisor_demo.py](advisor_demo.py) | Single managed-agent CLI: local preparation/inspection/human decisions and guarded chat; no publication |
| [definition.py](supply_chain/agents/resilience_advisor/definition.py) | Current agent definition and instruction/schema fingerprints |
| [advisor.txt](supply_chain/agents/resilience_advisor/prompts/advisor.txt) | Mission, investigation, human-decision boundary, failure behavior and model response contract |
| [agent.py](supply_chain/agents/resilience_advisor/agent.py) | `create_agent(...) -> FoundryAgent`: managed version binding, local functions, middleware and runtime options |
| [conversation.py](supply_chain/agents/resilience_advisor/conversation.py) | Interaction state, trusted human decisions, guarded tool dispatch and current/historical evidence validation |
| [tools.py](supply_chain/agents/resilience_advisor/tools.py) | Advisor-owned function contracts and dispatcher |
| [runtime.py](supply_chain/runtime.py) | Framework chat/function safety middleware: whole-batch guards, call IDs, cumulative limits, usage and metadata events; no orchestration loop |
| [observability.py](supply_chain/observability.py) | Shared trace provider/export lifecycle, per-agent off/metadata/content policy and native-span correlation |
| [session.py](supply_chain/session.py) | Native framework-session persistence, artifact/SDK drift checks, exclusive lock and uncertainty stop |
| [domain.py](supply_chain/domain.py) | Synthetic rules, option costs, feasibility and delivery margins; no SDK or database |
| [store.py](supply_chain/store.py) | SQLite snapshots, proposals, human approval and atomic reservation |
| [data.py](supply_chain/data.py), [scenario.json](data/scenario.json) | SDK-free input loader and versioned initial facts |
| [cases.json](evals/resilience_advisor/cases.json) | Agent evaluation scenarios/rubrics, not measured results |
| [demo.py](demo.py) | SDK-free manual tool exercise; not a local AI agent |
| [test_domain.py](tests/test_domain.py), [test_workflow.py](tests/test_workflow.py) | Business rules, transactions, concurrency, failures and manual CLI |
| [runtime_tests.py](tests/runtime_tests.py) | Actual framework invocation and SDK HTTP serialization with offline service responses, batch/call-ID checks, limits and failure behavior |
| [advisor_tests.py](tests/advisor_tests.py) | Framework conversations, evidence roles, trusted human controls, native-session persistence and mocked cloud-binding guards |
| [observability_tests.py](tests/observability_tests.py) | Native spans, concurrent policy isolation, privacy, explicit export failure and shutdown flush |

The [agents namespace](supply_chain/agents) can accommodate future agents;
only [resilience_advisor](supply_chain/agents/resilience_advisor) exists.
Each agent owns its prompts, definition, specialized controls, tool
contracts/dispatcher and evaluation assets. Business rules, data, store and
the generic runtime are shared solution capabilities. Tools are not
automatically exposed to every agent.

Start with [agent.py](supply_chain/agents/resilience_advisor/agent.py) to see
how the agent is composed. Its factory returns the actual framework
`FoundryAgent`, not a custom agent subclass or wrapper. It binds callbacks
and safety middleware to the supplied conversation state. The CLI composes
these objects; the conversation class does not construct its own agent.

There is no speculative shared-tool directory, agent registry, orchestrator,
web framework or hosted runtime. Extract a shared tool when another agent
actually needs it, rather than copying its implementation.
The root package retains SDK-free convenience exports used by the manual CLI.

The historical read-only and staged drivers/CLIs were retired in S-027.
Useful transport/safety tests now target the current advisor/runtime.
The [readonly instructions](supply_chain/agents/resilience_advisor/prompts/readonly.txt)
and [walkthrough instructions](supply_chain/agents/resilience_advisor/prompts/walkthrough.txt)
remain provenance assets, not alternate execution paths.
Recorded runs, cloud versions and decision history were not deleted.

## Synthetic Scenario

HUB-1 needs one BOARD-1. Two customer commitments need 60 boards, due on
days 3 and 4. W-A has 20. The delayed 40-board supplier receipt arrives on
day 6. W-B has 80 boards, with 30 reserved for unrelated work and 50 available.
Assembly takes one day; other materials and capacity are assumed sufficient.

| Option | Quantity | Cost | Arrival | Assembly complete | Margins C-1 / C-2 |
| ------ | -------- | ---- | ------- | ----------------- | ---------------- |
| STANDARD | 40 | 90 | Day 2 | Day 3 | 0 / 1 days |
| EXPRESS | 40 | 95 | Day 1 | Day 2 | 1 / 2 days |

Both satisfy the cost ceiling of 100. Five additional fictional cost units
buy one extra day of schedule margin. The planner selects that trade-off;
no unique optimum or late-delivery probability is assumed.

## How the Agent Uses Tools

This is Foundry function calling, not HTTP or MCP:

1. The managed definition binds the model, instructions and function schemas.
2. Foundry returns a function request with name, JSON arguments and call ID.
3. Chat middleware validates the complete batch before any local effect.
4. Agent Framework invokes the matching local `FunctionTool` implementation
   sequentially, with per-call guards and the existing business dispatcher.
5. The framework returns `function_call_output` preserving the call ID and
   continues through the native `AgentSession`.

The managed definition remains authoritative. Local `FunctionTool` instances
provide implementations with matching exact schemas; tool declarations are
not sent alongside an agent reference. Do not rely on dynamic `tool_choice`
or `parallel_tool_calls` enforcement by the service: this adapter ignores
them. Application middleware enforces permissions, and the framework executes
local functions sequentially.

| Model-invocable function | Result |
| ------------------------ | ------ |
| `read_planning_snapshot` | Current stock, commitments, receipt delay and snapshot version |
| `read_transfer_policy` | Policy version, cost ceiling and assumptions |
| `compare_transfer_options` | Exact feasible options, costs and margins without selecting |
| `create_transfer_proposal` | Proposal matching the trusted planner selection; no reservation |
| `execute_approved_transfer` | Request and source reservation for the exact human-approved proposal |
| `read_transfer_result` | Durable outcome for reconciliation and post-write verification |

Approval is a separate human-only application operation, not a model tool.
Text claiming approval cannot grant permission. The portal cannot execute
these local Python functions; an application must dispatch the calls.
Portal-only execution would require an appropriate remote tool integration.

### Current and Historical Evidence

The model returns exactly `message` and `evidence`, with complete unchanged
tool-result objects. Python checks provenance, not another model call.
The delivered application answer contains:

* `message`: the model's user-facing explanation
* `evidence`: exact results still current in the application's tool context
* `historical_evidence`: exact earlier results superseded or invalidated by a write

Only Python records historical objects, directly from successful tool calls.
The model cannot invent history or label an old snapshot as current.
For example, reserved stock 30 before the write belongs in historical evidence;
the durable result with reserved stock 70 belongs in current evidence.
If an unchanged result is obtained again, its current match takes precedence.

Changed/unknown objects are rejected. Required comparison/proposal results
must be current; comparisons invalidated by execution no longer masquerade
as current obligations. A completed action must include the exact current
result and a result lookup performed after the write. Historical evidence
cannot replace that lookup or its result.

These are deterministic data/authority checks, not a certification of every
free-text claim. Model-quality evaluation remains necessary. The model still
chooses tools, asks questions and explains trade-offs.

## Local Commands

From the repository root, using the optional SDK environment:

```powershell
src\supply-chain-resilience\.venv\Scripts\python.exe -B src\supply-chain-resilience\advisor_demo.py definition --deployment gpt-6.1-sol
src\supply-chain-resilience\.venv\Scripts\python.exe -B src\supply-chain-resilience\advisor_demo.py init --deployment gpt-6.1-sol --directory artifacts\local\supply-chain-advisor
src\supply-chain-resilience\.venv\Scripts\python.exe -B src\supply-chain-resilience\advisor_demo.py inspect --directory artifacts\local\supply-chain-advisor
```

`init` creates only a new local synthetic session/store. It does not create
an Azure agent or conversation and never overwrites an existing directory.
The model-request allowance defaults to ten; `init --model-request-limit 20`
explicitly sets twenty for a new authorized session. It does not modify
an existing run. Extensions need separate authorization and an audited
operator action without resetting cumulative usage.

`select --option STANDARD|EXPRESS` records a one-case human choice.
`approve --proposal-id ID --confirm` or `reject --proposal-id ID` records
the exact human decision without invoking the model. A rejected session
does not silently reopen or create another proposal.

`chat` takes `--message`, `--directory`, explicit project endpoint/tenant
configuration and `--agent-version`. It retrieves and verifies that exact
published cloud definition/version before inference, even if a newer version
exists. `FoundryAgent` uses a versioned `agent_reference` on the non-preview
project Responses endpoint. All reasoning turns use this same
command; no compare/propose/execute model stages are prescribed.
It cannot publish an agent. Matching v3 remains compatible with the local
definition. S-032 verified one new live case; any further live case still
requires explicit operational consent.

### Retained Failed Run

S-026's run is retained under ignored `artifacts\local\supply-chain-s026`.
Exactly one reservation exists: W-B 80/70/10, W-A 20. There was no shipping
or receipt. Its final-answer failure deliberately retained `running=true`
as a stop flag; no process is active and usage is reconciled.
Do not clear the flag, rewrite its source hash or retry the operation.

Historical S-026 state is not accepted by the new runtime or its `inspect`
command. Read its recorded JSON directly without Azure/model access:

```powershell
Get-Content artifacts\local\supply-chain-s026\advisor-session.json
```

Neither old staged sessions nor pre-framework advisor sessions are migrated.
Their retained JSON, SQLite and metadata trace remain read-only historical
evidence. Use a fresh authorized directory for the new runtime.

## Persistence, Limits and GenAIOps

The stable [instruction asset](supply_chain/agents/resilience_advisor/prompts/advisor.txt)
is tracked with code, schemas, model configuration, data, policies and
evaluation assets. Foundry versions identify publications, not local edits.
No automatic portal/Git synchronization, optimizer or release pipeline exists.
See the [prompt-lifecycle research](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#s-023---agent-led-design-and-prompt-lifecycle-review).

Each advisor directory contains:

| File | Purpose |
| ---- | ------- |
| `advisor-session.json` | Format `supply-chain-framework-1`: native `AgentSession.to_dict()` state, bindings, fingerprints, SDK versions, human decisions, current/historical facts, call IDs, allowance and usage |
| `planning.sqlite3` | Snapshot, exact proposal/approval and idempotent reservation |
| `events.jsonl` | Correlated metadata, statuses, durations and usage; no prompt, arguments, result payloads or model text |
| `advisor.lock` | Exclusive command lock; absent after normal completion |

Source hashing includes nested agent Python modules and the advisor CLI.
Source/prompt/schema/data/evaluation/SDK drift prevents silent resumption.
State is checkpointed before network requests; failed/interrupted turns
remain blocked instead of automatically retrying. History loading defaults
to empty when absent; it does not bypass drift checks or reconstruct facts.
These are local provenance controls, not signatures or a clean-commit claim.
Native framework state is restored with `AgentSession.from_dict()`, not
reconstructed from a transcript. It includes the service continuation
reference and framework provider state. Keep runtime artifacts local; do not
copy session payloads or conversation transcripts into project tracking.

The runtime permits twenty tools and requests at most 4,096 output tokens
per response. Cumulative 100,000-token/EUR 10 thresholds monitor reported
usage after each response and before the next request, not guaranteed
pre-inference limits. Missing/lost usage stops the run as unreconciled.
SDK automatic retries are disabled. The unsupported token-count endpoint
is not called; the prior HTTP 405 is historical.
Fatal function failures latch a stop before the framework's optional
service-conversation settlement can make another request. There is no
automatic thread repair or model retry; inspect durable effects first.
Token streaming is not enabled by this migration, and AG-UI/UI code is absent.

The estimate uses conservative EUR 5 input / EUR 20 output per million,
charging all tokens at the higher rate. It is not an invoice, actual tariff,
tax calculation or Azure spending cap. See the [pricing evidence](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#s-020-fresh-source-check-and-preflight-boundary).

The ten [evaluation cases](evals/resilience_advisor/cases.json) are synthetic
rubrics, not a passed scorecard or held-out benchmark. Local event inspection
is not distributed OpenTelemetry/Azure Monitor tracing.

## Shared Foundry Tracing

The CLI defaults to `--telemetry off`: no destination lookup or local trace
export. Opt in on an authorized `chat` with `--telemetry metadata` or
`--telemetry content`. Both use the existing project's linked Application
Insights, discovered through the public `project.connections` API; no telemetry resource or
agent version is created. Linking Insights alone does not instrument Python.

| Policy | Exported data |
| ------ | ------------- |
| `off` | No locally exported spans for that agent or its tools/model calls |
| `metadata` | Native agent/model/tool spans, IDs, timings, status and token counts; no messages or tool payloads |
| `content` | Metadata plus synthetic turn input/validated output and tool arguments/results |

`TelemetryPolicy` and a task-local `agent_trace(...)` scope are shared.
The advisor owns `DEFAULT_TELEMETRY_POLICY` in
[conversation.py](supply_chain/agents/resilience_advisor/conversation.py);
the CLI explicitly overrides it with the chosen flag. Programmatic callers
can pass `telemetry_policy=TelemetryPolicy("metadata")` when constructing
the conversation. A future agent can reuse the scope and tool callback
adapter without inheriting an advisor class or sharing its business state.

One provider is initialized at CLI bootstrap. Agent Framework's
process-global sensitive recording remains disabled: enabling content for
one agent cannot turn on native sensitive capture for another, including
concurrent tasks. Existing native spans are reused; a `supply_chain.turn`
parent correlates application validation with agent/model/tool children.
Content belongs to that turn and the tool spans, not every intermediate
model request. System instructions, raw SDK session state, arbitrary log
events and exception text are not exported. Payloads are bounded to 6,000
characters with explicit JSON truncation; common credential keys/patterns
are redacted. This is not a general-purpose data-loss prevention system:
content mode is approved only for synthetic, non-secret data.

The current exporter is pinned to `azure-monitor-opentelemetry-exporter`
`1.0.0b58` (beta), with OTel SDK `1.45.1`. Only traces are configured, not
automatic HTTP/log/metric instrumentation. Auxiliary exporter statistics/
control-plane workers and offline retry storage are disabled. The connection
string is neither printed nor persisted in candidate artifacts.
The installed Projects 2.7 telemetry convenience method accepts only API-key
credentials. Shared discovery also handles the observed project-managed
identity connection whose Insights connection string is in metadata.
Missing, ambiguous or unsupported layouts fail explicitly, without printing
credentials or changing the Azure connection.

The returned `telemetry.trace_id` and local `telemetry.started` metadata event
identify the trace for Foundry/Application Insights queries. CLI shutdown
flushes the provider on success and errors. Export failure is explicit and
does not authorize replaying an already completed model operation.
Successful export is not proof of ingestion or portal visibility; verify the
specific trace in the linked resource, allowing typical ingestion delay.
Old conversations are not retroactively exported.

S-034 verified one bounded read-only live case on 2026-11-04 in linked
Insights `ai-ai-demo-01`: all seven expected spans arrived (turn, agent,
two model calls and three tools), with correlation and selected synthetic
content. Initial partial visibility resolved after ingestion delay.
The case used 3,361 tokens with a conservative model estimate of EUR 0.06722;
zero proposals/reservations and unchanged stock were independently verified.
Backend ingestion was queried; the portal UI was not independently opened.
See [A-022](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-022---s-034-shared-per-agent-observability).

For a separately authorized bounded tracing case, initialize a new directory
with `--model-request-limit 5 --tool-call-limit 10 --total-token-limit 30000
--spend-eur-limit 2`. These limits are persisted and restored without changing
existing sessions. Token/cost bounds remain post-response monitoring.

## SDK-Free Manual Tool Exercise

The manual adapter demonstrates the same business functions without a model:

```powershell
Set-Location C:\repo\Microsoft\foundry-multi-agent\src\supply-chain-resilience
python -B demo.py init
python -B demo.py snapshot
python -B demo.py policy
python -B demo.py compare
$proposal = python -B demo.py propose EXPRESS | ConvertFrom-Json
$proposal | ConvertTo-Json
python -B demo.py --role approver approve $proposal.proposal_id --confirm
python -B demo.py execute $proposal.proposal_id
python -B demo.py result $proposal.proposal_id
```

Inspect the proposal before confirming. Repeated execution of the same
approved ID returns `already_requested` without another effect.
Initialization never overwrites a database. Alternate synthetic scenarios
include `ceiling-92`, `ceiling-80`, `no-impact`, `insufficient-stock` and
`missing-policy`; select a new filename with `--db` and `init --scenario`.

Roles are local fixtures, not authentication. Approval binds the exact
proposal and facts. Request insertion and stock reservation share one SQLite
transaction; failures roll back. Never expose this CLI/database to untrusted
users or real operational data. No physical transfer, destination receipt,
cancellation or ERP integration is implemented.

## Optional SDK Environment and Tests

Use the existing project environment. If setting it up separately:

```powershell
python -m venv src\supply-chain-resilience\.venv
src\supply-chain-resilience\.venv\Scripts\python.exe -m pip install -r src\supply-chain-resilience\requirements-foundry.txt
```

Configure `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT` and
`FOUNDRY_TENANT_ID` outside source control. The caller must be logged into
the intended Azure CLI tenant. `AzureCliCredential` uses that explicit
directory, not an implicit credential fallback or automatic login change.
Terminal validation uses Python 3.12.10, SQLite 3.49.1, framework core
1.24.0, Foundry adapter 1.16.0, OpenAI adapter 1.18.0, Projects 2.7.0,
Identity 1.27.0, OpenAI 3.38.0, OTel SDK 1.45.1 and Azure Monitor exporter
1.0.0b58 (beta). Projects 2.7.0 satisfies the adapter's
`>=2.2.0,<2.8.0` requirement; do not upgrade Projects independently.
This is not a supported-version matrix.

From the repository root:

```powershell
python -B -m unittest discover -s src\supply-chain-resilience -p "test_*.py" -v
src\supply-chain-resilience\.venv\Scripts\python.exe -B -m unittest discover -s src\supply-chain-resilience -p "*test*.py" -v
node --test scripts\test-copilot-customizations.mjs
```

There are 34 SDK-free tests and 122 combined tests, including 17 tracing
tests. Retired-driver-specific
tests were removed; relevant runtime and human-action safeguards remain
covered on the current path. The broader selector includes optional SDK
simulations, not cloud inference. The framework itself runs in these tests;
only service I/O is simulated, including HTTP transport-level checks.
All Python tests use isolated temporary
databases and remove only their own artifacts. They do not prove real IAM
isolation or general model quality.
