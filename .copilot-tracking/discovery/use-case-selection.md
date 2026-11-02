---
title: Demo use case discovery
description: Comparison of more impactful synthetic-data demos and open selection questions.
ms.date: 2026-11-02
status: direction-selected
---

## State and scope

Update on 2026-11-02: the user selected the supply-chain theme and a mixed
audience, but questioned the realism of the initial event. The domain
selection does not approve the candidate story or architecture.
Continue in [supply-chain-resilience](../projects/supply-chain-resilience/state.md).
The user subsequently selected manufacturing in project Q-003.
The original comparison and question records below are retained.

Initial phase: discovery, before a Foundry solution project was selected.
At that point no solution project ID was assigned. No architecture,
hosting target, or deployment is approved.
This pre-project record will be linked from the selected project's analysis,
not reused as an arbitrary solution project.

S-001 revision 1: completed documentary analysis requested by the user.
Scope: compare three stronger demo stories, check relevant public sources,
and record the next selection questions. No specialist was delegated.
Acceptance: explain each story, observable result, useful agent boundaries,
data, trade-offs, and security/GenAIOps/observability/RAI opportunities.

No application code, infrastructure, authenticated tenant access, paid
evaluation, package installation, deployment, commit, or push is authorized.
The next step is a user choice of direction, not implementation.

## Confirmed requirements

Faithful English summary of the user's Italian request, not a verbatim quotation:
the existing candidates are not compelling enough. Find a more interesting,
impactful demo; synthetic data remains required, and Azure databases, AI Search,
or other resources may be considered to make the solution more varied.

* RQ-001: Use synthetic business data, documents, events, and identities.
* RQ-002: Demonstrate a visible operational outcome beyond a chat answer.
* RQ-003: Preserve security, GenAIOps, observability, and Responsible AI goals.
* RQ-004: Keep APIM and paths requiring it out of scope.
* RQ-005: Consider Azure resources when they serve a concrete business purpose;
  this is not approval of any service, cost, or provisioning.
* RQ-006: Continue step by step; selecting an idea does not approve its design,
  implementation, or deployment.

Audience, preferred industry, budget, demo duration, and desired complexity
remain unknown. They are not inferred from previous assistant-setup decisions.

## Candidate comparison

All scenarios, roles, data sizes, UI ideas, and service mappings below are
lab proposals, not Microsoft reference architectures or verified outcomes.

| Candidate                | Visible result                                   | Why multiple agents may help                     | Main scope risk                           |
| ------------------------ | ------------------------------------------------ | ------------------------------------------------ | ----------------------------------------- |
| Supply Chain Rescue      | Compare recovery plans and update a demo order   | Evidence, operations, and commercial trade-offs  | Expanding into a real logistics optimizer |
| Travel Disruption Desk   | Build and approve a feasible replacement journey | Policy interpretation and itinerary evaluation   | Live booking and combinatorial complexity |
| Factory Quality War Room | Trace a suspect batch and simulate containment   | Quality evidence and operational impact analysis | Industrial integration and safety claims  |

### Supply Chain Rescue

A fictional consumer-electronics company is preparing a product launch.
A synthetic disruption delays a component shipment. The operator sees
affected orders and asks how to protect the launch without breaking
supplier or spending constraints.

Candidate reasoning responsibilities:

1. Evidence specialist retrieves versioned supplier agreements, transport
   terms, and substitution rules, with citations and explicit missing evidence.
2. Operations specialist examines authorized orders, inventory, supplier
   capacity, and lead times through constrained data tools.
3. Commercial specialist compares validated alternatives against business
   priorities and explains trade-offs; it does not invent prices or forecasts.

A deterministic workflow joins compatible results. Exact arithmetic,
capacity checks, feasibility, and proposal validity are code responsibilities.
Evidence and operational fact gathering may run independently; generating
and comparing feasible plans must wait for the facts and constraints.
An independent LLM reviewer is not assumed necessary.

Candidate data: a few hundred synthetic order lines, a small supplier network,
inventory snapshots, transport offers, and a few dozen short documents.
Use fixed versioned fixtures with known outcomes instead of an unbounded
web search or a realistic global routing engine.

Candidate UI: affected-order map or network, a timeline, and comparable plan
cards showing delivery dates, incremental cost, constraints, and citations.
These are estimated scenario results, not promises of actual deliveries.

The demo turning point is a new event while a proposal awaits approval.
That proposal becomes stale; the executor refuses it and requires a newly
validated version. Approval then changes only a reservation or recovery-plan
record in the demo database. A replay must not apply the change twice.

### Travel Disruption Desk

A synthetic flight cancellation affects a fictional team's multi-city trip.
The system combines a fixed timetable and seat inventory with travel policy,
connection rules, accessibility requirements, and a spending envelope.
It proposes feasible alternatives and explains which constraints cannot be met.

Candidate specialists interpret policy and compare itinerary options.
Deterministic checks validate connections, inventory, and exact totals.
The UI shows the original journey and replacement options on a timeline.
Approval updates a simulated booking, not an airline reservation or payment.

This is approachable for a broad audience and visually clear. Its main risk
is turning into a travel-planning product. Keep one disrupted leg, a bounded
set of alternatives, no live booking APIs, and fictional traveler profiles.
Accessibility needs are explicit constraints, not attributes inferred by an LLM.

### Factory Quality War Room

A synthetic quality report flags a suspect component batch in a fictional
electronics assembly network. The system links batch genealogy, inventory,
production orders, and quality procedures to show potentially affected units
and compare conservative containment options.

Candidate specialists retrieve quality evidence and assess operational
impact. Deterministic queries calculate genealogy and quantities. A dashboard
shows the batch-to-product graph and the effect of a proposed hold.
Approval changes a simulated quality-hold record only.

This has a strong industrial story and explainable data lineage. Its risk
is implying that the model certifies product safety or controls machinery.
No PLC/IoT actuation, real recall, safety clearance, or real production change
belongs in this demo. Telemetry and images would be optional later extensions,
not prerequisites or approved services.

## Recommended direction

D-001: proposed, not accepted. Prefer Supply Chain Rescue for the balance
of a clear story, visible state changes, varied data, and bounded execution.
Prefer Travel Disruption Desk for a non-specialist audience; prefer Factory
Quality War Room for an industrial audience interested in traceability.
The user may reject all three or suggest a different domain.

The smallest useful slice is one disruption, one operator scope, a small set
of candidate recovery plans, one constrained approved action, and a fixture reset.
More agents and Azure services are not success criteria.
Compare against a single-agent baseline with the same data and tools before
claiming a multi-agent improvement.

## Shared platform possibilities

These are options to evaluate after selection, not an architecture decision:

* Azure SQL Database could hold operational records, versions, reservations,
  and durable action records. Prefer typed, parameterized business tools
  over arbitrary SQL generated by an agent.
* Azure AI Search could retrieve versioned synthetic documents using keyword
  and vector retrieval. Search results are evidence, not the source of truth
  for current inventory, seat availability, or action authorization.
* A document store could retain the original synthetic files. An event service
  is optional: an explicit scenario-injection API is enough for the first slice.
* Foundry and an orchestration runtime could coordinate the reasoning.
  Model, language, hosting, identity boundaries, and region are not selected.
* Application Insights / Azure Monitor remain observability candidates from
  the knowledge base. Business audit must be durable and separate from traces.
* MCP is optional and justified only by a reusable capability boundary.
  APIM remains excluded.

Public documentation checked on 2026-11-02:

* [Agent Framework orchestration patterns](../../docs/research/sources.md#s07)
  documents sequential/concurrent patterns and human-in-the-loop support;
  this does not prove business authorization or distinct agent identities.
* [Azure AI Search and Azure SQL supporting sources](../../docs/research/sources.md#demo-discovery-supporting-sources)
  establish the retrieval and operational-store building blocks, not a
  built-in cross-service supply-chain, travel, or quality solution.

No subscription, model catalog, availability, region, SKU, price, quota,
end-to-end integration, or runtime behavior was checked.

## Controls and measurable outcomes

* Security: attempt an out-of-scope record read, reject it server-side,
  and show that document instructions cannot grant privileges.
* Responsible AI: cite evidence, distinguish estimates from facts,
  abstain when a constraint is unknown, and expose competing priorities.
* GenAIOps: use seeded fixtures with ground-truth feasible/infeasible plans;
  compare task success, constraint violations, groundedness, latency, and cost.
* Observability: correlate reasoning, data queries, validation, approval,
  refusal, and action without logging sensitive prompt content by default.
* Execution: reject stale, altered, expired, or unauthorized approvals;
  make approved demo actions idempotent and resettable.

These are proposed acceptance cases, not tests already run. No outcome
metrics or business savings have been measured.

## Open questions

### Q-001 - Direction to explore

Status: answered for domain selection only. Reason: choose the story before
deriving a project ID or design.
Alternatives: Supply Chain Rescue, Travel Disruption Desk, Factory Quality
War Room, or more/different ideas. Recommendation: Supply Chain Rescue.
Affected decision: D-001 and the next discovery scope.
At presentation, no user answer had been received.

Update on 2026-11-02: answered. Faithful translation of the Italian answer:
the supply-chain theme is appealing; the realism of the proposed event
is uncertain, and an integrated agentic system should manage unexpected
supply-chain events. Domain selected only; scenario remains open.
See [project Q-001](../projects/supply-chain-resilience/questions.md#q-001---supply-chain-direction).

### Q-002 - Audience

Status: answered. Reason: calibrate business storytelling versus engineering depth.
Alternatives: technical, business/presales, mixed, or still unknown.
Recommendation: do not infer an audience; a mixed option in the form is only
a suggestion. Affected decisions: scenario presentation and later scope.
At presentation, no user answer had been received.

Update on 2026-11-02: answered. User answer: mixed.
See [project Q-002](../projects/supply-chain-resilience/questions.md#q-002---audience).
