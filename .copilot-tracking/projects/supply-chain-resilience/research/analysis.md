---
title: "Analysis of supply-chain-resilience"
description: "Initial business framing and documented realism of supply-chain exception scenarios."
ms.date: "2026-11-02"
---

## Use Case and Expected Value

Confirmed: manufacturing supply-chain domain, synthetic data, and a mixed audience.
The user wants an agentic system integrated into a business process and
managing unexpected events, not an isolated question-answering assistant.
Q-004...Q-006 subsequently confirmed smart-home hubs with a delayed
controller-board receipt, protection of committed customer dates within
a spending ceiling, and an approved transfer request with a stock
reservation in the demo system.
Exact quantities, dates, spending limits, and technical choices remain open.

Working concept, not an approved product name: Supply Chain Exception
Control Tower. Support a planner from a changed supply fact to a validated,
approved recovery action and a visible update to demo operational state.

Actors proposed for discussion: supply-chain planner and authorized approver.
They are business roles, not automatically separate LLM agents.

## Discovery Continuation

On 2026-11-02 the user confirmed the direction and asked to continue.
This is a faithful English summary of an Italian statement, not a verbatim
quotation. It applies to S-003 revision 1: refine the proposed business
scenario, objective, and action boundary. It does not choose every detail
of the initial proposal or authorize architecture, code, or Azure operations.

The [question register](../questions.md) recorded Q-004...Q-006 before asking,
then captured the actual returned selections. Their recommendations were not
treated as answers before the user submitted the form.
S-003 revision 1 business discovery is completed; its authorization is consumed.

## Realism and Source Evidence

The public Dynamics 365 Supply Chain Management article
[How impact analysis works](../../../../docs/research/sources.md#demo-discovery-supporting-sources)
was checked on 2026-11-02. It documents:

* Changes to confirmed delivery dates, quantity reductions, and cancellations
  as causes of downstream purchase-order impact.
* Supply-to-demand relationships such as purchase order to production order
  to sales order, or purchase order to transfer order to sales order.
* Cases with impact, including delayed dependent orders and inventory
  threshold breaches, and cases without impact when sufficient buffer exists.

This is evidence that the business event is realistic, not evidence that
the proposed custom Foundry demo already works. The article explicitly
describes a production-ready preview and prerelease documentation.
Do not present the Dynamics capability as GA or as a novel lab invention.
Neither Dynamics nor its Procurement Agent is a selected dependency.

The demo would represent a bounded ERP/WMS-like operational system using
synthetic records. Real enterprise integration is a later scope decision.
An event service is not required merely to trigger a scenario.

## Proposed Business Story

The initial candidate was a supplier changing the confirmed date or
quantity of a purchase-order line. Q-004 selects a delivery-date delay
for controller boards. This is more precise than an unexplained external
crisis or a generic supplier-risk alert.

Business flow refined after Q-003...Q-006; implementation is not authorized:

1. Receive a synthetic supplier update tied to a known purchase-order line.
   If it arrives as an email/document, treat extraction as untrusted until
   the source and parsed facts are validated.
2. Read current inventory, reservations, expected receipts, and explicit
   supply-demand dependencies. Determine whether the change actually matters.
3. If there is no business impact, explain the buffer and stop.
   Do not generate a crisis for every late shipment.
4. If there is impact, identify affected orders and retrieve the constraints
   relevant to possible recovery options.
5. Compare feasible stock-transfer candidates under the spending ceiling.
   An alternate supplier or a proposed date change may be discussed as
   fallbacks, but purchasing and production replanning are not selected
   write capabilities. Do not assume every option is contractually permitted.
6. Require approval for a precisely versioned, authorized demo action.
   Apply it through deterministic code, not an unrestricted agent write tool.
7. Record the outcome and re-evaluate if a new event changes the facts.

The selected manufacturing slice needs a small explicit bill of materials
and production dependencies. Do not expand it into an unbounded ERP model.

## Requirements

* RQ-001, confirmed: supply-chain exception management; source Q-001.
* RQ-002, confirmed: mixed audience; source Q-002.
* RQ-003, confirmed: use a credible business event and process rather than
  assuming the initial dramatic launch scenario; source Q-001.
* RQ-004, confirmed: synthetic data and permitted consideration of Azure
  resources, not authorization to provision; source the user's request
  retained in the [pre-project record](../../../discovery/use-case-selection.md).
* RQ-005, confirmed lab constraint: APIM excluded; security, GenAIOps,
  observability, and Responsible AI remain part of the learning goals.
* RQ-006, confirmed lab constraint: single-step discovery and explicit
  approval before operational work.
* RQ-007, confirmed: manufacturing operating context; source Q-003.
* RQ-008, confirmed: smart-home hubs and a supplier delay affecting controller
  boards; source Q-004.
* RQ-009, confirmed: protect committed customer dates within a spending
  ceiling, with quantitative parameters still open; source Q-005.
* RQ-010, confirmed: support a human-approved transfer request and stock
  reservation in the demo system, not a physical movement; source Q-006.
* RQ-011, confirmed on 2026-11-02: the primary demo objective is learning
  Foundry agents; deterministic workflow complexity must not displace
  the agent-learning content. Source: the user's 15:36 +01:00 clarification.
* RQ-012, confirmed on 2026-11-02: use synthetic data and simplified business
  logic, not production-grade ERP or scheduling fidelity. Exact simplifications
  remain to be designed; this does not remove the approved-action boundary.

## Effective Decisions

The [decision register](../decisions.md) is the authoritative location for
status, answers, alternatives, consequences, and limits.
D-001, D-002, and D-004 preserve the earlier domain, audience, and context
choices. D-003 was initially proposed as a date/quantity change; Q-004 narrows
and accepts it as a delayed controller-board receipt.
D-005...D-007 record the accepted product, qualitative objective, and
future demo action. None selects an architecture or authorizes execution.

## Proposed Manufacturing Slice

History: this slice was initially proposed after Q-003, not accepted in full.
Q-004...Q-006 now confirm the product/event, business objective, and action.
The remaining fixture and design details below are still proposals:

* A fictional company assembles smart-home hubs from a compact,
  explicit bill of materials. Avoid a full factory scheduling model.
* One supplier changes the confirmed delivery date of a component purchase
  order. The update is linked to a known record and validated before analysis.
* The operational dataset connects that component receipt, available and
  reserved stock in two warehouses, production orders, and customer orders.
* The system determines whether existing buffer protects the commitments.
  If not, it identifies the affected orders and explains the dependency chain.
* The planner compares feasible transfer alternatives against committed
  customer dates and a spending ceiling. Alternate sourcing or date changes
  are possible future fallbacks, not selected purchasing/replanning actions.
  Respect stock already reserved for other orders; do not silently shift
  the shortage to another customer.
* The selected future demo action is an approved transfer request with a stock
  reservation in the demo database. This is not a physical shipment,
  a supplier commitment, or an instruction to production equipment.
  Creating the request must not count goods as received at the destination.
* A later inventory or receipt update invalidates an outdated proposal.
  Reconciliation and idempotency prevent duplicate reservations.

The business view would show affected production/customer orders,
the component dependency, alternative plans, evidence, and the changed
demo state. A technical view could expose correlated traces and audit.
Neither view has been implemented.

The qualitative objective is now agreed: protect committed customer dates
within a spending ceiling. Order priority, ceiling amount, buffer constraints,
and tie-breakers still need definition before ranking plans.
Do not claim an optimal recovery without a specified and validated algorithm.
All example plans remain bounded what-if scenarios.

## Data and Identity

All records, supplier communications, contracts, users, and events must
be synthetic. A relational store and document retrieval are options,
not selected Azure services or an approved architecture.

Operational quantities and dependencies need an authoritative data model.
AI Search cannot replace current transactional inventory. An agent must
not invent inventory, delivery promises, qualified substitutions, costs,
or the dependency graph.

Authorization must be enforced by data/tool services using verified context.
An agent role or supplier name in a prompt does not establish a principal.
No identities, hosting boundaries, authentication mechanisms, or IAM
assignments have been selected.

## Quality and Operations

Candidate acceptance scenarios:

* A supplier delay with enough inventory buffer correctly produces no action.
* A delay or quantity reduction with known dependencies identifies the
  expected impacted orders and excludes unrelated records.
* An infeasible recovery is rejected even if its explanation sounds plausible.
* Missing or conflicting constraints produce clarification or abstention.
* A new event invalidates an old proposal before execution.
* An approved lab action changes only the authorized record and is idempotent.
* A single-agent baseline and a multi-agent candidate use the same fixtures.

These are proposals, not measured outcomes. Exact metrics, datasets,
budgets, service availability, and thresholds remain to be agreed.
No cloud runtime, integration, or behavioral test has run.

## Assumptions and Open Questions

Q-003...Q-006 are answered. Manufacturing, smart-home hubs, the controller-board
delay, the qualitative objective, and the approved demo capability are selected.
The initial launch campaign, exact bill of materials, dates, quantities,
spending ceiling, roles/approval matrix, specific agent decomposition,
UI, database product, AI Search use, MCP, event service, and hosting
remain undefined or unapproved. No unseen numeric default is accepted.

## Proposed Next Investigation

S-004 revision 1, proposed: research and compare logical architecture options
for this business slice, mapping reasoning tasks, deterministic checks, tools,
data, and authorization boundaries, with a single-agent baseline.
Verify current product sources for any API-dependent recommendations.
No technical option, implementation, or deployment is approved yet.

## Documentary Validation

The repository's nine structural tests pass after adding the discovery
records, including metadata, local links, and source-register checks.
This result does not validate the proposed business logic, integration,
agent behavior, or cloud runtime.

## S-004 Logical Architecture Research Outcome

On 2026-11-02, the approved documentary comparison was performed directly,
without delegation. The [evidence](evidence.md) compares a single agent with
bounded tools, an explicit workflow with one reasoning agent, and a controlled
multi-agent workflow against the same RQ-001...RQ-010.

The recommendation is the explicit workflow with one reasoning agent,
retaining the single-agent baseline and treating specialization as a conditional
experiment. This is [proposed D-008](../decisions.md#d-008---controlled-workflow-as-a-design-candidate),
not user acceptance of an architecture. Agent Framework workflow concepts
illustrate a possible mapping; no framework or hosting option is selected.

The research separates authoritative data/calculations from explanatory
reasoning, defines logical approval/execution boundaries, and lists future
negative, replay, stale-data, and reconciliation cases. The retiring Foundry
visual builder is not recommended. No runtime, quota, price, or regional
availability claim follows from the documentary results.

Quantitative domain rules, approval lifecycle, atomicity strategy, and quality
thresholds remain open. No example dataset, generic lab limit, or support-ticket
RAI scenario becomes a requirement of this manufacturing project.

## Learning-First Scope Clarification

The user's 2026-11-02 clarification at 15:36 +01:00 gives priority to learning
Foundry agents and explicitly permits simplified business logic and synthetic
data (faithful English translation, not a verbatim quotation).
This narrows how the S-004 recommendation should be developed; it does not
invalidate its evidence or approve implementation.

Keep agent reasoning, grounded tool use, human approval, tracing and evaluation
visible. Use small explicit business rules instead of a general planning engine.
The minimum write boundary still validates permission, approval, stock availability
and duplicate prevention. Production-scale workflow durability, optimization,
integration and recovery infrastructure are not implicitly demo requirements.
Q-008 asks how much sequencing should be agent-led versus fixed.

Q-008 subsequently returned `thin-flow`. The accepted direction is a small
analysis/proposal, human-approval, and demo-action flow, with reasoning and
tool use inside the agent and essential write checks outside it.
This is not a request for a general workflow engine, production ERP behavior,
or a final number of agents. The learning value must drive later decomposition.

## S-006 Minimal Demo Sketch

Status: **proposal for discussion**, produced under Q-009 on 2026-11-02.
This is the historical first sketch. Its EXPRESS price and single-feasible-option
conclusion are superseded by the [S-007 revision](#s-007-revised-transfer-options)
below; the original figures are retained to preserve the design history.
The activity approval does not accept the example values or new rules.
See [proposed D-010](../decisions.md#d-010---minimal-demo-sketch).
This sketch narrows the earlier research to a learning increment, not a
production-fidelity implementation.

### Learning Goal and Visible Experience

A planner presents a synthetic supplier delay and asks the agent which
customer commitments are affected and whether a stock transfer can protect them.
The agent obtains authoritative demo facts through tools, explains the
dependency, compares validated alternatives, and proposes an action.
An authorized human approves the exact proposal outside model discretion.
The demo then displays the recorded request and source reservation.

Start the learning increment with one reasoning agent; this is a proposal,
not the final agent count. A subsequent specialist should teach an observable
delegation, context, or capability-isolation concept and be compared with the
same single-agent case. Do not add a specialist that merely repeats arithmetic.
No framework, model, SDK, hosting or Foundry resource type is selected here.

| Interaction | What the learner should observe |
| ----------- | ------------------------------- |
| Agent instructions and user event | The agent stays within the stated scenario and does not invent supplier facts |
| Read planning facts through a tool | Difference between a model's explanation and authoritative tool results |
| Read a short policy card through a tool | Grounded citation to a policy ID/version, without requiring a search service |
| Evaluate transfer alternatives through a tool | Structured feasible/infeasible results and grounded explanation of trade-offs |
| Produce a bounded proposal | Explicit targets, quantities, costs and evidence; no claim that a proposal changed stock |
| Pause for human approval | A model's recommendation is not an approval or a write permission |
| Submit an approved action and read its result | An action tool is narrow and checked; denied or duplicate calls have explicit outcomes |
| Inspect the run and evaluate its output | Trace model/tool calls and distinguish a fluent answer from a correct outcome |

These are learning objectives to demonstrate later, not tested Foundry features
or a prescribed API surface. Actual APIs and maturity need verification at
the later technology decision.

### Thin Flow

1. Select the synthetic delay scenario and submit it to the agent.
2. The agent reads the snapshot and policy, requests a small deterministic
   assessment, then explains impact and a proposal, or stops with no action.
   The agent chooses its bounded reads inside this stage; there is no
   fixed multi-stage ERP workflow or general-purpose planning engine.
3. If there is a feasible proposal, an authorized human approves that exact
   proposal/version through the demo's explicit approval path.
4. A narrow action tool validates approval and current preconditions,
   records the transfer request and reserves stock. The agent reports
   the authoritative result, never a simulated success after an error.

An application-level approval boundary is required, not a specific workflow
product. A policy card is sufficient for initial grounding; no vector index,
document ingestion pipeline, MCP server or A2A connection is implied.
The assessment can be one small helper with explicit arithmetic rather than
a graph of calculation executors.

### Proposed Small Synthetic Dataset

All IDs and values below are illustrative and **not yet accepted fixture values**.
Days are relative integer slots, not dates, time zones or working-day calendars.
Currency is a fictional demo cost unit, not an Azure-price estimate.

| Record | Proposed content |
| ------ | ---------------- |
| Product and bill of materials | HUB-1 needs one BOARD-1 per hub; other materials are always sufficient |
| Supplier order and event | Receipt of 40 BOARD-1 changes from day 1 to day 6; update known on day 0 |
| Assembly warehouse W-A | 20 BOARD-1 on hand, no existing reservation in this slice |
| Source warehouse W-B | 80 BOARD-1 on hand, 30 reserved for unrelated commitments, 50 available |
| Customer commitment C-1 | 40 HUB-1 due by end of day 3 |
| Customer commitment C-2 | 20 HUB-1 due by end of day 4 |
| Production dependency | Both commitments need BOARD-1; assembly takes one day after materials are available |
| Transfer option STANDARD | Arrival at W-A on day 2; fixed cost 10 plus 2 per board |
| Transfer option EXPRESS | Arrival at W-A on day 1; fixed cost 10 plus 3 per board |
| Policy P-1 version 1 | Protect both commitments, incremental cost ceiling 100, never borrow existing reserved stock |
| Demo roles | Planner can analyze; authorized approver can approve the exact proposal; no real user data |
| Initial action records | No proposal approval, transfer request or additional reservation exists |

Only the selected component limits production. Capacity is assumed sufficient
to assemble all 60 hubs in the stated one-day lead time. There is no detailed
production schedule, alternative component, purchasing, tax, exchange rate,
order-priority algorithm, split sourcing or partial-order optimization.
These simplifying assumptions must be visible to the audience.

### Proposed Simple Rules and Hand-Checked Walkthrough

The business assessment uses recorded facts, not model-generated quantities.

* Demand is 40 + 20 = 60 boards. The late receipt on day 6 cannot protect
  either day-3 or day-4 commitment.
* Local stock is 20, so the proposed transfer need is 60 - 20 = 40 boards.
  At W-B, available stock is 80 - 30 = 50; a 40-board reservation is allowed.
* STANDARD costs 10 + 2 x 40 = 90, within the ceiling of 100.
  Day-2 arrival plus one assembly day gives day-3 completion for both orders.
* EXPRESS costs 10 + 3 x 40 = 130, above the ceiling. Earlier arrival does
  not override the spending rule.
* STANDARD is therefore the only feasible listed option. The agent explains
  this result; it does not claim global optimality over unmodeled alternatives.
* After approval, create one request for 40 boards and reserve 40 at W-B.
  Source on-hand remains 80; reserved becomes 30 + 40 = 70; available becomes
  10. W-A remains at 20 until an actual receipt, which is not simulated here.
* Repeating the same authorized operation returns the recorded outcome,
  without another request or reservation. A changed payload under the same
  operation identity is rejected.

No human order-priority choice is needed in this example because both orders
are protected together. If no option protects both within the ceiling, report
infeasibility rather than silently sacrificing one customer or inventing a rule.

### Future Demo Cases and Expected Evidence

These are proposed walkthroughs, not executed tests or generated fixture files.
Each variant starts from its own clean scenario, not the preceding case's state.

| Case | Change from the proposed baseline | Expected result |
| ---- | --------------------------------- | --------------- |
| Feasible transfer | None | Explain both affected commitments; propose STANDARD, quantity 40, cost 90; no effect before approval |
| No impact | W-A has 60 rather than 20 boards | Explain sufficient buffer; no transfer, approval request or reservation |
| No feasible stock | W-B has 60 on hand and 30 reserved, leaving 30 available | Need 40 but only 30 available; no feasible full recovery or reservation |
| No feasible cost | Ceiling is 80 instead of 100 | STANDARD 90 and EXPRESS 130 both rejected; no action |
| Missing policy | Ceiling absent | Explain missing constraint; no claim of feasibility and no write |
| Rejected or unauthorized approval | Human rejects, or caller lacks approval authority | No action; explicit rejection/deny, not a model-generated approval |
| Stale proposal | Relevant stock or policy version changes after proposal | Reject old proposal for execution; refresh facts and seek new approval |
| Duplicate operation | Repeat the same already approved operation | Exactly one recorded request, total source reservation 70, available 10 |
| Tool failure | Snapshot, assessment or action result unavailable | Explicit error or unknown outcome; query authoritative result before retrying an uncertain write |

For approval, display source/destination, quantity, option, cost, proposal
version and the stock/policy facts used. Do not require a multi-role enterprise
approval engine for the first demo. The actual identity path, storage and
approval validity interval remain later choices.

### Essential Checks Versus Deliberately Deferred Complexity

Keep the write boundary small: verify caller permission and exact approval;
validate current source stock and proposal versions; prevent duplicate effects;
record a clear request/reservation outcome. The action must not leave a
half-created request presented as complete.

Do not implement distributed sagas, event buses, durable workflow orchestration,
full warehouse lifecycles, production schedulers, forecasting, or real ERP
connectors just to support this story. Storage-level consistency and failure
handling will be designed for the selected small backend, not assumed away.
Reset/cancellation is not an implicit permission to delete or release records.

For later validation, use a small case table with expected states and citations,
plus inspection of model/tool traces. Check the actual request/reservation,
not only the final prose. LLM judges, dashboards and cloud evaluation are
optional later learning topics, not prerequisites for this documentary sketch.
No performance, security certification or production-readiness claim follows.

### S-006 Outcome and Remaining Choice

The sketch ties each interaction to Foundry-agent learning while retaining
the agreed business outcome and thin write boundary. Quantities, costs and
relative timing reconcile by the arithmetic above; this is a manual documentary
check, not a running simulation.
Independent inline arithmetic assertions also passed for baseline demand,
shortage, availability, option costs, assembly timing, reservation totals,
no-impact, and insufficient-stock/cost variants. These check the written
example numbers only; they do not execute an agent, tool, approval or backend.
All 10 repository documentary/link tests passed.

Proposed next discussion: accept or revise this minimal scenario, learning
objectives and simplifying rules before selecting technologies.
The sketch, numbers, starting agent count and tool responsibilities are still
proposals. No executable schema, data file, package, code or cloud resource
was created.

## S-007 Revised Transfer Options

Status: **accepted demo design** by the user's 15:51 +01:00 confirmation
on 2026-11-02, recorded in D-010. The proposal and review history below
is retained; its earlier pending-acceptance statements are superseded by
this confirmation for the synthetic values and simple rules only.
S-007 revision 2 drafted this design.
Q-010 selected two feasible alternatives, not supplier-message extraction
or an additional policy agent. The original thin flow, learning objectives,
stock quantities, demand, one-day assembly assumption and ceiling of 100
remain proposed as before. No extra production or workflow logic is added.

### Revised Example and Learning Benefit

Only the EXPRESS price changes: fixed cost 15 plus 2 per board instead of
the historical fixed 10 plus 3 per board. Both options still transfer 40 boards.

| Option | Cost calculation | Cost | Arrival | Assembly complete | Margin to C-1 day 3 | Margin to C-2 day 4 |
| ------ | ---------------- | ---- | ------- | ----------------- | ------------------ | ------------------ |
| STANDARD | 10 + 2 x 40 | 90 | Day 2 | Day 3 | 0 days | 1 day |
| EXPRESS | 15 + 2 x 40 | 95 | Day 1 | Day 2 | 1 day | 2 days |

Both use 40 of the source's 50 available boards, meet both commitments,
and stay within the proposed ceiling of 100.
EXPRESS spends 5 extra fictional cost units for one additional day of schedule
margin. This is a timing comparison, not a measured reduction in delivery risk
or a reliability guarantee; no probability model is introduced.

The agent now needs to explain two valid options rather than merely reject
an over-budget one. It should cite stock and policy facts, state the
5-unit/one-day trade-off, and ask the planner to select the preferred option.
Protecting dates within a ceiling does not by itself establish how to value
extra margin. Do not silently add a cheapest-first or fastest-first rule,
invent a risk percentage, or label one option uniquely optimal.

The planner's selection becomes part of the exact proposal that the authorized
human approves. Choosing an option and authorizing its execution remain distinct,
even if the eventual demo presents them on one concise screen.
No new role, service, workflow engine or additional agent is required.

### Revised Expected Cases

These are documentary expectations for future tests, not executed tool behavior.
They replace any original expectation that EXPRESS must be rejected at ceiling 100.

| Case | Expected outcome |
| ---- | ---------------- |
| Baseline, ceiling 100 | Present both options, accurate costs and margins; no write before selection and approval |
| Planner selects STANDARD | Proposal binds quantity 40, cost 90, option and source/target; only that approved option may execute |
| Planner selects EXPRESS | Proposal instead binds quantity 40, cost 95 and earlier arrival; source reservation is still only 40 |
| Missing preference | Explain the trade-off and request selection; do not treat ambiguity as approval |
| Ceiling 92 | STANDARD feasible, EXPRESS over budget; explain why the choice narrows |
| Ceiling 80 | Neither feasible; no transfer action |
| No impact or only 30 source boards available | Original no-impact/insufficient-stock results are unchanged |
| Selection changes after approval | A new proposal/version needs new approval; the previous approval cannot authorize it |
| Duplicate, stale or unauthorized operation | Original guarded-action expectations remain unchanged |

For either selected option, a successful future reservation would leave W-B
on-hand at 80, reserved at 70 and available at 10. Destination stock remains
20 until a receipt outside this demo slice. Selecting or approving both
alternatives must not create two transfers for the same recovery proposal.

### Revision Boundary

The user's general acceptance of the idea and Q-010 selection support this
single extension. The revised numbers, detailed selection behavior and case
table are still proposed D-010 details, not accepted implementation requirements.
No other S-006 assumptions are expanded. The final agent count, technology
choices and executable fixtures remain undecided.

All 10 repository documentary/link tests passed after this revision.
Independent inline assertions verified both costs, the 5-unit difference,
completion times, both orders' margins, ceiling variants and reservation
totals. These are checks of the written example, not agent/backend tests.

## S-009 Technical Research Outcome

The [Python path comparison](evidence.md#s-009-revision-2---python-foundry-managed-paths)
recommends a named/versioned managed prompt agent in Foundry with a thin Python
driver, not an independently reasoning agent embedded in the application.
The driver executes bounded functions; Foundry holds the agent configuration.
Hosted remains a valid later learning path for code/runtime/deployment ownership.

The research produced proposed D-012; the user subsequently accepted that
technical direction on 2026-11-02 at 16:36 +01:00. It is not approval of
exact dependency versions, a model or deployment. The accepted Standard/Express
story and simple business rules are unchanged. Cloud evaluation support for
agent targets does not prove execution of our application-side function loop;
that and full trace/approval behavior need later authorized validation.
No implementation, installation, tenant query, resource or paid evaluation ran.
