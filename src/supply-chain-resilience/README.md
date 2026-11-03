---
title: "Supply Chain Resilience Agent"
description: "Agent-led Foundry conversation, explicit prompt assets, Python function tools and human-approved synthetic reservations."
ms.date: "2026-11-03"
---

## What Runs Today

One managed Foundry prompt agent investigates a delayed component receipt,
compares recovery options and conducts a conversation with the planner.
The agent chooses its tools and reasoning order. Python executes the tools,
records human decisions and enforces stock/approval safeguards; it does not
prescribe compare/propose/execute reasoning stages.

The published agent is `supply-chain-resilience-advisor`, version `3`.
S-026 exercised actual investigation, STANDARD choice, exact human approval,
one reservation and post-write read-back. Its final answer failed a local
evidence check because it also included genuine pre-write facts.
S-027 corrects that handoff locally by separating current and historical
evidence, with regression tests. The published prompt/schema/definition did
not change. **The correction has not yet been validated in another live run.**
See the [implementation log](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md).

## Source Layout

| Surface | Responsibility |
| ------- | -------------- |
| [advisor_demo.py](advisor_demo.py) | Single managed-agent CLI: local preparation/inspection/human decisions and guarded chat; no publication |
| [definition.py](supply_chain/agents/resilience_advisor/definition.py) | Current agent definition and instruction/schema fingerprints |
| [advisor.txt](supply_chain/agents/resilience_advisor/prompts/advisor.txt) | Mission, investigation, human-decision boundary, failure behavior and model response contract |
| [conversation.py](supply_chain/agents/resilience_advisor/conversation.py) | Agent-specific capabilities and current/historical evidence validation |
| [tools.py](supply_chain/agents/resilience_advisor/tools.py) | Advisor-owned function contracts and dispatcher |
| [runtime.py](supply_chain/runtime.py) | Shared Responses/function-output loop, call IDs, limits, usage and metadata events |
| [session.py](supply_chain/session.py) | Durable state, artifact/SDK drift checks, exclusive lock and uncertainty stop |
| [domain.py](supply_chain/domain.py) | Synthetic rules, option costs, feasibility and delivery margins; no SDK or database |
| [store.py](supply_chain/store.py) | SQLite snapshots, proposals, human approval and atomic reservation |
| [data.py](supply_chain/data.py), [scenario.json](data/scenario.json) | SDK-free input loader and versioned initial facts |
| [cases.json](evals/resilience_advisor/cases.json) | Agent evaluation scenarios/rubrics, not measured results |
| [demo.py](demo.py) | SDK-free manual tool exercise; not a local AI agent |
| [test_domain.py](tests/test_domain.py), [test_workflow.py](tests/test_workflow.py) | Business rules, transactions, concurrency, failures and manual CLI |
| [runtime_tests.py](tests/runtime_tests.py) | Real SDK response objects, batch/call-ID checks, limits, usage and failure behavior |
| [advisor_tests.py](tests/advisor_tests.py) | Conversational simulations, evidence roles, trusted human controls, persistence and cloud-binding guards |

The [agents namespace](supply_chain/agents) can accommodate future agents;
only [resilience_advisor](supply_chain/agents/resilience_advisor) exists.
Each agent owns its prompts, definition, specialized controls, tool
contracts/dispatcher and evaluation assets. Business rules, data, store and
the generic runtime are shared solution capabilities. Tools are not
automatically exposed to every agent.

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
3. Python dispatches it to the local business capability.
4. The runtime returns `function_call_output` preserving the call ID.
5. The agent continues within the same conversation.

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
configuration and `--agent-version`. It verifies the complete latest cloud
definition/version before inference. All reasoning turns use this same
command; no compare/propose/execute model stages are prescribed.
It cannot publish an agent. Matching v3 remains compatible with the local
definition, but another live case still requires explicit operational consent.

### Retained Failed Run

S-026's run is retained under ignored `artifacts\local\supply-chain-s026`.
Exactly one reservation exists: W-B 80/70/10, W-A 20. There was no shipping
or receipt. Its final-answer failure deliberately retained `running=true`
as a stop flag; no process is active and usage is reconciled.
Do not clear the flag, rewrite its source hash or retry the operation.

Read the durable outcome without Azure/model access:

```powershell
src\supply-chain-resilience\.venv\Scripts\python.exe -B src\supply-chain-resilience\advisor_demo.py inspect --directory artifacts\local\supply-chain-s026
```

Old staged sessions are not migrated into the advisor. Their retained JSON,
SQLite and metadata trace remain read-only historical evidence.

## Persistence, Limits and GenAIOps

The stable [instruction asset](supply_chain/agents/resilience_advisor/prompts/advisor.txt)
is tracked with code, schemas, model configuration, data, policies and
evaluation assets. Foundry versions identify publications, not local edits.
No automatic portal/Git synchronization, optimizer or release pipeline exists.
See the [prompt-lifecycle research](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#s-023---agent-led-design-and-prompt-lifecycle-review).

Each advisor directory contains:

| File | Purpose |
| ---- | ------- |
| `advisor-session.json` | Bindings, fingerprints, SDK versions, human decisions, current/historical tool facts, call IDs, allowance and usage |
| `planning.sqlite3` | Snapshot, exact proposal/approval and idempotent reservation |
| `events.jsonl` | Correlated metadata, statuses, durations and usage; no prompt, arguments, result payloads or model text |
| `advisor.lock` | Exclusive command lock; absent after normal completion |

Source hashing includes nested agent Python modules and the advisor CLI.
Source/prompt/schema/data/evaluation/SDK drift prevents silent resumption.
State is checkpointed before network requests; failed/interrupted turns
remain blocked instead of automatically retrying. History loading defaults
to empty when absent; it does not bypass drift checks or reconstruct facts.
These are local provenance controls, not signatures or a clean-commit claim.

The runtime permits twenty tools and requests at most 4,096 output tokens
per response. Cumulative 100,000-token/EUR 10 thresholds monitor reported
usage after each response and before the next request, not guaranteed
pre-inference limits. Missing/lost usage stops the run as unreconciled.
SDK automatic retries are disabled. The unsupported token-count endpoint
is not called; the prior HTTP 405 is historical.

The estimate uses conservative EUR 5 input / EUR 20 output per million,
charging all tokens at the higher rate. It is not an invoice, actual tariff,
tax calculation or Azure spending cap. See the [pricing evidence](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#s-020-fresh-source-check-and-preflight-boundary).

The ten [evaluation cases](evals/resilience_advisor/cases.json) are synthetic
rubrics, not a passed scorecard or held-out benchmark. Local event inspection
is not distributed OpenTelemetry/Azure Monitor tracing.

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
Terminal validation uses Python 3.12.10, SQLite 3.49.1, Projects 2.10.0,
Identity 1.27.0 and OpenAI 3.38.0; this is not a supported-version matrix.

From the repository root:

```powershell
python -B -m unittest discover -s src\supply-chain-resilience -p "test_*.py" -v
src\supply-chain-resilience\.venv\Scripts\python.exe -B -m unittest discover -s src\supply-chain-resilience -p "*test*.py" -v
node --test scripts\test-copilot-customizations.mjs
```

There are 34 SDK-free tests and 95 combined tests. Retired-driver-specific
tests were removed; relevant runtime and human-action safeguards remain
covered on the current path. The broader selector includes optional SDK
simulations, not cloud inference. All Python tests use isolated temporary
databases and remove only their own artifacts. They do not prove real IAM
isolation or general model quality.
