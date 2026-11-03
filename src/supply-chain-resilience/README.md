---
title: "Supply Chain Resilience Business Tools"
description: "Managed Foundry agent demo with Python function calling, human approval, durable synthetic state and local execution events."
ms.date: "2026-11-03"
---

## What Runs Today

The business functions run with Python's standard library and SQLite; the
manual walkthrough needs no extra packages. It exercises the same functions
as the optional managed Foundry adapter, not a local AI agent.

The optional adapter has been implemented and tested offline with the pinned
SDK dependencies. A real prompt-agent version and conversation were created
in the approved existing project. The previous live attempt stopped because
the service returned HTTP 405 for the SDK's pre-inference token-count endpoint.
On 2026-11-03 the user authorized removing that prerequisite; the driver now
monitors actual usage after each response and never calls that endpoint.
One authorized live read-only case subsequently passed: the agent called all
three fact tools and returned the exact options and trade-off explanation,
with unchanged baseline stock. It used four generation requests, three tool
calls and 2,997 reported tokens. This verifies the baseline read-only loop,
not by itself the complete human-approval/action demo.

The subsequent S-022 walkthrough also passed using the same agent's version
`2`: real comparison, human EXPRESS selection, proposal creation, separate
human approval, agent-requested reservation and durable-result read-back.
It used nine generation requests, six tool calls and 13,738 reported tokens.
The source ended at on-hand/reserved/available 80/70/10, destination 20.
One proposal/request and the order of the human approval were verified
against the durable store and 36 local trace events.
These are synthetic local effects, not real shipping or a production IAM test.

The current increment is tested with terminal Python 3.12.10 and SQLite 3.49.1.
It does not establish a supported version matrix for a future Foundry SDK.
The separate SDK environment uses Projects 2.10.0, Identity 1.27.0 and
OpenAI 3.38.0; see [requirements-foundry.txt](requirements-foundry.txt).

## Code Layout

| File | Responsibility |
| ---- | -------------- |
| [domain.py](supply_chain/domain.py) | Synthetic facts, demo actor fixtures, option costs, feasibility and delivery margins; no database or SDK |
| [store.py](supply_chain/store.py) | SQLite snapshots, proposals, human approval and atomic request/reservation |
| [tools.py](supply_chain/tools.py) | Function descriptions/JSON argument contracts and bounded dispatch |
| [demo.py](demo.py) | Thin manual terminal adapter |
| [foundry.py](supply_chain/foundry.py) | Optional SDK definition and bounded read-only function loop |
| [foundry_demo.py](foundry_demo.py) | Explicit-tenant preflight, one managed agent/conversation and read-only case |
| [walkthrough.py](supply_chain/walkthrough.py) | Reuses the bounded loop with application-enforced comparison, selection, approval and action stages |
| [walkthrough_demo.py](walkthrough_demo.py) | Staged CLI with durable local session, shared usage counters and metadata-only events |
| [test_domain.py](tests/test_domain.py) | Pure business-rule checks |
| [test_workflow.py](tests/test_workflow.py) | Persistence, dispatcher, approval, concurrency, failures and CLI checks |
| [foundry_adapter_tests.py](tests/foundry_adapter_tests.py) | Offline SDK objects, continuation IDs, read-only allowlist, limits and failure cases |
| [walkthrough_tests.py](tests/walkthrough_tests.py) | Complete staged flow, rejection, wrong IDs/options, shared budgets and trace persistence |

No web framework, generic repository layer, plugin system or workflow engine
is needed for this slice.

## How the Agent Will Use the Tools

The intended first integration is **Foundry function calling**, not HTTP or MCP:

1. The SDK adapter registers the definitions in `FUNCTION_TOOL_SPECS` on
   the named/versioned Foundry prompt agent.
2. Foundry returns a function request with its name, JSON arguments and call ID.
3. The Python driver calls `ToolSession.dispatch(name, arguments_json)`.
4. The driver serializes the result into the corresponding
   `function_call_output`, preserving the call ID and conversation.

The adapter creates SDK `FunctionTool` instances from the specifications
and registers a server-side `PromptAgentDefinition`. S-020's version `1`
exposes only snapshot, policy and comparison tools. S-022's version `2`
registers all six functions, but the application dispatcher allows only
the functions appropriate to the current stage.
The SDK adapter and call-ID loop have passed offline tests; real registration
succeeded. After removing the unsupported pre-count prerequisite with explicit
consent, one real model/function-output loop passed. The
[live evidence](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-013---s-020-revision-2-successful-live-read-only-case)
separates that baseline result from offline response fixtures; the
[complete walkthrough evidence](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-014---s-022-revision-1-complete-human-gated-walkthrough)
records the subsequent approved action.
See the [verified technical evidence](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#e-08---managed-prompt-agent-and-python-tool-execution).

| Model-invocable function | Result |
| ------------------------ | ------ |
| `read_planning_snapshot` | Current synthetic stock, commitments, receipt delay and snapshot version |
| `read_transfer_policy` | Versioned policy, cost ceiling and explicit assumptions |
| `compare_transfer_options` | Both options with exact costs/margins and feasibility reasons, without choosing |
| `create_transfer_proposal` | Proposal for the explicitly selected option; no reservation yet |
| `execute_approved_transfer` | Guarded request and source reservation, only after human approval |
| `read_transfer_result` | Durable outcome for reconciliation and safe repeated requests |

`DemoStore.approve` is a separate **human-only** application path. It is not
in the model's tool list. Actor identity and approval are not model arguments.
The bounded driver enforces at most ten generation requests,
twenty function calls and a requested maximum of 4,096 output tokens per response;
SDK automatic retries are disabled. The 100,000 aggregate input/output token
and estimated EUR 10 thresholds are checked against reported usage after each
response and before the next request, not guaranteed before inference.
A request may cross either monitoring threshold; the loop then stops.
Missing or invalid usage, malformed tool arguments or a forbidden write tool
stop the loop explicitly. An uncertain generation request is marked
`usage_unreconciled`; its unknown cost is not claimed to be zero or estimated
as an exact reservation, and it is not retried.
The complete walkthrough shares those counters across all stages and process
invocations. Human approval is a separate local command, never a model tool.

An HTTP API or MCP adapter could reuse these same functions if sharing or
remote execution is later justified. Neither is required for this first path.

## Synthetic Scenario

Two commitments need 60 boards; W-A has 20. The delayed 40-board receipt on
day 6 cannot protect delivery days 3 and 4. W-B has 80 boards, of which 30
are reserved for unrelated work, leaving 50 available.

| Option | Transfer quantity | Cost | Arrival | Assembly complete | Margins to C-1 / C-2 |
| ------ | ----------------- | ---- | ------- | ----------------- | ------------------- |
| STANDARD | 40 | 90 | Day 2 | Day 3 | 0 / 1 days |
| EXPRESS | 40 | 95 | Day 1 | Day 2 | 1 / 2 days |

Both satisfy the cost ceiling of 100. The planner selects the trade-off:
five extra fictional cost units buy one extra day of schedule margin.
No probability of late delivery or uniquely optimal solution is claimed.
Other materials and production capacity are assumed sufficient.

## Manual Walkthrough

Run in PowerShell:

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
python -B demo.py execute $proposal.proposal_id
python -B demo.py snapshot
```

Inspect the proposal before using `--confirm`. The first execution reports
`requested`; the repeated execution reports `already_requested` with the same
request ID and no extra effect. Source on-hand remains 80, reserved becomes
70 and available becomes 10. W-A remains at 20: nothing has shipped or arrived.
A pending request prevents a second recovery proposal for this tiny scenario.

Initialization refuses to overwrite an existing database. To try a separate
scenario, select a new filename; there is no implicit reset or deletion command.

```powershell
python -B demo.py --db ceiling92.sqlite3 init --scenario ceiling-92
python -B demo.py --db ceiling92.sqlite3 compare
python -B demo.py tools
```

Other initial scenarios are `no-impact`, `insufficient-stock`, `ceiling-80`
and `missing-policy`. Without a valid option and exact human approval,
no transfer is created.

Errors are explicit JSON on stderr and a nonzero CLI exit. Tool dispatch
returns an explicit `status: error` with a reason code, never a successful
fallback for invalid input or database failure.

## Boundaries and Failure Behavior

* `--role` selects a local fixture, **not authentication**. Do not expose this
  CLI or database to untrusted clients or use it with real operational data.
  Future caller identity must come from verified runtime context.
* Approval binds all proposal fields and the underlying planning facts.
  Changed stock, policy, option or amount requires a new proposal/approval.
  Fingerprints detect stale/mismatched content; they are not credentials.
* Request creation and source reservation commit in one SQLite transaction.
  A failed insert rolls back stock changes. The proposal ID uniquely binds
  the operation, including concurrent repeats.
* After an uncertain return, read the durable result before repeating the
  same operation; never generate another proposal to bypass an uncertain write.
* SQLite is the local demo store, not an ERP/WMS or production authorization system.
  No cancellation, physical transfer, destination receipt or shared-data cleanup
  is implemented or implicitly permitted.
* Baseline and human-approved action cases passed. Local structured execution
  events are inspected; distributed OpenTelemetry/Azure Monitor tracing and
  cloud evaluations were not implemented or run.

## Optional Foundry Environment

The SDK is isolated from normal business-package imports. From the repository root:

```powershell
python -m venv src\supply-chain-resilience\.venv
src\supply-chain-resilience\.venv\Scripts\python.exe -m pip install -r src\supply-chain-resilience\requirements-foundry.txt
```

Configure `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT` and
`FOUNDRY_TENANT_ID` outside source control. The caller must be logged into
Azure CLI as the intended account in the project's actual directory.
An enabled default CLI account does not prove the user or tenant is correct.
The CLI uses that explicit directory with `AzureCliCredential`; it does not
silently try other credential sources or change your login.

The following is a read-only deployment check, not an inference test:

```powershell
src\supply-chain-resilience\.venv\Scripts\python.exe -B src\supply-chain-resilience\foundry_demo.py preflight
```

`run` reuses `supply-chain-resilience-advisor` version `1`, verifies that its
definition matches the local read-only configuration, and creates a conversation,
then uses an isolated temporary baseline database with a viewer actor.
It does not create an agent or a new version. `--agent-name` and
`--agent-version` explicitly select an existing compatible identity/version.
Because the named endpoint follows its active/latest version, the baseline
driver now also checks that the latest version matches the requested version.
After creation of workflow version `2`, it refuses to invoke that endpoint
while pretending it still executes read-only version `1`.
Use the staged walkthrough below for the current agent; no implicit downgrade
or mutation of the cloud definition is performed.
The historical random-suffixed agent was deleted at the user's request after
the replacement definition was verified; its old conversation was retained.
It requires positive conservative EUR input/output rates and a price-source
reference before any Azure client is opened. Do not use the offline test's
pricing fixture as a live tariff. Each invocation is a new run, not a resume
or a persistent cross-process budget; authorization does not cover arbitrary
repeats.

The SDK exposes `responses.input_tokens.count`, but this project's service
returned 405. The user explicitly relaxed the mandatory pre-count on
2026-11-03. No guessed token count or fallback route is substituted:
the driver relies on post-response usage monitoring instead. A subsequent
authorized baseline live function loop passed; the old 405 is historical,
not a remaining blocker on the current request path.
No automatic cleanup or duplicate agent creation is appropriate.
The portal cannot execute these local Python functions: the application must
dispatch the calls and return outputs. Portal-only execution would require
an appropriate remotely executable tool integration, not just function schemas.
Resource references and the observed failure are in the
[implementation log](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-010-live-attempt-and-token-count-blocker).

The configured conservative cost rates for the attempted case were EUR 5
input and EUR 20 output per million, derived with margin from both official
Global context-tier USD tables and the 2026-11-02 ECB reference rate.
The application charges all estimated tokens at the higher rate: 100,000
tokens estimate EUR 2, below EUR 10. These are not actual contracted tariffs,
tax calculations, an Azure spending cap or proof of billable usage.
See the [pricing evidence](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#s-020-fresh-source-check-and-preflight-boundary).

## Complete Human-Gated Walkthrough

The executed S-022 session is in `artifacts\local\supply-chain-s022` relative
to the repository root. This directory is ignored by Git and deliberately
retained for inspecting the result and local trace. Its synthetic SQLite
database is not shared with the manual demo's database.

Read the existing result without any model or Azure call:

```powershell
src\supply-chain-resilience\.venv\Scripts\python.exe -B src\supply-chain-resilience\walkthrough_demo.py result --directory artifacts\local\supply-chain-s022
```

For a separately authorized fresh demonstration, the CLI stages are:

1. `prepare`: select a **new** local directory; verify the existing deployment
   and agent, reuse the matching workflow version and create one conversation,
   initialize the synthetic store and record resource references.
   Never rerun it to bypass or reset an existing session. If the workflow
   definition is already present, no new agent version is created. If the
   active version is still the known baseline, the authorized initial upgrade
   creates the workflow version. Any unrelated definition causes an error
   rather than being silently overwritten.
2. `compare`: agent reads the three fact tools and explains both alternatives.
3. `propose --option STANDARD|EXPRESS`: record the planner's one-case choice;
   the application permits creation of one proposal for that exact option.
4. Inspect the proposal. `approve --proposal-id ID --confirm` records
   human-only approval. Alternatively, `reject --proposal-id ID` closes
   the session without reserving stock.
5. `execute`: only after durable human approval, the agent may execute that
   exact proposal ID and read the authoritative outcome.
6. `result`: locally inspect durable state and usage, including after an
   interrupted or uncertain response. This command never retries a write.

Each command requires `--directory PATH`. Approval alone does not call the
model or execute a reservation. The CLI uses demo actor fixtures, not real
authentication for the planner/approver. Do not treat trusted local session
files as an untrusted multi-user authorization boundary.
Selection is not a permanent STANDARD/EXPRESS preference or policy change.

Files in the session directory:

| File | Purpose |
| ---- | ------- |
| `planning.sqlite3` | Durable snapshot, exact proposal/approval and idempotent request |
| `session.json` | Safe resource references, stage, synthetic artifacts, used call IDs and aggregate usage |
| `events.jsonl` | Local event trace: correlation IDs, stage, tool names, response/call IDs, durations, statuses and usage |
| `session.lock` | Exclusive command lock; absent after normal completion |

State is checkpointed before a model request. A failed/interrupted stage stays
flagged as running or usage-unreconciled and cannot automatically retry;
inspect `result` before deciding recovery. Do not manually clear flags or
create a fresh proposal to bypass uncertainty. The local events contain no
complete prompts, function arguments, results, model text or credentials.
This is **local application tracing**, not OpenTelemetry spans, model-internal
reasoning, Azure Monitor export or a distributed trace in the Foundry portal.

## Tests

From the repository root:

```powershell
python -B -m unittest discover -s src\supply-chain-resilience -p "test_*.py" -v
node --test scripts\test-copilot-customizations.mjs
```

For the combined business and optional SDK suite, use the local environment:

```powershell
src\supply-chain-resilience\.venv\Scripts\python.exe -B -m unittest discover -s src\supply-chain-resilience -p "*test*.py" -v
src\supply-chain-resilience\.venv\Scripts\python.exe -m pip check
```

The SDK-free suite has 34 tests; the combined suite has 70 tests, including
SDK adapter and staged walkthrough checks.
The wider filename selector deliberately includes the optional SDK tests.
Their synthetic response fixtures and test rates are not live results.

Python tests use isolated temporary databases and remove only their own
artifacts. They cover exact costs/margins, no-impact/infeasible/missing-policy
cases, explicit errors, role boundaries, stale/mismatched approval, duplicate
and concurrent calls, rollback, persistence/reconciliation and the CLI.
They do not call Foundry, use an LLM or prove real IAM isolation.
