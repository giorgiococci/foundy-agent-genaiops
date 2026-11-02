---
title: "Logical Architecture Research for supply-chain-resilience"
description: "S-004 comparison, freshly verified official evidence, proposed boundaries, and unresolved design choices."
ms.date: "2026-11-02"
---

## Research Question and Authority

S-004 revision 1 asks which logical architecture best supports the confirmed
smart-home controller-board delay scenario, without selecting a stack.
Q-007 explicitly approved documentary research; the user reconfirmed execution
with "procediamo" on 2026-11-02 at 15:30 +01:00.
See the [contract and execution record](../state.md).

Confirmed inputs are [RQ-001...RQ-010](analysis.md#requirements) and
[D-001...D-007](../decisions.md). The actors are a planner and an authorized
approver, not automatically separate agents. Operational records and
communications remain synthetic. The observable future outcome is either
a justified no-action result or a precisely approved transfer request with
source-stock reservation, not a physical shipment or destination receipt.

All architecture, contracts, controls, and evaluation cases below are research
proposals. No product, implementation, fixture, or numeric threshold is selected.

## Fresh Official Evidence

All entries were directly retrieved on **2026-11-02**. Section names identify
the evidence actually inspected, including bounded excerpts of longer pages.
These are documentary facts, not tenant or runtime verification.
The [source register](../../../../docs/research/sources.md) supplies the broader
baseline; these entries record the fresh checks for this particular step.

### E-01 - Explicit Workflow and State

* Sources: [Workflow concepts](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/)
  and [Workflow state](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/state),
  corresponding to baseline S06 and its linked state guide
* Sections: Workflow APIs; Graph and runtime model; State Visibility and Scope Behavior
* Generation: Microsoft Agent Framework library, not the Foundry visual builder
* Facts: graph workflows connect executors through edges and conditions;
  events and checkpoints expose execution progress. Shared state has
  language-specific visibility semantics.
* Maturity: graph APIs are documented; the Python functional API is explicitly
  experimental. No blanket GA assertion or cross-language parity is inferred.
* Limitation: these concepts do not establish atomicity across external
  inventory writes, approval consumption, and workflow checkpoints.

### E-02 - Orchestration and Human Input

* Sources: [Workflow orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/)
  and [Human-in-the-loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop),
  baseline S07 and its linked guide
* Sections: orchestration pattern table and HITL tip; Overview and request ports
* Generation: Microsoft Agent Framework
* Facts: sequential, concurrent, handoff, group-chat, and magentic patterns
  are documented. Request/response handling allows a workflow to wait for
  external human input; orchestration tools can require approval.
* Maturity: documented capabilities; no overall GA claim from absence of a label
* Limitation: pausing for a response does not itself specify the business
  approver's permissions, proposal version, expiry, or replay policy.

### E-03 - Visual Builder Retirement

* Source: [Build a workflow in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow),
  baseline S08
* Section: opening retirement notice and workflow definition
* Generation: Foundry visual, declarative workflow builder
* Fact and maturity: the page is labeled Preview and announces retirement
  on **2026-12-01**, recommending Microsoft Agent Framework for new workflows.
* Consequence: do not propose this visual builder for new investment.
  This is not a retirement of Agent Framework workflows.

### E-04 - Endpoint Roles and Downstream Identity

* Sources: [Foundry RBAC](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)
  and [Toolbox authentication](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-authentication),
  baseline S10 and S11
* Sections: Scope; Built-in roles; authentication boundaries; auth-type table
* Generation: current Foundry resource/project/agent and Toolbox documentation
* Facts: agent-scope roles are currently evaluated for agent endpoint access.
  Toolbox access identity and downstream user identity are distinct boundaries.
  Project identity, agent identity, OAuth, and user Entra-token modes differ.
* Maturity: documented, not a blanket maturity assertion for each integration
* Limitation: no chosen connector, actual principal propagation, or record-level
  authorization has been tested. Separate prompts do not establish IAM isolation.

### E-05 - Tracing and Sensitive Content

* Sources: [Agent Framework observability](https://learn.microsoft.com/en-us/agent-framework/agents/observability)
  and [Foundry client-side tracing](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-client-side),
  baseline S20 and S18
* Sections: OpenTelemetry Integration; duplication warning; Enable GenAI tracing;
  Enable content recording
* Generation: Framework instrumentation versus Foundry SDK instrumentation
* Facts: Framework emits OTel traces, logs, and metrics. Instrumenting both
  client and agent can duplicate captured information. Content recording
  can include user messages, model outputs, and tool arguments.
* Maturity: Foundry SDK GenAI instrumentation is explicitly experimental preview;
  the Framework page alone does not establish a uniform stability guarantee.
* Limitation: no exporter, cross-service propagation, or full-hop coverage was
  tested. Application audit remains distinct from best-effort diagnostic export.

### E-06 - Outcome and Process Evaluation

* Source: [Agent evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators),
  baseline S21
* Sections: evaluator table; System evaluation; Process evaluation
* Generation: current Foundry evaluation guidance
* Facts: system evaluators assess final outcomes; in multi-agent systems they
  apply to the main orchestrator or final agent. Process evaluators assess
  tool selection, input accuracy, success, and output use.
* Maturity: Task Completion, Task Adherence, Intent Resolution, and composite
  evaluators are marked preview; Quality Grader is deprecated and cannot run.
  Do not assign GA to other rows merely because they lack a preview label.
* Limitation: judging a transcript is not evidence that a stock transaction,
  authorization deny, or idempotency constraint actually held.

### E-07 - Guardrails

* Source: [Guardrails and controls overview](https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview),
  baseline S14
* Sections: opening definition; hosted egress note; agents-versus-models matrix
* Generation: Foundry model and agent controls, with target-specific applicability
* Facts and maturity: agent guardrails are preview; network egress controls
  are preview and apply only to hosted agents. Not all model controls apply
  to agents, and unsupported controls do not take effect for that target.
* Limitation: no guardrail validates this demo's stock ownership or spending
  rules merely by being enabled. No target is selected here.

## Common Logical Flow and Boundaries

The following application design is proposed for all candidates. Product
support for orchestration does not implement these business guarantees for us.

| Stage | Deterministic responsibility | Permissible reasoning contribution |
| ----- | ---------------------------- | --------------------------------- |
| Receive update | Authenticate source, validate known order line and event version, deduplicate | Extract candidate facts from synthetic text, if such input is later selected |
| Read snapshot | Scope access to current inventory, reservations, receipts, dependencies, and policies; retain versions | Identify relevant permitted evidence |
| Assess impact | Compute dependency and time/quantity effects using explicit rules | Explain affected orders and uncertainty |
| Compare recovery | Calculate feasible quantities, lead times, costs, and ceiling compliance | Explain trade-offs among validated candidates |
| Form proposal | Validate referenced candidate and persist immutable version and evidence | Produce a planner-readable recommendation |
| Human decision | Authenticate approver, authorize action and target, record exact proposal version | Explain the requested action, never fabricate approval |
| Execute | Revalidate current stock, dependencies, policy and approval; commit request and reservation with durable outcome | No discretionary write authority |
| Report | Read authoritative result and audit status | Explain the actual outcome, not a guessed success |

Inventory, reservations, supply-demand links, and approved policies are
authoritative operational data. Retrieved manuals or supplier prose are
explanatory or untrusted input, never a substitute for transactional stock.
No component substitution or supplier purchasing is added by this research.
Missing dates, quantities, ceiling, priorities, or timing rules lead to an
explicit incomplete result, not a fabricated feasible plan.

### Logical Capability Contracts

Names below describe responsibilities, not executable schemas or SDK classes.

| Capability | Required evidence and result | Authority boundary |
| ---------- | ---------------------------- | ------------------ |
| Read planning snapshot | Authorized record references, data versions, relevant receipts and reservations | Read-only, filtered by verified caller scope |
| Assess impact | Snapshot/version, explicit dependency and calendar rules; affected or unaffected orders with reasons | Calculation service, not an LLM-generated dependency graph |
| Evaluate transfer options | Authorized source stock, timing, quantities, cost evidence and policy version; feasible, infeasible, or incomplete result | Deterministic eligibility; cannot borrow another order's reserved stock |
| Read policy evidence | Permitted document ID, version, passage, provenance and applicability | Untrusted content cannot change policy or privileges |
| Persist proposal | Validated candidate, targets, versions and rationale references; immutable proposal ID/version | Does not reserve or move inventory |
| Record approval | Verified approver, proposal version, action, scope, validity and usage state | Human decision path, not model-supplied identity or consent |
| Execute approved transfer | Exact proposal/approval, current preconditions and idempotency identity; durable outcome | Restricted executor; no arbitrary query, target URL, or general write tool |
| Read execution outcome | Operation identity and authoritative request/reservation status | Scope-checked reconciliation, not permission to retry a write blindly |

All contracts need bounded inputs/results, contract versions, deadlines, and
distinct unauthorized, invalid, insufficient-data, infeasible, conflict,
unknown-outcome, and failed statuses. A run/trace ID is correlation, not authority.
MCP and A2A are not prerequisites for these logical capabilities.

### State, Failure, and Recovery

* Bind approval to the immutable proposal, action, targets, data/policy versions,
  authenticated approver, validity, and usage state. Recheck permissions at execution.
* Reject stale proposals after relevant stock, receipt, dependency, or policy
  changes; recompute and obtain new approval rather than editing approved content.
* Define an atomic business boundary for request creation, reservation,
  approval consumption, idempotency result, and durable audit intent. The
  storage/transaction mechanism remains a later design choice.
* If that boundary cannot be atomic in the chosen system, design explicit
  pending/reconciliation states before implementation; never report a partial
  request or reservation as complete. Compensation and reservation release
  require their own authorized lifecycle, not an invented rollback promise.
* For a timeout after submission, query the durable operation outcome before
  retrying. Same key and payload recover the same authorized result;
  same key with changed payload is rejected. Concurrent requests must not
  over-reserve stock or consume one approval twice.
* Diagnostic-export failure must be visible. Durable business audit is part of
  the commit boundary; an unavailable required audit path cannot be bypassed.
* Set future bounds for calls, fan-out, retries, runtime, and spend. No numbers
  from generic lab guides are adopted as this project's requirements.

## Three Candidates on the Same Requirements

### A - Single Agent with Bounded Tools

One reasoning agent chooses permitted read/calculation tools, explains impact,
and submits a validated proposal. An external approval/execution gate enforces
the common rules; this baseline is not an unrestricted autonomous writer.
It can cover the full business slice with minimal agent decomposition.
Its variable tool sequence increases the importance of process evaluation
and explicit stop conditions. It remains the mandatory comparison baseline.

### B - Explicit Workflow with One Reasoning Agent

Application stages enforce event validation, snapshot and impact calculations,
candidate evaluation, proposal validation, human approval, execution, and audit.
One reasoning agent explains grounded results and trade-offs at bounded points.
No agent call is required to manufacture a proposal for a no-impact event.
The workflow can be ordinary application orchestration; E-01/E-02 illustrate
a possible library mapping, not a selected framework or hosting service.

This adds state/transition design but makes the critical business path inspectable
and less dependent on model-selected sequencing. It best fits the current fixed
process; calculational correctness still depends on future domain specifications.

### C - Controlled Workflow with Specialized Agents

Retain B's deterministic stages and executor. A policy-evidence specialist
produces bounded cited findings; a recovery-advisory specialist explains the
validated impact and candidates. Neither gets unconstrained stock-write access.
Keep dependent work sequential; only genuinely independent evidence branches
could run concurrently, with bounded fan-out and a validated join.

Specialization may reduce irrelevant context if policies become numerous or
genuinely heterogeneous. Today no such requirement or measured advantage exists.
A second model opinion is not independent business validation or an IAM boundary.
Conflicting or missing evidence must produce review/incomplete status rather
than a majority vote authorizing a transfer.

### Comparative Trade-offs

These are qualitative engineering assessments, not benchmarks or price estimates.

| Dimension | A: single agent | B: workflow, one agent | C: workflow, specialists |
| --------- | --------------- | --------------------- | ------------------------ |
| Build complexity | Fewest agent components; guard services still required | Explicit stage/state logic | B plus specialist contracts, joins and context routing |
| Controllability | Gate controls effects; model selects read/tool trajectory | Predetermined critical path and exits | Predetermined outer path, more probabilistic internal transitions |
| Quality risk | Missed tool step or broad context | Incorrect domain rules or misleading explanation | B risks plus conflicting evidence and cross-agent distortion |
| Latency | Variable repeated tool/model turns | More predictable placement of reasoning, not necessarily faster | Additional serial turns; parallelism helps only independent work |
| Cost | Variable tokens/retries | Bounded reasoning opportunities; implementation effort remains | Extra prompts, transfers, evaluation and telemetry |
| Testability | Final state plus tool trajectory | Stage invariants and end-to-end gates | B tests plus specialist and join contracts |
| Mixed-audience demo | Simple assistant narrative | Clear fact-to-impact-to-approved-action story | Explains specialization only if its benefit is observable |

### Requirements Traceability

| Requirement | Common obligation | A evidence to collect | B evidence to collect | C evidence to collect |
| ----------- | ----------------- | --------------------- | --------------------- | --------------------- |
| RQ-001 | Handle a connected exception, not only answer questions | Correct end-to-end tool trajectory | Correct stage transitions | Correct specialist integration and same outcome |
| RQ-002 | Mixed audience | Grounded business explanation with technical trace | Same, with stage view | Same, without hiding additional handoffs |
| RQ-003 | Credible event and downstream dependency | Uses authoritative impact calculation | Enforced impact stage | No specialist invents dependencies |
| RQ-004 | Synthetic data; no implicit cloud permission | Same isolated records | Same records and gates | Same records, no extra data exposure |
| RQ-005 | No APIM; security, operations and RAI | External authorization and audit | Same plus stage-level diagnostics | Same plus per-specialist scope/trace checks |
| RQ-006 | Single-step guidance and explicit approvals | No operational authority from this research | Same | Same; runtime agents are not development delegates |
| RQ-007 | Bounded manufacturing chain | Same explicit bill of materials | Same dependency model | Same model shared through validated results |
| RQ-008 | Controller-board delivery-date delay | No added cancellation/quantity scenario | Same event validation | Same event interpretation at all boundaries |
| RQ-009 | Protect committed dates within a ceiling | Only validated feasible candidates | Explicit feasibility stage | Specialists cannot override ceiling or ranking rules |
| RQ-010 | Human-approved request and reservation | Common deterministic executor | Same executor | Same executor, no specialist approval privilege |

## Evaluation, Observability, and Responsible AI

Use the same future synthetic fixtures, domain rules, tool contracts, permission
scope, model configuration where comparable, and outcome rubric for A/B/C.
Record any intentional differences. Measure correct affected-order sets,
feasible-candidate precision, explanation grounding, abstention, forbidden
effects, duplicate effects, latency, model/tool calls, tokens, and total cost.
Report denominators, repeated-run variability, and failures. Thresholds, sample
sizes, budgets, models and cloud evaluators are not selected here.

E-06 supports separating outcome and process evaluation. Judge scores supplement,
not replace, deterministic assertions on actual state. C needs additional
specialist-output and join tests; do not assume the final evaluator covers them.
No measured superiority is established by this research.

| Future case | Required observable outcome in all three candidates |
| ----------- | -------------------------------------------------- |
| Delay absorbed by buffer | Explain no impact; no transfer proposal, approval, or reservation |
| Impact and feasible transfer | Correct dependent orders and feasible candidate; effect only after valid approval |
| No feasible transfer | Explain failed constraints; no invented stock, overspend, or alternative write |
| Missing ceiling or dependencies | Explicit incomplete/clarification outcome; no claimed optimal recovery |
| Stale approval | Changed relevant data invalidates old proposal; zero effects under that approval |
| Unauthorized user or target | Server-side deny; no prohibited reads, writes, or leaked evidence |
| Duplicate and concurrent request | At most one request/reservation for the approved operation; no over-reservation |
| Timeout or partial failure | Reconcile authoritative status; no success-shaped fallback or blind replay |
| Instruction hidden in supplier/policy text | Treat as untrusted data; no privilege, policy, or destination changes |
| Telemetry or explanation mismatch | Detect missing diagnostics and false success; preserve durable business audit |

Instrument stages, model/tool calls, policy decisions and commit/reconciliation
outcomes with correlated run/proposal/operation versions. Separate elapsed
human-approval waiting from processing latency. Preserve explicit failures
and avoid duplicate token accounting. Keep content capture off; use minimized
synthetic evidence and never export credentials or hidden reasoning.
E-05 documents possible instrumentation, not verified coverage or a selected backend.

Supply-chain-specific RAI risks include overstated delivery certainty, moving
shortage to an unrelated customer, opaque prioritization, and operator overreliance.
Show facts, assumptions, infeasibility and actual execution status separately.
Order priority and acceptable trade-offs require human-defined business rules;
personal attributes and unconstrained model preference must not determine allocation.
E-07 controls can supplement, not replace, authorization and business constraints.
The generic support-ticket examples in the local RAI guide are not adopted here.

## Recommendation and Open Decisions

Propose **B**, an explicit workflow with one reasoning agent, as the first logical
design direction. Retain **A** as the same-capability baseline.
Keep **C** as a conditional experiment, justified only by a specific evidence
need and demonstrated quality, capability-isolation, or controllability benefit
that outweighs extra complexity and cost.
See proposed [D-008](../decisions.md#d-008---controlled-workflow-as-a-design-candidate).

The reason is the fixed business sequence and transactional approval boundary,
not a claim that one model is always better than multiple models.
Agent Framework graph workflows are an illustrative documented mapping;
the retiring visual Foundry builder is not recommended.
No language, SDK version, model, runtime, hosting, database, protocol,
network profile, Azure service, or integration is selected.

Before detailed design, resolve or explicitly defer:

* Whether the user accepts B, A as baseline, and C as conditional rather than mandatory
* Bill of materials, dependency/calendar rules, quantities, dates, spending
  ceiling, order priorities and tie-breakers
* Approver authority, validity, separation of duties, cancellation and release lifecycle
* Authoritative snapshot/version and atomicity or reconciliation strategy
* Demo duration, operational budget, performance targets and measurable comparison gates

After later stack selection, separately verify region/model/tool/network
compatibility, SDK maturity, identity propagation, tenant quota/capacity,
pricing and actual telemetry coverage. None was queried here.

## Provenance and Validation Boundary

Research was performed directly by the principal without delegation.
Local inputs were the effective tracking, knowledge map, research method,
source register, and platform/orchestration/security/observability/GenAIOps/RAI
guides. Public fetches sent only documentation URLs, not repository contents.

A guessed checkpoint URL returned HTTP 404. The linked Workflow concepts and
State pages were then retrieved successfully; no unavailable page is cited as
evidence. The inspected material supports workflow state/checkpoints, not
exactly-once external writes.

Acceptance is documentary: the three alternatives cover the same requirements,
logical boundaries and failure cases, with explicit recommendation and limits.
Repository structural/link checks are recorded in [state](../state.md).
No code, executable schemas, fixtures, tenant access, paid evaluations,
runtime tests, integrations, provisioning, deployment, IAM changes, commits,
or pushes occurred.

## S-009 Revision 2 - Python Foundry-Managed Paths

Authority: Q-012 returned `approve-python-foundry-comparison` on 2026-11-02.
This is a public documentary comparison, not approval of a stack, installation
or deployment. Q-011's external-agent option was not executed.
Inputs are accepted D-008...D-011 and the
[two-option demo](analysis.md#s-007-revised-transfer-options).
The earlier S-004 research above remains historical, not a second current design.

### Fresh Technical Evidence

Access date for all checks: **2026-11-02**. The principal performed the research
directly without delegation. Only public documentation URLs were fetched;
no repository code, tenant data, subscription or credentials were submitted.
Existing same-day prompt-agent creation and function-calling checks from
[Q-011](../questions.md#q-011-clarification-evidence) were reused, then the
Python function-loop example and the other relevant sections were inspected.

#### E-08 - Managed Prompt Agent and Python Tool Execution

* Sources: [Create a prompt agent](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent)
  and [Use function calling](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling)
* Sections: Install packages and authenticate; Create a prompt agent;
  Create an agent with function tools, Python Prompt Agents sample
* Generation: Foundry projects new, Azure AI Projects 2.x; not Projects 1.x/classic
* Facts: Python creates a named agent version through `AIProjectClient` and
  `PromptAgentDefinition`. The version is a server-side Foundry resource.
  The model requests a named function; Python executes it and returns
  `function_call_output` in the same conversation.
* Requirements observed: prompt quickstart specifies `azure-ai-projects>=2.3.0`;
  authentication uses `azure-identity`. These are documented sample requirements,
  not an exact tested dependency set or selected model.
* Maturity: documented path; these excerpts do not establish blanket GA
  for all models, tools, identity modes or related features.
* Limitation: an executable Python tool dispatcher and its business checks
  still belong to the application. Portal-only configuration is insufficient
  for editing custom function definitions according to the function guide.
* Pitfall: that guide's tab labeled Hosted Agents demonstrates an ephemeral
  in-process `FoundryChatClient` agent. The label is not evidence that the
  sample deploys a hosted agent. That excluded path is not a candidate here.

#### E-09 - Actual Hosted Runtime and Version Lifecycle

* Source: [Hosted agents](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents),
  baseline S03
* Sections: When to use hosted agents; How it works; Agent identity and endpoint;
  Versioning; Observability; Scaling and right-sizing; Pricing
* Generation: Foundry Agent Service hosted runtime, not a generic container service
* Facts: custom code runs in an Agent Service sandbox backed by a container
  image, with dedicated agent identity and endpoint. Protocol libraries
  provide server/health/OTel support; the framework is not mandated.
  Agent versions are immutable and the endpoint routes to one version at a
  time, with 100% of traffic; native splitting is not supported in this guide.
* Operational distinction: compute scales per session. Runtime billing is based
  on CPU and memory consumed across active sessions, in addition to other
  solution costs. No pricing rate, cost estimate or budget was queried.
* Maturity: hosted behavior is documented; overall hosted-runtime GA is not
  established by these excerpts. A2A protocol GA/preview labels do not establish
  the status of the entire runtime.
* Limitation: session persistence and a durable state store do not implement
  the demo's approval transaction, stock consistency or exactly-once effect.
  Default instrumentation is not proof every custom business stage is traced.

#### E-10 - Python Hosted Source Deployment Requirements

* Source: [Deploy your first hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-hosted-agent),
  baseline S04
* Sections: Prerequisites, Python; Python Steps 1...5; azd source-deployment explanation
* Facts: the Python SDK deployment path requires an existing project and model;
  it does not provision them. The sample packages source, uses
  `create_version_from_code` with remote dependency resolution, waits for an
  active version and explicitly routes the endpoint before invoking it.
  A local Docker build is not required by this source-upload sample; the
  deployed hosted runtime is still container-backed.
* Requirements observed: local Python 3.13+, `azure-ai-projects>=2.3.0`,
  `python-dotenv`, Azure CLI authentication and documented development tools.
  The shown remote build specifies `runtime="python_3_14"`.
  Local interpreter prerequisite and remote runtime are different settings.
* Maturity: a documented Python sample, not proof of every dependency's GA
  or interoperability. No exact package/protocol lock set was resolved.
* Lifecycle pitfall: the sample's finalizer restores previous routing and
  deletes the temporary agent version. It is a validation deployment, not
  a keep-running demo deployment script. Persistent routing and cleanup
  would need separately approved lifecycle choices.
* Limitation: nothing was cloned, installed, built, deployed or invoked.

#### E-11 - Tracing Coverage and Python Requirements

* Sources: [Foundry client-side tracing](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-client-side),
  baseline S18; hosted Observability in E-09
* Sections: Language-specific prerequisites; Enable GenAI tracing;
  hosted built-in observability
* Facts: client-side instrumentation can expose the Python driver and
  custom tool logic. The tracing guide specifies Python 3.10+ and
  `azure-ai-projects>=2.0.0` for that tracing example, plus exporter packages.
  This does not lower E-08's prompt sample requirement of Projects >=2.3.0
  or E-10's hosted deployment interpreter requirement.
* Maturity: Foundry SDK GenAI instrumentation is explicitly experimental preview
  and requires opt-in. E-05's sensitive-content and duplicate-span cautions apply.
* Limitation: no exporter or end-to-end hop coverage was tested. Keep content
  capture off, correlate proposal/action outcomes and verify custom stages later.

#### E-12 - Evaluation Options, Not Automatic Tool Execution

* Sources: [Evaluation overview](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-overview),
  [Evaluate models and agents](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/cloud-evaluation-targets)
  and [Evaluate your hosted agent](https://learn.microsoft.com/en-us/azure/foundry/observability/quickstarts/quickstart-evaluate-hosted-agent)
* Sections: evaluation approaches; Evaluate an agent target; hosted quickstart
  overview and prerequisites
* Facts: documentation supports existing-output datasets and runtime agent
  targets. The target guide documents both prompt and hosted agents, optional
  explicit agent versions and structured output mappings for tool context.
  Hosted Responses targets share the shown target pattern; Invocations differs.
* Maturity: the hosted quickstart explicitly marks the azd evaluation experience
  preview. Evaluator-specific preview/deprecation distinctions remain as in E-06.
* Important gap: these target examples do not demonstrate running our local
  Python function dispatcher during a cloud evaluation of the prompt agent.
  Generic prompt-agent target support is not proof the entire custom-tool
  scenario works unattended. Do not promise that integration.
* Proposed initial learning method: run approved cases through the real driver
  when implementation is separately authorized, assert business states, and
  inspect synthetic outputs/tool traces. Evaluate recorded outputs or investigate
  a supported target integration later under its own cost/access approval.
* Limitation: no dataset upload, judge-model invocation or paid evaluation ran.

#### E-13 - Managed Agent Versus Channel Publication

* Sources: [Agent Service overview](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)
  and [Publish to Copilot and Teams](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot)
* Sections: Choose how to build; opening publication explanation and prerequisites
* Facts: Foundry runs prompt agents and hosts code agents. Teams/Microsoft 365
  publication is a further operation using a stable endpoint, with extra
  permissions/resources and data-handling implications.
* Consequence: learning a real Foundry agent does not require adding a Teams
  channel, Azure Bot Service or Microsoft 365 integration to this demo.
  Creating a version is not synonymous with publishing to a channel.
* Limitation: endpoint activation and consumer access still need explicit
  design and checks for whichever path is later selected.

#### E-14 - Permission Boundaries

* Source: [Hosted agent permissions reference](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agent-permissions);
  E-04 remains the current RBAC/Toolbox baseline
* Sections: opening permission classes and least-privilege guidance
* Facts: developer, project and agent permissions are separate; ARM control
  permissions and Foundry data-plane permissions are not interchangeable.
* Generation caveat: this reference advertises classic-and-new coverage.
  Use the new quickstart for current sample/API shape and verify operation-specific
  role definitions rather than transplanting a classic example.
* Limitation: no actual assignment or token propagation was inspected.
  Neither managed agent identity nor endpoint access supplies planner/approver
  business authority automatically.

### Same Demo, Two Runtime Ownership Models

| Aspect | Managed prompt agent plus Python driver | Python hosted agent |
| ------ | --------------------------------------- | ------------------- |
| Agent exists in Foundry | Named/versioned prompt-agent resource | Deployed/versioned hosted-agent resource |
| Model-driven reasoning | Foundry agent uses configured model/instructions/tools | Python agent code/framework calls the model inside hosted runtime |
| Python responsibility | Invoke agent, dispatch bounded function calls, approval and demo state | Agent implementation plus tools, approval/state integration and runtime dependencies |
| What the learner sees first | Foundry agent resource, tools, conversations and evidence | Hosted version, endpoint, code/runtime behavior and deployment lifecycle |
| Custom business logic | Small Python functions; not a second external agent | Same simple checks can execute in hosted code or a backend |
| Need for Agent Framework | Not required for the documented prompt SDK loop | Optional; hosted protocol libraries are framework-agnostic |
| Setup burden | Project/model/access and driver dependencies | Same plus source/build/protocol/deployment/routing and runtime configuration |
| Operations and costs | Inference, observability and any chosen application/data services | Same plus active-session CPU/memory, build/image and runtime lifecycle |
| Primary extra learning value | Managed agent behavior and application/tool boundary | Managed code hosting, agent identity, custom control and deployment |
| Main learning risk | Mistaking Python function execution for an external agent; forgetting caller in evaluations | Spending the increment on packaging and runtime plumbing instead of agent behavior |

This is a qualitative assessment, not a measured setup-time/cost comparison.
The driver must not become an independently reasoning code-only agent.
For both paths, the same accepted STANDARD/EXPRESS comparison and essential
permission/approval/stock/idempotency boundaries remain in force.

### Learning Objectives Mapped to Both Paths

| Objective | Prompt path | Hosted path | Remaining application responsibility |
| --------- | ----------- | ----------- | ------------------------------------ |
| Instructions and agent versions | Configure the server-side prompt-agent version | Version code/instructions with the hosted artifact | Record resolved configuration, not just a friendly agent name |
| Tool use | Observe function call and returned output in conversation | Observe framework/custom loop invoking bounded tools | Validate arguments, scope results and report explicit errors |
| Grounding | Read synthetic policy P-1 through a function | Same policy tool in hosted code | Cite exact policy/data versions; no search service required |
| Compare recovery | Agent explains two validated feasible options | Same outcome under code-defined agent behavior | Deterministic numbers; no invented cost-versus-margin priority |
| Human approval | Driver/application stops before guarded action | Hosted application must preserve the same boundary | Authenticate approver, bind exact selection/version, reject stale approval |
| Execute and report | Narrow action function returns authoritative outcome | Narrow action in code/backend returns same outcome | At most one request/reservation; never report destination receipt |
| Tracing | Client/tool spans complement Foundry traces | Hosted protocol OTel plus custom-stage instrumentation | Test actual coverage, privacy and cross-boundary correlation |
| Evaluation | Driver-led cases and state assertions; cloud custom-tool gap remains | Deployed target evaluation is documented; state assertions still needed | Judge scores cannot prove permission, stock correctness or idempotency |

### Recommendation for the Next Decision

Propose the **managed prompt agent created/versioned in Foundry, with a thin
Python driver**, as the first learning increment.
This satisfies the user's Foundry-managed preference without putting an
independently reasoning agent in the app. It prioritizes Foundry agent
configuration, model-driven tool calls, conversations, grounded explanations,
approval and telemetry over infrastructure work.

Keep the hosted path as a later, separately approved learning increment when
we explicitly want to learn code-agent deployment, runtime identity,
session behavior, custom framework control or server-side encapsulation.
It is a valid Foundry path, not an inferior product; the current thin business
flow does not itself require that extra ownership.
No automatic migration or extra agent is assumed.
See proposed [D-012](../decisions.md#d-012---managed-prompt-agent-with-a-thin-python-driver).

### Outstanding Checks and Scope Limits

* The user has not selected a technical path or approved implementation.
* A later bounded spike must verify full tool-loop handling, structured outputs,
  approval/resume behavior, denied/stale/duplicate actions and trace coverage.
* Python/SDK/server/protocol/exporter exact versions need a compatible,
  tested dependency set. Observed lower bounds are not a lockfile.
* The function guide mixes historical run-expiry/setup language with new
  Responses examples and an ephemeral sample under a hosted tab. Use the
  relevant new prompt-agent example, not tab names or old run semantics, as
  the basis for later API validation.
* Samples include endpoint placeholder differences and end-of-sample cleanup.
  Use the actual project endpoint when separately authorized; do not generate
  one by guessing a hostname. Do not copy cleanup into a persistent demo.
* Model, region, networking, data store, application entry point, runtime
  identities, access, retention, actual quota and price/budget remain unselected
  or unverified. No tenant query, authenticated catalog or price lookup ran.
* Exact portal behavior for executing application-side custom functions,
  complete cloud evaluation of that loop, and consumer endpoint activation
  are not proven by this research. Explicitly test rather than promise them.
* Source deployment's current Python runtime requirements do not imply that
  the prompt-agent client must use that same hosted runtime.

Acceptance is documentary: both paths are mapped to the same learning goals,
the platform/application split is explicit, prerequisites and maturity are
recorded, and the recommendation remains proposed.
Checks and closure are recorded in [state](../state.md).
No code, fixture, package, cloud resource, IAM assignment, deployment,
paid evaluation, commit or push was created or run.

### Post-Research Technical Decision

On 2026-11-02 at 16:36 +01:00, the user explicitly accepted the managed
prompt-agent/Python-driver direction in D-012. The recommendation and
pending-decision wording above describe the research-time status; this later
acceptance supersedes that status, not its evidence gaps.
The next proposed activity is documentary planning only. No package set,
model, region, environment, implementation or cloud action is approved.
