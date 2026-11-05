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

The [CopilotKit chat](#copilotkit-chat) is the single default browser interface
on that runtime, with native AG-UI streaming and contextual human controls.
The first submitted question creates the real Foundry conversation.
Only the business facts and reservation store are synthetic. Scripted model
responses exist exclusively in automated test fixtures.

S-039 verifies a real first-question browser turn on 2026-11-04: two model
requests, three tools, 3,467 reconciled tokens and 69 native text events,
followed by application validation and successful completion. Reload
restores history without inference. This check stops at the human choice;
it creates no proposal or reservation.

The current release is `supply-chain-resilience-advisor`, version `5`.
S-043 adds data-driven calendar dates, currency and descriptive labels,
plus generic writing guidance and Markdown rendering for human questions.
Its exact managed definition is published and retrieved for comparison.
164 related Python tests, 16 frontend tests and three offline SDK/SSE
integrations pass. Browser checks cover dates, EUR amounts, labels,
Markdown, one-click continuation, reload and a 390px viewport.
No new live model run or prose-quality evaluation is claimed for v5.

The historical baseline is version `3`.
Native human-handoff version `4` adds two request-only tool schemas.
Version 3 cannot run this changed
definition; it and its historical conversations remain preserved.
S-041 publishes and verifies version `4`: a real Italian browser conversation
reaches a native choice, then one EXPRESS click automatically resumes it into
an Italian exact-proposal approval request. The bounded check uses four model
requests, six tools including the two human requests, and 7,760 tokens.
No live approval/reservation is performed; those branches pass offline SDK,
wire and browser tests. Reload retains the actual pending call without inference.
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
| [service.py](supply_chain/service.py) | Shared exact managed-version and native-conversation binding for CLI and UI |
| [ui_demo.py](ui_demo.py), [ui.py](supply_chain/ui.py) | Real loopback chat entry point, first-question initialization, server-owned state and trusted actions |
| [ui_stream.py](supply_chain/ui_stream.py) | Official framework AG-UI adapter binding and same-origin native streaming |
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
| [streaming_tests.py](tests/streaming_tests.py), [ui_tests.py](tests/ui_tests.py) | Actual native HTTP streaming and AG-UI adapter, complete human-controlled case, provisional text, failures and disconnects before/after writes |
| [frontend](frontend) | Default CopilotKit v2 React/TypeScript chat, pinned lockfile, guarded transport and SDK/wire tests |

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

There is no speculative shared-tool directory, agent registry, orchestrator
or hosted runtime. The web interface is a local-development application.
Extract a shared tool when another agent
actually needs it, rather than copying its implementation.
The root package retains SDK-free convenience exports used by the manual CLI.

The historical read-only and staged drivers/CLIs were retired in S-027.
Useful transport/safety tests now target the current advisor/runtime.
The [readonly instructions](supply_chain/agents/resilience_advisor/prompts/readonly.txt)
and [walkthrough instructions](supply_chain/agents/resilience_advisor/prompts/walkthrough.txt)
remain provenance assets, not alternate execution paths.
Recorded runs, cloud versions and decision history were not deleted.

## CopilotKit Chat

The default chat uses CopilotKit's styled `CopilotChatView`,
`CopilotChatMessageView` and composer with an explicit-run AG-UI client.
No Copilot Runtime, provider key, Intelligence account or hosted service is
required. The direct agent provider is development-only, not production
hosting. FastAPI serves the built application at `/`; the old static client
and `/copilot/` preview route have been removed.

The selected available pin is react-core 1.82.0, with AG-UI JS 1.0.2,
React/ReactDOM 19.2.0 and Zod 3.25.76. The 1.84.1 metadata candidate from
research was unavailable in the configured feed. No registry/certificate
configuration was changed, and no prerelease was substituted.
The launcher explicitly depends on `python-dotenv` for local configuration.

From the repository root, build the frontend after dependency installation:

```powershell
Set-Location src\supply-chain-resilience\frontend
npm ci --ignore-scripts --no-audit --no-fund
npm run build
npm test
Set-Location ..
.\.venv\Scripts\python.exe -m pip install -r requirements-ui.txt
Copy-Item .env.example .env
```

If you already have a local `.env`, keep it instead of copying over it.
Set your approved tenant in `.env`, then launch:

```powershell
.\.venv\Scripts\python.exe -B ui_demo.py
```

The UI launcher loads `.env` beside [ui_demo.py](ui_demo.py), regardless of
the working directory. Precedence is CLI arguments, existing environment
variables, then `.env`. The local file is Git-ignored; [.env.example](.env.example)
is the shareable template. Do not store passwords or tokens there: authentication
continues to use Azure CLI. The separate advisor CLI does not load `.env`.

Use your existing authorized Azure CLI sign-in in that tenant. Open
`http://127.0.0.1:8080/` and ask a question. No new-case button or fabricated
opening message is required. Startup fails explicitly if configuration or the
frontend build is missing. Startup/page opening do not infer; first Send
creates local synthetic planning state and the actual managed conversation,
then streams the exact submitted question's answer. New chat only clears the
view; the next question initializes another conversation.

The URL retains a local chat ID for reload. Validated history, contextual
cards and human receipts are reconstructed from backend persistence, not
browser approval state. Reload does not infer or replay an interrupted turn.
Source, dependency lock, served build files (including binary assets) and
Python SDK identity are fingerprinted; drift blocks mutation, not inspection.
Historical runs are not migrated or rebound.
After this update, restart the server and choose New chat instead of
continuing an old v4 conversation. The local `.env` now selects v5;
an existing environment variable or explicit CLI argument still overrides it.

Limits apply cumulatively per conversation. Defaults are ten model requests,
twenty tools, 100,000 tokens and EUR 10 estimated monitoring. For a smaller
read-only check, use `--model-request-limit 5 --tool-call-limit 10
--total-token-limit 30000 --spend-eur-limit 2`. Token/cost thresholds are
checked after responses, not guaranteed Azure billing caps. There are no
automatic retries. Telemetry export defaults to off.

### Scenario Context and Readable Explanations

[scenario.json](data/scenario.json) version 2 defines a fixed day-one date
(`2026-11-09`), EUR synthetic costs and descriptive labels keyed by stable
entity IDs. Day slots are consecutive calendar days: day 1 is 9 November,
day 3 is 11 November, and day 6 is 14 November. No business-day or holiday
calendar is assumed; wall-clock today does not shift saved cases.

The domain returns exact order/receipt/transfer dates with this context in
authoritative tool results. SQLite preserves the context per case and copies
it into each exact proposal; approval covers the currency and calendar too.
The browser renders these supplied values, rather than inventing dates or
assuming every cost is EUR. Without context, it explicitly shows relative
days and unspecified cost units.

The advisor prompt specifies writing principles only: explain impact first,
compare meaningful differences in short paragraphs, bullets or a small table,
and ask one focused question. It contains no fixture-specific IDs, dates,
names or currency. Native human questions use CopilotKit's Markdown renderer.
Alternate calendar, label and currency tests exercise the same implementation.
The underlying demo business model is still synthetic; this change is not an
ERP adapter or a general scheduling engine.

### Offline Automated Tests

The fixture is a test runner, not an alternative application launch:

```powershell
.\.venv\Scripts\python.exe -B -m tests.ui_fixture_server --directory C:\temp\supply-chain-copilot-test --port 8876
```

Use a new empty test directory. Its root page explicitly labels simulated
upstream responses. `--invalid-final` exercises validation failure.

In another terminal, with the offline fixture running:

```powershell
Set-Location src\supply-chain-resilience\frontend
$env:UI_FIXTURE_URL = "http://127.0.0.1:8876"
npm run test:integration
```

The wire suite refuses a bootstrap that is not explicitly an offline
fixture. The actual CopilotKit core handles the two native human tools and
automatically follows each backend-verified response into the next HTTP leg.
It proves one actual user message, then two real tool results, exact approval,
one reservation/read-back, Origin/token checks and interrupted-turn blocking.

The model requests `request_transfer_choice` or `request_transfer_approval`.
The v2 `useHumanInTheLoop` hook waits for a human click. The backend checks
the actual native call ID, current facts, feasible option/exact proposal and
explicit confirmation, records a receipt and returns it. Only then does
`respond` release the hook and let core continue. No extra Continue, hidden
English message or model-granted approval exists.

The client projects one genuine user message or one correlated human-tool
result, not display history. Projection recognizes human results even when
assistant narration follows their call in SDK history. Server-owned native
definitions are authoritative; frontend schema text is never execution
authority. The server reconstructs the actual stored call for the AG-UI
adapter and gives the native agent only the checked stored function output.

Each leg needs application validation and a matching successful terminal.
`validated_pause` means a persisted native human request, not business
completion; `validated_answer` means a checked answer. Validation failure
rejects the transport before core can continue, even if SDK subscribers
swallow errors. No initial, reload, suggestion or retry inference is configured.
Only a recorded real human response triggers an automatic follow-up.
New chat unmounts the previous composer; a running turn prevents switching.

Assets, including small fonts, are served locally under the existing strict
script/style/network CSP. No `unsafe-inline`, `unsafe-eval`, data-font or
external host allowance was added. Package installation skips all scripts,
including Scarf; the lockfile retains package/license metadata.
The styled package graph is substantial and Vite reports large chunks.
No dependency security audit or production readiness is claimed.

Automated fixture success is not live Foundry evidence or final user UX
acceptance. No production, dependency-security or accessibility certification
is claimed.

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
Two additional declaration-only functions request choice or exact-proposal
approval. The model calling either does not select, approve or reserve.
Human requests must occur alone, without executable sibling calls; they
count once in the tool allowance. All six business tools retain their guards.
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

`select --option STANDARD|EXPRESS --tool-call-id CALL_ID` records a one-case
human choice for the actual pending native call.
`approve --proposal-id ID --confirm --tool-call-id CALL_ID` or
`reject --proposal-id ID --tool-call-id CALL_ID` records
the exact human decision without invoking the model. A rejected session
does not silently reopen or create another proposal.

`chat` takes `--message`, `--directory`, explicit project endpoint/tenant
configuration and `--agent-version`. It retrieves and verifies that exact
published cloud definition/version before inference, even if a newer version
exists. `FoundryAgent` uses a versioned `agent_reference` on the non-preview
project Responses endpoint. All reasoning turns use this same
runtime; no compare/propose/execute model stages are prescribed. The CLI
operator can use `resume` with the same cloud configuration instead of
`chat --message` after recording a human response. It submits the genuine
stored tool result, not a synthetic user sentence. The browser does this
automatically after its one decision click.
The CLI cannot publish an agent. The native definition needs its new exact
published version; v3 is historical, not a fallback. Live use requires
explicit operational consent.

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

Source hashing includes nested agent Python modules, CLI/UI entry points
and browser assets. UI-created cases also record their optional UI SDK versions.
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

## Local AG-UI Interface and Native Streaming

Install the optional UI environment from the repository root:

```powershell
src\supply-chain-resilience\.venv\Scripts\python.exe -m pip install -r src\supply-chain-resilience\requirements-ui.txt
```

Then follow the [single chat build and launch](#copilotkit-chat).

Configure the same approved endpoint, tenant and deployment used by the CLI.
Set `FOUNDRY_AGENT_VERSION` or `--agent-version` to the exact published
native-handoff version; the launcher no longer guesses version 3.
The server verifies its exact definition before inference.
Telemetry defaults to `off`; `--telemetry metadata` or `--telemetry content`
additionally enables export to the existing linked destination and requires
live authorization. Content mode is only for approved synthetic inputs.
Targets, credentials and policy remain server-side, not browser settings.
Cases default to `artifacts\local\ui`; do not point this interface at old
CLI/live runs or reset/rebind their fingerprints.

The UI uses the official `AgentFrameworkAgent` adapter and AG-UI event
encoder over HTTP Server-Sent Events. CopilotKit's AG-UI SDK consumes the
stream; the frontend requires a Node build, but no second model loop.
`FoundryAgent.run(..., stream=True)` still owns native model/tool continuation.
The SDK transport binding retains server-owned native session state and outer
evidence validation, instead of registering the unguarded raw agent.

1. Send your question and inspect streamed text,
   tool activity, evidence, usage and case/run/conversation/trace IDs.
2. When the advisor requests a preference, select STANDARD or EXPRESS.
   The backend records the choice; CopilotKit returns its real tool result
   and the advisor continues automatically to its next tools.
3. Inspect the exact proposal, check its confirmation and approve or reject
   using the dedicated controls. Chat text cannot grant approval.
4. The advisor continues automatically. An approved reservation must be read back and
   evidenced before the answer is marked validated. No physical shipment occurs.

The renderer extracts only the incremental top-level JSON `message` string,
including split escapes, and handles separate native messages independently.
Streamed text remains provisional. Terminal usage/status and the complete
assembled call batch are checked before native function dispatch; sibling
calls cannot execute first and bypass a forbidden call.
Only a validated-answer event followed by `RUN_FINISHED` validates a completed
answer. A validated pause enables the native human card, not a success badge.
The framework's unbuffered result-gate warning is expected: partial text
is intentionally visible before validation, but tools remain gated.

Stop stream, a disconnect, missing terminal usage, invalid evidence or a
failed tool never clear a durable uncertain turn or trigger replay. A
reservation already committed remains committed. Inspect the durable
snapshot; do not retry an uncertain case. Duplicate user runs and consumed,
stale or cross-case human results are refused. Logical SDK run IDs may span
human legs; the pending native call and receipt are single-use.
Reload the chat URL to restore the pending question without inference.
A decision saved just before a lost continuation remains visible, but is
not automatically replayed or requested again. Inspect it explicitly.
Browser messages/state/tools/forwarded properties are never authoritative.

This is a single-user local lab, not a production or multi-user service.
It binds loopback, checks Host/Origin and a local action token, enables no
cross-origin access, and does not render returned content as HTML.
The token protects local browser actions; it is not user identity or enterprise
authentication. Per-case file locks serialize CLI/UI effects.

The [test-only fixture server](tests/ui_fixture_server.py) uses the real
framework, OpenAI HTTP streaming types and official AG-UI adapter, but scripted
service responses. It is visibly labeled `OFFLINE TEST FIXTURE / NOT FOUNDRY`.
It proves browser/protocol/safety integration, not real Foundry inference,
live output quality or new Azure trace ingestion.

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
The optional UI manifest includes these same pins and adds
`agent-framework-ag-ui==1.7.1`, `fastapi==0.141.0` and `uvicorn==0.38.0`.
No proven framework pins were upgraded for the UI.

From the repository root:

```powershell
python -B -m unittest discover -s src\supply-chain-resilience -p "test_*.py" -v
src\supply-chain-resilience\.venv\Scripts\python.exe -B -m unittest discover -s src\supply-chain-resilience -p "*test*.py" -v
node --test scripts\test-copilot-customizations.mjs
```

Install the UI manifest before running the combined selector.
There are 34 SDK-free tests and 150 combined tests, including 17 shared
observability tests and 28 streaming/UI tests. Retired-driver-specific
tests were removed; relevant runtime and human-action safeguards remain
covered on the current path. The broader selector includes optional SDK
simulations, not cloud inference. The framework itself runs in these tests;
only service I/O is simulated, including HTTP transport-level checks.
All Python tests use isolated temporary
databases and remove only their own artifacts. They do not prove real IAM
isolation or general model quality.
