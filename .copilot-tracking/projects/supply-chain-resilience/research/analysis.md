---
title: "Analysis of supply-chain-resilience"
description: "CopilotKit integration analysis and retained business framing for the Foundry learning demo."
ms.date: "2026-11-04"
---

## User-Scoped Knowledge, OBO and Database RLS

* Date: 2026-11-04 at 17:30 +01:00.
* Scope: requested local/public architectural analysis, not a vulnerability
  audit or permission to change authentication/cloud resources.
* User interest: storage for small knowledge plus access limited to the
  signed-in user's documents/rows. Q-046 reports SharePoint/two-user
  prerequisites available but asks whether database RLS is too complex.
  This does not confirm SQL availability or admin consent capability.

### Identity and authorization distinctions

* Rechecked S09: narrow capabilities, trusted identity context, resource
  binding and deny-path auditing are relevant. The blog's ToolContext/
  ToolGrant classes are custom examples. Its Blob path check with a supplied
  credential does not itself demonstrate a downstream OBO token exchange.
* OBO obtains a token for the downstream audience on behalf of the user.
  It is not forwarding one bearer token everywhere, nor does it automatically
  enforce document ACLs or database rows. Agent/service identity can remain
  at technical boundaries while data access uses delegated user authority.
* Current code: cloud_agent in ui.py uses server-side AzureCliCredential.
  Loopback Origin/action-token checks are not browser Entra login; session.py
  uses fixture business actors. Two browser users do not yet have distinct
  authenticated identities or protected conversation ownership.
* Full design must cover real sign-in, validated token audience/issuer/tenant,
  delegated scopes/consent, principal authorization, per-user runs/history/
  caches, and deny behavior. No token belongs in prompts, tool arguments,
  AG-UI state, receipts or telemetry.

### Storage alternatives

* SharePoint: a small same-tenant library preserves source permissions.
  The Foundry SharePoint tool explicitly documents delegated/OBO access,
  citations and two-user permission checks; it is preview and has license/
  pay-as-you-go, tenant and tool/channel constraints. Exact local integration
  is unverified.
* Blob/ADLS plus Search: separate canonical files, indexed chunks and
  permission metadata. Security-string filtering is application enforcement,
  not end-user database authentication; native ACL/RBAC/sensitivity-label
  paths have preview/source/API constraints. A shared copied index must not
  be assumed to inherit source ACLs.
* Database: appropriate for protected operational rows or a few short
  knowledge records. Real SQL RLS uses a security policy/predicate in the
  database. Use user-delegated SQL tokens if proving true end-user OBO;
  shared service identity plus trusted SESSION_CONTEXT is a different design.

### Bounded recommendation after Q-046

* Database RLS is a manageable candidate, not equivalent to adding a WHERE
  clause to the current SQLite demo. Most added work is genuine end-user
  authentication/token/consent handling, which SharePoint also requires
  in this multi-user browser application.
* Proposed slice: two actual Entra users, one narrow read-only knowledge
  function, one small SQL table plus access mapping/security policy. A
  record may contain a synthetic knowledge document with source/version,
  allowing document-level access through row visibility without introducing
  vector retrieval or a separate document platform.
* Model chooses the business query; verified request identity determines
  access. SQL applies RLS before any hidden text reaches the model. Expose
  only required fields and bounded results; do not expose arbitrary SQL,
  connection parameters, identity or permission filters to the model.
* Verify actual SQL caller identity and same-query/different-user results.
  Include forbidden-ID reads, empty authorized results versus authorization
  errors, expiry/no fallback, concurrent users, history/citation/cache
  isolation and absence of another broadly privileged tool bypass.
* Sources: [LE04-LE07](../../../../docs/research/sources.md#le04---delegated-tool-identity-and-obo).
  The DAB OBO sample is architectural evidence, not a selected extra service
  or a proven Python driver integration. No database or Entra tenant query
  was performed.
* Next candidate: S-044 revision 3 feasibility/design only. No backend has
  been approved for deployment, and no new application/cloud work is started.

## Learning Expansion Options After Advisor v5

* Date: 2026-11-04 at 17:24 +01:00.
* User feedback (English translation): the solution seems to work well;
  consider knowledge, more tools/scenarios and further Foundry learning.
  This is a request for recommendations, not implementation authorization.
* Current distinction: STANDARD and EXPRESS are two modes of the same
  recovery strategy. Existing fixtures already cover no impact, infeasibility
  and missing policy, but the live interface remains centered on transfers.
* Highest learning value: combine authoritative operational tools with a
  small synthetic document corpus, source-backed answers, and honest handling
  of missing, outdated or conflicting knowledge. Documents inform decisions;
  they do not grant human approval or replace stock/price feasibility checks.
* Backend alternatives: managed file search, an existing Azure AI Search
  index, or a bounded local document-reading function. The last is simpler
  but must not be presented as native Foundry retrieval or semantic RAG.
  Select only after exact SDK/runtime/citation compatibility and prerequisites
  are studied. Public source candidates:
  [LE01-LE03](../../../../docs/research/sources.md#learning-extension-research).
* Second strategy candidate: when source stock cannot cover the shortage,
  a read-only supplier-recovery tool supplies synthetic expedited/new-supplier
  quotes and delivery facts. The model decides whether to inspect it based
  on the question and evidence, not a new hardcoded orchestration branch.
  Start with advisory recommendations; no new purchasing write is implied.
* Further learning: a small measured evaluation suite for tool selection,
  grounding, citations, refusal, latency and cost; then consider a bounded
  specialist with distinct supplier/quality context. MCP is an integration
  option when reuse warrants it, not required for every new function.
* Important scope: multiple components/orders/cases need actual data/model
  changes; adding a fixture JSON alone does not remove current domain IDs,
  arithmetic assumptions or STANDARD/EXPRESS human-control enums.
  A second strategy must account for evidence and UI/permission contracts.
* Recommendation: one next design increment (S-044), not simultaneous
  implementation of knowledge, an optimizer, multiple agents and MCP.
  Preserve the user's learning-first/simple synthetic-business approach.
* This activity changed tracking only. No application edits, authenticated
  tenant access, resource provisioning, ingestion, publication or inference.

## S-042 User Feedback on Explanation Readability

* Date: 2026-11-04 at 14:16 +01:00.
* User feedback (English translation): the flow works; the advisor's dense
  explanation is hard to read, and synthetic day numbers lack meaning.
  This is flow-level feedback, not final acceptance of all presentation.
* Local review: the quoted quantities, option costs and schedule margins
  match the initial business model. The shortage is 40 across the two
  commitments, not necessarily a specific allocation of shortage per order.
  Costs have no declared currency; do not silently label them EUR.
* Presentation issue: one human-tool question carries situation, inventory,
  order quantities, deadlines, feasibility, costs, margins and the decision.
  The current prompt asks for a concise question but does not require
  a scannable summary or a defined calendar reference.
* Recommendation, not implemented: separate problem, two alternatives and
  one decision question. Explain zero margin as completion on the deadline,
  not as an inferred probability of failure. Keep detailed evidence available
  without repeating every field in the question.
* A later bounded improvement could introduce a fixed synthetic scenario
  date and explicit day-slot mapping in authoritative tool facts, plus
  descriptive names retaining stable IDs. Do not have the model invent dates,
  infer business-day calendars or use wall-clock today for persisted cases.
* No application/prompt/data change, cloud access, publication, inference
  or historical conversation mutation is authorized by this review.

## S-040 Conversational Decision Handoff Design

* Date: 2026-11-04
* Authority: Q-042, S-040 revision 1; local/public research only.
* Outcome: recommend real frontend human-tool requests/results, with
  application-verified durable receipts and automatic core continuation.
  This is a concrete proposed contract, not implemented compatibility.
* Sources: [CK10-CK13](../../../../docs/research/sources.md#conversational-human-handoff-research).

### Alternatives and recommendation

1. Automatically send the old Continue message, perhaps translated/hidden:
   reject. This preserves false user-message semantics and only masks the UX.
2. Structured application decision events, followed by application-owned
   continuation: viable simpler alternative. It needs a proper typed input
   contract and truthful model context, but does not demonstrate the model
   requesting and receiving native frontend human-tool results.
3. Agent-requested CopilotKit human tools: recommend for this learning demo.
   The model requests the decision; the hook waits; a real human response is
   validated by the backend and becomes the matching native function output.
   No separate Continue or pretend user text. Cost: update the managed
   definition and replace the old adapter/transport/lifecycle assumptions.

Native Framework `always_require` approval is also available. It is suitable
for Boolean permission but not STANDARD/EXPRESS preference collection.
Combining that mechanism with a different preference mechanism is possible,
not prohibited. For this small demo, use the same two human-tool pattern for
both decisions and retain backend exact-proposal authorization. Do not add a
second confirmation dialog merely to exercise another API.

### Proposed agent contract

Keep the six current business tools. Add two declaration-only human tools:

* `request_transfer_choice` asks STANDARD or EXPRESS in the user's language.
  It requires a current authoritative comparison, no existing proposal and
  feasible options only.
* `request_transfer_approval` asks about one exact proposal ID in the user's
  language. It requires the current proposal/facts and no prior decision.

Neither tool approves anything by being called. They have no server
implementation that manufactures a human answer. The frontend supplies the
interaction; only the backend's checked human event changes permission.
The model never gains an `approve_transfer` capability.

Tool arguments contain the question and, for approval, proposal identity.
Render quantities, costs and feasible options from server-owned facts, not
unverified model argument copies. The backend binds each actual model call
to its case, service conversation, native call ID, immutable arguments and
snapshot/policy versions before enabling a response.

The prompt must require the human tool when a decision is needed, preserve
the user's language and distinguish waiting from final JSON answers.
No new workflow engine or deterministic investigation sequence is required:
the model still decides what to investigate and when it needs a human.

### One interaction and one continuation

1. The native agent produces a real human-tool call; the backend validates
   its entire batch and reconciles usage before accepting a waiting state.
2. Persist the pending request and actual native/session identity. Close
   resources and the current HTTP stream normally. Waiting for a person is
   not an uncertain model call and must not keep an Azure inference open.
3. The v2 human hook renders the pending question. One click submits the
   actual option or exact proposal decision through the local action boundary.
4. Under the case lock, verify the pending call, facts and local actor boundary,
   record the event once and return a durable receipt. Do not continue if
   that write fails. The receipt is evidence of this event, not client authority.
5. Call `respond` with that receipt. CopilotKit core produces the tool-result
   continuation automatically. The server verifies correlation and uses its
   stored receipt to construct the matching native function result.
6. Agent Framework resumes the same managed conversation. The advisor
   creates a proposal after choice, or may execute/read back only the exact
   approved proposal after approval. Rejection never permits execution.

The real user-message list contains only text actually submitted by the
person. A human response is a typed tool result/card receipt, never an English
or translated invented sentence. Preserve the last genuine user language;
the existing prompt already requests it. No language-detection model is needed.

### Required changes to the current integration

* Publish a new version of the existing advisor with the two human schemas
  and prompt changes. Managed v3 cannot discover these tools from React.
  Do not overwrite v3, guess the new version number or rebind old sessions.
* Compose `useHumanInTheLoop` through the pinned v2 core run path. Bare
  `agent.runAgent` currently bypasses the frontend-handler/follow-up owner.
  Continue to avoid high-level chat automatic initial runs and suggestions.
* Replace the ordinary-user-text-only run contract with two narrow inputs:
  a genuine new user message, or one correlated human-tool receipt/result.
  Do not accept client history, arbitrary tool schemas, approvals or state.
  Human tools use exact server-owned allowlisted declarations; unknown tools
  remain fatal. Frontend and server business-tool names must not collide.
* Update the binding to forward native tool declarations/results and the
  actual server-owned session instead of dropping those inputs. The current
  text-only conversation helper cannot represent this handoff.
* Separate a checked waiting terminal from a validated final answer:
  proposed application events `validated_pause` and existing
  `validated_answer`. Waiting means current request/usage persisted, not a
  completed reservation. Continue using the SDK for SSE; no new parser.
* Persist native human-call history and receipts so reload reconstructs the
  same pending card and cannot create approval. Do not use client history or
  a new in-memory adapter as the authority for restored pending work.
* Distinguish logical SDK run identity from accepted native-call phases.
  Core can reuse a run ID across a human follow-up; replace the blanket
  run-ID-only rejection with atomic phase/receipt consumption tied to the
  pending native call. Never disable replay checks to accommodate core.
* Account for human requests once in call budgets. Preserve complete-batch
  validation before effects, fatal sibling failure and exact read-back.
* Route CLI/operator decisions through the same authoritative pending-event
  logic where relevant; do not create an alternate weak approval path.

### Lifecycle and failure rules

Pending human input is an explicit safe state, separate from active inference,
final validation, completed outcome and uncertainty. A reload may restore the
question without invoking a model. A duplicate click returns the same event
receipt, not a second decision/continuation. Claiming a continuation must be
atomic; an already-consumed or mismatched native call cannot be replayed.

If a response is saved but the subsequent model call becomes uncertain, show
the saved decision and an explicit blocked/reconciliation state. Do not ask
the person to approve again or silently resend the result. Losing a frontend
promise must not lose the durable human request or imply an approval.

Stop during inference preserves the existing uncertainty rules. Leaving a
waiting question unanswered makes no reservation. Cancellation/rejection is
a real event, not an automatically injected dummy tool result.

Provide immediate, accurate phases such as recording the choice and then
waiting for the advisor's response. The current action route does no model
inference; exact selection latency remains unmeasured. Repeated readiness/
frontend-fingerprint checks are visible in source, but are only profiling
candidates. Optimize only after measuring and without weakening drift checks.

### Verification gates and scope

Before any publication, prove the pinned native declaration-only pause and
tool-result continuation with actual framework/JS SDK code and test-only
upstream responses. Check same service conversation/call ID, core follow-up
identity, zero generated user text, one continuation per human event, failure
and reload/restart handling, guards, budgets, source/build provenance and CSP.
These fixtures are internal tests, not an alternative user application.

Then a separately authorized new managed version and real browser walkthrough
must prove the integration. No new resource, model provider, hosted runtime,
APIM or extra agent is proposed. Direct migration replaces the old UI contract;
there is no permanent legacy/simulated application fallback.

S-040 has inspected sources only: no SDK invocation, server, build, model,
publication or tenant access. Native compatibility and latency have not been
measured in this step. Q-043 asks for the architectural decision; operational
implementation/publication requires a separate bounded contract.

## User Review of the S-039 Decision Handoff

* Date: 2026-11-04 at 11:58 +01:00
* User feedback, faithful English translation: the application generally
  works, but selecting EXPRESS, waiting, separately continuing, seeing an
  invented English user message, approving and separately continuing again
  is cumbersome and unacceptable. Preserving the previous interaction
  contract is not an adequate product design.
* Verified local facts: `Conversation.act` records `/actions` and stops.
  `DecisionCard` then exposes a separate Continue. Its callback sends the
  hard-coded English sentence `Continue using the recorded human decision.`
  through the ordinary user-message path, which adds it to the transcript.
  This is actual application-generated text attributed to the user, not
  a requirement of CopilotKit or AG-UI.
* The backend action handler records/validates the decision without invoking
  the model. The observed selection wait cannot be called model reasoning
  on this path. Its exact latency has not been measured; do not attribute
  the seconds to a specific validation/hash/database operation without proof.
* The hard-coded English continuation is an unwanted language input and a
  plausible contributor to the language switch, not a proven sole cause.
* Desired interaction: one explicit selection submits the real choice and
  resumes the advisor; one explicit exact-proposal approval submits that
  decision and resumes the permitted execution/read-back. No extra Continue
  and no application-invented user sentence. Preserve conversational language.
* Safety does not require the redundant UI action: the backend must still
  validate/store the exact human event before permitting the agent to
  continue. Selection never implies proposal approval. Reload, retries or
  the model itself must not manufacture a human event.
* Design implication: revisit the frontend/backend interaction contract,
  including the endpoint that currently requires one new user text and
  rejects resume/tool results. Do not silently hide the old English message,
  translate it, or auto-click Continue as a substitute for proper semantics.
* Proposed next step: S-040 verifies the supported native Agent Framework/
  AG-UI/CopilotKit handoff for the installed versions and produces one
  concrete replacement contract. Native HITL/resume suitability is not yet
  established by this local review; do not claim a transparent adapter
  migration or managed-agent compatibility without checking it.
* Boundary: source review and tracking only. No application changes,
  authenticated access, model calls, publication or deployment in this turn.
  S-039's live evidence remains valid but does not prove user UX acceptance.

## S-037 CopilotKit Integration Analysis

Subsequent implementation evidence:
[S-038/A-025](../implementation/log.md#a-025---s-038-local-copilotkit-compatibility-slice)
tests the available stable 1.82.0 candidate locally. The boundary below
describes S-037 at completion; it does not erase the later separately
authorized compatibility slice or establish live Foundry verification.

### Outcome and evidence boundary

CopilotKit is a suitable candidate for the requested chat-first demo.
Recommend a local React/TypeScript frontend using its v2 styled components
and AG-UI client, retaining FastAPI, the guarded Agent Framework path and
the managed Foundry advisor. Do not introduce a second agent runtime,
CopilotKit-hosted model or application workflow engine.

This is a completed documentary/local-source analysis, not a working
CopilotKit integration. No frontend packages were installed, no application
code changed, no servers started and no Azure/model/export operation ran.
The [source register](../../../../docs/research/sources.md#copilotkit-complete-integration-analysis)
records freshly inspected public sources, exact published package metadata
and limitations. [Q-039](../questions.md#q-039---conversational-ui-library)
selects CopilotKit for analysis; implementation remains unapproved.

The recommendation is based on Microsoft's explicit integration reference,
the AG-UI-maintainer ecosystem and the fit to agent/tool/human interaction,
not a claim that assistant-ui cannot provide these capabilities.
No Microsoft support or production certification is inferred.
Sources: [CK01](../../../../docs/research/sources.md#ck01),
[CK07](../../../../docs/research/sources.md#ck07).

### Existing backend and concrete integration gaps

| Surface | Verified current behavior | CopilotKit implication |
| ------- | ------------------------- | --------------------- |
| [ui.py](../../../../src/supply-chain-resilience/supply_chain/ui.py) | One user message per run; browser history, tools, state, resume and forwarded authority are rejected | Default full-thread SDK requests are not plug-and-play |
| [ui_stream.py](../../../../src/supply-chain-resilience/supply_chain/ui_stream.py) | Official framework adapter, provisional message text and native tool events | Retain it; replace browser parsing with the SDK rather than another model loop |
| [conversation.py](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py) | Trusted selection/approval outside the model; final evidence equality/read-back checks | Render contextual actions against existing backend methods |
| [advisor.txt](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/prompts/advisor.txt) | Ask for missing preference, explain exact proposal and wait for application approval | No new frontend approval tool is necessary |
| [session.py](../../../../src/supply-chain-resilience/supply_chain/session.py) | Native session, drift checks, running/usage uncertainty and file locks | Frontend threads must bind to actual server-created case IDs |
| Existing stream terminal | `CUSTOM validated_answer`, then `RUN_FINISHED`, after resource closure and persistence | Generic SDK completion is insufficient to mark the application answer validated |
| Existing startup | No inference unless explicitly enabled; no Azure call for bootstrap | Replace ambiguous status labels, not the authorization boundary |
| Existing browser history | Planner text and validated result; no complete persisted SDK event transcript | Hydrate display history without pretending to replay/reconnect a live model run |

### Recommended local architecture

```text
Browser: CopilotKit v2 styled chat/view + contextual application cards
  -> case-bound AG-UI HttpAgent transport
  -> same-origin FastAPI /api/cases/{case_id}/run
  -> existing official framework AG-UI adapter and guarded conversation
  -> native FoundryAgent stream / server-owned AgentSession
  -> existing exact managed Foundry advisor version

Contextual cards -> existing trusted /actions route
Diagnostics -> read-only case snapshot/history/events
```

Use React and TypeScript with a Vite build under a dedicated frontend
directory. Serve its built assets from the existing Python origin.
Node is a frontend development/build dependency, not necessarily another
running application server. Do not add Next.js server rendering, a GraphQL
gateway or a Copilot Runtime just to host static chat components.
Keep the user-facing launch path to one documented command after building.

The documented direct local agent option is `agents__unsafe_dev_only`.
It is a deliberately dev-only integration, not a security certification or
a production pattern. The local backend must keep its Host/Origin checks,
action token, no permissive CORS and server-owned capability checks.
Production would require a separate choice between the recommended
TypeScript runtime path and a properly licensed self-managed route.
Sources: [CK02](../../../../docs/research/sources.md#ck02),
[CK03](../../../../docs/research/sources.md#ck03).

Do not treat the Python Agent Framework backend as CopilotKit's separate
Python Copilot Runtime. The latter has different Intelligence requirements.
Do not enable Intelligence, built-in model agents, memory, analytics,
automatic learning, A2UI, sandboxed UI, MCP Apps or frontend tools for this
increment. Those are optional product capabilities, not demo prerequisites.

### Versions, packaging and license findings

| Item | Observed evidence | Proposed treatment |
| ---- | ----------------- | ------------------ |
| `@copilotkit/react-core` | Versioned package 1.84.1, MIT, `/v2` and `/v2/styles.css` exports | Candidate baseline; not yet installed or approved as a final pin |
| CopilotKit v2 | API import surface inside package version 1.84.1 | Do not confuse API v2 with npm major version 2 or mix v1 imports |
| AG-UI JS | react-core/core 1.84.1 depend on client/core 1.0.2 | Align direct dependency with 1.0.2 initially; avoid a second latest 1.0.3 instance |
| React | Published peers support 18 or 19 | Choose one compatible exact React/ReactDOM pair in the implementation lockfile |
| Zod | react-core peer `>=3.25`; AG-UI client uses `^3.25.76` | Prefer an aligned Zod 3 resolution for the first compatibility check |
| Node | CopilotKit core declares `>=20`; local Node is 26.13.0, npm 11.20.0 | Numeric bound satisfied, not proof of the complete toolchain support matrix |
| Python integration | Installed framework AG-UI 1.7.1, protocol 0.1.22, core 1.24.0 | Preserve proven pins; do not upgrade Python to match JS package numbers |
| Wire protocol | JS package advertises AG-UI protocol 1.0 | Test actual Python-emitted events; SDK version differences alone prove neither compatibility nor incompatibility |
| License | Published react-core license and project OSS guide say MIT | Retain required notices; separately evaluate any non-OSS feature before using it |
| Registry access | Public npm metadata reads failed TLS through PowerShell and curl | Environment prerequisite for future installation, not a package incompatibility; no certificate bypass |

Versioned public CDN manifests and declarations were readable after npm
registry TLS failures. They establish the inspected artifacts, not successful
resolution against this machine's configured package feed or a verified latest
release. Do not persist credentials or change registry/certificate settings
without separate agreement. Pin the selected artifacts and commit the
lockfile only under a future authorized implementation.
Sources: [CK04](../../../../docs/research/sources.md#ck04),
[CK05](../../../../docs/research/sources.md#ck05).

The OSS guide explicitly supports chat, AG-UI and application-owned storage
without Intelligence. Saved cross-device "AG-UI Streams" is a separate
product feature, not the ordinary SSE stream already implemented here.
The existing local persistence can remain authoritative. No new CopilotKit
account, model-provider key or subscription is justified.

The package graph is not minimal: react-core includes other renderers and
`@scarf/scarf`. Installation analytics, browser network defaults, optional
feature activation and third-party notices must be checked. There is no
measured bundle size, vulnerability audit or zero-egress proof yet.
The acceptance target is no automatic traffic to CopilotKit-hosted or
other unapproved services, beyond approved package acquisition.

### Chat-first UX and human interaction

Use one central conversation, a compact case selector/new-conversation
control and an optional diagnostic drawer. Start from CopilotKit's styled
view, composer and message components; customize slots rather than
rebuilding a bespoke chat shell.

| Moment | User-visible behavior | Authoritative source |
| ------ | --------------------- | -------------------- |
| First visit | Welcome, explanation of synthetic scope and a usable start action | Local application copy, explicitly not an agent-generated greeting |
| Question | Send creates/binds a fresh case if needed, then streams the agent response | One explicit user submission, one run ID |
| Investigation | Concise tool activity can expand inline; partial answer is labeled provisional | Actual AG-UI events, not a scripted stage animation |
| Preference needed | Inline comparison card beside the validated explanation, showing cost, quantity, dates and both customer margins | Exact current comparison evidence |
| Selection | Card records STANDARD or EXPRESS and shows a human-action receipt | Existing backend selection action; no inference from chat text |
| Next turn | Explicit "Continue with advisor" within the conversation | Existing separate run action |
| Proposal ready | Exact-proposal card with route, quantity, cost, timing and approval/rejection | Validated proposal plus fresh server decision state |
| Approval/rejection | Decision receipt appears inline; pending buttons become disabled | Backend exact-ID approval/rejection, never a client tool result |
| Completion | Verified reservation summary with expandable current/historical evidence | Validated final result and durable read-back |

Do not translate fictional option costs into EUR merely because inference
budgets use EUR. Business costs are synthetic cost units. Explain that
STANDARD costs 90 and EXPRESS 95; EXPRESS buys one day of margin, without
inventing a probability or a uniquely optimal option.

Render-only `useRenderTool` can enrich backend tool activity without
registering callable functions. An actionable card must wait until the
application's final validation and successful terminal event, even when
its underlying tool result has already streamed. Anchor decision cards
after the corresponding assistant explanation, not permanently in a sidebar
or before the user has context. Message slots can supply that placement.
Sources: [CK06](../../../../docs/research/sources.md#ck06),
[CK07](../../../../docs/research/sources.md#ck07).

The current model contract contains exactly `message` and `evidence`;
it has no machine-readable `request_human_choice` intent. Recommended
baseline: project card eligibility server-side from the last validated
current comparison/proposal evidence, actual decision state and snapshot.
The existing prompt instructs the agent to ask and stop at those boundaries.
This is contextual application UI, not a claim that the model emitted an
AG-UI interrupt. Do not infer request intent by searching natural-language
words. If an exact explicit agent-request signal is required in every case,
designing and publishing a revised model response contract or request tool
is a separate step, not a silent part of this frontend migration.

Revalidate card eligibility and staleness at action time. Earlier cards
remain readable but cannot approve a different/newer proposal. Validate
server eligibility for selection too; browser visibility is not a permission.
Display disabled states with reasons, including pending stream, prior
decision, stale facts, drift and uncertainty.

Retain separate decision recording and Continue by default. A future
"Select and continue" or "Approve and execute" action changes cost/behavior
and must be explicitly agreed; merely moving buttons into chat does not
authorize automatic inference.

### Native human-in-the-loop hooks are not a drop-in replacement

CopilotKit's `useHumanInTheLoop` creates a frontend tool and resolves it
through a UI response callback. Our managed definition exposes no approval
tool, and the HTTP boundary explicitly rejects client tool declarations.
Installing that hook would change the contract, not connect the existing
approval mechanism automatically. `useInterrupt` similarly expects an
interrupt/resume protocol the current application does not implement.

Use render-only components and application action callbacks for the first
integration. These actions remain out-of-band trusted human events and
are recorded before the next native model turn. Do not add model-callable
approval, relax the allowlist or fake a paused framework function.
This distinction preserves the existing agent-led conversation without
building a new deterministic reasoning flow.

### Message transport, validation and lifecycle

The SDK owns event decoding and message reconstruction. A small case-bound
transport specialization may use the documented `HttpAgent.requestInit`
extension to send only the new trailing plain-text user message, plus the
actual case/run IDs and local action token. Reject unsupported outgoing
client tools/state/resume rather than silently granting their semantics.
The server's existing input/authority checks remain the security boundary.

CopilotKit's provider `messageFilter` is documented in source for runtime-
proxied agents, not direct agent instances. It is not sufficient to solve
our direct request mismatch. Test the transport extension against the
selected published types, including `clone()` preserving case URL, token,
projection and cancellation. Do not invent private hooks or manually
duplicate the framework's function/model loop.
Sources: [CK03](../../../../docs/research/sources.md#ck03),
[CK05](../../../../docs/research/sources.md#ck05),
[CK08](../../../../docs/research/sources.md#ck08).

The high-level `CopilotChat` documents an initial automatic run; its source
also manages connection/suggestion behavior. Prefer `CopilotChatView` plus
`useAgent` and explicit submit/stop handlers if the selected package cannot
disable every automatic operation through supported settings.
This still uses CopilotKit's UI; it does not mean returning to custom
HTML/SSE parsing. Opening, mounting, reloading or switching cases must
generate zero inference requests. No automatic suggestions, retry,
regenerate, edited-message resubmission or tool follow-up should run.

Maintain per-run validation state through `onCustomEvent` and terminal
subscriptions. A tool renderer's `complete` status is not a validated answer.
`onRunFinalized` fires on failures too and cannot authorize success.
Require the matching server `validated_answer`, then `RUN_FINISHED`;
transport errors or EOF before both mean no UI success. Replace provisional
text with the authoritative validated message and refresh the durable
read-only view. Any reconciliation is inspection, not inference replay.

Bind a single active frontend agent to one server-created case. Abort and
dispose subscriptions before replacing it; prevent cross-case event leakage.
The browser case ID is not the native Foundry conversation ID: preserve
the shared telemetry correlation and existing exact managed-version binding.

Hydrate validated display history from the backend, not local storage as
authority. Add stable turn/display-message identifiers and typed
interaction/validation metadata to UI history/events as necessary.
Keep metadata separate from model inputs and native AgentSession state.
Do not store complete vendor transcripts or native credentials in tracking.
Restoring display history does not resume a stopped/in-flight run.
Historical cases affected by new fingerprints remain read-only/blocked;
no migration/reset/rebind is implicit.

### Connection status, observability and visual acceptance

Separate transport configuration from a verified live model call:

| State | Required explanation and action |
| ----- | ------------------------------- |
| Inference disabled | "Foundry calls are disabled for this server"; explain startup configuration before showing a usable composer |
| Configured, not verified | "Configured for Foundry; no call has been made yet"; do not claim a successful connection |
| Running | Visible streaming/Stop state; no concurrent decisions or sends |
| Previously verified | Identify managed agent/version and last successful turn without implying every future request will succeed |
| Offline test fixture | Persistent, unmistakable "simulated responses, not Foundry" label |
| Blocked/uncertain | Explain that effects may already exist; allow inspection/new case, not retry/reset |

Do not automatically authenticate just to make a connection badge green.
Keep endpoint/tenant/credentials and live/export policy server-side.
Live model calls and trace export remain separately authorized operations.
The UI can explain missing configuration without granting itself permission.

Place tool details, usage, IDs and raw evidence in a closed-by-default
diagnostic drawer. Show concise human-readable summaries in the chat.
Maintain keyboard navigation, focus after actions, readable contrast,
screen-reader streaming/status announcements and mobile layouts.
Test raw HTML/script payloads, Markdown links and external images; never
enable unrestricted HTML. Preserve script CSP and same-origin action
protection; identify style/nonces needed by actual components instead of
blindly weakening policy. Browser console/CSP failures are acceptance failures.

Use the existing common telemetry module, once per server, with per-agent
policy. CopilotKit Inspector can optionally inspect local events during
development; it is not a replacement for Foundry/Application Insights
traces, and saved Inspector/Intelligence features are out of scope.

### Change surfaces and retirement strategy

| Surface | Expected future change |
| ------- | ---------------------- |
| New frontend directory | Package manifest/lock, TypeScript/Vite config, CopilotKit provider/view, case transport, contextual cards and focused UI tests |
| Existing static web assets | Replace after parity; do not keep a second user-facing legacy interface or alternate runtime path |
| [ui.py](../../../../src/supply-chain-resilience/supply_chain/ui.py) | Serve hashed build assets, clearer configuration/interaction projections and stable UI history metadata |
| [ui_stream.py](../../../../src/supply-chain-resilience/supply_chain/ui_stream.py) | Preserve native binding; expose only required stable UI metadata without changing managed instructions |
| [session.py](../../../../src/supply-chain-resilience/supply_chain/session.py) | Explicit frontend source/lock/build identity rather than reading arbitrary generated directories as text |
| [ui_demo.py](../../../../src/supply-chain-resilience/ui_demo.py) | One clear local launch path and startup explanation; never silently enable live/export |
| Tests and README | Actual SDK wire tests, composer/card lifecycle, no auto-runs, build/launch and failure instructions |
| Managed agent/domain/store/runtime | Reuse unchanged unless a proven tightly coupled defect requires a separately reviewed scope adjustment |

Fingerprint relevant frontend sources, lockfile and actually served build
identity, excluding node_modules and volatile caches. The current top-level
web-file hashing cannot simply be pointed at a generated assets directory.
Retain open-source notices in distribution and make a missing build an
explicit actionable error, not a fallback to the old interface.

### Acceptance gates and residual risks

| Gate | Required measurable evidence |
| ---- | ---------------------------- |
| Dependency reproducibility | Exact pins/lockfile, peer/type/build checks; no disabled TLS verification or hidden hosted requirement |
| Protocol compatibility | Actual Python SSE consumed by selected JS client: split text/arguments, tool results, custom validated event, success/error terminals |
| No unsolicited inference | Zero requests on mount/reload/case switch, decision-only actions and default-disabled startup |
| Conversation continuity | Second/third turn succeeds without resending trusted history; no duplicate model context; reload preserves validated display |
| Card timing | No choices on welcome/unrelated turns; interactive comparison/proposal cards only after matching successful validation |
| Human safety | Wrong/stale IDs, browser state/tools/approval text and double clicks cannot grant or duplicate reservation |
| Success semantics | No validated badge/card activation on malformed evidence, error, resource-close failure or incomplete stream |
| Cancellation | Abort before terminal and after committed write retains durable uncertainty/effects, releases lock and never replays |
| Full synthetic case | One reservation/read-back, source 80/70/10, destination 20; no physical shipment claim |
| Case isolation | Switching/unmounting cannot send to another case or leak late events into it |
| Privacy/network | No unapproved third-party runtime traffic or payload export; preserved per-agent trace filtering and managed conversation identity |
| Usability | Desktop/mobile/browser keyboard checks, visible reason for disabled Send, no primary raw-JSON panels, no console/CSP failures |
| Regression | Existing Python application/SDK-free tests and documentary checks continue to pass |

None of these new CopilotKit integration gates has been executed in S-037.
Prior S-036 tests cover the existing backend, not this new frontend stack.
The most important unresolved gate is actual wire/SDK behavior with the
pinned Python adapter; another is package access after registry TLS failure.
Do not replace either with assumptions based on matching marketing terms.

### Proposed next increment

Recommend [S-038 revision 1](../plan/plan.md#s-038-revision-1-local-copilotkit-compatibility-slice):
one local compatibility slice with the selected published CopilotKit
components, actual guarded backend and explicitly simulated upstream I/O.
Prove transport, no unsolicited inference, terminal-validation rendering
and contextual decision behavior before replacing the entire interface.
If it fails, stop with the exact gap; do not automatically upgrade the
proven Python packages, add Intelligence or publish a new agent contract.

This limits the next implementation commitment without postponing the
design: the target UX, responsibilities, build path and full acceptance
matrix above are already defined. Live Foundry walkthrough and any
full-interface replacement require their own explicit scope and approval.

## S-023 Learning-Goal Correction

On 2026-11-03 the user explicitly requested an agent-led experience, clear
agent/tool/data code separation and a renewed prompt-management/GenAIOps
review. This is a faithful English summary, not a verbatim quotation.
The existing positive S-022 test remains valid, but the fixed phase driver
is a baseline rather than fulfillment of conversational agent autonomy.
The [documentary review](evidence.md#s-023---agent-led-design-and-prompt-lifecycle-review)
records source verification, the current architecture gap and recommendation.

* RQ-013, confirmed user expectation: make agent definition/instructions,
  runtime transport, tools and data responsibilities explicit without
  overengineering; reinforces the earlier code-organization request.
* RQ-014, confirmed requested analysis: verify prompt lifecycle practices
  against the knowledge base and current public Microsoft sources, including
  GenAIOps. A particular file format or pipeline has not been accepted yet.
* RQ-011 remains effective: agent learning must drive the demo. Recommend
  agent-led information gathering and conversation, not adding more agents.

The proposed D-013/S-024 direction narrows the application to tool execution,
human approval and invariant enforcement, retaining D-012's managed Foundry
agent. It revises D-008's detailed phase enforcement if accepted; the learning
goal, selected business scenario and approval/write boundary do not change.
No application-code changes or further cloud authorization follow from this
analysis request.

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

## S-011 Planning Output

The [version 1 implementation plan](../plan/plan.md) translates the accepted
learning-first design and managed prompt-agent/Python direction into bounded
future steps. It is proposed and does not authorize implementation.
Cloud prerequisites, exact package compatibility, simple store/actor choices,
budgets and trace/evaluation gaps remain explicit gates rather than assumed
configuration. S-012 is the next proposed documentary plan review.

## S-019 Revision 2 Local Tool Outcome

After clarification of the local preparation versus real Foundry agent,
the user explicitly authorized reusable Python business functions at
16:59 +01:00 on 2026-11-02 and requested simple, organized code at 17:06.
This superseded the paused S-019 revision 1 form without erasing its history.
Plan version 2 consolidates the work into three milestones; only the first
local increment is authorized.

The [implementation log](../implementation/log.md) records the package's
domain, SQLite and dispatcher boundaries, thin CLI, actual files and tests.
All 34 runtime tests passed. The six future function-calling tools reuse
the same calculations and durable action functions; human approval remains
outside model-invocable tools. No HTTP API or MCP service was added.
The original learning-first scope and accepted synthetic numbers remain intact.
This is not runtime evidence for a Foundry agent, SDK, identity or tracing.
All 10 documentary/link checks also passed. S-019 revision 2 is completed;
its authorization is consumed. The next real-agent milestone is proposed
only, with no cloud target, model, permissions or call budget silently chosen.
