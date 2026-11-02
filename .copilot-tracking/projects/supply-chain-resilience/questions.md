---
title: "Questions and Answers for supply-chain-resilience"
description: "Progressive answers and open business-scenario questions for supply-chain discovery."
ms.date: "2026-11-02"
---

## Translation Provenance

English summaries of Italian user answers are labeled translations.
They are not verbatim English quotations. A selected domain is not
approval of the assistant's initial scenario or architecture.

## Q-001 - Supply Chain Direction

* Date and phase: 2026-11-02, discovery
* Reason and affected decisions: choose the domain before designing the demo
* Question: which of the three directions should be explored?
* Alternatives and recommendation: supply chain, travel disruption, factory
  quality, or more ideas; supply chain was recommended
* Status: answered
* User answer, faithful translation: the supply-chain theme is appealing.
  The realism of the described event is uncertain; consider an agentic
  system integrated into the supply chain to manage unexpected events.
* Interpretation: select the domain only; validate the event and operating
  context before treating the initial story as agreed.
* References: [pre-project Q-001](../../discovery/use-case-selection.md#q-001---direction-to-explore),
  RQ-001, D-001
* Supersession: none; no initial scenario was approved

## Q-002 - Audience

* Date and phase: 2026-11-02, discovery
* Reason and affected decisions: calibrate business storytelling and technical depth
* Question: who is the demo intended for?
* Alternatives: technical, business/presales, mixed, or unknown
* Status: answered
* User answer: mixed
* Interpretation: show a clear business process with optional technical
  drill-down; this does not set a duration, budget, or technology.
* References: [pre-project Q-002](../../discovery/use-case-selection.md#q-002---audience),
  RQ-002, D-002
* Supersession: none

## Q-003 - Operating Context

* Date and phase: 2026-11-02, discovery
* Reason and affected decisions: define the business dependencies and
  meaningful actions before designing agents or infrastructure
* Question: which supply-chain context should anchor the demo?
* Alternatives: manufacturing, retail/distribution, transport/logistics,
  or still undecided
* Recommendation: manufacturing if richer supply-to-demand dependencies
  are desirable; distribution if a simpler, broadly understandable
  stock-to-customer story is preferable. No answer is inferred.
* Status: answered on 2026-11-02
* User answer: manufacturing
* Interpretation: use a manufacturing context; no specific product, event,
  recovery action, architecture, or implementation is approved.
* References: RQ-003, S-002 revision 1
* Supersession: none

## Q-004 - Concrete Product and Event

* Date and phase: 2026-11-02, discovery, S-003 revision 1
* Reason and affected decisions: define the business dependency and event
  before modeling data or designing agents
* Question: which concrete manufacturing scenario should anchor the first demo?
* Alternatives: smart-home hubs with delayed controller boards; furniture
  with a reduced panel delivery; industrial pumps with delayed motors;
  or a custom scenario
* Recommendation: smart-home hubs with delayed controller boards, because
  a compact bill of materials makes the component-to-customer chain visible
  without industrial equipment or a large production model.
* Status: answered on 2026-11-02
* User answer: `smart-home-delayed-boards`
* Interpretation: smart-home hubs with delayed controller boards is the
  selected first business scenario. Detailed product specifications,
  quantities, dates, and a launch campaign are not selected.
* References: RQ-003, RQ-007, proposed D-003, S-003 revision 1
* Supersession: none

## Q-005 - Business Priority

* Date and phase: 2026-11-02, discovery, S-003 revision 1
* Reason and affected decisions: delivery dates, incremental cost, and
  inventory buffer can conflict; do not silently invent a ranking objective
* Question: which business objective should drive the recovery comparison?
* Alternatives: protect committed customer dates within a spending ceiling;
  minimize incremental cost while accepting explicit delays; or present
  trade-offs for the planner without an automatic ranking
* Recommendation: protect committed customer dates within a spending ceiling.
  The ceiling, prioritization rules, and fixture values remain to be agreed.
* Status: answered on 2026-11-02
* User answer: `delivery-with-cost-cap`
* Interpretation: protect committed customer dates within a spending ceiling.
  No amount, prioritization rule, or optimization algorithm is approved.
* References: RQ-001, S-003 revision 1
* Supersession: none

## Q-006 - Permissible Demo Action

* Date and phase: 2026-11-02, discovery, S-003 revision 1
* Reason and affected decisions: define a visible but bounded outcome
  without silently introducing an external procurement or production action
* Question: which action may the future demo support after human approval?
* Alternatives: create a transfer request and stock reservation in the demo
  system; create an alternate-supplier purchase-request draft in that system;
  or keep the first demo read-only
* Recommendation: a transfer request with a stock reservation, limited to
  authorized, available demo stock; no physical shipment or real commitment.
* Status: answered on 2026-11-02
* User answer: `transfer-and-reservation`
* Interpretation: the future demo may create an approved transfer request and
  reserve authorized, available stock in the demo system. This does not
  authorize implementation, execution, Azure provisioning, or physical movement.
* References: RQ-004...RQ-006, S-003 revision 1
* Supersession: none

## S-003 Outcome

Q-004...Q-006 were answered through the structured form. The defaults above
were recommendations when asked; the actual returned selections are now
recorded explicitly. See [D-003 and D-005...D-007](decisions.md).
S-003 revision 1 business discovery is completed; its authorization is consumed.
No architecture, implementation, or cloud step is authorized by these answers.

## Q-007 - Logical Architecture Research Scope

* Date and phase: 2026-11-02, discovery-to-research boundary, S-004 revision 1
* Reason and affected decisions: agree the research boundary before comparing
  architectures; preserve D-001...D-007 and RQ-001...RQ-010 without treating a
  business capability as operational authorization.
* Proposed question: approve S-004 revision 1 as specified in the
  [step contract](state.md#proposed-s-004-revision-1-contract), revise its scope,
  or defer research?
* Alternatives: approve documentary comparison only; revise the comparison
  or outputs; defer the activity.
* Recommendation: compare the single-agent baseline, a controlled workflow
  with one reasoning agent, and a justified multi-agent candidate before
  choosing a stack. Keep deterministic business checks and authorization
  separate from model reasoning in every candidate.
* Status: answered on 2026-11-02 through native `ask_user`
* User answer: `q007=approve-documentary-research`; `scope_notes` was empty.
* Interpretation: explicit approval of the unchanged S-004 revision 1
  documentary-research contract only. This is not architecture acceptance
  or implementation, cloud, or delegation authorization.
* References: D-001...D-007, RQ-001...RQ-010, S-004 revision 1
* Supersession: none

### Q-007 Submission Retry on 2026-11-02

At 15:25 +01:00, the user asked to submit Q-007 through `ask_user`, reported
a successful capability test, and explicitly stated that the test does not
approve S-004 (faithful English translation of the Italian request).
This is not an answer to Q-007.

Checks: the supplied read-only principal snapshot permits `ask_user`; the
[capability guide](../../../docs/engineering/copilot-guide.md#structured-questions-and-confirmations)
records the reported successful test. The current callable inventory exposes
neither `ask_user` nor tool discovery. No call was possible or attempted.
The question remains open and unsubmitted, not refused or cancelled.
S-004 revision 1 is unchanged and no research has started.

### Q-007 Native Submission Preparation on 2026-11-02

The user again requested Q-007 through `ask_user` and explicitly excluded
approval of S-004 from the successful capability test (faithful English
translation). The current callable inventory exposes native `ask_user`.
This supersedes the earlier tool-availability blocker for this session,
without changing the historical retry record or the research contract.
Q-007 is open pending the actual form response. No research has started.

### Q-007 Structured Answer on 2026-11-02

Native `ask_user` returned `approve-documentary-research`, with no scope notes.
The selected Italian option explicitly approved only documentary research
under S-004 revision 1. The form presented the objective, alternatives,
local outputs, exclusions, checks, costs/risks, prerequisites, and recovery
strategy of the unchanged [contract](state.md#proposed-s-004-revision-1-contract).
This actual response, not the capability test, is the consent reference.
S-004 is approved but has not started. This turn ends after the requested
question submission and answer recording; no research results are claimed.

### Q-007 Execution Reconfirmation and Research Result

On 2026-11-02 at 15:30 +01:00, the user said "procediamo", reconfirming
execution of the single unchanged S-004 revision 1 research step.
This is not acceptance of a resulting architecture recommendation.
The [research comparison](research/evidence.md) now records the three candidates
and proposes D-008 without changing accepted D-001...D-007.
No new business answer, quantitative value, or implementation authorization
is inferred. Closure and documentary validation are recorded in [state](state.md).

## Q-008 - Learning-First Orchestration Direction

* Date and phase: 2026-11-02, logical design, S-005 revision 2
* Reason: RQ-011 and RQ-012 explicitly prioritize Foundry-agent learning
  over deterministic workflow complexity. Clarify sequencing before design.
* Question: prefer a thin explicit flow with one reasoning agent, an agent-led
  flow with bounded tools, or defer the choice?
* Alternatives: a few fixed stages with reasoning/tool use inside the agent;
  agent-selected read/analysis tool sequence with an external approval/write
  gate; or revise/defer. Both use synthetic data and simple business rules.
* Recommendation: a thin explicit flow, not a general workflow engine;
  preserve meaningful agent reasoning/tool use and only essential write checks.
  Agent-led sequencing offers more autonomy to study but a less predictable trace.
* Affected decisions: proposed D-008, accepted D-009; RQ-001...RQ-012
* Scope: choose and record a logical direction only, in state, questions,
  decisions and analysis; no implementation, stack selection, cloud operations,
  paid evaluations, fixtures or delegation.
* Checks, risk and recovery: consistent boundaries and documentary/link tests;
  no cloud cost. Revise the proposal if the user chooses differently;
  retain earlier research and answers.
* Status: answered on 2026-11-02 through native `ask_user`
* User answer: `q008=thin-flow`; `notes` was empty.
* Interpretation: accepts only the narrowed logical direction in D-008,
  under D-009's learning-first constraints. The form did not select a final
  agent count or authorize implementation or cloud activity.
* Consent: the selected form option applies to S-005 revision 2's logical
  choice and tracking only; no defaults or user notes were inferred.

## Q-009 - Minimal Demo Design Scope

* Date and phase: 2026-11-02, design, S-006 revision 1
* Reason: present the complete documentary step contract before producing
  the minimal design; preserve D-008/D-009 and learning-first requirements.
* Question: approve the minimal design sketch only, revise scope, or defer?
* Alternatives: one compact design with learning objectives and proposed
  synthetic examples; revise the outputs; defer.
* Recommendation: one compact sketch in the existing analysis, including
  visible agent interactions, a small dataset, simple rules, and a short
  future validation walkthrough. All new quantities and rules remain proposals.
* Affected decisions: D-008/D-009 and RQ-001...RQ-012; no stack or final agent
  count is approved by approval of this activity.
* Scope: update research/analysis, questions, state and decisions if a new
  proposal is needed. No new design file, executable fixture, code, package,
  stack selection, authenticated access, spending, Azure operation or delegation.
* Checks and acceptance: show the learning outcome of each interaction;
  internally reconcile proposed stock, shortage, cost and timing values;
  cover no-impact, feasible, infeasible and rejected/duplicate action paths;
  run repository documentary/link tests without claiming runtime validation.
* Risk, prerequisites and recovery: no Azure cost; prerequisite is the current
  learning-first direction. Main risk is reintroducing ERP complexity;
  revise only the proposal and preserve historical requirements and answers.
* Status: answered on 2026-11-02 through native `ask_user`
* User answer: `q009=approve-minimal-design`; `notes` was empty.
* Interpretation: approves production and documentary verification of the
  S-006 revision 1 proposal only. No proposed number, business rule, stack,
  fixture, or implementation is accepted by this activity approval.

### Q-009 Activity Outcome

S-006 revision 1 produced the
[minimal sketch](research/analysis.md#s-006-minimal-demo-sketch) and proposed D-010.
All 10 repository documentary/link tests and independent arithmetic assertions
for the written example passed. No agent/backend or approval runtime was run.
The activity is completed and consent consumed; acceptance of the resulting
sketch and its numbers remains a separate decision.

## Q-010 - One Modest Learning-Oriented Extension

* Date and phase: 2026-11-02, design, proposed S-007 revision 2
* User clarification, faithful translation: the idea is acceptable, but
  make it slightly more complex. This accepts the general direction, not
  an unspecified extension or implementation.
* Reason: "slightly more complex" has several meaningful interpretations;
  select one bounded learning objective rather than expand the ERP logic.
* Question: add two feasible recovery choices, an unstructured supplier
  message, or a bounded policy specialist?
* Alternatives: cost-versus-delivery-margin reasoning; fact extraction and
  validation from synthetic text; or a read-only policy specialist that
  supplies cited policy findings to the recovery agent.
* Recommendation: two feasible options with different costs and delivery
  margins, because this creates a real agent explanation task without
  adding infrastructure or a complex planning algorithm.
* Affected decisions: D-010 remains a proposal pending the selected revision;
  D-008/D-009 and RQ-011/RQ-012 remain effective.
* Step contract: choose one extension and draft its revised logical sketch
  in the existing analysis; update state, questions and decisions only.
  New example numbers and detailed rules remain proposals for review.
* Exclusions: code, executable fixtures, stack/API selection, packages,
  tenant access, Azure operations, costs, deployment and development delegation.
  A proposed runtime specialist is not authorization to launch a subagent.
* Checks and acceptance: preserve the thin approval/action boundary, identify
  the learning benefit and revised expected cases; check any changed example
  arithmetic and repository documentary/link tests. No runtime claims.
* Cost, risk and recovery: no Azure consumption. Add only the selected
  extension; preserve the original sketch and revert the proposal's direction
  through documented revision if it distracts from learning.
* Status: answered on 2026-11-02 through native `ask_user`
* User answer: `q010=two-feasible-options`; `notes` was empty.
* Interpretation: select only the cost-versus-delivery-margin extension and
  authorize its documentary sketch under S-007 revision 2. Neither message
  extraction nor a policy specialist is selected. Revised numbers remain proposals.
* Outcome: revised sketch and proposed D-010 details recorded; all 10
  documentary/link tests and arithmetic checks passed. S-007 revision 2
  completed; activity consent consumed, no implementation authorized.

### Revised Sketch Accepted After Q-010

On 2026-11-02 at 15:51 +01:00, the user said "si va bene. procediamo"
in direct response to the revised two-option example and its pending
acceptance. This confirms D-010's simplified design and numeric rules.
It is a free-form answer to the presented proposal, not a native form result.
No implementation or technology choice follows from this acceptance.

## Q-011 - Foundry Technical-Path Research Scope

* Date and phase: 2026-11-02, proposed S-009 revision 1
* Reason: compare technical paths against the accepted learning-first design
  before choosing language, runtime or hosting.
* Question: approve a public documentary comparison, revise scope, or defer?
* Alternatives: managed prompt agent with application-executed tools;
  code-defined agent running locally against Foundry; hosted code agent
  only if a concrete learning benefit justifies the extra deployment.
* Language comparison: inspect Python and .NET requirements and sample parity;
  no language is selected by this research approval.
* Recommendation: favor the smallest path that makes agent tool use, grounding,
  human approval, tracing and evaluation visible; distinguish service learning
  from framework/application-code learning.
* Outputs: extend research/evidence; update state, questions, analysis and
  proposed decisions as needed. No new standalone planning document.
* Exclusions: code, packages, executable fixtures, SDK installation, authenticated
  catalog/subscription queries, quota/price checks in a tenant, Azure resources,
  IAM, deployment, paid evaluations, APIM, commits, pushes and delegation.
* Checks and acceptance: official sources freshly verified for Foundry generation,
  API/package requirements and feature maturity; map each path to D-010 and
  RQ-011/RQ-012, compare setup burden and learning coverage; identify gaps,
  verify citations/local links and run repository documentary tests.
* Cost, prerequisites and recovery: no Azure consumption, accepted D-010 input;
  label unavailable evidence and previews explicitly, avoid selecting a path
  on unsupported assumptions. Preserve earlier evidence rather than overwrite it.
* Status: deferred on 2026-11-02; clarification requested through native `ask_user`
* User answer, faithful translation: option 1 is unclear. Does it mean the
  agent is integrated into the application rather than published/deployed
  in Foundry? The user does not want that path without a strong justification.
* Notes, faithful translation: prefers Python to .NET.
* Interpretation: no research approval. Explain that a managed prompt agent
  is persisted/versioned in Foundry while custom function code may execute
  in the caller; distinguish this from a code-only external agent.
  Revise the research scope around Python and Foundry-managed agent paths
  before requesting any new authorization.
* Approval: none; a free-form clarification request is not one of the
  approval options and is not treated as consent.

### Q-011 Clarification Evidence

Only the documentation necessary to answer the user's distinction was checked
on 2026-11-02; the proposed technical comparison has not started.

* [Prompt agent quickstart](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent),
  Foundry projects new, Create a prompt agent: creates a server-side agent
  version with a name, ID, model and instructions. This is not a definition
  that lives only in the calling application.
* [Function calling](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling),
  opening definition and Create an agent with function tools: the agent
  requests a function call, the application executes the function and returns
  its result. Client-side tool execution does not make the prompt agent external.
* Limitation: this checks only that conceptual distinction. No SDK installation,
  complete package compatibility, global maturity, deployment/publication
  lifecycle, or tenant availability is validated by these excerpts.

The local [development guide](../../../docs/knowledge/development.md#prompt-agent-path)
already makes the same distinction. D-011 records Python and Foundry-managed
agent priority. Next proposal: S-009 revision 2 comparing Python prompt and
hosted agent paths, with an application-only agent excluded unless separately
justified and agreed. No approval is inferred from this explanation.

### Q-011 Clarification Acknowledged

On 2026-11-02 at 15:56 +01:00, the user acknowledged the distinction with
"ok perfetto va bene". This confirms understanding of the explanation and
the Python/Foundry-managed direction, not approval of an unpresented revised
research contract or implementation.

## Q-012 - Python Foundry-Managed Path Comparison

* Date and phase: 2026-11-02, research proposal, S-009 revision 2
* Reason: replace Q-011's ambiguous three-path scope with the clarified
  Python preference and Foundry-managed agent priority in D-011.
* Question: approve documentary comparison of managed prompt versus hosted
  agents, revise scope, or defer?
* Alternatives: Python client with a persisted/versioned Foundry prompt agent
  and explicit application-side function execution; Python code deployed as
  a Foundry hosted agent. External/code-only agents are excluded.
* Recommendation method: compare learning coverage and minimum setup for
  accepted D-010, rather than automatically prefer code-first or containers.
* Scope and outputs: freshly inspect official public sources for agent
  creation/versioning, tool execution, approval boundaries, tracing/evaluation,
  Python SDK/runtime requirements, maturity and deployment prerequisites.
  Append evidence and a reasoned recommendation to research/evidence; update
  state, questions, analysis and proposed decisions as needed.
* Exclusions: code, executable schemas or fixtures, package installation,
  authenticated access, tenant/region/quota/price queries, provisioning,
  IAM, deployment, paid evaluations, APIM, commits, pushes and delegation.
  No subscription, environment or cloud operation is targeted.
* Acceptance and checks: map both paths to the same learning objectives and
  accepted two-option scenario; distinguish platform features from application
  responsibilities; record URLs, access dates, generation, maturity and gaps;
  validate citations, metadata, local links and repository documentary tests.
  No runtime or actual tenant-availability result may be claimed.
* Cost/risk and recovery: no Azure consumption; risks are stale/mixed-generation
  documentation and setup complexity eclipsing agent learning. Preserve prior
  records, label uncertain evidence, and stop affected conclusions if unsupported.
* Prerequisites: accepted D-008...D-011 and explicit consent to this revision.
  The resulting recommendation is proposed, not a final stack decision.
* Status: answered on 2026-11-02 through native `ask_user`
* User answer: `q012=approve-python-foundry-comparison`; `notes` was empty.
* Interpretation: approves only the S-009 revision 2 public documentary
  comparison and checks. No stack, runtime, implementation or cloud operation
  is approved by this answer.

### Q-012 Research Result

The [technical comparison](research/evidence.md#s-009-revision-2---python-foundry-managed-paths)
maps both Foundry-managed paths to the accepted learning goals and recommends
the managed prompt agent with a thin Python driver as proposed D-012.
This is not acceptance of that path. Current source evidence identifies
runtime/sample lifecycle pitfalls and an unresolved custom-function cloud
evaluation integration; no tenant or runtime checks were executed.
Validation and activity closure are recorded in [state](state.md).

### Technical Recommendation Accepted After Q-012

On 2026-11-02 at 16:36 +01:00, the user confirmed the immediately preceding
managed prompt-agent recommendation with "perfetto procediamo cosi"
(ASCII transcription of the Italian free-form answer).
This accepts D-012's technical direction. It is not a new native form result
and does not change Q-012's historical research-only approval.
No implementation, spike, package installation, authenticated tenant access,
provisioning or deployment is authorized.
The next proposal is a bounded documentary implementation plan, not execution.
