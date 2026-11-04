---
title: "Implementation of supply-chain-resilience"
description: "Authorized local business-tool implementation, module boundaries and verified test evidence."
ms.date: "2026-11-04"
---

## Activity Log

## A-020 - S-031 Explicit Agent Factory

* Date: 2026-11-04
* Authority: Q-030, user's acceptance of the single local design recommendation
* Status: local refactor verified on the existing `feat/agent-framework` branch
* Scope: factory extraction, callers/tests, source-layout documentation and tracking

The new [agent module](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/agent.py)
exposes `create_agent(project, agent_version, conversation=...) -> FoundryAgent`.
It composes the managed version, exact local function implementations, middleware,
limits and retry configuration. The returned object is the framework agent,
not a custom agent class or wrapper.

[AdvisorConversation](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
retains interaction state, human decisions, guarded dispatch and current/historical
evidence. Its public `invoke_tool` callback connects those controls to the factory.
Removed its construction method; there is no alias or parallel creation path.
CLI and all ten test/helper factory callers use the new module. Managed
definition, prompts, tool schemas, dependencies and runtime behavior are unchanged.

Verification:

* All 71 framework/runtime/advisor tests passed in 3.009 seconds through the
  extracted factory, including actual offline function invocation, serialized
  HTTP requests, exact human gates, budgets, evidence and native-session restore
* Extended the existing provenance regression to cover `agent.py` as well as
  `tools.py`; the focused regression passed after that test change
* All 15 current application/test Python files parsed under the application
  interpreter; Pylance also reports no syntax errors in the new factory module
* Pylance reports all ten factory call sites compatible, but renders external
  SDK types as `Any`; this is not a clean dependency-aware editor type-check
* No remaining Python references to the retired `build_agent` or private
  `_invoke_tool` entry points
* All ten documentary/link checks passed; `git diff --check` reports no
  whitespace errors

Existing uncommitted S-030 changes were retained. No Azure access, inference,
publication, dependency installation, old-session migration/rebinding, commit
or push occurred. Existing session source hashes intentionally drift after
the extraction; no historical run was adjusted to bypass that protection.
S-031 local approval is consumed. A fresh bounded live framework case remains
the one proposed next activity and requires separate operational consent.

## A-019 - S-030 Direct Agent Framework Migration

* Date: 2026-11-03
* Authority: Q-029, S-030 revision 1 local-only contract
* Branch: `feat/agent-framework`, created from the clean `main`
* Status: application implementation and offline integration verified
* Boundary: no authenticated Azure access, inference, publication, UI,
  actual-run migration/retry/deletion, commit or push

### Single Framework Runtime

Replaced the generic custom Responses loop with the actual Microsoft
`FoundryAgent`. The [advisor](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
owns its managed-agent construction, exact local `FunctionTool` bindings and
business capability/evidence adapter. The framework executes functions and
continues the conversation. There is no custom model loop or fallback.
The [shared runtime module](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
now contains cumulative budget/call policy and framework middleware only.

Chat middleware checkpoints each service request before I/O, reconciles
raw SDK response usage/status and validates the whole function batch before
any effect. Function middleware validates unused call IDs, emits metadata,
checks authoritative results and propagates fatal failure. Calls are locally
sequential. A failure latch prevents the framework's hosted-conversation
settlement request from making extra I/O; no automatic recovery is attempted.
Expected and unexpected function errors stop rather than becoming recoverable
model inputs. Model request default remains ten, with explicit allowance up
to twenty; tool/token/output/spend limits remain unchanged.

The asynchronous [CLI](../../../../src/supply-chain-resilience/advisor_demo.py)
uses tenant-bound credentials and an async Projects client with retries off.
It retrieves the exact published version, checks its complete definition,
then supplies versioned `agent_reference` through the framework's non-preview
project endpoint. A newer latest version does not silently substitute for
the requested one. No publication API is implemented. Native framework
conversation creation is checkpointed, bound and reused.

The [session adapter](../../../../src/supply-chain-resilience/supply_chain/session.py)
persists actual `AgentSession.to_dict()` state and restores it using
`from_dict()`, alongside current/historical facts, exact human decisions,
call IDs, counters and source/asset/SDK provenance. Its new
`supply-chain-framework-1` format rejects old runs without migration.
Local inspection of those historical artifacts uses their recorded
JSON/SQLite, not a legacy runtime path. Failed turns remain blocked.

### Dependencies and Regression Evidence

Updated the [manifest](../../../../src/supply-chain-resilience/requirements-foundry.txt)
before installing only in the application's existing environment:
framework core 1.24.0, Foundry 1.16.0, OpenAI adapter 1.18.0, Projects 2.7.0,
Identity 1.27.0 and OpenAI 3.38.0. Projects 2.7.0 satisfies the adapter's
declared `<2.8.0` ceiling. `pip check` reports no broken requirements.

Validation:

* All 105 combined application tests passed in 11.590 seconds
* All 34 SDK-free business/manual tests passed independently in 3.018 seconds
* All ten repository documentary/link checks passed; `git diff --check`
  reports no whitespace errors
* Actual framework function invocation is exercised, not replaced by a mocked
  `agent.run`; network/service responses alone are simulated
* Real OpenAI HTTP serialization verifies version reference, conversation,
  matching tool outputs and absence of local tool declarations in requests
* A real SDK HTTP 503 fixture makes exactly one request despite a client
  fixture initially configured for retries; uncertain usage blocks continuation
* Whole-batch capability/argument/call-ID/tool-count guards, trusted exact
  selection/approval, stale approval, idempotency, mandatory read-back,
  current/historical evidence and failure stops pass
* Native session round-trip, bound conversation creation/reuse, cumulative
  counters/call IDs, metadata-only trace and old-format refusal pass
* All 14 current application/test Python files parsed under the application
  interpreter; no remaining executable `AgentRuntime`, `AdvisorLimits` or
  application-level model loop was found
* Existing prompt/schema/definition fingerprint tests pass unchanged

An initial full test process ended without a result (exit 1073807364).
Focused rerun and subsequent full 105-test run passed.
Initial targeted failures exposed framework `list[Content]` result handling
and incomplete service-conversation fixtures; both were corrected and covered.

Editor validation limitation: Pylance selected Python 3.14 rather than the
application environment and reported `reportMissingImports` for framework/
async Azure modules. An environment-update tool reported success but the
next environment query still showed 3.14. Package inventory independently
confirmed the modules in the application environment. Subsequent Pylance
syntax requests failed at MCP transport initialization; no clean Pylance
type-check result is claimed. Runtime signatures and all migrated call
surfaces are exercised by the passing tests; interpreter-based syntax passes.

S-026 artifacts were not rewritten, rebound, migrated, resumed or retried.
Their failed live acceptance remains historical, not superseded by offline
tests. The managed v3 prompt and schemas are unchanged. A fresh bounded live
framework case is the one proposed next activity, requiring separate consent.
No new inference or successful live migration is claimed.

## A-018 - S-027 Revision 2 Evidence Separation and Legacy Retirement

* Date: 2026-11-03
* Authority: user's 17:02 +01:00 local correction request and Q-028's explicit
  historical/current choice plus obsolete-code deletion request
* Status: local implementation verified; no further live validation claimed
* Scope: advisor evidence/persistence, retired local drivers, tests and docs

### Evidence Correction

The observed failure is reproduced by an offline test: read snapshot,
policy and comparison before execution, execute the exact human-approved
proposal, read its durable result, then include those unchanged earlier
facts alongside the current result. Before the fix it raises the same
`ungrounded_answer`; after the fix it completes with separate collections.

The [advisor](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
archives successful tool results when superseded or invalidated. Historical
facts persist with human decisions, using an empty default for older records;
this is not a source-hash migration or a means of reconstructing missing facts.
Python classifies the model's exact returned objects into `answer.evidence`
(current) and `answer.historical_evidence` (historical), leaving the message
unchanged. The model still returns exactly `message` and `evidence`.

Only actual locally recorded tool results can match either collection.
Changed or invented objects fail. A historical result cannot satisfy a
required current operation result or replace the mandatory post-write lookup.
Execution invalidates earlier comparison/read obligations as well as facts,
avoiding a stale comparison requirement after that comparison has been
removed from the current cache. This does not prescribe a reasoning workflow.

Regression checks cover authentic history with current read-back, modified
history, omission of the current result, refreshed snapshots, durable history
restoration and older records without invented history. Existing forged
approval, wrong ID, rejection, stale facts, duplicate execution and interrupted
write checks remain. Free-text correctness is not semantically certified.

### Retired Executable Paths

After confirming no active advisor/session import depends on them, removed:

* Historical read-only adapter `supply_chain/foundry.py` and `foundry_demo.py`
* Historical staged adapter `supply_chain/walkthrough.py` and `walkthrough_demo.py`
* Their retired-path suites `tests/foundry_adapter_tests.py` and
  `tests/walkthrough_tests.py`
* Legacy definition factories/profile generation and the unused shared-runtime
  result hook/called-tool accumulator

Useful SDK response fixtures and transport/usage/batch/call-ID/error checks
now live in [runtime tests](../../../../src/supply-chain-resilience/tests/runtime_tests.py)
against the current advisor. Cloud binding/version reuse guards are covered
in [advisor tests](../../../../src/supply-chain-resilience/tests/advisor_tests.py),
with mocked clients only. This avoids preserving a dead implementation just
to test shared safeguards. The SDK-free manual tool adapter, business
capabilities, explicit historical prompt assets and actual run evidence remain.
Historical links below now identify retired source paths instead of linking
to nonexistent files; their original outcomes and decisions remain unchanged.

Validation:

* The failing reproduction passed after the correction
* All 95 combined tests passed in 4.095 seconds; the lower total reflects
  retirement of obsolete driver-specific tests, not removal of active guards
* Pylance reports all eight current definition-factory call sites compatible;
  advisor diagnostics contain no items
* All 34 SDK-free tests passed independently in 2.313 seconds
* All ten documentary/link checks passed; retired implementation references
  no longer create broken links
* Changed application Python files have no syntax errors; no remaining
  Python references to the retired adapters/factories/hooks were found
* Current and historical prompt/schema/definition hashes still pass their
  existing regression assertions; no new publication is needed solely for
  this local adapter change

S-026 remains a failed historical live acceptance with one completed synthetic
reservation. Its session, stop flag, counters, source hash, database, events
and cloud version were not rewritten or retried. A new live case using the
unchanged v3 definition requires separate operational authorization.
Read-only inspection confirmed original 14/11/48,338 counters, source binding,
one request and 80/70/10 stock; session, SQLite and trace bytes were unchanged
by that inspection. The published definition fingerprint remains
`46e916cf4ce54c524d41472d24e506d83d26eea91c9b1d001623502fed254da2`.
No authenticated Azure access, inference, installation, commit or push occurred.

## A-017 - S-026 Live Agent-Led Validation

* Date: 2026-11-03
* Status: blocked at final-answer acceptance; live attempt ended and
  operational authority consumed. No automatic retry or rollback.
* Authority: Q-024 publication and bounded live case; Q-025 STANDARD choice;
  Q-026 revision 2 allowance/local correction; independent Q-027 exact approval
* Target: existing project/deployment, same agent version 3 and conversation
* No new provisioning, IAM, prompt change, telemetry export, commit or push

Version 3 was published and its complete definition read back before inference.
The first natural-language turn used snapshot/policy/comparison, then asked
for a preference: four requests, three tools, 6,104 tokens, no effects.
After Q-025's trusted STANDARD selection, a second conversational message
caused a fresh read of those three tools, proposal creation and a stop for
approval. No fixed propose-stage model command was used.

The exact proposal is `bf144275-ec8f-4ad3-bdd2-b63b9ff4616f`: STANDARD,
40 BOARD-1 W-B to W-A, cost 90, arrival 2/completion 3, snapshot 1/P-1:1.
At the pause, 9 requests/7 tools/22,345 tokens had been consumed,
conservative estimate EUR 0.4469. Independent local inspection confirmed
fully reconciled usage, `running=false`, no request, unapproved proposal
and stock 80/30/50 at W-B, 20 at W-A.

Q-026 explicitly extended the same run to 20 cumulative requests, not twenty
additional requests. Historical `RunLimits` still defaults/caps at ten;
the advisor subclass permits twenty while its session defaults to ten.
The allowance is persisted and restored. Initial CLI setup accepts explicit
10/20; it never changes an existing session's allowance automatically.
All 101 tests passed in 3.849 seconds, including actual twenty-versus-
twenty-first simulated request enforcement, legacy cap rejection and
restoration retaining nine requests and seen call IDs.

The authorized local-source transition changes only this clean session's
source fingerprint and allowance, with all bindings, usage, decisions and
seen call IDs retained. It is not an automatic migration or a means of
clearing uncertain operations. All other drift checks remain in force:

* Old source: `d87f70f707ec149ea0909ce73c18874c9e2dc14d35af6c2e2e60d23809667e9b`
* New source: `ff5fc9ca7047961e84904b7355cc8166fe50ec9a9389522396bd3ee78ab26f14`
* Instructions/schema/full cloud definition remain unchanged

Q-027 independently approves the exact proposal, not a future proposal,
shipment or receipt. Human-path approval and agent-requested execution/
read-back were the next authorized actions at that checkpoint.

### Actual Action and Final-Answer Failure

The human-only CLI recorded approval before model continuation; trace event
34 is `human.approved`, preceding execution at event 45. The agent chose
snapshot, policy, execution, then durable-result read-back, without a fixed
application execution-stage command. Exactly one proposal and one request
exist. The request is `682a1ce9-1600-4e75-bae9-c0338df29f82`, bound to the
exact approved STANDARD proposal. Snapshot advanced to version 2:
W-B on-hand/reserved/available 80/70/10; W-A remains 20.
No shipping, receipt, purchasing or factory scheduling occurred.

The final model response was rejected with `ungrounded_answer`; CLI exit 1.
Read-only retrieval of the existing response
`resp_09d5d47071f1bef3006aea038f03f48190b00355a300d6214c` and bounded
conversation-item inspection required no additional model inference.
All three evidence objects match actual earlier function outputs exactly:
pre-write snapshot 1, policy, and the correct post-write durable result.
The prose describes the reservation and before/after values accurately.
The failure is therefore a temporal evidence-contract mismatch, not observed
fabricated tool data or failed execution: the application invalidates cached
read results after a write, while the model also copied those historical
facts into its final evidence. This does not justify accepting stale facts
as current state or disabling the guard.

Separate-process reconciliation verified:

* One proposal/request, correct IDs, source 80/70/10, destination 20
* Human approval precedes the single execution; subsequent result read-back
* All eleven tool starts/completions have matched unique call IDs
* All 53 local events share run/conversation correlation and contain no raw
  prompts, arguments, model text or tool-result payloads
* Fourteen model requests, eleven tools; 45,189 input + 3,149 output =
  48,338 tokens, estimate EUR 0.96676, not invoice
* Usage reconciled; `running=true` retained as the failed-turn stop flag,
  not evidence of an active process. No flags cleared or write retried.

The 101 offline tests passed; all ten documentary/link checks and changed
application Python syntax checks passed before closure. These checks do
not turn the failed live final-answer contract into a successful test.
No new version, prompt change or recovery operation was performed to mask it.
The next proposed local increment is to correct the historical/current
evidence handoff with regression coverage; any publication and further live
case require a separate operational contract.

## A-016 - S-025 Revision 1 Multi-Agent-Ready Source Layout

* Date: 2026-11-03
* Authority: Q-023 explicitly approved the local reorganization, with the
  clarification that tools can be agent-specific or shared.
* Status: completed; local approval consumed
* Scope: source ownership/imports/assets/provenance/tests/documentation only

The [resilience advisor package](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor)
now owns its definition, conversational controls, prompts and six tool
contracts/dispatcher. Its
[evaluation cases](../../../../src/supply-chain-resilience/evals/resilience_advisor/cases.json)
are grouped by agent. Package initializers do not eagerly load the SDK.
The [root package](../../../../src/supply-chain-resilience/supply_chain/__init__.py)
retains SDK-free tool convenience exports for existing callers.

The [shared runtime](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
depends only on a small structural `FunctionDispatcher` protocol, not the
advisor or a concrete business tool session. Agent-specific approval handlers
and historical baseline adapters explicitly retain their business store/actor.
Domain rules, store transactions and solution data are reused without copying.
No shared-tool directory is invented before actual reuse; a later agent can
own different schemas/permissions or reuse an extracted common capability.
The application session/CLI still explicitly binds the single advisor.

All imports, asset paths, applicable historical links and README were updated.
Source hashing now includes nested agent Python modules, rather than only
root-level package files. Existing candidate source hashes are not rewritten
or silently migrated; drift still blocks continuation while local inspection
remains available. No persisted run artifacts were changed.

Validation:

* All 99 combined tests passed in 3.946 seconds: the previous 96 and three
  additional source-layout/decoupling regression tests
* All 34 SDK-free tests passed independently
* All 10 repository documentary/link checks passed
* Captured pre-move candidate instruction, tool-schema and full-definition
  hashes match after relocation; exact historical v1/v2 instruction hashes
  also still match
* A simulated nested tool-source change changes source provenance and
  triggers `candidate_drift`; no actual source modification is used by the test
* A dispatcher without advisor/store members works with the shared runtime
* Pylance conversation diagnostics returned no items; runtime diagnostics
  contain only unused-parameter hints in its pre-existing extension hooks

This is multi-agent-ready organization, not multi-agent orchestration,
delegation or identity isolation. Only the original advisor exists.
No prompt behavior, schema, dependency, cloud definition, tenant context,
inference, telemetry export, commit or push changed.
The next proposed activity remains separately authorized candidate publication
and bounded live conversational validation; it was not started.

## A-015 - S-024 Revision 1 Agent-Led Local Candidate

* Date: 2026-11-03
* Authority: user's 16:22 +01:00 "procedi" confirms the single local
  increment presented after S-023. This is free-form consent, not an
  invented native-form answer or new cloud approval.
* Status: local implementation verified; no publication or inference
* Accepted direction: D-013, RQ-011...RQ-014, existing Python/managed-agent
  choice and unchanged synthetic stock/approval invariants

### Implemented Boundaries

* [Agent definitions](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/definition.py)
  load explicit text instructions and bind tools/model. No deployment logic.
* [Advisor instructions](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/prompts/advisor.txt)
  cover investigation, uncertainty, planner preference, external approval,
  failure/reconciliation, language and exact-evidence output.
* [Generic runtime](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
  owns Responses continuation, call IDs, usage/limits and metadata events.
  Supply-chain instructions and required read-tool sequences are absent.
* [Conversation](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
  accepts arbitrary planner messages; guards capabilities using trusted human
  decisions, not comparison/proposal/execution reasoning phases.
* [Candidate session](../../../../src/supply-chain-resilience/supply_chain/session.py)
  persists decisions, synthetic evidence, seen call IDs, usage and asset
  references. Exclusive locking and checkpoint-before-request semantics
  block blind retries after interrupted/failed turns.
* [Candidate CLI](../../../../src/supply-chain-resilience/advisor_demo.py)
  provides local definition/init/inspect/select/approve/reject commands and
  a future guarded chat path. It contains no agent publication command.
  Chat verifies the full latest definition/version before opening the
  Responses client; historical cloud v2 is not a matching candidate.
* [Scenario](../../../../src/supply-chain-resilience/data/scenario.json)
  and [loader](../../../../src/supply-chain-resilience/supply_chain/data.py)
  separate versioned initial snapshot facts from code. The small fixed
  product/order/cost model remains explicit in the existing domain module;
  no ERP abstraction, alternate data service or ORM was introduced.
* [Evaluation asset](../../../../src/supply-chain-resilience/evals/resilience_advisor/cases.json)
  defines ten synthetic scenarios/rubrics, not measured model outcomes.
* [README](../../../../src/supply-chain-resilience/README.md)
  distinguishes the unpublished candidate from real historical baseline
  evidence and explains local preparation versus future authorized chat.

The existing tool schemas, business arithmetic, SQLite transactions and
human-only approval store were reused. The historical fixed-flow drivers
remain available and their sessions are not migrated.
The read-only and walkthrough instruction assets exactly preserve committed
v1/v2 content: regression SHA-256 values were independently derived from
the committed source and match the extracted files.
No `.replace` construction of workflow instructions remains.

### GenAIOps and Provenance

The stable candidate instruction path is tracked as source, without copied
numbered candidate files or a templating dependency. Candidate state records
instruction/schema/definition hashes, source-content hash, exact SDK versions,
scenario/evaluation hashes and actual remote bindings only when verified.
These content references are not a clean-commit claim, signed release or
fabricated Foundry version. Model deployment is configuration; resolved
model version and publication evidence await an authorized cloud step.

Any detected code/prompt/schema/scenario/evaluation/SDK drift blocks
resumption rather than silently changing the running candidate. Prompt
changes in the portal do not synchronize into Git. The existing latest-version
guard remains; no historical-version routing or automatic rollback is claimed.

### Validation and Limits

The combined suite passed 96 tests, including 26 new offline candidate tests
and all 70 historical tests. The 34 SDK-free business tests independently
passed with terminal Python. `pip check` found no broken requirements.
All 10 documentary/link checks passed.

Candidate cases use real SDK Response objects and real local SQLite effects
with a simulated model. They verify:

* Multiple read-tool orders, partial investigation and tool-free clarification
* Explicit human selection, exact proposal/approval and rejection without writes
* Forbidden self-approval, wrong IDs/options and stale facts
* Exact evidence preservation, mandatory read-back after execution, and a
  pre-execution result read not satisfying post-execution confirmation
* One effect for duplicate execution and persistent reconciliation after
  a lost response, without another model request
* Shared budgets, restored call IDs, metadata-only trace correlation, command
  locking, version-format rejection, prompt/schema/SDK drift and no overwrite
* No Azure authentication from local commands and no Responses client opened
  when the existing cloud definition does not match the candidate

Pylance syntax checks passed for conversation, session and CLI. Initial syntax
tool calls required an explicit workspace root; after supplying it, all three
checks passed. Editor diagnostics reported `reportMissingImports` for Azure
Projects imports in agent/CLI while execution/imports succeeded in the pinned
application-local environment. No editor-interpreter setting was changed and
no fully clean strict workspace type-check is claimed.

Free-text message correctness is not certified by JSON/evidence validation.
No live candidate conversation, model-quality score, optimizer, cloud
evaluation, new agent version/conversation or telemetry export was run.
Trusted local files/demo roles are not a production authorization boundary.
One proposal is allowed per candidate session; rejection does not silently
create a replacement proposal. The existing completed S-022 artifacts were
not reset, migrated or removed.
No dependencies, environment configuration, cloud resources, IAM, APIs/MCP,
harness/hosted runtime, Git commits or pushes changed.

The next proposed activity is bounded candidate publication and live
conversational validation; operational targets/limits and business approval
must be confirmed separately. Local S-024 implementation consent is consumed.

## A-014 - S-022 Revision 1 Complete Human-Gated Walkthrough

* Date: 2026-11-03
* Authorization: Q-020 explicitly approved implementation, one workflow version,
  one live synthetic case and local metadata-only tracing. Q-021 selected
  EXPRESS only for this case. Q-022 separately approved the exact proposal
  and synthetic reservation. No answer inferred from implementation consent.
* Status: completed; live and local acceptance verified, authorization consumed
* Identity: `supply-chain-resilience-advisor`, workflow version `2`, same
  existing project and `gpt-6.1-sol` deployment. Read-only version `1` retained.
* Conversation: `conv_0492c8bfd1d8311400NkVZtm61THqvWjwXjqoRmDf8V11OUHvm`
* Run correlation ID: `fff4d313-f9d5-4e46-ab47-853b65cb7ae1`
* Proposal: `4113e1b5-55a0-4137-b1e3-4d5481adcf3b`
* Durable request: `6c0fdd7f-66c1-4a08-906e-c8fef52a82ed`

### Implemented Surfaces

The paths below describe the S-022 implementation at that time. The old
drivers were retired in S-027; shared safeguards now live in the
[current runtime](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
and current advisor tests.

* Shared loop (`supply_chain/foundry.py`, retired):
  reuse of request accounting, call-ID continuation, batch validation and
  explicit-error behavior; optional metadata-only event callback
* Workflow stages (`supply_chain/walkthrough.py`, retired):
  human-selected option and exact approved proposal checks independent of
  model instructions; no model approval tool
* Staged CLI (`walkthrough_demo.py`, retired):
  durable session and SQLite state, atomic session-file replacement,
  exclusive command lock, persistent shared usage and uncertainty flags
* Workflow tests (`tests/walkthrough_tests.py`, retired):
  success, rejection without reservation, early execution/self-approval
  rejection, wrong IDs/options, duplicate proposal prevention, shared budgets,
  state/trace restoration and confirmation/uncertainty guards
* Baseline CLI (`foundry_demo.py`, retired):
  explicitly rejects a different latest named-endpoint version rather than
  silently invoking the new workflow definition as read-only v1
* Adapter regression tests (`tests/foundry_adapter_tests.py`, retired)
  and [README](../../../../src/supply-chain-resilience/README.md) updated

No new dependency, framework, MCP/API server, workflow engine, cloud
infrastructure, IAM mutation, hosted runtime or Copilot harness was added.
The active named endpoint now uses the workflow version; local dispatch
still enforces current-stage tool permissions.

### Actual Live Evidence

The same retained conversation completed three model stages:

| Stage | Cumulative model requests | Cumulative tool calls | Cumulative tokens |
| ----- | ------------------------- | --------------------- | ----------------- |
| Comparison | 4 | 3 | 3,658 |
| EXPRESS proposal | 6 | 4 | 6,865 |
| Human-approved execution and read-back | 9 | 6 | 13,738 |

Final reported usage is 12,919 input and 819 output tokens, with no
unreconciled request. Conservative application model-cost estimate is
EUR 0.27476, not actual invoiced cost. All configured bounds/monitoring
thresholds stayed clear; no automatic retries.

The model created the selected EXPRESS proposal through its function tool:
40 BOARD-1 from W-B to W-A, cost 95, arrival day 1, completion day 2.
Before approval the source remained reserved 30. The user asked for
clarification rather than selecting in the first form; the process paused,
clarified one-case semantics and waited for explicit EXPRESS selection.
The subsequent exact-proposal approval was recorded outside the model.
The model then called execution and durable-result lookup, returning exact
authoritative tool JSON rather than an invented successful action.

A separate CLI `result` process confirmed snapshot version 2, source on-hand
80, reserved 70, available 10 and destination on-hand 20. SQL inspection found
exactly one proposal and one request. No shipment or receipt was claimed.

Durable local session:
`artifacts/local/supply-chain-s022` (ignored by Git, deliberately retained).
The metadata-only JSONL trace contains 36 events: nine model start/end pairs,
six function start/end pairs, and six lifecycle events.
Verified matching unique function call IDs, consistent run/conversation IDs,
durations, and `human.approved` before `execution.started`.
The lifecycle is comparison ready, planner selected, proposal ready,
human approved, execution started, execution completed.
No prompts, function arguments, tool results, model text or credentials
are recorded in these trace events. This is not a distributed OpenTelemetry
trace or Azure Monitor export.

### Validation and Limits

The initial combined implementation run passed all 67 tests before the live
case. The final combined suite passed **70 tests in 4.338 seconds**, including
the latest-version regression and preparation reuse/conflict checks.
`pip check` reported no broken requirements. All **10 repository documentary
and link checks** passed. Preparation reuses a matching workflow version for
a separately authorized fresh session rather than producing duplicate
versions; unrelated definitions are never silently overwritten. No second
live session was started to validate this offline-tested reuse path.
Editor problem checks on the shared loop, workflow and staged CLI returned
no errors; this is not a claim of a separately configured strict type check.

Negative/rejection/idempotence cases are offline evidence; only the approved
positive EXPRESS case ran live. Demo actors and trusted local state files
are not real multi-user identity enforcement. One pending synthetic transfer
is requested/reserved, not physically shipped. The session is completed and
retained for inspection; no reset, cancellation or further inference is implied.
No resource deletion, real data, telemetry export, paid evaluation, commit
or push occurred.

The approved S-022 increment and this exact synthetic business approval are
consumed. No further model calls or resource changes are authorized by
completion. A proposed next activity is a user-led demonstration/review of
the completed flow; Copilot harness study remains a separate future topic.

## A-013 - S-020 Revision 2 Successful Live Read-Only Case

* Date: 2026-11-03
* Authorization: Q-019 native confirmation returned true after the explicit
  revised target, limits and post-response monitoring contract
* Status: completed; this single-run authorization is consumed
* Reused agent `supply-chain-resilience-advisor` version `1` and existing
  `gpt-6.1-sol`, model version `2026-09-29`, GlobalStandard, in the approved
  existing project. No agent/version creation or mutation.
* Created and retained conversation
  `conv_0c9bfd4440046b6b009z6TCANKGYxuSL8kTUa2qI506VmAhJxG`;
  no old conversation deletion or automatic cleanup.
* Live CLI exited 0 with `status: completed`. Real calls covered
  `read_planning_snapshot`, `read_transfer_policy` and
  `compare_transfer_options`. Function outputs continued the same conversation.
* Actual model-reported usage: four generation requests, three dispatched
  function calls, 2,577 input tokens, 420 output tokens, 2,997 total;
  no unreconciled usage.
* Application conservative model-cost estimate: EUR 0.05994, charging every
  reported token at the higher EUR 20/million estimate rate. Not an invoice
  or exact contracted price. All configured monitoring thresholds stayed clear.
* Returned structured options exactly matched authoritative tool output:
  quantity 40 for both; STANDARD cost 90, arrival day 2, completion day 3,
  margins C-1/C-2 of 0/1; EXPRESS cost 95, arrival day 1, completion day 2,
  margins 1/2. Both feasible under ceiling 100.
* Explanation inspection: correctly identified shortage 40, source available
  50 excluding unrelated reservations, supplier day 6 delay and the extra
  cost 5 for one extra margin day. It left selection to the planner and did
  not claim proposal creation, approval, execution or stock movement.
* `baseline_unchanged: true`: read-back snapshot equaled the initial synthetic
  baseline. Viewer actor and registered read-only tool subset were used.
  Temporary local database was removed by its context manager.
* No mandatory token-count endpoint, write tool, stock mutation, provisioning,
  IAM change, telemetry export, paid evaluation, dependency change or Git
  mutation. No automatic retries or additional test cases.
* Limitations: this proves one baseline live function-calling case, not live
  human approval/action, full tracing, negative-case cloud evaluation, real
  production authorization or universal SDK/model compatibility.
* Next proposed activity: the complete interactive planner-selection and
  human-approved action flow with trace visibility, under a separate bounded
  contract. Not started or authorized by this completed case.

## A-012 - Relaxing the Mandatory Token Pre-Count

* Date: 2026-11-03
* Authorization: user's explicit 15:09 request to relax the prerequisite;
  no new cloud operation or unlimited spending inferred
* Status: completed, local implementation and validation only
* Removed `responses.input_tokens.count` from the request path; no alternate
  route or guessed input count is substituted
* Preserved ten generation requests, twenty function calls, requested 4,096
  output tokens per response, no automatic retries and read-only tool access
* Aggregate 100,000 tokens and estimated EUR 10 are now monitoring thresholds
  checked against actual returned usage; a request can cross a threshold,
  at which point the loop stops. No hard pre-request budget guarantee.
* Missing/lost/invalid usage is explicitly unreconciled and cannot silently
  retry. Summary identifies `post_response_monitoring` enforcement.
* Updated adapter tests and README. All 56 combined Python tests passed in
  2.657 seconds. Tests include an unavailable counter that must never be
  called, actual-usage thresholds and uncertain-request reporting.
* No model call, conversation creation, cloud resource mutation, dependency
  installation, IAM change, commit or push occurred.
* Mandatory-pre-count blocker removed locally; a live function-loop result
  remains unverified. Earlier pre-count/reservation records are historical.

## A-011 - S-021 Revision 2 Meaningful Agent Identity

* Date: 2026-11-03
* Authorization: explicit Q-018 answer to change the name and delete the old
  agent; replacement creation/verification precedes deletion
* Status: completed; cloud result verified, local checks recorded below
* Target: same existing project as S-020; no subscription or IAM changes
* Created `supply-chain-resilience-advisor` version `1` using the previous
  version's exact prompt-agent definition; read-back equality verified
* Deleted only `supply-chain-readonly-847751e8dee6`, without force;
  response reported `deleted: true`, and subsequent lookup returned not-found
* Retained the historical conversation. No conversation creation, inference,
  tool dispatch, stock mutation, resource provisioning or other deletion
* Initial attempt failed before project access because Azure CLI was absent
  from the current process PATH. Verified its known installation and added
  that directory to the retry process PATH only; no global environment or
  login mutation.
* Updated the live CLI to get the explicit semantic name/version and verify
  its definition, never create random agent identities. Added a mocked CLI
  reuse regression test and updated README.
* Authorization consumed: yes. S-020 remains blocked by token-count HTTP 405;
  this naming change does not authorize an inference retry.
* Portal clarification: function specifications are server-side, Python
  implementations remain local; portal chat alone cannot execute them.
* Validation: all 56 combined Python tests passed in 2.895 seconds and all
  10 documentary/link checks passed. The new mocked CLI test initially failed
  because its conversation ID fixture was a mock rather than a string;
  corrected that fixture and reran the full Python suite successfully.

The local business milestone is completed. S-020 subsequently implemented
the SDK adapter, passed offline tests, verified the existing deployment and
created one real agent/version and conversation. The live function loop is
blocked before inference by the service's token-count HTTP 405, as recorded
in A-010. No completed real-agent comparison or trace is claimed.

## A-010 - S-020 Revision 1 Preflight Blocker

* Date: 2026-11-02
* Status: blocked before inference; not completed. The initial identity
  blocker was resolved; the latest blocker is the token-count API's HTTP 405.
* Authorization: explicit Q-015 approval of S-020 revision 1, targeting only
  Q-014's existing project and deployment, with ten model requests, twenty
  function calls, 100,000 aggregate input/output tokens and a 10 EUR ceiling
* Actual local actions: created
  [requirements-foundry.txt](../../../../src/supply-chain-resilience/requirements-foundry.txt),
  created the application-local ignored `.venv`, and installed the declared
  SDK dependencies there; no global installation or shell login change
* Installed runtime facts: `azure-ai-projects` 2.10.0, `azure-identity` 1.27.0,
  `openai` 3.38.0 on Python 3.12.10. This is not a successful live compatibility
  certification or a full dependency lock.
* Auth check: existing Azure CLI account reported enabled. No token, key,
  account dump or credential was recorded.
* Read-only project action: `AIProjectClient` with existing
  `AzureCliCredential` attempted `project.deployments.list()` against the
  exact approved endpoint. The service returned a tenant-mismatch error.
  No deployment metadata was successfully obtained.
* Outcome: stopped at the authentication blocker. No agent/version,
  conversation, inference, model deployment, IAM change, stock mutation,
  telemetry export, deletion or Git operation occurred.
* Code/tests: no Foundry adapter or new adapter tests created yet. Existing
  local business code was not changed; its previous 34-test result remains
  historical, not a new S-020 validation run.
* Pricing limitation: the public pricing page confirms deployment-type and
  model distinctions, but the directly retrieved table contains price
  placeholders. Search snippets are not sufficient evidence for this actual
  deployment's EUR rate. No safe cost estimate is certified.
* Recovery: Q-016 requests the correct existing directory/CLI context and
  explicit same-target retry. No automatic account switching or tenant
  enumeration. The local virtual environment is retained, not deleted.
* Authorization state: no further cloud action until the authentication
  blocker is resolved and continuation reconfirmed; Q-015's approved scope
  and limits do not expand.

Commands executed:

```powershell
python -m venv src\supply-chain-resilience\.venv
src\supply-chain-resilience\.venv\Scripts\python.exe -m pip install -r src\supply-chain-resilience\requirements-foundry.txt
az account show --query "{state:state}" --output json --only-show-errors
```

SDK introspection verified the installed `FunctionTool`,
`PromptAgentDefinition`, `create_version` and `get_openai_client` interfaces.
It did not create an agent. The lookup failure prevents determining the
underlying model/version, deployment type, region, actual price or quota.

### A-010 Interrupted Tenant Retry

Q-016 supplied an explicit directory identifier and authorized retrying the
same project's read-only metadata lookup. That value was passed explicitly
to `AzureCliCredential`, without modifying the global login/account state.
The ten-second credential subprocess timeout expired before metadata could
be read. A same-context retry with a sixty-second credential timeout was
interrupted. At 17:39 +01:00 the user challenged the tenant selection.

All further cloud activity stopped. A subsequent process-session check
reported no active PowerShell sessions. No successful deployment metadata,
agent/version, conversation or inference is claimed. Q-017 preserves the
dispute and requests clarification; Q-016 is not treated as continuing
authorization to retry the disputed directory.

The user subsequently confirmed the same directory value and specified the
intended account. Comparing only the cached CLI account with those inputs
returned false for both tenant and user equality, with the account enabled.
Only Boolean comparison results are retained; the personal account name is
not stored. No Foundry request or global authentication change occurred.
The active blocker is correction of the CLI user/directory context, followed
by explicit continuation within the unchanged S-020 limits.

### A-010 Corrected Preflight and Adapter Preparation

The user confirmed completing the corrected login and explicitly authorized
resuming S-020 with the same limits. Cached CLI identity equality checks then
passed, and the exact deployment lookup succeeded: `gpt-6.1-sol`,
version `2026-09-29`, publisher OpenAI, SKU `GlobalStandard`, capacity 100.
No global login state was changed by the assistant.

Added SDK adapter `supply_chain/foundry.py`, live CLI `foundry_demo.py` and
offline SDK tests `tests/foundry_adapter_tests.py` (these historical paths
were subsequently retired in S-027; current runtime checks were retained).
Pinned direct dependencies to installed Projects 2.10.0, Identity 1.27.0 and
OpenAI 3.38.0. SDK imports remain outside the business package's normal imports.

The first SDK-test run failed because the installed response model requires
`cache_write_tokens` in its usage details; the offline fixture was corrected.
Then all 21 SDK tests passed. The 34 SDK-free business/CLI tests also passed.
This is offline adapter evidence, not live function-calling success.

Direct official pricing HTML and ECB exchange-rate evidence now support
conservative model estimate rates of EUR 5 input and EUR 20 output per
million, covering both published context tiers. At 100,000 total tokens,
charging all tokens at the higher rate estimates at most EUR 2 before
account-specific billing differences, within the EUR 10 approved allowance.
See the [source evidence](../research/evidence.md#s-020-fresh-source-check-and-preflight-boundary).
This does not certify negotiated prices or an instant billing cutoff.
Creation of the one demo agent/version and conversation and the bounded
live test are next within the reconfirmed existing contract; no result is
claimed before execution.

### A-010 Live Attempt and Token-Count Blocker

The final combined offline suite passed **55 tests** in 2.954 seconds, and
`pip check` reported no broken requirements. The existing SDK-free suite
also passed independently with terminal Python. No static type checker or
Pylance diagnostics were run.

After confirming corrected-login consent, exact deployment metadata and
conservative prices, the one authorized run used the explicit project,
deployment and tenant context. The service created:

* Agent name: `supply-chain-readonly-847751e8dee6`
* Agent version: `1`
* Conversation: `conv_03047129d38afdfd00nbRimtiK1xgyUhPZ5EMSGamwMdOV8jlb`

The agent definition contains only snapshot, policy and comparison functions.
No proposal, approval or transfer-action function was registered for this slice.
The agent/version and conversation were intentionally retained, as cleanup
was excluded from the approval.

The first `responses.input_tokens.count` returned HTTP 405. The explicit-error
path stopped the run before `responses.create`. Observed counters:

| Counter | Observed value |
| ------- | -------------- |
| Generation requests | 0 |
| Function dispatches | 0 |
| Reported model input/output tokens | 0 / 0 |
| Unreconciled generation reservations | 0 |
| Application model-cost estimate | EUR 0 |

These are execution counters, not a statement from Azure billing.
No stock mutation or model/tool result occurred. Temporary local stores were
removed by their owning context manager. No default demo database was reset.
No retries or additional agents/conversations were started after this error.

The installed client exposes token counting, but that does not prove service
support on this project's route. Do not disable the guard or quietly replace
it with a token guess. Live inference, real call-ID continuation and final
business-answer acceptance remain unverified.

Authorization is suspended at this compatibility error; resource deletion,
duplicate creation and another live attempt are not automatically authorized.
The proposed next activity is a bounded compatibility correction for counting
tokens and resuming the existing agent/conversation, with a revised contract
if the enforcement approach changes. It has not started.

Final documentary validation: all 10
`node --test scripts\test-copilot-customizations.mjs` checks passed,
including metadata, local links and anchors. S-020 remains blocked despite
the passing local checks; no successful live function loop is claimed.

## A-009 - S-019 Revision 2

* Authorization: the user's explicit 2026-11-02 16:59 +01:00 implementation
  request after the Q-013 pause and clarification. The
  [question history](../questions.md#q-013-clarification-followed-by-implementation-consent)
  records the actual scope; the earlier paused form is not consent.
* Organization constraint: at 17:06 +01:00 the user requested well-organized
  code from the outset without overengineering (faithful English translation).
  This refined the authorized local implementation, not its cloud boundary.
* Status: completed; runtime and documentary criteria verified.
* Runtime: terminal Python 3.12.10 and SQLite 3.49.1. No dependency installation,
  environment change or editor-interpreter claim.
* Authorization consumed: yes. No subsequent implementation or cloud activity
  is authorized by this completed increment.

### Actual Files and Organization

The [application directory](../../../../src/supply-chain-resilience) contains
one small package and a manual CLI adapter. A future SDK driver is deliberately
not implemented. Package responsibilities are:

| File | Implemented responsibility |
| ---- | -------------------------- |
| [domain.py](../../../../src/supply-chain-resilience/supply_chain/domain.py) | Synthetic snapshot, local actor fixtures, shared feasibility/cost/margin rules |
| [store.py](../../../../src/supply-chain-resilience/supply_chain/store.py) | SQLite schema, transactions, exact-proposal approval, durable request and reservation |
| [tools.py](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/tools.py) | Six strict JSON function specifications and explicit-error dispatcher |
| [package exports](../../../../src/supply-chain-resilience/supply_chain/__init__.py) | Stable entry points shared by callers |
| [demo.py](../../../../src/supply-chain-resilience/demo.py) | Thin manual CLI; demo role selection is not authentication |
| [domain tests](../../../../src/supply-chain-resilience/tests/test_domain.py) | Pure scenario arithmetic and fixture validation |
| [workflow tests](../../../../src/supply-chain-resilience/tests/test_workflow.py) | Approval, persistence, dispatch, concurrent/failed/repeated requests and CLI |
| [test package](../../../../src/supply-chain-resilience/tests/__init__.py) | Root-level standard-library test discovery |
| [README](../../../../src/supply-chain-resilience/README.md) | Tested commands, synthetic scenario, boundaries and future function-calling exposure |
| [local ignore rules](../../../../src/supply-chain-resilience/.gitignore) | Exclude local SQLite files and journals |

The initial single module was split without changing tool names, argument
contracts, CLI commands or scenario values. No HTTP/MCP server, framework,
repository interface, container, workflow engine or production identity layer
was added. Business calculations are shared by comparison and write checks.
The dispatcher returns explicit errors for corrupt stored outcomes rather
than reporting success or silently substituting data.
Related state, question history, analysis and plan version 2 were updated.

### Commands and Observed Results

From the repository root:

```powershell
python -B -m unittest discover -s src\supply-chain-resilience -p "test_*.py" -v
```

Final runtime run: **34 tests passed in 4.095 seconds**, exit code 0.
Earlier runs passed 32 tests before the module split and 33 afterwards;
the final run includes the durable subprocess CLI walkthrough.

Verified acceptance:

* Exact transfer quantity 40, STANDARD 90 and EXPRESS 95, ceiling equality
  and schedule margins 0/1 versus 1/2.
* No-impact, unavailable stock, missing policy and infeasible budget outcomes.
  No invented policy defaults or automatic option selection.
* Strict model arguments; caller-owned actor context; no approval tool.
  Missing, stale, changed or mismatched approval prevents execution.
* Approval/proposal creation does not reserve stock. One successful request
  leaves source on-hand/reserved/available at 80/70/10 and W-A at 20.
* Twelve concurrent requests for the same proposal produce one durable
  request and eleven idempotent repeats. Stock is reserved once.
* Failed request insertion rolls back the reservation. Corrupt stored JSON
  and invalid recorded outcomes return explicit errors, not successful fallbacks.
* Independent CLI processes initialize a temporary database, compare both
  costs, propose, reject execution before approval, require explicit approval
  confirmation, execute, repeat idempotently and retrieve the persistent result.
  A subsequent comparison reports the existing pending transfer.
* Initialization cannot overwrite an existing store; missing stores are not
  silently created on read. Temporary test databases are cleaned by the tests.

Repository documentary/link validation:

```powershell
node --test scripts\test-copilot-customizations.mjs
```

All **10 tests passed**, exit code 0, including Markdown metadata, local links
and anchors. Python imports and execution were exercised; no static type
checker or Pylance diagnostics were run.

### Limitations and Next Point

This is a reusable local business-tool increment, **not a live Foundry demo**.
The JSON definitions have not been instantiated with or validated against a
Foundry SDK. No live function call IDs, conversation continuation, model-loop
limits, real authentication, traces or cloud evaluation have been verified.
Role fixtures and fingerprints are not real IAM or tamper-resistant credentials.
No default demonstration database, Azure resource, API/MCP endpoint, Git commit
or push was created.

One proposed next activity: S-020 revision 1, connect these same functions to
the real managed Foundry prompt agent, after explicitly agreeing the target,
model, permissions and bounded call budget. Status: proposed; its operational
contract is not approved and it is not started. Provisioning, IAM changes
and cleanup remain outside the proposal.
