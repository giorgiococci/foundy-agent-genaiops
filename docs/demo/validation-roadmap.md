---
title: Validation and build roadmap
description: Spikes, decisions, and exit criteria before building the Foundry demo.
ms.date: 2026-11-02
status: proposal-not-approved
---

## Initial state

Documentary research completed as a baseline; implementation not started.
No resources, cloud evaluations, or cost measurements have been produced.
The [candidate use case](use-case.md) is a proposal awaiting approval.

The roadmap is the operational follow-up requested for the research,
not an already authorized deployment plan.

## Decisions before provisioning

| Decision        | Starting proposal                                        | Required evidence                           |
| --------------- | -------------------------------------------------------- | ------------------------------------------- |
| Domain          | Support Case Resolution Lab                              | Demo interest and fixture availability      |
| Language        | Compare .NET and Python on the vertical slice            | SDK compatibility and target skills         |
| Hosting         | Foundry hosted agents as the primary candidate           | Lifecycle, auth, and tracing test           |
| Model           | Select for tool calling and output schema                | Evaluation, cost, quota, and version        |
| Region          | Intersection of capabilities and geographic requirements | Actual subscription catalog and quotas      |
| Tools           | Business APIs; MCP if justified                          | Reuse, auth, and server management          |
| Initial network | Synthetic data, mandatory auth                           | Accepted residual risks; separate hardening |
| Budget          | To be agreed after meter estimation                      | Current prices, number of runs and sessions |

You do not need to decide every detail to read the guides. Explicit
decisions are required before creating billable resources.

## Blocking technical spikes

All spikes are **pending execution**. Sources document capabilities;
they do not provide results for our environment.

| ID  | Test                                                  | Verifiable exit criterion                                                    |
| --- | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| P01 | Compatible region/model/hosting/tool/evaluation       | Actual matrix, quotas, and versions recorded                                 |
| P02 | Consistent SDKs on the chosen vertical slice          | Repeatable build and run with pinned dependencies                            |
| P03 | Identity reaching every hop and user context          | Principals/audiences verified; spoofing rejected                             |
| P04 | Read-only tools and record scope                      | Read allowed; cross-scope access and writes denied, including in the backend |
| P05 | Client/runtime/tool tracing and exporter              | Correlated trace, no double counting, visible degradation                    |
| P06 | Trace and artifact privacy                            | Canary absent from all inspected sinks                                       |
| P07 | Approval, idempotency, timeout, and resume            | One note per valid command, none for a forbidden command                     |
| P08 | Chosen evaluators: input, output, scale, and maturity | Repeatable minimal run and correct result mapping                            |
| P09 | Monitoring/recurring evaluation without APIM          | Native path tested or gap declared with an OTel alternative                  |
| P10 | Runtime costs and limits                              | Meters identified, cost/run and session, application stop verified           |
| P11 | State and deletion                                    | Destinations inventoried and cleanup tested for each                         |

Primary sources: [development](../knowledge/development.md),
[security](../knowledge/security.md),
[observability](../knowledge/observability.md), and
[GenAIOps](../knowledge/genaiops.md).

If P03 fails with a shared connection, assess a supported delegation
mode or service separation. Do not pass the spike using an
unauthenticated identity header.

If P09 requires out-of-scope components, limit the dashboard
integration and document the limitation. Do not introduce APIM implicitly.

## Proposed increments

### M0 - Scope confirmation

Approve the use case, roles, synthetic data, maximum budget, candidate
region, and permitted previews. Record the decision, alternatives, and rationale.
Do not create empty code folders yet.

### M1 - Single-agent vertical slice

Create one agent, one read tool, and one authorized/forbidden case.
Complete P01-P06 and produce the first manifest.
The exit is a repeatable run with an auth check and trace, not
a response obtained once in the playground.

### M2 - Multi-agent workflow

Add two specialists and verifiable output contracts.
Use the same data and tools as the single-agent baseline.
Measure outcome, latency, tokens, and limits. If multi-agent adds
no value, simplify or change the task decomposition.

### M3 - Approved action and failures

Add a versioned proposal, approval, and deterministic executor.
Complete P07, including deny, concurrent replay, timeout with an uncertain
outcome, cancellation, and resume. No production system is involved.

### M4 - Evaluation and release

Prepare the proposed dataset, complete P08, and integrate authorized
offline and cloud checks. Publish baseline/candidate reports,
the manifest, residual risks, and rollback procedure.

### M5 - Operations and hardening

Complete P09-P11, applicable dashboards and alerts, budget, and cleanup.
Add the private-network profile only after verifying its cost,
compatibility, and actual educational value.

### M6 - Optional experiments

Study identity per distributed specialist, A2A, Copilot harness, or
optimizer separately. Each experiment retains its comparison, cost,
and regression tests; it does not become an implicit lab dependency.

## Future structure, only when needed

Proposed conventions to avoid a disorganized repository:

| Future path        | Expected content                                       |
| ------------------ | ------------------------------------------------------ |
| `src/`             | Application, workflows, and business/MCP services      |
| `tests/`           | Unit, integration, policy, and failure tests           |
| `evals/`           | Synthetic datasets, rubrics, and configurations        |
| `infra/`           | IaC after stack selection                              |
| `scripts/`         | Repeatable build, evaluation, deployment, and cleanup  |
| `docs/decisions/`  | Decisions with status, alternatives, and evidence      |
| `docs/runbooks/`   | Operations, incidents, cost control, and teardown      |
| `artifacts/local/` | Local outputs excluded from Git, never the only result |

These paths are planned, not existing. Selected synthetic reports may
be versioned; logs or real data may not. Release artifacts must remain
retrievable in the chosen system, not only on a PC.

## Demo definition of done

* A clean clone can reproduce builds and tests with documented prerequisites.
* The architecture identifies identities, data, trust boundaries, and adopted previews.
* The suite demonstrates least privilege and checks effects in the backend.
* The single/multi-agent comparison uses declared datasets and metrics.
* Each demo run has useful traces/audit without sensitive content.
* A business change requires verified approval and is not duplicated.
* Quality, privacy, and budget gates are measured, not merely described.
* Failures, residual risks, and sample limitations are known.
* Provisioning, shutdown, rollback, and cleanup are repeatable.
* No dependency on APIM or personal credentials in the runtime.

These criteria are proposed for the future build. They are not already
satisfied by the knowledge base alone.
