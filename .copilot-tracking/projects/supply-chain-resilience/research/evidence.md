---
title: "Logical Architecture Research for supply-chain-resilience"
description: "S-004 comparison, freshly verified official evidence, proposed boundaries, and unresolved design choices."
ms.date: "2026-11-05"
---

## Demo Reader MFA Prompt Guidance

* Date: 2026-11-05
* User report, faithful English summary: login requests MFA although the
  user believes it is disabled. This is not verified policy evidence.
* Sources retrieved 2026-11-05:
  [per-user MFA state](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userstates),
  [security defaults](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults),
  [MFA sign-in reporting](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-reporting).
* Evidence: Disabled in per-user MFA does not disable Conditional Access
  or security-default requirements. Security defaults require all users
  to register; registration and an MFA challenge are different events.
  Sign-in authentication details and Conditional Access results help
  identify the actual requirement.
* Recommendation: keep MFA enabled for the two demo readers. Diagnose the
  actual event before considering any separately approved policy change.
* Boundary: public/local reads only; no tenant policy/log inspection,
  security-default/Conditional Access change or MFA bypass performed.

## S-047 - Blocked Directory User Creation

* Date: 2026-11-04
* Authority: Q-050/S-047 revision 1; A-032 is blocked.
* Preflight succeeds for approved operator/tenant, verified domain, absent
  proposed accounts and empty existing SharePoint reader groups.
* Actual result: first Graph create returns HTTP 403
  Authorization_RequestDenied. Second create is not attempted. Read-back
  confirms both aliases still absent and groups 10/11 unchanged.
* Current-operator role evidence: successful, non-paginated transitive
  directory-role GET returns Global Reader only. This is not sufficient
  evidence of User Administrator; SharePoint site-owner access does not
  confer directory administration.
* Source [LE10](../../../../docs/research/sources.md#le10---entra-test-user-provisioning)
  documents User Administrator as the least-privileged role for user
  creation, in addition to appropriate Graph client permissions.
* Boundary: no privilege grant/activation, consent, account switch, license,
  membership or user creation occurred. No PIM eligibility was established.
  Unused credentials remain encrypted locally; contents are not evidence.

## S-046 - Executed SharePoint Knowledge Setup

* Date: 2026-11-04
* Authority: Q-049/S-046 revision 1; completed A-031.
* Actual evidence: exactly one ready site at the approved target; two empty
  site-local reader groups; unique folder ACLs matching the approved matrix.
  General reads groups 10/11; Restricted Procurement reads group 11 only.
  Full Control remains with owners. Four Word files inherit these ACLs.
* Content evidence: all four remote word/document.xml hashes exactly match
  the approved local bodies. Whole ZIP bytes changed during SharePoint
  processing and their separate remote hashes/lengths are retained in
  [A-031](../implementation/log.md#a-031---s-046-sharepoint-knowledge-site-provisioning).
* Verification channel: authenticated same-owner browser GET after Graph
  CLI read-back returned Forbidden. No broadened scopes, tenant/account
  changes, new consent or privileged credential fallback.
* Boundary: source-side configuration only. No assigned non-admin readers,
  actual two-user trimming test, Search/index readiness, citations, Foundry
  connection, live inference or OBO integration is established.
* Sources: [LE08-LE09](../../../../docs/research/sources.md#le08---sharepoint-site-provisioning).

## S-045 - Targeted SharePoint Preflight

* Date: 2026-11-04
* Authority: Q-047 selects drafts_and_targeted_readonly_preflight for the
  user-identified demo tenant. No SharePoint write or consent approved.
* Verified: Azure CLI active tenant equals the authorized tenant.
  Graph GET /v1.0/sites/root?$select=id,webUrl succeeds and returns
  <https://mngenvmcap946525.sharepoint.com>. Do not derive a site URL solely
  from an onmicrosoft.com account suffix.
* Failure: a read-only request to that host's /_api/web for Url, Title and
  EffectiveBasePermissions cannot obtain/use SharePoint authentication;
  CLI reports Unauthorized/invalid_request and interactive authentication.
  No logout/login, broad consent or privileged fallback was attempted.
* Alternative: integrated browser opened the verified host, which redirects
  to the specified tenant's Microsoft sign-in page. User interaction is
  required. Admin status and site-creation/ACL capabilities are not proven.
* Available tools: Azure CLI and PowerShell; no m365 executable or installed
  PnP.PowerShell/SharePoint Online management module was found. None installed.
* Public source: [LE08](../../../../docs/research/sources.md#le08---sharepoint-site-provisioning).
  Describes modern communication and non-group-associated team site REST
  creation; it does not prove access with the current credential.
* User requested group creation. Prefer two site-local groups to avoid
  unnecessary directory objects. Exact site, groups, reader membership,
  source ACLs and operational consent remain open.
* After Q-048 sign-in: browser same-origin GET succeeds and the expected demo
  account matches. Root CurrentUser.IsSiteAdmin is false; this does not prove
  or disprove tenant administrator eligibility. No privileged fallback.
* Proposed site status: read-only SPSiteManager status returns SiteStatus=0,
  SiteUrl empty, after explicitly requesting OData v4 JSON. No existing site
  has been adopted and no site creation/write capability has been tested.
* Local corpus verification is recorded in
  [A-030](../implementation/log.md#a-030---s-045-synthetic-sharepoint-corpus-and-preflight);
  it does not demonstrate source permissions, indexing or OBO behavior.

## S-043 - Executed Data-Driven Readability

* Date: 2026-11-04
* Authority: Q-045/S-043 revision 1; D-021 records the data/prompt separation.
* Local evidence: validated context, fixed calendar mapping, explicit currency
  and labels survive SQLite/proposal/read-back. Alternate dates (including a
  leap day), USD and different labels preserve quantities, costs and margins.
  Missing context does not create calendar dates or a currency. Changed or
  tampered context invalidates proposal/approval as appropriate.
* Prompt inspection/test: generic writing principles, no synthetic IDs,
  specific date, names or currency. Human-question Markdown reaches the
  existing CopilotKit renderer. Offline browser confirms lists, supplied EUR
  dates/labels, native continuation, reload and mobile layout.
* Current API check:
  [AgentsOperations.create_version](https://learn.microsoft.com/en-us/python/api/azure-ai-projects/azure.ai.projects.operations.agentsoperations?view=azure-python#azure-ai-projects-operations-agentsoperations-create-version).
  Fetched 2026-11-04; page updated 2026-10-08. Matches installed Projects
  2.7.0 operation signature; draft candidates are separately marked preview
  in that reference. This activity publishes a normal release version.
* Actual cloud evidence: exactly one version, v5, retrieved and compared to
  the complete local definition; model and eight tool schemas unchanged.
  Zero inference requests. No resource/IAM/account changes or old-case writes.
* Validation: 164 related Python tests, 16 frontend tests, three actual
  offline JS/Python SSE checks, build/type-check and offline browser checks.
  Does not establish live model prose quality or final UX acceptance.
* See [A-029](../implementation/log.md#a-029---s-043-readable-data-driven-explanations)
  for hashes, resolved test issues and cleanup.

## S-041 - Executed Native Human Handoff

* Date: 2026-11-04
* Authority: Q-044/S-041 revision 1; D-020 architecture accepted separately.
* Exact published advisor v4 matches the candidate prompt and eight schemas.
  No dynamic per-request managed schema extension is assumed.
* Actual native Framework tests prove declaration-only pauses and matching
  function-output continuation after session reload. Actual CopilotKit core
  processes both frontend handlers and automatically follows their checked
  results over Python SSE; approval/execution is fixture-only.
* Real browser: one Italian question, native preference request, one EXPRESS
  click, same conversation resumed with a real tool output, then Italian
  exact-proposal approval request. No separate Continue or invented user text.
* Usage: four requests, six tools including human requests, 7,760 reconciled
  tokens and EUR 0.1552 conservative estimate. No new live approval,
  reservation, retry or telemetry export. Reload makes no inference.
* Durable state survives a fresh Python process; incomplete human receipt
  persistence fails closed. Native IDs and actual receipts, not an AG-UI
  process-local approval registry or browser history, remain authoritative.
* Tests: 114 focused Python, 14 frontend and three actual JS/Python wire tests
  pass; build/type-check passes. Browser covers one-click choice/approval,
  pending-approval reload, exact confirmation and post-write validated
  completion offline; real coverage stops before approval. Mobile 390px
  has no horizontal overflow.
* See [A-028](../implementation/log.md#a-028---s-041-native-human-handoff-migration)
  for actual IDs, limits, cleanup and evidence boundaries.

## S-040 - Human Handoff Documentary Evidence

* Date: 2026-11-04
* Authority: Q-042; source inspection and current public research only.
* Sources: [CK10-CK13](../../../../docs/research/sources.md#conversational-human-handoff-research).
* Installed core 1.24.0: `FunctionTool` supports `func=None`. Its native
  function invocation layer recognizes declaration-only calls separately
  from unknown calls and marks caller-input pauses without invoking a tool.
* Installed AG-UI 1.7.1: tool converter constructs declaration-only tools;
  approval/resume support exists. Its default approval authority store is
  process-local and cannot itself prove persisted recovery.
* Installed Foundry 1.16.0: managed references remove per-request tool
  declarations and retain the published agent's tool definition.
* Installed CopilotKit 1.82.0 v2: hook declarations and source maps show
  `respond` resolving the frontend-tool promise. Core's run handler processes
  handlers and schedules follow-ups, sometimes retaining the logical run ID.
* Current binding discards native input/tool forwarding and requires a
  text-only final response. Current transport rejects tool results/resume;
  current validation requires a final answer before any successful terminal.
  These are real changes to make, not a hook that can simply be dropped in.
* Recommended contract: two model-requested frontend human tools and
  server-verified durable responses, not fabricated user messages.
  See [the design](analysis.md#s-040-conversational-decision-handoff-design).
* Evidence boundary: no native SDK scenario was executed, no latency was
  measured and no managed definition was published. Source-level capability
  is not end-to-end compatibility or new cloud authorization.

## S-038 - Executed Local CopilotKit Compatibility Evidence

Launch clarification on 2026-11-04 at 11:23 +01:00: current source confirms
the default UI still depends on `supply_chain/web`; the fixture adds
`/copilot/` only with `--copilotkit` and an existing frontend build.
The directory is pending replacement, not currently unused. Instructions
are guidance for an offline preview, not authorization to start a service,
remove files, activate the default replacement or call Foundry.

* Date: 2026-11-04
* Authority: Q-040 and S-038 revision 1; local/offline only
* Installed: react-core/core 1.82.0, AG-UI JS client/core 1.0.2,
  React/ReactDOM 19.2.0, Zod 3.25.76, TypeScript 5.9.3 and Vite 7.2.2.
  Selected a verified available stable pin instead of inaccessible 1.84.1;
  no prerelease, registry change or TLS bypass.
* Package scripts, audit and funding requests disabled during installation;
  actual peer resolution deduplicates AG-UI, React and Zod.
  Python pins are unchanged.
* Build/type-check: pass against installed published v2 exports. CopilotKit
  message-view slot requires its static `Cursor` member; preserve the
  published component shape instead of forcing a type cast.
* SDK unit tests: 12 pass, including history projection, headers, clone,
  rejected client authority, missing/mismatched terminal, malformed/duplicate
  validation and finalization not granting success.
* Actual Python wire tests: 3 pass. Complete STANDARD case across three
  explicit turns, no model usage change for decision-only actions, exact
  approval, one reservation/read-back, token/Origin/history rejection and
  abort uncertainty. Upstream SDK responses are explicitly simulated.
* Measured investigation stream: 6 text deltas, first at 1.929 seconds,
  completion at 3.498 seconds. Proposal: 5 deltas, 1.649/3.201 seconds.
  Reservation/read-back: 7 deltas, 3.175/4.739 seconds. These are local
  fixture measurements with intentional upstream delays, not Foundry latency.
* Targeted Python regression: 30 UI/native-streaming tests pass, including
  rejection of early selection and tool results without validated history.
* Browser: clean final STANDARD case produces exactly 3 run requests,
  including reload/reselection, and ends unblocked at source 80/70/10,
  destination 20. Keyboard submission, checkbox-gated approval, contextual
  cards only after validation, decision-only actions, hidden Continue after
  reservation, Stop, invalid final answer and inference-disabled state tested.
* Isolation/rendering: case switching shows no previous transcript in an
  empty case; user HTML remains literal without image creation/execution.
  No external browser requests or console/page errors in final clean flows.
  A 390-pixel viewport has no horizontal overflow. This is not a full
  accessibility, adversarial assistant-content or exhaustive egress audit.
* Corrected issues: dependency/API type mismatches; subscriber exceptions
  not reliably rejecting promises; small fonts inlined as data URLs under
  strict CSP; old composer remaining mounted during case loading; Continue
  initially checking the wrong durable-result key. All addressed locally.
* Harness limits: browser request-context cookie API is unsupported.
  A forced delayed-route experiment stalled; it was removed and normal
  HTTP/reload/case-switch flows were rerun. No claim of exhaustive
  slow-network race verification.
* Details: [A-025](../implementation/log.md#a-025---s-038-local-copilotkit-compatibility-slice),
  [CK09](../../../../docs/research/sources.md#ck09) and the
  [current chat instructions](../../../../src/supply-chain-resilience/README.md#copilotkit-chat)
  (the S-038 preview was replaced by the S-039 real default application).
* Limit: fixture-only preview, not the default/live interface. Full routing,
  source/build fingerprints, durable card/decision presentation and final
  UX/accessibility acceptance remain a separately approved replacement step.

## S-037 - Complete CopilotKit Integration Analysis

* Date: 2026-11-04
* Authority: user's explicit complete-analysis request at 10:20 +01:00
* Deliverable: [project-specific analysis](analysis.md#s-037-copilotkit-integration-analysis)
* Sources: [CK01...CK08](../../../../docs/research/sources.md#copilotkit-complete-integration-analysis)
* Finding: CopilotKit v2 is a suitable candidate, but the guarded endpoint
  is not plug-and-play with default full-thread SDK requests, automatic
  chat startup behavior or frontend HITL tools.
* Verified local baseline: Node 26.13.0/npm 11.20.0; Python framework core
  1.24.0, framework AG-UI 1.7.1, protocol 0.1.22 and FastAPI 0.141.0.
  Inspected actual Python request/event model fields without agent execution.
* Verified published candidate: react-core/core 1.84.1 depend on AG-UI JS
  1.0.2; package exports expose v2 components/styles; license is MIT.
  JS SDK declares protocol 1.0. Version numbers alone establish no wire
  compatibility result.
* Environment limitation: public npm registry metadata failed TLS with both
  PowerShell and curl. Versioned public CDN manifests/declarations and the
  matching official repository manifest were accessible. No package install,
  TLS bypass or registry configuration change was attempted.
* Target: direct local-development provider, case-bound HttpAgent extension,
  reusable styled CopilotChatView/message/input components, render-only tool
  UI and contextual cards backed by existing trusted action routes.
* Important distinction: high-level chat documents an automatic initial
  run; `onRunFinalized` fires after failures; `useHumanInTheLoop` registers
  a frontend tool. None is automatically compatible with current safeguards.
* Product/licensing: core chat/AG-UI/application persistence need no hosted
  CopilotKit service. Intelligence, saved cross-device streams and production
  self-managed mode are separate choices, not implied by the MIT packages.
* Limit: no packages imported/executed, browser prototype, actual SDK wire
  test or live Foundry/export operation. Analysis completion is documentary
  acceptance only. Proposed S-038 must prove the integration before a full
  frontend replacement or any separately authorized live test.

## Conversational UI Library Follow-up

Follow-up after the user's response to Q-039: the repository identities are
[CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit) and
[assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui).
The user requests stronger reasons than reduced setup complexity; neither
library is selected. Revise the initial simplicity-first recommendation.

[CopilotKit self-managed agents](https://docs.copilotkit.ai/ag2/backend/self-managed-agents),
freshly inspected on 2026-11-04, documents both runtime-backed connections
and a direct local-development AG-UI agent registry. An additional Node
application runtime is therefore not universally mandatory for the local
lab. The direct development setting is explicitly named
`agents__unsafe_dev_only` and must not be presented as production setup.
The production `selfManagedAgents` path is marked as part of Intelligence;
actual package/version/feature requirements need verification rather than
assuming every integration path is free of hosted/commercial prerequisites.
The [v2 reference](https://docs.copilotkit.ai/reference/v2) documents built-in
chat, styling, headless hooks and tool-call rendering, with distinct v1/v2
provider/import surfaces. Do not mix examples across those APIs.

The CopilotKit repository identifies the maintainers as the team behind
AG-UI. Combined with Microsoft's explicit Agent Framework integration
reference, this supports evaluating CopilotKit first for a learning lab
centered on that ecosystem. It is not a Microsoft support commitment,
exclusive endorsement, certification or runtime-quality benchmark.

assistant-ui's repository explicitly documents composable Thread/Message/
Composer primitives, styled component starters, accessibility, streaming,
generative tool UI and inline human approvals. These are real strengths for
a product whose primary requirement is detailed chat UX control, not
evidence of inferior Agent Framework compatibility.
Its AG-UI runtime documents message reconstruction and resume behavior;
experimental thread-list APIs and automatic pending-tool cancellation need
careful selection against the application's no-retry/uncertain-state rules.
Both libraries require actual integration validation. Neither moves
authorization from the existing trusted backend into browser tool results.

The initial comparison below is historical where the new findings refine it.

* Date: 2026-11-04, following Q-038 and the user's request to proceed
* Microsoft source: [Agent Framework AG-UI overview](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/),
  section "Build agent UIs with CopilotKit"
* Finding: Microsoft explicitly features CopilotKit for streaming chat,
  human interaction and generative UI. The documented connection registers
  an AG-UI `HttpAgent` in the CopilotKit runtime. This is an integration
  recommendation, not a requirement to use it or proof that our guarded
  endpoint already accepts its managed histories/frontend tools.
* CopilotKit source: [Microsoft integration](https://docs.copilotkit.ai/microsoft-agent-framework),
  which currently redirects to a .NET-labeled integration page. It describes
  Python/.NET agents behind an AG-UI HTTP bridge and a React frontend/runtime.
  Its current quickstart includes cloud Intelligence onboarding; do not
  infer that onboarding, a new hosted service or its prerequisites are
  approved for this Python lab.
* Direct alternative: [assistant-ui AG-UI overview](https://www.assistant-ui.com/docs/runtimes/ag-ui/overview)
  and [quickstart](https://www.assistant-ui.com/docs/runtimes/ag-ui/quickstart).
  They document React 18/19, `@assistant-ui/react-ag-ui`, `@ag-ui/client`,
  `HttpAgent` and `useAgUiRuntime`, with streaming/tool/state reconstruction.
  This path can connect the browser directly to the existing Python server.
* Trade-off: CopilotKit has the explicit Microsoft integration reference
  and wider agent-UI runtime; assistant-ui is a closer fit to a small
  chat-first surface without adding an application proxy runtime.
  Both introduce a Node frontend build and require custom contextual cards.
* Boundaries: package versions, installed compatibility and guarded history/
  terminal-validation behavior are not tested yet. No library removes
  backend authorization. Preserve single-user local scope, no hosted
  account/service requirement, no live inference and no frontend tool authority.

## S-036 - Verified Local AG-UI and Native Streaming Integration

* Date: 2026-11-04
* Authority: Q-037 and S-036 revision 2, local implementation/tests only
* Evidence: [A-023](../implementation/log.md#a-023---s-036-ag-ui-and-native-streaming)
  and [exact API/dependency findings](../../../../docs/research/sources.md#ag-ui-native-streaming-implementation-follow-up)
* Result: the official adapter works with the pinned framework generation
  through a guarded server-owned case binding. Native streaming uses terminal
  response/update gates, not a second model/function loop or completed-text
  animation. The runtime's earlier streaming rejection is replaced with
  actual terminal/batch/usage validation.
* Caveat: public sample registration alone does not provide application
  human authorization, persistence or final evidence validation. The binding
  retains these outer controls. Provisional text remains visibly distinct.
* Correlation finding: AG-UI overrides native telemetry conversation ID with
  its local thread ID. An actual streamed-span test reproduced the mismatch.
  The common exporter now preserves the authoritative managed conversation
  ID from the trusted per-agent scope, without private framework APIs.
* Limit: offline SDK HTTP responses and browser tests do not establish live
  Foundry streaming, new Insights ingestion or model quality.

The following S-035 design observations are historical. The non-streaming
recommendation was superseded, not implemented.

## S-035 - Local Testing UI Scope and Integration Choice

Update on 2026-11-04 at 09:38 +01:00: Q-036 explicitly requires AG-UI and
real streaming. The initial bespoke non-streaming recommendation below is
superseded before implementation, not accepted architecture.
The [official getting-started guide](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/getting-started)
was freshly consulted: Python provides a FastAPI AG-UI integration with SSE
streaming. Installed `RunSafety` rejects streaming and validates complete
`Response` objects; this is a concrete implementation adaptation required
by the new requirement, not evidence that Foundry cannot stream.
The current final contract is JSON message/evidence: provisional text
rendering and terminal authoritative validation must be deliberately separated.
Exact installed streaming/adapter compatibility remains to be verified
under [S-036 revision 2](../plan/plan.md#s-036-revision-2-ag-ui-testing-interface-and-native-streaming).
No native streaming integration or live compatibility is claimed yet.

* Date: 2026-11-04
* Authority: user's request to move to the interface; local/public design only
* Functional choice: Q-035 returned `full_human_controlled`
* Sources: [current UI follow-up](../../../../docs/research/sources.md#testing-ui-design-follow-up)
* Outcome: recommend one thin local UI increment, proposed as
  [S-036](../plan/plan.md#s-036-revision-1-local-human-controlled-testing-ui).
  No application edits, installation, server or authenticated Azure operation.

The user selected chat/tool inspection plus explicit option selection and
exact-proposal approval/rejection, not just read-only chat. Preserve the
learning objective: the agent decides reasoning/tool order; the UI presents
facts and trusted human actions, not a new deterministic reasoning engine.

Fresh Microsoft documentation describes DevUI as a standalone development
sample, not production UI, with direct agent registration. AG-UI is an
optional protocol for richer interactive clients, not a ready-made screen.
The Python AG-UI integration maps streaming agent execution into SSE.
None of `agent-framework-devui`, `agent-framework-ag-ui`, `fastapi` or
`uvicorn` is installed in the application environment.

The actual guarded path is `AdvisorConversation.reply` and
`CandidateSession.reply`, not an unguarded `agent.run` registration.
`RunSafety.process` rejects streaming. A sample attached directly to the
agent would not automatically preserve outer evidence validation, durable
case uncertainty, trusted decisions and drift checks. AG-UI compatibility
with these boundaries has not been executed or certified.

Recommend a thin local FastAPI/static-browser interface for the initial
increment, rather than migrating runtime safety and token streaming solely
to obtain a UI. Display existing tool-status events and publish final text
only after validation. AG-UI remains a later option if standardized clients
or token streaming justify a separate change, not a requirement assumed here.

The managed chat operation currently belongs to the CLI and creates/shuts
down telemetry once per invocation. A long-running server must extract the
guarded service path without duplicating it and own telemetry once at startup.
Backend actions retain exact proposal IDs, case locks and authoritative state;
browser state/chat cannot authorize a reservation. The proposed increment
includes offline/browser validation only; live model/telemetry testing
requires separate explicit scope.

## S-034 - Shared Policy and Actual Trace Ingestion

* Date: 2026-11-04
* Authority: Q-034 and S-034 revision 1
* Outcome: shared tracing implemented; all seven live spans verified in
  the existing linked Application Insights
* Sources: [implementation follow-up](../../../../docs/research/sources.md#shared-tracing-implementation-follow-up)
* Execution evidence: [A-022](../implementation/log.md#a-022---s-034-shared-per-agent-observability)

Installed framework global sensitive switches cannot serve as per-agent
policy. A task-local scope plus sampler/correlation processor and allowlisted
export supports off, metadata and selected synthetic content independently.
Native sensitive capture stays globally off; existing agent/chat/tool spans
remain the instrumentation source. One application parent includes final
validation. No speculative multi-agent registry or inheritance is needed.
Offline native and concurrent-policy tests prove isolation; a real threaded
batch-export test also verifies complete flush after context exit.

The actual linked Insights connection uses `ProjectManagedIdentity` with
its connection string in metadata. Projects 2.7's convenience method rejects
that layout, before any conversation/inference. Public `connections.list/get`
supports explicit handling of the observed layout and API-key connections.
Unsupported/ambiguous/missing layouts fail closed; connection values were
never displayed, stored in candidate artifacts or copied into tracking.

The sole live read-only case used two model requests and three tools.
Actual linked-resource query results eventually contained all seven expected
spans for trace `cc4f5d7e2c1e90743c06f80ccfbf0001`, with parent/run/
conversation/managed-version correlation and selected content-presence flags.
Initial partial visibility was ingestion delay, not a basis for replaying
inference or claiming missing tool instrumentation. Queries remained scoped
to that trace, and no transcripts/payloads were copied into tracking.
Backend ingestion is established; independent portal rendering is not.

## S-033 - Why Live Conversations Are Not Visible as Foundry Traces

* Date: 2026-11-04
* Authority: user's 09:00 +01:00 diagnostic question; local/public reading only
* Status: completed explanation; no implementation or cloud inspection
* Sources: [fresh observability check](../../../../docs/research/sources.md#framework-tracing-diagnostic-follow-up)

The current application emits local metadata to `events.jsonl` through the
session event callback. No application Python source configures OpenTelemetry
providers, Azure Monitor export or content recording. The manifest contains
framework/Projects/Identity/OpenAI packages, not Azure Monitor exporters.
Actual application-environment inspection finds `opentelemetry-api==1.45.1`,
but no `opentelemetry-sdk`, `azure-monitor-opentelemetry` or Azure Monitor
exporter. The default tracer provider is `ProxyTracerProvider`. Checked
exporter endpoint/connection-string environment variables are absent; only
presence was inspected, no configuration values were printed.

The installed environment is decisive; current framework documentation's
general statement about included OTel dependencies is not proof that its
optional packages are installed in this application's pinned generation.
There is no configured application-to-Application-Insights export path.
Waiting cannot cause these missing client spans to appear retrospectively.
S-032 deliberately authorized local metadata only, excluding external telemetry.

Fresh Microsoft documentation distinguishes service-side traces for portal
execution from client-side spans for local model/tool/application calls.
Foundry's trace view reads exported telemetry in linked Application Insights;
linking that resource is not equivalent to instrumenting the local process.
The client tracing guide says traces typically appear after 2-5 minutes
once configured, not a visibility SLA or an explanation for missing export.
Persisted Conversations and exported distributed traces are distinct stores.
Trace metadata and full message/tool payload capture are also distinct:
content recording is an explicit sensitive-data choice, not a prerequisite
for basic tracing.

Recommended next increment: assess/configure the pinned framework's supported
OTel provider and Azure Monitor exporter, target the project's linked Insights
resource without exposing its connection string, correlate agent identity,
conversation and run, flush on CLI shutdown, and validate one new bounded
live trace. Avoid duplicate model instrumentation. Keep sensitive content off
unless separately agreed even for synthetic data. Existing run telemetry
cannot be retroactively reconstructed by waiting; do not replay writes.

No Azure configuration, ingestion, portal filters or RBAC were inspected:
the user's linked-Insights statement is accepted as context, not independently
verified. Server-side trace presence is not established by this local diagnosis.
No environment/package/code/cloud/run changes occurred.

## S-030 - Installed Framework API and Safety Verification

* Date: 2026-11-03
* Authority: Q-029, local migration only
* Sources: [managed integration](../../../../docs/research/sources.md#agent-framework-managed-foundry-integration-follow-up)
  and installed package source/runtime inspection

Verified framework core 1.24.0, Foundry adapter 1.16.0 and OpenAI adapter
1.18.0 with Projects 2.7.0, Identity 1.27.0 and OpenAI 3.38.0.
The Foundry package requires Projects `>=2.2.0,<2.8.0`; installing Projects
2.10.0 alongside it would violate the declared constraint. `pip check` passes.

`FoundryAgent(project_client=..., agent_name=..., agent_version=...,
allow_preview=False)` uses the project Responses API and injects a versioned
`agent_reference`. It strips local tool declarations and ignores dynamic
service tool-selection overrides. The stored agent remains authoritative;
matching `FunctionTool` instances provide local implementations. Existing
exact JSON schemas are accepted as `input_model` without decorator-generated
schema drift. `AgentSession.to_dict/from_dict` persists native continuation
and provider state, rather than a custom reconstruction of conversation history.

The installed client's function-invocation layer wraps chat middleware, so
chat policy observes each actual service call and validates its complete
function batch before invocation. Built-in `max_function_calls` is best-effort
after a batch, not a substitute for the demo's strict pre-dispatch limit.
Local invocation is configured sequentially; permissions and exact human
decisions are also rechecked at dispatch.

Ordinary function exceptions may become recoverable tool-error results.
`MiddlewareFailure` is the documented fatal escape, but a service-managed
conversation may trigger an additional best-effort settlement request.
The demo latches fatal failure and rejects that request in chat middleware
before network/accounting. Offline tests verify no sibling effect, model
continuation or settlement I/O after fatal or unexpected function errors.
This intentionally leaves interrupted hosted conversation state for inspection,
not automatic repair. SDK retries are disabled on the actual framework client.

Function middleware receives parsed results as `list[Content]`, not a raw
JSON string. An initial offline regression exposed that mismatch; the adapter
now checks one text content containing the authoritative JSON result. Response
fixtures include the service conversation ID, matching native continuation
rather than accidentally switching to response-ID continuation.

The actual framework and real OpenAI HTTP serialization are exercised with
offline service responses, including version binding, function outputs and
one-request behavior on HTTP 503. No authenticated Azure access, inference
or new publication occurred. Live compatibility and UI/streaming remain unverified.

## S-029 - Why the Current Runtime Does Not Use Agent Framework

* Date and authority: 2026-11-03, user's 17:19 +01:00 clarification request
* Status: completed historical/public-source analysis, not migration approval

D-012 chose a named/versioned managed prompt agent over a code-defined hosted
agent for the initial increment. It did not establish that Agent Framework
is incompatible with managed agents or record a user rejection of the
framework. The direct Projects/Responses driver was the implementation's
initial minimal-dependency approach, not a Foundry constraint.

Fresh [official integration documentation](../../../../docs/research/sources.md#agent-framework-managed-foundry-integration-follow-up)
explicitly supports Python `FoundryAgent` connecting to an existing Prompt
Agent by project/name/version, with matching local callable implementations
for functions already declared on that agent. This can preserve the managed
agent principle while using framework run/streaming/session abstractions.
It is distinct from a sample that creates an application-owned agent from
a direct model client.

With the user's current UI and future multi-agent learning goals, assess
this first-party integration before choosing a custom AG-UI bridge or adding
more handwritten generic runtime plumbing. The previous S-028 compatibility
caution still applies, but must not imply that a custom adapter is preferred
or that framework adoption requires abandoning the existing managed agent.

The framework would not eliminate business rules, SQLite transactions,
exact-proposal approval, current/historical evidence checks or explicit
budget/uncertainty policy. A bounded compatibility assessment must verify
SDK dependencies, callable/schema matching, explicit tenant/agent targeting,
tool-permission guards, persistence, retry/usage accounting and UI integration.
No automatic one-to-one replacement or successful migration is claimed.

No source/dependency change, authenticated tenant access, inference, published
definition change or run-data operation occurred. The user asked why; no
framework/UI implementation or cloud execution is authorized by that question.
Recommended next activity is a bounded Agent Framework integration assessment
that preserves the managed agent and application safeguards.

## S-028 - UI Protocol Documentary Review

* Date and authority: 2026-11-03, user's 17:15 +01:00 question about a testing
  interface and whether Microsoft's best practice is always AG-UI
* Status: completed public/local documentary analysis only
* User intent, faithful English summary: obtain an interface for testing
  the existing agent, whose local functions cannot be run by the playground
  alone, and understand the recommended integration approach.

Fresh [official sources](../../../../docs/research/sources.md#ag-ui-integration-follow-up)
describe AG-UI as a protocol, not a ready-made user interface or mandatory
Foundry component. Microsoft documents direct agent use as an alternative
and recommends considering AG-UI for streaming, observable tool activity,
interactive components, state synchronization and approval interactions.
The overview links CopilotKit as an ecosystem frontend component option.

This fits a reusable learning/demo interface with chat, visible tool activity,
STANDARD/EXPRESS selection, exact-proposal approve/reject controls, current/
historical facts and usage. A minimal direct local web UI remains a simpler
alternative when only quick testing is needed. The AG-UI option is a
recommendation to evaluate, not an accepted implementation requirement.

The current application uses its own Projects Responses loop and a managed
named/versioned prompt agent, not an Agent Framework `Agent`. The documented
Python package installs framework integration; using that sample unchanged
would not preserve this runtime automatically. Design must assess a thin
protocol adapter without replacing the managed agent or inventing another
orchestration workflow. Compatibility has not been tested.

Human approval must still bind the exact proposal through trusted backend
operations; a browser message/state flag cannot self-authorize execution.
Follow Microsoft's trusted frontend-server boundary rather than exposing
privileged raw AG-UI inputs directly to an untrusted browser. UI progress
events also must not present unvalidated final evidence as completed output.
The existing runtime has metadata callbacks but does not yet implement
token streaming; AG-UI availability alone does not add that behavior.

No UI stack, framework migration, deployment or new live test is approved
by this clarification. No source code, dependencies, tenant state, run
artifacts or published agent changed; no authenticated access occurred.
Proposed next activity: bounded UI design/compatibility assessment, preserving
the current advisor/tools/session and human-action safeguards.

## S-023 - Agent-Led Design and Prompt Lifecycle Review

* Date and authority: 2026-11-03, user's explicit request for document,
  knowledge-base and prior-analysis review; analysis and tracking only
* Status: completed documentary review, not implementation authorization
* User intent, faithful English summary: move toward the original agent-learning
  goal, make agent/tool/data boundaries visible, and revisit prompt management
  with GenAIOps rather than retaining a minimal embedded prompt.

### Findings Against the Existing Baseline

Accepted D-009/RQ-011 already prioritize agent learning over deterministic
orchestration. D-010 describes agent-led analysis within a thin approval flow;
D-012 selects a named/versioned Foundry prompt agent with a Python tool driver.
These do not require a fixed CLI phase per reasoning step.
The completed S-022 case remains valid technical evidence, but is not evidence
that the agent can independently manage an open-ended conversation.

Observed source boundaries:

* `foundry.py` mixes agent instructions, initial case prompt, SDK definition,
  generic Responses continuation and usage monitoring.
* `walkthrough.py` derives instructions using literal string replacement,
  adds stage-specific prompts and imposes comparison/proposal/execution stages.
* `tools.py`, `store.py` and `domain.py` already separate tool contracts,
  durable business state and arithmetic. Synthetic facts are still defined
  in code rather than a separately versioned scenario asset.

The prompt is optimized for the successful narrow contract, including exact
JSON copying; a longer version of that prompt alone would not create autonomy.
Both application sequencing and instruction design need revision.

### Fresh Official Evidence and Limits

Consulted 2026-11-03:

* [Prompt-agent definition](../../../../docs/research/sources.md#prompt-agent-definition-follow-up):
  saved prompt-agent versions
  include model, instructions and tools. Keep this managed resource; no
  hosted/harness migration is needed merely to separate local modules.
* [Prompt lifecycle training](../../../../docs/research/sources.md#prompt-lifecycle-training-follow-up):
  Microsoft training explicitly
  describes separate `.txt`/`.md` prompts and Git-based development, testing,
  review and promotion. Its SDK examples use older API shapes; current S02's
  `PromptAgentDefinition`/`create_version` path takes precedence for code.
* [Existing GenAIOps guidance](../../../../docs/knowledge/genaiops.md):
  behavior is a release of code, instructions, model, tools, data and policies,
  not a prompt file alone. Its 100-case dataset and pipeline are proposals,
  not requirements already accepted for this compact demo.
* Fresh S23 and [evaluation-target checks](../../../../docs/research/sources.md#evaluation-targets-follow-up)
  distinguish turn/conversation evaluation, process
  evaluation and runtime targets. S32 supports instruction/tool-description
  optimization but explicitly cannot evaluate client-side function execution
  during tool-description optimization. Native optimization is not an
  end-to-end reservation test.

No tenant queries, inference, evaluation, installation or deployment occurred.
No specific Prompty/Prompt flow integration was verified for this SDK path.
They are not prerequisites for a source-controlled text instruction asset.
Repository documentary validation initially rejected adding S34...S36 because
the original S01...S33 baseline is intentionally fixed. New public sources
are recorded as named follow-up sections instead; no test was weakened.
After that correction, all 10 documentary/link checks passed.
Application tests were not rerun because no executable code changed.

### Recommended Direction

One managed agent should conduct the conversation: recover relevant facts,
compare feasible options, explain trade-offs, ask for missing preferences,
prepare the selected proposal and report the authoritative result.
It may give a conditional recommendation but must not invent a permanent
cost-versus-speed policy or select on the planner's behalf.
The client loop should transport messages, dispatch tools and enforce limits,
not prescribe a tool sequence for every reasoning turn.

Keep human selection/approval as trusted application events, exact proposal
binding, freshness checks, role checks and atomic/idempotent reservation in
deterministic code. Natural-language claims by the model are not approval.
Retain a minimal pending-approval/resume control, not a workflow engine.
The model need not repeat every read tool on every turn merely to pass a
sequence test; evidence requirements must follow the actual operation.

Recommended separation, not yet implemented: agent definition module and
one explicit instruction file; generic runtime; existing tool contracts and
dispatcher; existing SQLite store and business rules; a synthetic scenario
asset and a small versioned evaluation dataset. Avoid a directory hierarchy
for every class or a new framework.

For prompt management, start with one stable `.txt` instruction path tracked
by Git, plus explicit configuration/provenance. Do not fork prompts into
`v1`, `v2`, `v3` source copies or derive production instructions by `.replace`.
Use an assembled instruction hash and record agent version, tool schemas,
resolved model information, scenario/policy and evaluation dataset versions.
If source is uncommitted, record that fact/content hashes, not a fabricated
release commit. Git tracks source; Foundry versions track published definitions.
They do not synchronize automatically, including changes made in the portal.

Instructions should cover mission, fact/tool grounding, uncertainty,
planner trade-offs, application approval boundary, conversation behavior,
tool-error/uncertain-outcome handling and concise evidence-based explanations.
Do not request hidden chain-of-thought or hardcode the successful EXPRESS
answer. A couple of behavioral examples may help but must not overlap the
held-out acceptance cases.

Evaluation should compare the current fixed-flow baseline with the candidate
on outcomes, not an identical tool order: grounded alternatives, missing
preference clarification, irrelevant/no-impact input, infeasible options,
rejected approval, false approval/injected instructions, stale proposals,
and uncertain/duplicate execution. Offline fixtures prove contracts, not
actual model quality. Authorized live evaluation of the complete local
dispatcher is a separate later activity.

### Release and Recovery Caveat

The existing named endpoint follows the latest version; the baseline CLI
already stops on a version mismatch. Do not promise historical-version
routing, traffic splitting or instant rollback without verifying a supported
route. The proposed local increment must not publish the candidate or make
retained v2 sessions invoke a different definition. Preserve S-022 artifacts.
Future authorized publication must verify the assembled definition and
record actual version/endpoint behavior. Recovery may require a controlled
republish of a prior artifact, not merely editing a local prompt file.

## S-020 Fresh Source Check and Preflight Boundary

### Token-Count Investigation on 2026-11-03

The user explicitly requested verifying whether the blocking pre-count can
work, accepting that it might not be possible. This investigation used public
sources and installed SDK source only; no authenticated project access,
inference, resource mutation or application-code changes occurred.

Observed installed code:

* Projects 2.10.0 `_resolve_openai_base_url` selects
  `{project_endpoint}/agents/{agent_name}/endpoint/protocols/openai` when an
  agent name is supplied.
* OpenAI 3.38.0 `responses.input_tokens.count` unconditionally issues POST
  `/responses/input_tokens` on that base URL. Its presence in the generic
  OpenAI client is not an Azure service-support guarantee.
* The earlier real attempt returned 405 before generation on that route.
  No new network probe or attempt on another route was made.

Public supporting evidence:

* [Microsoft Q&A answer dated 2026-03-01](https://learn.microsoft.com/en-us/answers/questions/5791830/azure-openai-response-api-input-token-counting-wit)
  states that Azure OpenAI did not provide a standalone input-token estimation
  endpoint and reports usage after generation instead. Retrieved 2026-11-03.
  This is dated support guidance, not a normative current API contract or
  proof for every Foundry agent route. Its unrelated compaction claims are
  not adopted.
* The [Responses API guide](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)
  is the linked product reference. No verified current support for the
  agent-scoped pre-count route was established by this investigation.

Conclusion: the current requirement for a successful server-side pre-count
is an application-introduced blocker, not evidence that the agent's generation
or function-calling APIs fail. No supported correction to obtain an exact
pre-count for this managed conversation was verified. Do not retry guesses
of API versions/routes or silently substitute an exact-looking token estimate.

Proposed direction, not implemented or authorized for inference: explicitly
replace the exact-pre-count requirement with bounded requests/tool calls and
per-response output limits, local input/history estimates clearly labeled as
estimates, and reconciliation against actual returned usage. Such estimates
cannot guarantee a hard aggregate input-token or EUR cutoff before a request.
The enforcement change requires user agreement before modifying the guard or
resuming paid calls. The existing 100,000-token/EUR 10 limits are not silently
relaxed.

Checked on 2026-11-02 for S-020 revision 1:

Latest verification after the user corrected login and explicitly reconfirmed
continuation: the cached CLI user/directory matches the requested context.
The exact approved deployment lookup succeeded and returned model
`gpt-6.1-sol`, version `2026-09-29`, publisher OpenAI, SKU `GlobalStandard`,
capacity 100. This is not a successful Responses/function-calling test.

Subsequent live evidence: managed prompt-agent version and conversation
creation succeeded, but `responses.input_tokens.count` returned HTTP 405.
The installed method's existence is not proof of service-route support.
The fail-closed guard prevented `responses.create`: zero generation requests
and zero tool dispatches. No automatic fallback or duplicate creation ran.
Safe references and acceptance gaps are in the
[live attempt record](../implementation/log.md#a-010-live-attempt-and-token-count-blocker).

The earlier pricing-placeholder limitation below was subsequently resolved
by reading the first-party pricing HTML's `data-amount` attributes, rather
than relying on search snippets or rendered placeholders:

| Published Global tier, USD per million | Input | Cached input | Cache writes | Output |
| ------------------------------------- | ----- | ------------ | ------------ | ------ |
| GPT-6.1 Sol short context | 2 | 0.10 | 2.50 | 10 |
| GPT-6.1 Sol long context | 4 | 0.20 | 5 | 15 |

Source: [Azure OpenAI pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/),
retrieved directly on 2026-11-02. Each inspected Global row returned the same
values across its listed regions. Do not infer the context-tier threshold:
the conservative estimate covers both tiers instead.

[ECB reference rates](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)
for 2026-11-02 report USD 1.1216 per EUR. The highest listed input/cache-write
rate is therefore approximately EUR 4.46 per million and output EUR 13.38
per million at that reference rate. Configure deliberately higher application
estimate rates of EUR 5 input and EUR 20 output per million. Charging every
token at the higher rate bounds 100,000 tokens at an estimated EUR 2,
below the accepted EUR 10 ceiling. These are conservative estimate inputs,
not actual contracted EUR tariff values or a guaranteed billing cutoff;
taxes, billing conversion and account terms can differ.

[Agent Service pricing](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/)
states no additional charge for creation/running of native prompt/workflow
agents, while models, paid tools and hosted compute are separate.
This slice uses native prompt agents with local read-only functions only,
no paid built-in tools, hosted compute or telemetry export.

* [Function calling](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling):
  Python prompt-agent sample uses `FunctionTool`, `PromptAgentDefinition`,
  `agents.create_version`, `get_openai_client`, a conversation and
  `function_call_output` preserving each call ID. The sample's cleanup
  operations are excluded from this project's approved contract.
  The page distinguishes ephemeral Agent Framework execution from server-side
  prompt agents and notes a separate harness-specific strict-schema limitation.
* [SDK quickstart](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code):
  the inspected Python setup specifies Projects >=2.3.0 and existing CLI
  authentication. Installed local versions are recorded in A-010, not assumed
  compatible merely because installation succeeds.
* [Azure OpenAI pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/):
  deployment types and model/context tiers affect prices. The direct page
  retrieval returned numeric price placeholders, so no EUR rate or cost
  estimate is inferred. Search snippets do not establish this project's rate.
* User-supplied deployment `gpt-6.1-sol` is configuration, not verified model
  identity or availability. The approved project lookup returned a
  tenant-mismatch error before metadata could be obtained. No inference ran.

See the [preflight record](../implementation/log.md#a-010---s-020-revision-1-preflight-blocker).

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
