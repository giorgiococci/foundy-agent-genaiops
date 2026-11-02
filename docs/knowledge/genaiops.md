---
title: GenAIOps and AgentOps
description: Evaluations, versioning, releases, costs, and regression management for the future demo.
ms.date: 2026-11-02
status: research-baseline
---

## Proposed release unit

Behavior depends on code, prompts, models, tools, data, and policies.
Versioning only the image or prompt is not enough.
Foundry documents agent versions and reusable datasets; the complete
manifest proposed here is a lab convention.
Sources: [S02](../research/sources.md#s02),
[S03](../research/sources.md#s03), [S22](../research/sources.md#s22).

Each release should identify:

* Code commit and image digest, if present
* Exact SDK, protocol library, and exporter versions
* Agent versions and instruction hashes
* Model deployment, resolved version, and available parameters
* Tool schema/version and Toolbox/connections used, without credentials
* Policy version and guardrail configuration
* Datasets, rubrics, evaluators, and judge model
* Network configuration, region, and infrastructure references
* Gate results and release approval

If the model or a service changes behind an alias, record the
reproducibility limitation. Do not promise bit-identical responses from a
probabilistic system or dependencies that cannot be pinned.

## Evaluate outcomes and process

The documentation distinguishes system evaluation from process evaluation.
In multi-agent solutions, system evaluators apply particularly
to the orchestrator or final agent. Do not assume that they automatically
evaluate every intermediate specialist.
Source: [S21](../research/sources.md#s21).

| Aspect          | Evaluation to consider                     | Complementary deterministic test                     |
| --------------- | ------------------------------------------ | ---------------------------------------------------- |
| Task outcome    | Task Completion, Intent Resolution         | Final case state and explicit requirements           |
| Task adherence  | Task Adherence                             | Permitted actions and output schema                  |
| Tool use        | Tool Selection, Tool Call Accuracy         | Permitted tool sequence per scenario                 |
| Parameters      | Tool Input Accuracy                        | Schema, record scope, and server-side constraints    |
| Tool outcomes   | Tool Call Success, Tool Output Utilization | Backend outcome and no fabricated data               |
| Grounding       | Evaluator relevant to the chosen format    | Existing evidence, version, and verifiable citations |
| Action security | Adversarial suite and red teaming          | Denies, zero prohibited effects, and idempotency     |

The names come from [S21](../research/sources.md#s21).
Outputs and scales differ: some are pass/fail, while others
derive from scores with thresholds. Validate required inputs, outputs, and
failure reasons for each evaluator before integrating CI.

Task Completion, Intent Resolution, Task Adherence, and composite evaluators
are marked preview in the guide. Other evaluators are not marked
the same way in the reviewed text: do not automatically declare them GA
or preview. Quality Grader is listed as deprecated.
Source: [S21](../research/sources.md#s21).

An LLM-as-judge can be inconsistent or sensitive to the text being evaluated.
Do not use it as the sole proof of authorization, a write, or
a tenant boundary.

## Proposed dataset

Foundry supports JSONL/CSV inputs and versioned dataset uploads.
Source: [S22](../research/sources.md#s22).

Initial proposal: **100 distinct synthetic scenarios**, divided into:

| Group                           | Cases | Expected behavior                                      |
| ------------------------------- | ----- | ------------------------------------------------------ |
| Happy paths and grounding       | 40    | Evidence-backed answer and proposal                    |
| Missing or ambiguous data       | 15    | Request clarification or abstain                       |
| Auth, scope, and injection      | 25    | Correct refusal, no prohibited reads/writes            |
| Timeouts, 429, and dependencies | 10    | Explicit status, bounded retries, and defined recovery |
| HITL, replay, and concurrency   | 10    | Approved changes only, at most one effect              |

These datasets have not yet been generated. For each scenario, record the ID,
user role, fixtures, inputs, expected evidence, prohibited actions, business
outcome, rubric, and version.

Use separate development and acceptance sets.
Do not optimize prompts/run optimizers on held-out acceptance cases.
Real traces may feed new cases only after minimization,
applicable consent/legal basis, and removal of sensitive data.

## Proposed pipeline

```text
pull request
  -> static checks and contracts
  -> policy/idempotency unit tests
  -> tool integration tests with synthetic fixtures
  -> authorized cloud evaluation in a test environment
  -> baseline/candidate comparison and report
  -> release approval
  -> deploy immutable version
  -> smoke tests and controlled switch
  -> observation / rollback / new dataset
```

Documented integrations exist with GitHub Actions and Azure DevOps.
Extension compatibility with the chosen API generation, target, and
authentication must be tested. An SDK call from the pipeline is
an alternative if the extension does not cover the required contract.
Sources: [S23](../research/sources.md#s23),
[S24](../research/sources.md#s24), [S25](../research/sources.md#s25).

Do not run untrusted PR code with cloud credentials. Proposal:
OIDC/federation where supported, a protected environment, least privilege,
approval for costly runs, and no permanent keys in the repository.

## Proposed quality gates

These thresholds belong to the lab, not Microsoft requirements or SLAs.
They must be calibrated after the first baseline.

| Gate                    | Proposed initial criterion                                            |
| ----------------------- | --------------------------------------------------------------------- |
| Contracts and policies  | 100% of mandatory deterministic tests pass                            |
| Prohibited actions      | 0 unauthorized effects in negative and replay cases                   |
| Tasks on 40 happy paths | At least 36/40 correct according to the rubric, with errors inspected |
| Missing/ambiguous data  | 15/15 without fabricated facts or authorizations                      |
| Telemetry privacy       | 0 sensitive canaries found in inspected outputs                       |
| Integration tracing     | All expected hops in controlled runs are correlated                   |
| Latency                 | p95 <= 30 s over at least 50 normal runs, excluding HITL waiting time |
| Costs                   | Within the per-run/session budget agreed after measurement            |

Report numerator, denominator, distribution, and number of repetitions,
not just percentages. A 0/25 result in the negative sample does not prove zero risk.
For LLM comparisons, repeat critical cases and report variability;
any confidence intervals do not turn a small sample
into certification.

A critical security regression blocks the release even if average
quality improves. For noncritical quality regressions, use the
baseline, a declared tolerance margin, and review of changed cases.

## Recurring evaluation and monitoring

The dashboard guide distinguishes scheduled evaluation from continuous evaluation
on sampled live traffic and documents limits such as `maxHourlyRuns`.
The indicated features are in preview.
Source: [S19](../research/sources.md#s19).

Proposal: repeatable offline evaluation first, then scheduled scans on
a synthetic dataset, and finally live sampling if justified.
Limit run count and cost; do not collect real user
content solely to populate charts.

Evaluations that require transcripts can conflict
with content recording OFF. Resolve this with synthetic datasets or a
minimized, authorized collection path; do not silently enable global
capture. Sources: [S18](../research/sources.md#s18),
[S22](../research/sources.md#s22).

## Costs and quotas

The proposed total cost to measure is the sum of:

* Inference for all agents, retries, and repeated contexts
* Judge models, synthetic datasets, and red teaming
* Active hosted compute or external hosting
* Conversation/session storage and business data
* Managed tools, retrieval, and other services used
* Telemetry ingestion/retention, registry, and networking

Hosted documentation describes CPU/memory billing during active sessions;
idle timeout and concurrency affect cost. This is not equivalent to model
call time alone. Sources: [S03](../research/sources.md#s03),
[S29](../research/sources.md#s29).

Inference quotas, evaluation limits, and application rate limits are different.
For 429 responses, use `retry-after`, backoff with jitter, and a deadline;
retries must not multiply calls and side effects without bounds.
Sources: [S28](../research/sources.md#s28),
[S30](../research/sources.md#s30).

An Azure budget is a financial alert; it is not assumed here to be
an automatic cutoff. Proposal: workflow limits, maximum
concurrency, tool rate limits, and an operational command to stop runs.

## Rollback and incidents

Proposal: retain the previous manifest and configuration; restore
the served version and verify with smoke tests. Software rollback
does not undo notes or other changes already written.

In the event of an error or data leak: stop the executor, preserve
minimized audit records, identify affected releases/runs, revoke access
if necessary, and add a regression case before release.
Do not run optimizer auto-fixes or auto-promotion in production.
