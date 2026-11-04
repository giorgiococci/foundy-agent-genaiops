---
title: "Decisions for supply-chain-resilience"
description: "Confirmed business scope and boundaries of the supply-chain demo."
ms.date: "2026-11-04"
---

## D-017 - Shared Tracing and Explicit Per-Agent Content

* Status: accepted in Q-034; implemented locally under S-034 revision 1
* Date: 2026-11-04
* Authority: user's cross-agent observability request and explicit synthetic
  content/bounded live-validation choices
* Decision: one shared OTel provider and Azure Monitor trace exporter, with
  task-local off/metadata/content policy. The advisor owns its policy.
  CLI export is off unless explicitly selected.
* Privacy: keep native process-global sensitive recording disabled.
  Capture only selected synthetic turn/tool content under the active agent
  scope, with bounded size, known-key redaction and allowlisted exported
  attributes. Do not export arbitrary events, exception text, instructions,
  raw sessions, credentials or tracking documents.
* Simplicity: reuse native framework agent/model/tool spans; one application
  turn parent includes validation and correlation. No business-agent base
  class, registry, plugin system, second agent or new telemetry resource.
* Lifecycle: discover the existing project's linked destination without
  exposing its connection string; flush on success/error and explicitly
  report delivery failures without retrying model/business operations.
* Dependencies: OTel SDK 1.45.1 and Azure Monitor exporter 1.0.0b58 (beta),
  compatible with the approved framework generation.
* Alternative rejected: toggle framework sensitive settings per agent,
  which would leak policy across concurrent agents in this SDK generation.
* Evidence: [A-022](implementation/log.md#a-022---s-034-shared-per-agent-observability)
  and the [implementation sources](../../../docs/research/sources.md#shared-tracing-implementation-follow-up).

## D-016 - Direct Microsoft Agent Framework Runtime

* Status: accepted in Q-029 and implemented locally under S-030 revision 1
* Date: 2026-11-03
* Authority: user's explicit direct-migration/no-legacy request, followed by
  Q-029's compatible-dependency and new-branch consent
* Decision: use `FoundryAgent` for the existing named/versioned managed agent.
  Agent Framework owns invocation and continuation; remove the handwritten
  generic loop rather than retaining a selectable fallback.
* Ownership: D-012's managed-agent choice, D-014's per-agent packages and
  D-015's current/historical evidence remain. This replaces D-013's generic
  custom-loop implementation choice, not its agent-led behavior or prompt lifecycle.
* Business safeguards: selection/approval remain external application events.
  Middleware validates the complete batch before dispatch, accounts for each
  service call, and stops on fatal function failures without a settlement
  request. Domain/store transactions remain source-independent.
* Binding/persistence: explicit version lookup and non-preview versioned
  `agent_reference`; native `AgentSession` serialization in a new format.
  No silent latest-version substitution or historical-run migration.
* Dependencies: approved Projects 2.7.0 with framework core 1.24.0, Foundry
  1.16.0 and OpenAI adapter 1.18.0; preserve declared dependency bounds.
* Alternatives rejected: retain both loops; disguise a direct-model local
  agent as the managed agent; weaken safeguards to fit a sample.
* Scope: local/offline integration only on `feat/agent-framework`; no UI,
  AG-UI, actual second agent, cloud access/publication/inference or Git publication.
* Evidence: [S-030 API findings](research/evidence.md#s-030---installed-framework-api-and-safety-verification)
  and [A-019](implementation/log.md#a-019---s-030-direct-agent-framework-migration).

## D-013 - Agent-Led Conversation and Prompt-as-Code

* Status: accepted for the local unpublished S-024 revision 1 candidate
* Date and evidence: 2026-11-03,
  [S-023 review](research/evidence.md#s-023---agent-led-design-and-prompt-lifecycle-review)
* Requirements: RQ-011...RQ-014, user's explicit learning/organization concern
* Recommendation: one managed Foundry agent conducts the case, with a generic
  Python function loop and trusted external approval; separate definition,
  text instructions, runtime, tool contracts, business rules and scenario data.
* Alternatives: keep the current fixed-flow driver; refactor to this bounded
  agent-led path; adopt a hosted/harness runtime. Recommend the middle option,
  with no extra framework or runtime migration.
* Prompt lifecycle: Git-tracked stable instruction file, explicit configuration,
  hashes and release provenance; versioned synthetic evaluation cases; later
  authorized publication creates/verifies the matching Foundry definition.
  No mandatory Prompty/Prompt flow or automatic optimizer.
* Behavior: agent may explain or conditionally recommend a trade-off, but
  cannot replace planner selection or exact human approval with its own text.
* Consequences if accepted: revise D-008's fixed sequencing, not D-009's
  learning priority or D-012's managed-agent choice. Preserve old positive
  evidence and run state; candidate remains unpublished until authorized.
* Consent: the analysis request did not authorize implementation. The user's
  subsequent 2026-11-03 16:22 +01:00 "procedi" explicitly confirms the single
  proposed S-024 local increment. No new cloud execution is authorized.
* Outcome: local candidate implemented and offline-verified in
  [A-015](implementation/log.md#a-015---s-024-revision-1-agent-led-local-candidate);
  S-024 consent consumed. Managed cloud v2 is unchanged.

## D-014 - Per-Agent Packages with Shared Solution Capabilities

* Status: accepted for local S-025 revision 1 with Q-023 ownership clarification
* Date: 2026-11-03, user's 16:34 +01:00 clarification
* User intent, faithful English summary: organize the repository to accommodate
  several agents in a multi-agent solution, although only one is implemented now.
* Recommendation: group the advisor's definition, instructions and specialized
  conversation controls under `supply_chain/agents/resilience_advisor`.
  Keep advisor-specific tool schemas/dispatch in that package. Retain the
  common runtime, reusable store/domain operations and solution data outside
  agent packages; group evaluation cases by agent. Do not create a shared-tool
  package without an actual shared capability.
* Boundary: this prepares source ownership, not a working multi-agent runtime,
  isolated identities, delegation or new deployed agents. Keep the existing
  application session advisor-specific rather than inventing a generic registry.
* Alternatives: flat single-agent files; per-agent packages with shared
  capabilities (recommended); a plugin/registry/orchestrator framework (defer).
* Consequences: move code/assets, repair imports/links, include nested source
  files in provenance, preserve exact published instruction content and behavior.
* Implementation authority: Q-023 explicitly confirms S-025's local structural
  increment with the above tool-ownership clarification. No cloud publication,
  new runtime agents or additional scope is authorized.
* Outcome: implemented and locally verified in
  [A-016](implementation/log.md#a-016---s-025-revision-1-multi-agent-ready-source-layout).
  Local S-025 consent consumed; only one advisor and no new orchestrator.

## D-015 - Current Versus Historical Evidence and One Active Driver

* Status: accepted and locally implemented in S-027 revision 2
* Date and authority: 2026-11-03, Q-028 and the user's explicit cleanup request
* Problem: genuine pre-write tool results in S-026's final answer were rejected
  after cache invalidation, even though the current post-write result was present.
* Decision: the application separates exact known historical tool objects
  from exact current objects; the current result and a post-write lookup
  remain mandatory. Historical evidence is not current stock or execution proof.
* Alternative: omit historical objects entirely. The user selected keeping
  separately labeled history for before/after explanations.
* Boundary: keep the model's existing two-key response contract and unchanged
  published prompt/schema/definition. Python adds `historical_evidence` to
  the delivered answer; it does not prescribe the agent's reasoning order.
* Source cleanup: retire unused read-only/staged execution paths and factories,
  move useful safety regression coverage onto the current runtime/advisor,
  and preserve manual business tools, prompt assets and actual run evidence.
* Consequences: one managed-agent CLI; no legacy-driver compatibility facade.
  Old runs remain stopped/read-only; source drift is not silently rebound.
* Validation and limitations: see
  [A-018](implementation/log.md#a-018---s-027-revision-2-evidence-separation-and-legacy-retirement).
  Local regression success does not supersede S-026's failed live acceptance
  or authorize another cloud case.

## Scope and Evidence

These are business-scope decisions, not implementation or deployment approvals.
The [question register](questions.md) retains the actual answers and their
interpretations. Dates below refer to 2026-11-02.
The [analysis](research/analysis.md) retains context and proposal history.
No operational authorization follows from an accepted business requirement.

## D-001 - Supply Chain Domain

* Status: accepted
* Requirements and answers: RQ-001, Q-001
* Alternatives: supply chain, travel disruption, factory quality, or more ideas
* User decision: explore supply-chain exception management.
* Evidence of consent: Q-001, a labeled translation of the actual user answer
* Consequences: investigate a connected operational process, not a standalone
  question-answering assistant. The initial launch story was not selected.
* Supersedes / superseded by: none

## D-008 - Controlled Workflow as a Design Candidate

* Status: accepted only in the learning-first, thin-flow form confirmed by Q-008
* Date and step: 2026-11-02, S-004 revision 1
* Requirements and answers: RQ-001...RQ-010; Q-007 approves research only
* Alternatives: A, one agent with bounded tools; B, explicit workflow with
  one reasoning agent; C, controlled workflow with specialized agents
* Recommendation: B as the first logical design direction, A as the
  same-capability baseline, and C only as a justified later experiment
* Rationale: the confirmed process has a fixed dependency and human-approval
  sequence. Deterministic impact, feasibility, authorization, and transaction
  checks matter more than introducing an agent per business role.
* Evidence: [S-004 research](research/evidence.md), including E-01...E-07
  and its requirements traceability and qualitative comparison
* Consequences if accepted: design explicit state transitions and narrow
  capabilities, keeping write authority outside model reasoning.
  Acceptance would not choose a stack, approve a plan, or authorize implementation.
* Limitations: no performance/cost benchmark or multi-agent advantage measured;
  business parameters and transaction/approval details remain unresolved
* User decision and consent: Q-008 `thin-flow` on 2026-11-02; accepts the
  narrowed logical direction below, not the full production-oriented control
  discussion or an implementation. Q-007 and "procediamo" authorized research only.
* Supersedes / superseded by: none; D-001...D-007 remain unchanged

### D-008 Scope Qualification on 2026-11-02

The user's 15:36 +01:00 clarification supports proceeding only with the
learning-first constraints in D-009. Do not treat the broad S-004 workflow
discussion as a requirement to build production-grade orchestration.
The exact thin-workflow versus agent-led direction remains open in Q-008.
The original research recommendation above is retained as history.

### D-008 Thin-Flow Acceptance

Q-008 returned `thin-flow`, with no notes. The user selected a small explicit
analysis/proposal, human-approval, and demo-action flow. Reasoning and bounded
tool use remain inside the agent; essential permission, approval,
stock-availability and duplicate-prevention checks stay outside model discretion.
No general workflow engine or production ERP logic is required.
This confirms the logical shape, not a final agent count, framework, stack,
runtime, plan, executable fixture or implementation.
The single-agent baseline and conditional treatment of specialization remain
research guidance; any concrete additional agent needs a learning objective.

## D-009 - Learning-First Demo with Simplified Business Logic

* Status: accepted as an explicit user constraint
* Date and source: 2026-11-02, user's 15:36 +01:00 clarification
* Requirements: RQ-011 and RQ-012; reinforces synthetic-data RQ-004
* User statement, faithful translation: the demo's goal is training on
  Foundry agents; too much deterministic-workflow complexity defeats that
  purpose. The demo will use synthetic data and simplified logic.
* Consequences: prioritize visible agent capabilities and a small business
  slice, not ERP fidelity or infrastructure sophistication. Do not introduce
  a general optimizer, factory scheduler, or durable orchestration platform
  solely to make the demo realistic.
* Boundaries: simplification does not authorize implementation, fabricate
  successful outcomes, remove human approval, or permit invalid reservations.
  Exact agent count, sequencing, technologies and numeric rules remain open.
* Alternatives: production-fidelity workflow versus learning-first bounded demo;
  the user explicitly prefers the latter
* Supersedes / superseded by: none; qualifies proposed D-008 without changing
  the accepted business capabilities in D-001...D-007

## D-010 - Minimal Demo Sketch

* Status: accepted for the revised two-option demo design on 2026-11-02
* Date and step: 2026-11-02, S-006 revision 1
* Requirements and authority: RQ-001...RQ-012, accepted D-008/D-009;
  Q-009 authorizes drafting only
* Proposal: [minimal demo sketch](research/analysis.md#s-006-minimal-demo-sketch)
  with agent-led analysis inside a thin proposal/approval/action flow,
  one product/component, two warehouses, two customer commitments and two
  transfer options
* Learning focus: bounded tools, policy grounding, understandable proposal,
  external human approval, guarded action, traces and outcome checks
* Alternatives: this compact scenario versus a larger manufacturing model;
  starting with one reasoning agent versus adding an unproven specialist
* Recommendation: start compact; accept example rules explicitly before
  fixtures or technology selection. Add agents only for a named learning benefit.
* Limitations: acceptance covers the revised synthetic values and simple rules,
  not a final agent count, tool/API schema, implementation or stack.
  Only arithmetic and documentary consistency checked, no runtime validation.
* User decision: the user's 15:51 +01:00 "si va bene. procediamo" explicitly
  accepts the immediately preceding revised example and rules. Q-009 and Q-010
  alone had authorized drafting, not acceptance of these resulting details.
* Supersedes / superseded by: none; accepted decisions and historical research retained

### D-010 Revision Request

On 2026-11-02 at 15:47 +01:00 the user accepted the general idea and requested
a slightly more complex demo (faithful English translation).
The original sketch remains historical; Q-010 asks which single extension
should be drafted. Do not treat this request as acceptance of all numeric
details, an arbitrary extra agent, or permission to implement.

### D-010 Revised Proposal After Q-010

Q-010 returned `two-feasible-options`, with no notes. S-007 revision 2 drafts
only that extension in the [revised options](research/analysis.md#s-007-revised-transfer-options).
The proposed comparison is STANDARD at 90 with zero C-1 schedule margin versus
EXPRESS at 95 with one extra day, both within ceiling 100.
The planner selects; the system does not invent a cost-versus-margin priority.
The earlier EXPRESS-at-130 example is historical, not the current proposal.
D-010 remains proposed at the detailed-design level; the selected extension
does not authorize implementation, a second agent, or supplier-message ingestion.

### D-010 Acceptance of the Revised Sketch

On 2026-11-02 at 15:51 +01:00, the user confirmed the immediately preceding
STANDARD/EXPRESS proposal and asked to proceed. This is a free-form confirmation,
not an invented structured-form response.
The accepted reference is the [S-007 revised sketch](research/analysis.md#s-007-revised-transfer-options):
60-board demand, 20 local, 40 to transfer, 50 available at source;
STANDARD costs 90 and completes assembly on day 3, EXPRESS costs 95 and
completes on day 2, both within ceiling 100.
The planner chooses the cost-versus-margin trade-off; human approval binds
that exact choice. The original 130-cost EXPRESS example remains superseded.
Acceptance is of the simplified demo design, not proof it runs, a technology
selection, fixture creation, deployment, or a request for another agent.

## D-011 - Python Preference and Foundry-Managed Agent Priority

* Status: accepted as user preferences and a research-scope constraint
* Date and source: 2026-11-02, actual Q-011 free-form answer and notes
* User preference, faithful translation: prefers Python over .NET.
  Does not want an agent integrated only into the application rather than
  published/deployed in Foundry unless there is a strong justification.
* Consequences: focus the next proposed technical comparison on Python and
  Foundry-managed agent paths; an external code-only path requires an
  explicit rationale and user decision, not an automatic baseline choice.
* Open distinction: explain persisted/versioned agent configuration versus
  where custom tool code executes; no specific Foundry runtime is selected.
* Authorization: none to research or implement; Q-011 requested clarification,
  not execution. No new research step has started.

## D-012 - Managed Prompt Agent with a Thin Python Driver

* Status: accepted on 2026-11-02
* Date and step: 2026-11-02, S-009 revision 2 under Q-012
* Inputs: accepted D-008...D-011; RQ-001...RQ-012 and Python preference
* Alternatives: a managed Foundry prompt agent with Python function dispatcher;
  a code-defined Python agent deployed in Foundry's hosted runtime
* Recommendation: managed prompt agent for the first learning increment;
  consider hosted only for a separately agreed runtime/deployment learning goal
* Evidence: [technical research](research/evidence.md#s-009-revision-2---python-foundry-managed-paths),
  E-08...E-14, including shared learning coverage and application responsibilities
* Rationale: a real named/versioned Foundry agent, meaningful tool/grounding/
  approval/observability learning, without initially owning a hosted-code lifecycle
* Boundary: the Python driver executes functions but is not an independent
  code-only reasoning agent. Business approval and state checks remain required.
* Gaps: custom-function execution during direct cloud evaluation, exact package
  compatibility, full traces and endpoint activation need a bounded later spike
* User decision: "perfetto procediamo cosi" at 16:36 +01:00, confirming
  the immediately preceding managed prompt-agent recommendation
  (ASCII transcription of the Italian free-form confirmation).
  Q-012 itself authorized research only.
* Consequences: this is the technical direction for the first learning
  increment. A bounded plan is the next proposal, not automatic
  implementation, cloud access, deployment, installation or spike execution.
* Supersedes / superseded by: none; the accepted demo design is unchanged

### D-012 Acceptance Boundary

The user explicitly accepted the recommendation after the research result.
Foundry holds the named/versioned prompt agent; the Python driver executes
bounded functions and preserves the external approval/write checks.
Hosted remains a potential later learning activity, not an authorized migration.
No exact interpreter/SDK set, model, region, endpoint, data store or application
entry point is selected by this confirmation. The evidence gaps above remain
open and must be addressed through later separately authorized increments.

## D-002 - Mixed Audience

* Status: accepted
* Requirements and answers: RQ-002, Q-002
* Alternatives: technical, business/presales, mixed, or unknown
* User decision: mixed audience.
* Evidence of consent: Q-002
* Consequences: explain business impact first and offer technical drill-down.
  Demo duration and UI implementation are not decided.
* Supersedes / superseded by: none

## D-003 - Delayed Component Receipt

* Status: accepted for a confirmed delivery-date delay only
* Requirements and answers: RQ-003, RQ-008, Q-004
* History: initially proposed as a purchase-order date or quantity change;
  Q-004 selects the date-delay scenario for controller boards.
* Alternatives: delayed boards, reduced furniture-panel quantities, or delayed motors
* User decision: a supplier delays controller boards for smart-home hubs.
* Evidence of consent: Q-004 selection `smart-home-delayed-boards`
* Sources and limitations: the [domain source](../../../docs/research/sources.md#demo-discovery-supporting-sources)
  documents delayed receipts and downstream dependencies, not this custom
  scenario's implementation or results.
* Consequences: link a known supplier order line to inventory, production,
  and customer commitments. Exact dates and quantities remain undefined.
  Quantity reduction and cancellation are not additional approved scenarios.
* Supersedes / superseded by: none; the original proposal was narrowed, not executed

## D-004 - Manufacturing Context

* Status: accepted
* Requirements and answers: RQ-007, Q-003
* Alternatives: manufacturing, distribution, transport/logistics, or undecided
* User decision: manufacturing.
* Evidence of consent: Q-003
* Consequences: model a bounded component-to-production-to-customer chain,
  not a complete ERP, factory scheduler, or industrial-control system.
* Supersedes / superseded by: none

## D-005 - Smart-Home Hubs

* Status: accepted
* Requirements and answers: RQ-008, Q-004
* Alternatives: smart-home hubs, furniture, industrial pumps, or a custom scenario
* User decision: smart-home hubs with delayed controller boards.
* Evidence of consent: Q-004 selection `smart-home-delayed-boards`
* Recommendation adopted: a small electronic product supports a readable bill
  of materials and dependency chain.
* Consequences: use fictional products, suppliers, components, and documents.
  Product specifications and the detailed bill of materials remain open.
* Supersedes / superseded by: none

## D-006 - Delivery Protection Within a Spending Ceiling

* Status: accepted as a qualitative objective
* Requirements and answers: RQ-009, Q-005
* Alternatives: protect committed dates within a ceiling; minimize added cost
  with explicit delays; or show trade-offs without automatic ranking
* User decision: protect committed customer dates within a spending ceiling.
* Evidence of consent: Q-005 selection `delivery-with-cost-cap`
* Consequences: cost cannot be ignored to rescue every order. Explain
  infeasibility when no candidate satisfies the constraints.
  The ceiling amount, order prioritization, tie-breakers, and ranking
  algorithm are not approved or defined.
* Supersedes / superseded by: none

## D-007 - Approved Transfer Request and Stock Reservation

* Status: accepted as a future demo capability
* Requirements and answers: RQ-010, Q-006
* Alternatives: transfer request with reservation; alternate-supplier
  purchase-request draft; or read-only analysis
* User decision: create a transfer request and reserve stock in the demo
  system after human approval.
* Evidence of consent: Q-006 selection `transfer-and-reservation`
* Consequences: the write must be limited to authorized, available demo stock.
  It does not physically ship goods, issue a real purchase order, operate
  machinery, or move stock reserved for unrelated customer commitments.
  Inventory remains reserved at the source until a separately defined
  transfer lifecycle advances it; a request is not a completed movement.
* Residual questions: approval rules, state transitions, cancellation,
  reservation release, and persistence technology require later design.
* Supersedes / superseded by: none
