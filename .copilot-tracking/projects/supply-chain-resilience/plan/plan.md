---
title: "Implementation Plan for supply-chain-resilience"
description: "Proposed learning-first increments for a managed Foundry prompt agent with a thin Python driver."
ms.date: "2026-11-02"
plan_version: 2
status: "three-milestone-demo-completed-local-tracing"
---

## Current Version 2 - Three Learning Milestones

Current completion on 2026-11-03: S-022 revision 1 completed milestone 3 with
explicit Q-020 scope, Q-021 one-case EXPRESS selection and separate exact
Q-022 approval. Real agent v2 requested the action and read its durable
result; source stock is 80/70/10 and destination remains 20.
All 70 offline tests and 10 documentary/link checks pass. Local execution
tracing was explicitly chosen instead of Azure export: 36 correlated events
were inspected. No distributed OpenTelemetry coverage is claimed.
The three-milestone synthetic demo is implemented and verified for this
positive case. The completed authority is consumed; additional cloud runs,
production work and Copilot harness study are not implied.
See [A-014](../implementation/log.md#a-014---s-022-revision-1-complete-human-gated-walkthrough)
for actual references, live usage and limitations.
Earlier proposed/partial descriptions below remain historical.

Latest outcome on 2026-11-03: S-020 revision 2's single authorized live
read-only case passed. The existing managed agent called all three fact
tools, returned exact costs/margins and left stock unchanged. Actual usage:
four model requests, three function calls, 2,997 tokens. Its authorization
is consumed. The prior mandatory token-count blocker was explicitly relaxed;
remaining budget checks monitor reported usage after responses.
See [A-013](../implementation/log.md#a-013---s-020-revision-2-successful-live-read-only-case).
Milestone 2 is complete for this baseline read-only case. Milestone 3,
interactive human approval/action and traces, remains proposed only.
Earlier blocked status descriptions below are retained as history.

The user requested a shorter path and, after clarification, explicitly authorized
the reusable Python functions on 2026-11-02 at 16:59 +01:00.
Only milestone 1, S-019 revision 2, was authorized. No approval of version 1,
its unexecuted S-012...S-018, or either cloud milestone is implied.
Milestone 1 is completed: its 34 runtime tests and all 10 documentary/link
tests passed, and its authorization is consumed. The
[implementation evidence](../implementation/log.md) records actual files,
module boundaries, subprocess walkthrough and unverified cloud surfaces.

Subsequent S-020 revision 1 received explicit Q-015 consent and Q-017
corrected-login reconfirmation: ten generation requests, twenty function calls,
100,000 aggregate tokens and EUR 10. The adapter and all 55 offline tests now
pass; exact deployment lookup and creation of one managed-agent version and
conversation succeeded. Token-count preflight returned HTTP 405 before any
generation request. Milestone 2 is blocked, not completed.
Existing resource references are retained in
[A-010](../implementation/log.md#a-010-live-attempt-and-token-count-blocker).
No duplicate creation, cleanup or guard bypass is authorized automatically.
The next proposed activity is a bounded compatibility correction that reuses
the existing agent/conversation. Milestone 3 remains proposed only.

| Milestone | Result | Authority |
| --------- | ------ | --------- |
| 1: reusable business tools | Synthetic snapshot/policy, comparison, proposal, human-only approval and atomic reservation; bounded dispatcher and tests | S-019 revision 2 completed; local implementation consent consumed |
| 2: real Foundry agent | Existing managed agent and real read-only function loop verified | S-020 revision 2 completed; single-case authorization consumed |
| 3: complete learning walkthrough | Real selection/proposal, separate human approval, guarded reservation and inspected local trace | S-022 revision 1 completed; implementation and exact-case approval consumed |

Milestone 1 is not an autonomous offline agent or a required standalone app.
It prepares the functions the real Foundry agent will request. A thin CLI
exists only to exercise those functions manually. No HTTP API, MCP server,
cloud SDK or third-party dependency is needed for this increment.
Approval is deliberately outside model-invocable tools.

The current contract and actual consent are in
[state](../state.md#current-s-019-revision-2-contract-and-consent) and
[Q-013 history](../questions.md#q-013-clarification-followed-by-implementation-consent).
The following version-1 sections are retained as historical planning evidence;
their old sequence/status wording is superseded by this current section.
Their cloud safety boundaries still apply.

## Objective and Authority

Implement a small educational demo of a **named/versioned prompt agent in
Foundry**, with a Python driver for bounded tools and human approval.
The agent explains STANDARD versus EXPRESS; deterministic functions provide
facts and protect the final request/reservation. No independent code-only
reasoning agent, hosted container or general workflow engine is planned.

Baseline: [RQ-001...RQ-012](../research/analysis.md#requirements),
accepted [D-008...D-012](../decisions.md), and the
[revised scenario](../research/analysis.md#s-007-revised-transfer-options).
The [technical evidence](../research/evidence.md#s-009-revision-2---python-foundry-managed-paths)
records API-generation, function-execution, tracing and evaluation caveats.

S-011 revision 1 authorizes drafting this plan only.
**This plan is proposed, not approved for execution.**
S-012 would approve the document; each subsequent S-ID requires its own
bounded contract and current consent. Future cloud contracts must name actual
targets and budgets before they can be approved.

## Smallest Useful Product

* One initial reasoning agent, one product/component, two warehouses, two
  commitments and two transfer options. Later agents require a separate
  learning objective and comparison; they are not part of this plan.
* Thin flow: agent analysis/proposal, explicit human selection/approval,
  guarded demo action and authoritative outcome.
* Demand 60, local stock 20, transfer 40; source on-hand 80, already reserved
  30, available 50. STANDARD costs 90 and completes assembly on day 3;
  EXPRESS costs 95 and completes on day 2; ceiling 100.
* The planner chooses 5 extra cost units versus one extra day of margin.
  No invented cheapest-first, fastest-first or probabilistic-risk objective.
* A request reserves at source; it does not ship goods or increment destination
  inventory. No optimizer, scheduler, real ERP, event bus, search index,
  MCP/A2A service, web frontend or Teams channel is required.

Prefer a simple interactive driver over UI work. Concrete entry point,
packaging and storage are proposals to resolve in S-013, not silent decisions.

## Decision Gates Before Execution

| Gate | Decision or evidence needed | Blocks |
| ---- | --------------------------- | ------ |
| G-01 | User approval of plan version 1, distinct from implementation consent | All implementation |
| G-02 | Actual local Python interpreter, compatible exact SDK/exporter versions, package layout, test command, entry point and smallest reliable demo store | S-014 and SDK instrumentation |
| G-03 | Explicit subscription/project/model target, permission to inspect it, and region/network constraints; no secrets in tracking | Authenticated preflight |
| G-04 | Available project/model and permissions confirmed; exact agent target, maximum inference calls, spend ceiling, stop conditions and retention/lifecycle agreed | Any live agent creation or invocation |
| G-05 | Exact approval actor/context, proposal validity and local state-commit semantics agreed | Approval/action implementation |
| G-06 | Trace export destination/access, content capture off, supported instrumentation and final live case/run count agreed | Export and final cloud walkthrough |

G-02 should avoid unnecessary tooling. Standard-library tests and a small
transactional local store are candidates; neither a framework nor storage
product is selected here. The interpreter/package matrix needs verification,
not blind adoption of the hosted quickstart's runtime.

No subscription, project, model, region or budget is currently selected.
If a suitable project/model does not already exist, provisioning and IAM
changes require new separately scoped activities, not an expanded S-015/S-016.
Publishing to a channel and deleting resources are also outside this plan.

## Sequence and Actual Dependencies

These are reserved future step IDs, all revision 1 and **proposed**.
No execution authorization exists for any row.

| Step | Learning increment and output | Actual dependencies |
| ---- | ----------------------------- | ------------------- |
| S-012 | Review and approve/revise this plan as a document | Completed S-011 |
| S-013 | Resolve local compatibility and minimal implementation choices | S-012 |
| S-014 | Local business baseline and Python function dispatcher with offline tests | S-013 |
| S-015 | Separately authorized, read-only cloud target preflight | S-013; G-03 |
| S-016 | Live Foundry read-only tool-loop vertical slice | S-014, S-015; G-04 |
| S-017 | Local exact-proposal approval/action and tracing instrumentation | S-014; G-05 and local part of G-06 |
| S-018 | Bounded live end-to-end validation and short demo walkthrough | S-016, S-017; refreshed G-04/G-06 |

S-015 does not depend on S-014. S-017 does not depend on a live run in S-016.
These are genuine branches, not permission to execute multiple steps at once.
Single-step autonomy remains in force. Early code tests are not Foundry
runtime evidence; S-016 supplies the first live single-agent baseline.

## Contract S-012 - Plan Review

* Revision and status: 1, proposed; no consent recorded
* Objective: accept, revise or defer plan version 1, without starting its steps.
* Scope/actions: read this plan and effective tracking; use structured
  confirmation and record the actual decision in plan/state/questions.
* Exclusions: code, environment changes, cloud calls, installation and delegation.
* Prerequisite: completed S-011 and this version available for review.
* Checks/exit: record the actual plan-version decision; resolve scope changes
  through a new plan revision rather than implying consent.
* Cost/risk/recovery: no Azure cost; preserve the original proposed version
  and record revisions. Plan approval is not step approval.

## Contract S-013 - Local Readiness and Choices

* Revision and status: 1, proposed; no consent recorded
* Objective: close G-02 and propose G-05's simple local actor/state model,
  keeping the first implementation small.
* Scope/actions: read existing source/manifests, check the selected local Python
  interpreter without dumping environment variables, consult necessary public
  SDK documentation, and record compatibility and user choices in tracking.
* Targets: existing empty `src/supply-chain-resilience` directory and local
  development environment; no code or package changes in this step.
* Exclusions: installation, activation/configuration changes, authenticated
  tenant access, inference, credentials in chat, and cloud resources.
* Dependency: approved S-012; significant packaging/store/actor choices require
  actual user confirmation before becoming implementation assumptions.
* Checks/exit: known interpreter and exact candidate dependencies, chosen
  package/test entry points and persistence boundary; remaining uncertainty
  blocks the affected implementation contract.
* Cost/risk/recovery: no Azure cost. Missing interpreter or incompatible packages
  lead to a separate setup decision, not an unapproved install.

## Contract S-014 - Offline Baseline and Tool Driver

* Revision and status: 1, proposed; no consent recorded
* Objective: encode the tiny accepted scenario and understand the Python
  function-call boundary before incurring inference cost.
* Proposed file scope: package manifest, minimal package/modules, synthetic
  fixture, tests and usage notes within `src/supply-chain-resilience`;
  record exact paths in the executable contract after S-013.
* Allowed future actions: implement the baseline, bounded read/policy/assessment
  functions and function dispatcher; add the agreed manifest dependencies;
  restore only after manifest changes or a genuine missing-dependency failure.
  Run the agreed local unit/static checks.
* Exclusions: agent creation, authenticated calls, cloud inference, real data,
  independent local reasoning agent, action authorization or UI infrastructure.
* Dependency: S-013 and G-02.
* Checks/exit: exact arithmetic and scope tests pass; dispatcher handles all
  returned calls, correlates call IDs and explicit errors, and stops within
  configured bounds. Fake model responses are labeled offline unit tests,
  not a working Foundry agent.
* Cost/risk/recovery: no Azure cost. Keep changes isolated in the package;
  no broad repository refactor or unrelated dependency updates.

## Contract S-015 - Cloud Preflight Only

* Revision and status: 1, proposed and not executable until G-03 names targets
* Objective: verify the approved existing target and identify missing prerequisites.
* Scope/actions: only explicitly approved authenticated read-only checks of
  the named project/model, relevant identity permissions, region/network and
  actual quota/capacity as permitted. Record minimized findings, never tokens.
* Exclusions: resource/model creation, permission grants, connection changes,
  agent versions, inference, installations, price commitments and cleanup.
* Dependencies: S-013 and G-03; read current best practices and relevant public
  documentation before any approved Azure query.
* Checks/exit: distinguish available, unavailable and unverified prerequisites;
  establish inputs for G-04, including budget and allowed model-call count.
  A documented regional list alone is not target readiness.
* Cost/risk/recovery: no paid inference authorized. If access or capacity is
  missing, stop and propose a separate scoped remediation; do not broaden IAM.

## Contract S-016 - Live Read-Only Agent Vertical Slice

* Revision and status: 1, proposed and not executable until G-04 names targets/limits
* Objective: create/version the managed prompt agent and exercise actual
  function calling through Python for the two-option explanation.
* Scope/actions: approved creation/update of one specifically named agent version
  on the agreed existing project/model; bounded inference through the driver.
  Bind instructions/model/tools to the resolved version and actual project endpoint.
* File scope: driver/configuration references, narrow tests and usage notes in
  the same package; no secrets or real tenant payloads in files.
* Exclusions: provisioning, model deployment, IAM, hosted code, channels, write
  tools, paid judge evaluations, automatic sample cleanup and resource deletion.
* Dependencies: S-014, S-015 and G-04; fresh operational consent for that target.
* Checks/exit: capture real function-call/output correlation and final response;
  both valid options, exact costs and margin explained using policy/data evidence;
  unavailable facts produce explicit failure/clarification, not invention.
  Record actual model/tool counts and latency, without an unagreed SLA.
* Cost/risk/recovery: inference is paid and must fit the agreed cap. Stop on
  limits/errors; preserve version/operation identifiers. No automatic replay
  of an uncertain action or deletion of a version at sample-script exit.

## Contract S-017 - Approval, Guarded Action and Local Trace Coverage

* Revision and status: 1, proposed; no consent recorded
* Objective: make the distinction between recommendation, human approval and
  authorized effect observable without creating an enterprise workflow engine.
* Scope/actions: minimal proposal/selection/approval records, guarded
  request/reservation operation, outcome lookup and local instrumentation
  in the same package; run local tests and inspect local synthetic telemetry.
* Dependencies: S-014, G-05 and agreed instrumentation dependencies from G-02.
* Actor boundary: local actor fixtures test business rules only; they are not
  proof of Entra authentication. A runtime principal must come from verified
  context, not a model argument or untrusted header.
* Exclusions: live model calls, cloud telemetry export, new cloud services,
  identity assignments, autonomous agent approval and production auth claims.
* Checks/exit: no effect before valid exact-proposal approval; stale, unauthorized,
  changed-selection/payload and duplicate cases behave as specified.
  Commit request/reservation and durable outcome consistently in the agreed
  local store; an uncertain result is reconciled, not guessed successful.
  Capture business stages and correlation without message content/secrets.
* Cost/risk/recovery: no Azure consumption. Isolated synthetic test stores
  permit test cleanup only; no permission to delete or reset shared demo state.

## Contract S-018 - Bounded Live Demo and Outcome Validation

* Revision and status: 1, proposed and not executable until G-04/G-06 refreshed
* Objective: complete the learning walkthrough with real agent behavior,
  explicit approval and inspected request/reservation outcomes.
* Scope/actions: agreed finite live case/run list using the approved named
  agent/version/model and isolated synthetic state; only specifically approved
  local demo writes. Export telemetry only to the approved destination.
  Add a short walkthrough/result summary to package usage notes and tracking.
* Dependencies: S-016 and S-017; fresh consent for inference limits, approval
  actor, telemetry destination and exact synthetic write scope.
* Exclusions: paid cloud judges/evaluation runs, hosted migration, additional
  agents, real procurement/shipments, resource provisioning/IAM and cleanup.
* Checks/exit: inspect both explanation/tool trajectory and actual state using
  the acceptance table below; separate human wait from processing latency,
  identify agent/tool/policy versions, and verify trace correlation/content
  exclusions. Report failures, actual run counts and costs where available.
* Cost/risk/recovery: inference/telemetry cost bounded by the agreed limits.
  On timeout inspect the recorded operation before retry; a failed check blocks
  the relevant exit criterion. No production-readiness or zero-risk claim.

## Shared Acceptance Evidence

These are proposed measurable plan criteria, not already achieved outcomes.
All mandatory deterministic assertions must pass, with zero prohibited or
duplicate effects in the tested cases. Model explanations must satisfy the
stated case rubric; report each failure, not only an aggregate score.
Live run/repetition counts and monetary ceilings are G-04/G-06 decisions.

| Case | Required facts or effects |
| ---- | ------------------------- |
| Baseline comparison | Demand 60, shortage 40, free source 50; costs 90/95, first-order margins 0/1; request selection |
| Both selection paths | STANDARD and EXPRESS each produce their own exact proposal; no silent preference or automatic approval |
| No impact | Local stock 60; no transfer or approval request |
| Stock infeasible | Source free 30 versus need 40; no feasible full recovery or reservation |
| Ceiling variants | At 92 only STANDARD; at 80 neither option; no overspend |
| Missing preference or policy | Clarification/incomplete status; no authorization inferred |
| Denied/stale/changed approval | Zero effects; refresh/version and obtain new approval when required |
| Valid approved action | One request for 40; source on-hand 80, reserved 70, available 10; destination remains 20 |
| Duplicate/concurrent operation | At most one request/reservation; changed payload under same operation identity rejected |
| Tool timeout/error | Explicit error/unknown outcome; authoritative reconciliation before uncertain-write retry |
| Untrusted tool text | Instructions embedded in policy/tool content cannot grant approval, change permitted targets or bypass guarded action |
| Trace and evidence | Model/tool/business-stage correlation, data/policy/agent versions, no secrets or captured message content |

The same fixtures and tool contracts provide the single-agent baseline.
No multi-agent improvement is claimed or required. A future specialization
experiment needs a new objective, consent and baseline comparison.
Documentary tests are never substituted for local, integration or cloud checks.

## Plan Confirmation

* Plan version: 1
* Status: proposed; no approval of this document recorded
* S-011 drafting consent: user's 2026-11-02 16:40 +01:00 "perfetto procediamo",
  referring only to the previously presented documentary planning contract
* Approval boundary: S-012 approves/revises this document only. Each subsequent
  step needs a current contract/revision and explicit consent; unresolved
  targets, budgets or design gates prevent operational approval.
* Delegation: none included

## Revision History

| Version | Date | Change | Authorization impact |
| ------- | ---- | ------ | -------------------- |
| 1 | 2026-11-02 | Initial learning-first plan from accepted demo and managed-agent direction | Proposed document; no execution authorized |
| 2 | 2026-11-02 | Consolidate into three learning milestones; implement reusable local tools rather than a standalone offline agent | Only S-019 revision 2 local scope approved; cloud remains unapproved |
