---
title: "Implementation of supply-chain-resilience"
description: "Authorized local business-tool implementation, module boundaries and verified test evidence."
ms.date: "2026-11-03"
---

## Activity Log

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

* [Shared loop](../../../../src/supply-chain-resilience/supply_chain/foundry.py):
  reuse of request accounting, call-ID continuation, batch validation and
  explicit-error behavior; optional metadata-only event callback
* [Workflow stages](../../../../src/supply-chain-resilience/supply_chain/walkthrough.py):
  human-selected option and exact approved proposal checks independent of
  model instructions; no model approval tool
* [Staged CLI](../../../../src/supply-chain-resilience/walkthrough_demo.py):
  durable session and SQLite state, atomic session-file replacement,
  exclusive command lock, persistent shared usage and uncertainty flags
* [Workflow tests](../../../../src/supply-chain-resilience/tests/walkthrough_tests.py):
  success, rejection without reservation, early execution/self-approval
  rejection, wrong IDs/options, duplicate proposal prevention, shared budgets,
  state/trace restoration and confirmation/uncertainty guards
* [Baseline CLI](../../../../src/supply-chain-resilience/foundry_demo.py):
  explicitly rejects a different latest named-endpoint version rather than
  silently invoking the new workflow definition as read-only v1
* [Adapter regression tests](../../../../src/supply-chain-resilience/tests/foundry_adapter_tests.py)
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

Added [SDK adapter](../../../../src/supply-chain-resilience/supply_chain/foundry.py),
[live CLI](../../../../src/supply-chain-resilience/foundry_demo.py) and
[offline SDK tests](../../../../src/supply-chain-resilience/tests/foundry_adapter_tests.py).
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
| [tools.py](../../../../src/supply-chain-resilience/supply_chain/tools.py) | Six strict JSON function specifications and explicit-error dispatcher |
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
