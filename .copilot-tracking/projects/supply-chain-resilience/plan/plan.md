---
title: "Implementation Plan for supply-chain-resilience"
description: "Proposed learning-first increments for a managed Foundry prompt agent with a thin Python driver."
ms.date: "2026-11-05"
plan_version: 2
status: "sharepoint-source-knowledge-provisioned"
---

## Current Version 2 - Three Learning Milestones

## S-048 Revision 1 Assign Existing Demo Readers

* Status: completed as A-033 under Q-051/Q-052; authority consumed.
  Exact users, exclusive reader memberships and unchanged folder ACLs
  verified. Both users have zero assigned licenses; direct reader sign-in
  and Foundry delegation remain separate, unapproved work.
* Objective: assign the two manually created demo users to the existing
  SharePoint reader groups. User-reported names are not verified identities.
* Target: demo tenant db60e921-9c3c-4fd4-98d1-4445db7ab425 and
  <https://mngenvmcap946525.sharepoint.com/sites/supply-chain-resilience-lab>.
* Proposed exact aliases: UserDemo01 and UserDemo02 in
  MngEnvMCAP946525.onmicrosoft.com, pending user confirmation.
  Do not search broadly or select accounts by ambiguous display names.
* Recommended matrix: UserDemo01 to group 10 only, UserDemo02 to group 11
  only. General already grants both groups Read; Restricted Procurement
  already grants only group 11 Read.
* Included actions: targeted operator/exact-user verification, enabled
  Member state and active directory-role checks; same-owner site/group,
  membership, site-admin and folder ACL preflight; ensure the two site
  principals, add only the agreed reader memberships and verify read-back.
* Excluded: user creation, password/credential handling, license/role/consent
  changes, account switching/elevation, folder ACL changes, broad inventory,
  deletion, interactive test-user sign-in, runtime/OBO, inference and Git
  publication. Preserve S-047's unused encrypted credential files untouched.
* Acceptance: exact approved existing users, no observed admin role or
  site-admin status, agreed exclusive reader matrix, unchanged folder ACLs.
  Membership does not prove licenses, interactive allow/deny or Foundry OBO.
* Cost/risk: document Read grants only; no purchase, new Azure resource or
  model call. Stop if identities/rights/grants are ambiguous or unexpected;
  preserve and report partial writes without escalation or automatic removal.
* Alternatives: reversed mapping, targeted read-only preflight, or defer.

## S-047 Revision 1 Two Entra Demo Users and Reader Membership

* Status: blocked under Q-050/A-032. First create POST returns HTTP 403
  Authorization_RequestDenied. Both users are confirmed absent and neither
  SharePoint membership was changed.
* Observed prerequisite gap: current operator has Global Reader only in
  the successful transitive directory-role read. User Administrator is the
  documented least-privileged administrator role for creating these users.
  Do not activate/grant any role or consent automatically.
* Preserved local partial state: two unused DPAPI-encrypted credentials
  in LOCALAPPDATA/FoundryMultiAgentLab/credentials/
  supply-chain-resilience-s047, restricted to the current Windows user.
  Future resumption must explicitly handle these without overwriting them.
* Next prerequisite: user checks/activates an eligible User Administrator
  role through their approved process, if available, or obtains help from
  an authorized administrator. No eligibility or role change is assumed.
  Reconfirm execution after this pause before any new POST.
* Objective: create two synthetic non-admin member users and assign each
  to its intended existing site-local reader group.
* Target: existing demo tenant db60e921-9c3c-4fd4-98d1-4445db7ab425 and
  <https://mngenvmcap946525.sharepoint.com/sites/supply-chain-resilience-lab>.
  Confirm its verified account domain and current operator before writing.
* Proposed aliases: scr-planner-demo and scr-procurement-demo; display
  names SCR Planner Demo and SCR Procurement Demo. Resolve exact names
  and check collisions; do not adopt, reset or overwrite an existing user.
* Reader matrix: planner to SharePoint group 10 only; procurement to group
  11 only. Preserve existing folder ACLs, owners and empty-directory-group
  design. Do not add users to site Members, Owners or administrator roles.
* Credential option: cryptographically generated distinct temporary
  passwords, force first-sign-in change, Windows DPAPI encrypted
  credential file(s) outside the repository in LOCALAPPDATA/
  FoundryMultiAgentLab/credentials. Verify local decryptability without
  exposing plaintext. Secure passwords before create to avoid losing
  credentials after a successful directory operation.
* Alternative mode: create disabled accounts without enabling sign-in,
  or perform only the targeted read-only preflight, as selected in Q-050.
* Preflight: only operator/domain, two exact proposed users and the named
  SharePoint groups/site. No broad directory inventory or permission grant
  to make an unsupported client work. Use supported Graph v1.0 user create
  and same-tenant owner-authenticated SharePoint membership operations.
* Acceptance: two intended directory objects with selected enabled state;
  no assigned administrator role or site-admin status; correct, exclusive
  reader-group membership; no new license/role assignment; folder ACL
  matrix unchanged. Distinguish configuration from actual user sign-in.
* Risk/cost: new login identities and local credential material; no new
  license purchase, direct assignment or Azure resource/model spend.
  Existing tenant policies still apply. An unlicensed user may not be able
  to use SharePoint even with correct group membership.
* Excluded: app registration/consent, role elevation, MFA/security-default/
  Conditional Access changes, license assignment, Entra groups, other-site
  changes, existing-account password reset, deletion, user sign-in as those
  accounts, Foundry/OBO integration, inference, delegation and remote Git.
* Recovery: stop on collision, missing rights, ambiguous create result or
  secure-storage failure. Preserve and report partial results with secrets
  redacted; no blind POST retry or automatic deletion.
* Source: [Graph create user](https://learn.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0),
  retrieved 2026-11-04, updated 2026-07-04; requires verified UPN domain,
  accountEnabled, displayName, mailNickname and passwordProfile. Permissions
  and operator role remain unverified; none are automatically granted.

## S-046 Revision 1 SharePoint Site, Groups, Folder ACLs and Upload

* Status: completed under Q-049 authorize_site_groups_upload_acl, A-031.
  Authority consumed; reader groups remain empty as explicitly requested.
* Outcome: one ready non-group-associated site; default Documents library;
  General and Restricted Procurement have unique, exactly checked folder
  grants. Two approved Word files in each folder inherit those grants.
  Reader groups 10 and 11 are empty, cannot edit membership and cannot
  self-join. Authenticated owner and associated owners retain Full Control.
* Payload check: all four approved word/document.xml hashes match remote
  reads exactly. SharePoint processed the ZIP packages, so full package
  lengths/hashes are recorded separately rather than claimed identical.
  No Foundry/SQL integration or two-user retrieval test occurred.
* Objective: one actual SharePoint knowledge site with two permission-
  separated folders and four approved synthetic Word documents.
* Exact target:
  <https://mngenvmcap946525.sharepoint.com/sites/supply-chain-resilience-lab>
  in the previously verified demo tenant; title Supply Chain Resilience Lab.
  Use a non-group-associated team site, English locale, current verified
  demo caller as owner. No directory group, mailbox or Team is requested.
* In scope: create at most one new site; check readiness; use/create one
  document library; create General and Restricted Procurement; create two
  site-local groups SCR Planning Readers and SCR Procurement Readers.
  Preserve owners' Full Control; reader groups have no approval/write powers.
* Matrix: General grants Read to both reader groups. Restricted Procurement
  grants Read only to SCR Procurement Readers. Break inheritance on the
  new protected scopes where necessary and remove broad/inherited grants
  that would bypass this matrix, only in the newly created site.
* Upload exactly Disruption Response Guide.docx and Transfer Evaluation
  Guide.docx to General; Supplier Recovery Conditions.docx and Commercial
  Escalation Guide.docx to Restricted Procurement. No PDFs or source copies.
* Membership: initially empty groups unless a user-approved local mapping
  supplies actual test users. No invented principal or automatic group-wide
  membership grant. No personal account data in canonical tracking.
* Acceptance: ready site at the approved URL; read back actual folder role
  assignments and permission inheritance; two reader groups without elevated
  roles; four correct filenames/lengths/content hashes; no anonymous, external
  or tenant-wide grants created. Owners necessarily retain privileged access.
* Explicit limitation: no two-user allow/deny claim until real non-admin
  readers are assigned and tested. This is SharePoint setup, not Foundry
  delegated retrieval, index readiness or OBO integration verification.
* Methods: authenticated browser/SharePoint REST within the verified host,
  normal UI file upload from the approved local files; no token export or
  fallback to a different tenant/account. Recheck caller before first write.
* Risks/cost: approximately 213 KB of payload plus site overhead against
  existing SharePoint quota/licensing. No Azure resource or model spend.
  A successful read does not prove site-creation or permission-change rights.
* Stop controls: if target already exists, identity differs, rights fail or
  provisioning result is ambiguous, inspect only this target's status and
  report the blocker. No blind creation retry or adoption of an existing site.
* Excluded: root/other-site ACL changes, Entra groups/users, consent/app
  registration, privilege elevation, external invitations/sharing links,
  runtime integration, publication, inference, SQL, delegation and remote Git.
* Recovery: preserve and report named partial resources; deletion or an
  alternate target requires separate consent. No automated rollback deletion.

## S-045 Revision 1 SharePoint Corpus and Targeted Preflight

* Status: completed under Q-047/Q-048, recorded in A-030; consent consumed.
* Outcome: four English synthetic DOCX/PDF guides, each two pages, sources
  retained beside outputs in session files/sharepoint-knowledge. Strict
  content checks, all-page visual review and payload checks pass.
  Word-dialect sources stay with standalone deliverables, not repo documents.
* Browser preflight: expected demo account matches; root IsSiteAdmin=false;
  proposed new URL returns SiteStatus=0. Neither result proves write/admin
  authority. No remote write, upload, consent or account change occurred.
* User request: create synthetic documents, a SharePoint site and two folders
  with distinct access. Provisioning awaits exact targets/access matrix.
* Objective: prepare four short English synthetic knowledge documents and
  verify the named SharePoint target, existing group references and available
  site/folder/upload/ACL operations before presenting an execution contract.
* Suggested site name: Supply Chain Resilience Lab. Proposed folders:
  General and Restricted Procurement. Planner readers can read General;
  procurement readers can read both; owners retain administrative access.
  No broad default member/visitor grant may bypass the restricted folder.
* Draft content: disruption triage and transfer evaluation for General;
  synthetic supplier recovery conditions and commercial/escalation guidance
  for Restricted Procurement. Stable source IDs/version/date, explicit
  synthetic status and no conflict with authoritative stock/cost/approval.
* Local deliverables: standalone source/DOCX/PDF corpus in the session
  files/sharepoint-knowledge folder; necessary canonical tracking stays in
  this project. DOCX is the selected upload format after Q-048.
  No application dependency or runtime change.
* Read-only scope after consent: only the named tenant/site or parent,
  current ownership/creation capability, named groups and relevant ACLs.
  No broad tenant, directory or unrelated site inventory.
* Acceptance: coherent draft contents and source metadata, named target
  and access matrix, supported operation/permission evidence or explicit
  blockers. Documentary checks cover Markdown links/structure.
* Tool discovery so far: WorkIQ exposes SharePoint folder creation/upload
  preparation and drive-item permissions; no SharePoint site creation or
  inheritance-management action was returned. This is capability discovery,
  not authenticated tenant verification or proof of write authority.
* Actual preflight: current CLI tenant matches the authorized demo tenant;
  Graph GET sites/root returns
  <https://mngenvmcap946525.sharepoint.com>. Direct SharePoint REST read fails
  with Unauthorized/invalid_request and requires interactive authentication.
  Browser sign-in is open; no account logout/login or consent was performed.
* Group refinement requested by user: propose two site-local reader groups
  rather than new Entra/Microsoft 365 groups. Names and memberships remain
  unapproved; site-owner privileges are not a valid denied-user test.
* Excluded: site/group/user creation, upload, grants/inheritance changes,
  admin consent, app registrations, external/anonymous sharing, deletion,
  Foundry publication/integration/inference, SQL, delegation and Git changes.
* Cost/risk: no provisioning or model cost in this step; drafts contain only
  synthetic data. No secrets/tokens or personal identities in tracking.
* Recovery: preserve drafts and report missing capability/permissions.
  Do not replace source ACLs with prompt rules or broaden privileges.
* Follow-up contract: exact site/folders, verified group IDs, upload format,
  ACL changes, owners, storage impact, read-back and two-user allow/deny
  checks; separate approval before the first remote state change.

## S-044 Revision 3 Database OBO and RLS Feasibility

* Status: deferred proposal after the 17:41 SharePoint document request.
  No SQL execution was authorized or started.
* Objective: define the smallest real user-delegated database slice before
  choosing SharePoint solely as an easier alternative.
* Candidate: existing Python/AG-UI chat, genuine Entra sign-in, a narrow
  read-only function, Azure SQL with user-delegated tokens and a database
  RLS security policy. No generic SQL tool or model-selected principal.
* Knowledge option: a few short synthetic document/knowledge rows with
  title/body/source/version and per-user access. This demonstrates protected
  knowledge retrieval through a tool, not native Foundry file search or a
  newly implemented semantic-RAG platform.
* Design scope: local/public sources and canonical tracking; identify
  identity/token audiences, API consent/SQL principals, exact Python driver
  candidate, costs/prerequisites and user-owned history/cache boundaries.
  No authenticated tenant inventory is included without separate consent.
* Acceptance design: prove SQL sees user A versus B, same tool returns only
  permitted rows, a direct forbidden-ID query cannot bypass RLS, and
  authentication failures do not fall back to developer/agent credentials.
  Keep restricted data out of other tool paths, context, citations and logs.
* Simplicity: one table plus necessary access mapping/policy, one read-only
  capability, two real test users. No purchasing writes, new agents, MCP
  server, DAB deployment, vector engine or complex workflow.
* Excluded: code/package changes, provisioning, IAM/consent/app registrations,
  data ingestion, model runs, publication, delegation or Git operations.
* Recovery: report unsupported token/driver/tenant constraints. SharePoint
  remains an alternative; never label a shared SQL identity plus a model
  user_id filter as true user OBO.

## S-044 Revision 2 User-Scoped Knowledge Design

* Status: superseded proposal by revision 3 after Q-046's database question.
  No implementation was started.
* Reason for revision: user prioritizes document location and least-privilege
  user delegation/OBO, including future structured-data RLS, over adding
  another business strategy immediately.
* Objective: one small knowledge slice with genuine signed-in user identity
  and effective per-document authorization, not a prompt-based permission.
* Expected design: compare SharePoint delegated retrieval with Azure storage/
  Search; define browser login and token audiences, resource enforcement,
  citation projection, user-owned conversations/cache/audit, and two-user
  allow/deny tests. Explicitly identify native/preview/custom components.
* Separate follow-up: structured-data tool and real RLS; OBO authenticates
  the user while database/API policies determine permitted rows.
* Scope: local/public sources and canonical tracking only until an execution
  contract is accepted. No tenant queries, app registrations, IAM/consent,
  provisioning, ingestion, application edits, publication or inference.
* Acceptance: actual identity at each boundary, no developer/agent-wide
  fallback for denied user reads, no unauthorized snippets/titles/citations
  entering the model context, no cross-user history/cache access.
* Cost/recovery: no model spend or cloud state change in design. Keep v5
  operational; report unsupported channel/delegation combinations instead
  of silently approximating OBO with a user ID parameter.

## S-044 Revision 1 Knowledge and Alternate Recovery Design

* Status: superseded proposal by revision 2 after the 17:30 user direction;
  no implementation was started.
* Objective: define one learning-focused vertical slice: a small synthetic
  knowledge corpus plus a second, advisory supplier-recovery strategy.
* Expected outcome: explain the document/source contract, exact retrieval
  integration candidate, one read-only business-tool contract, one alternate
  scenario and a small set of measurable evaluations.
* Analysis scope if approved: local application/contracts and current public
  Foundry/Agent Framework knowledge/citation sources, canonical tracking.
  Compare managed file search, reuse of an existing search index and bounded
  local document reads without misrepresenting their different capabilities.
* Acceptance: distinguish documents from authoritative operational facts and
  human permission; define how citations survive the JSON/AG-UI/UI boundary;
  identify actual domain and human-control changes for a non-transfer option.
  Specify a missing/conflicting-document case and a transfer-infeasible case.
* Excluded: application/package changes, authenticated tenant inventory,
  document upload/index creation, infrastructure/IAM, publication, paid
  inference/evaluation, ordering/reservation, delegation and Git publication.
* Cost/recovery: no Azure operational change or model spend in this design
  step. Report unsupported paths and prerequisites rather than automatically
  adding infrastructure or a homegrown retrieval service.

## S-043 Revision 1 Readable Data-Driven Explanations

* Status: completed under Q-045/A-029; authority consumed.
* Outcome: exact advisor v5 published/read-back verified; local `.env`
  selects v5. All 164 Python/16 frontend/three offline wire tests pass;
  final frontend build/type-check and offline browser rendering/reload pass.
  No model inference, real human action or saved-case migration was performed.
* Objective: a generic explanation style driven by authoritative dates,
  entity labels and currency, not prompt examples tied to the fixture.
* Local scope: scenario/domain/tool output and necessary persistence,
  prompt, frontend rendering where required, exact-definition regression
  tests, local `.env` version and README/tracking.
* Proposed fixture convention: day 1 is 2026-11-09; consecutive calendar
  days, not business days. Explicit EUR synthetic costs and descriptive
  entity labels retaining stable IDs. These values belong to data only.
* Prompt: explain impact, distinguish options and ask one clear question;
  no fixed products, orders, warehouses, dates, costs or answer template
  filled with scenario values. Missing context must not be invented.
* Acceptance: unchanged quantities/cost/feasibility/approval rules; dates
  map exactly to day slots; alternate calendar/labels/currency tests;
  readable Markdown reaches the actual human question renderer; native
  handoff and source-evidence guards remain intact.
* Optional cloud scope only if selected in Q-045: verify the existing
  tenant/project/advisor/deployment from Q-044, publish at most one new
  advisor version after local checks, retrieve/compare its exact definition,
  update local `.env` to that returned version. No model run is included.
* User correction at 14:19 +01:00 permits necessary saved-case changes
  and asks not to add migration complexity. Do not build a migration system.
  Prefer a new chat for the new definition; do not rewrite historical
  model utterances or manufacture human approvals.
* Excluded: inference, human decision/reservation, resource/IAM/account
  changes, new services/dependencies unless separately justified, delegation,
  stopping user-owned servers, commits or pushes.
* Cost/recovery: no model spend; no new resources. Do not delete versions
  or bulk reset cases. If publication is ambiguous, stop without retry;
  report actual state. Do not bind a new prompt to the old version.

## S-040 Revision 1 Conversational Decision Handoff Design

* Status: completed under Q-042/A-027; analysis authority consumed.
  [The concrete contract](../research/analysis.md#s-040-conversational-decision-handoff-design)
  recommends native human-request tools; Q-043 accepts that architecture.
* Objective: one explicit human action per actual choice/approval, followed
  by advisor continuation after backend verification, without an extra
  Continue or fabricated user text. Preserve conversational language.
* Scope: local frontend/backend/agent contract and installed SDK inspection,
  current official Agent Framework/AG-UI/CopilotKit documentation, and
  canonical analysis/decision/plan tracking. Verify native HITL/resume and
  structured action-result support against the actual managed Foundry path.
* Deliverable: one concrete interaction contract and implementation scope,
  identifying any required managed definition/version changes rather than
  disguising a translated/hidden synthetic user message as a native result.
  Distinguish application decision latency from actual model inference.
* Acceptance: explain exact selection and approval event provenance,
  backend verification before continuation, language preservation, pending
  UI feedback, double-submit protection, cancellation and reload behavior.
  Retain selection versus approval separation and post-write read-back.
* Excluded: application edits, package changes/installations, server/model
  execution, authenticated tenant access, publication, infrastructure/IAM,
  historical-run mutation, delegation, commits and pushes.
* Cost/recovery: no Azure spend or operational state change. Preserve prior
  technical evidence and user corrections. If native support is unsuitable,
  report it and propose a truthful event-driven alternative rather than
  forcing an unsupported SDK pattern.

## S-041 Revision 1 Native Human Handoff Migration Proposal

* Status: completed under Q-044/A-028. Operational authority consumed.
  Published exact advisor v4, verified one real native human choice and
  automatic proposal continuation, and stopped at pending approval.
* Objective: replace action/Continue and invented user messages with the
  selected native decision contract, not a second preview application.
* Expected scope: human tool schemas/prompt/definition, native function
  declarations, conversation/guard/session/UI binding, backend boundary,
  CopilotKit core/hook/transport/lifecycle, related CLI surfaces, regression
  fixtures and launch/tracking documentation.
* Dependency: S-040's architecture decision. First establish actual pinned
  framework/JS compatibility locally; do not assume installed capability is
  an executed integration.
* Real activation requires a new version of the existing managed advisor.
  Before execution, present explicit publication target, live limits, exact
  human-decision boundaries and acceptance/recovery. No publication or
  inference is authorized by the analysis or architectural choice.
* Acceptance direction: one real click per choice/approval, no invented
  user text, same managed conversation/native call provenance, persistent
  waiting and receipts, idempotent phases, no automatic inference on
  mount/reload, explicit uncertainty, final evidence/read-back and language
  preservation. Stop and report if private SDK interfaces would be needed.
* Excluded by default: infrastructure/IAM, new service/provider/agent,
  historical-run rebind/deletion, legacy fallback, delegation, commits/pushes.

### Execution contract presented in Q-044

* Revision: 1. User requests execution at 12:20 +01:00; cloud scope remains
  conditional on Q-044, not inferred from that generic continuation.
* Local scope: the existing application/frontend/tests/README, advisor
  prompt/definition and native tool/session/guard bindings, and canonical
  tracking. Keep current dependency pins unless a proven blocking
  incompatibility requires a separate decision.
* Checks: actual native Framework pause/function-output behavior; pinned
  CopilotKit core runner and JS/Python wire tests; choice/approval/rejection,
  duplicate/stale/cross-case input, cancellation/uncertainty, reload/restart,
  one continuation, zero invented user messages, model-request budgets,
  exact-proposal execution guards, frontend build/type-check and documentary
  checks. Internal upstream fixtures are tests, never a user application.
* Conditional cloud actions: verify the existing Q-044 target; publish at
  most one new advisor version only after local gates; bind fresh cases to
  that exact returned version. One real browser case may run through choice
  and proposal, with expressly authorized EXPRESS preference, then stop
  before human exact-proposal approval. Preserve v3 and all historical cases.
* Limits: 10 native model requests, 20 tools, 40,000 aggregate tokens and
  EUR 2 estimated monitoring, no telemetry export or automatic retries.
* Actual: 4 requests, 6 tools including human requests, 7,760 reconciled
  tokens and EUR 0.1552 conservative estimate, not actual billing.
* Recovery: stop on an unknown SDK contract, target mismatch, source drift,
  ambiguous consumption or exhausted limit. Keep native state/evidence;
  no hidden user text, forced success or automatic retry/rebind. Stop all
  bounded test servers; do not activate a persistent service implicitly.

## S-042 Revision 1 Native Chat UX Review Proposal

* Status: completed as the user's local feedback review at 14:16 +01:00.
  Flow works according to the user; dense explanations and abstract day
  numbers need improvement. S-043 is separately authorized by Q-045.
* Objective: review the user's experience of the real v4 handoff before
  adding more features. Do not infer UX acceptance from technical tests.
* Scope direction: inspect feedback and existing evidence first. Any new
  assistant-led live run or exact-proposal approval requires its own
  explicit target/limits/decision contract.
* Excluded: automatic model work, publication, infrastructure/IAM, historical
  state mutation and Git publication.

## S-037 Revision 1 CopilotKit Integration Analysis

* Status: completed as analysis on 2026-11-04; local/public authority consumed
* Outcome: [complete analysis](../research/analysis.md#s-037-copilotkit-integration-analysis)
  and [A-024](../implementation/log.md#a-024---s-037-complete-copilotkit-analysis).
  Ten documentary/link tests and whitespace pass. SDK integration and live
  compatibility are not claimed.
* Authority: user requests a complete analysis with CopilotKit after Q-039.
  This selects the analysis candidate, not operational implementation.
* Objective: establish a sourced, project-specific architecture and UX for
  CopilotKit over the existing guarded AG-UI backend, with exact dependency,
  licensing, human-decision and lifecycle considerations.
* Scope: public official documentation/package/source reads, local source/
  metadata inspection and canonical analysis/research/question/plan/state
  updates. No authenticated tenant or subscription resource is in scope.
* Included checks: source/API/package-metadata consistency, mapping to actual
  backend behavior, acceptance-test design and repository documentary checks.
  Distinguish documented capabilities from unexecuted integration hypotheses.
* Acceptance: explain contextual choices/approval, actual-versus-offline
  connection status, streaming/final validation, persistence, no-retry
  cancellation, local architecture, version/licensing constraints, affected
  files, risks and one proposed bounded implementation increment.
* Excluded: application edits, dependency installation, package execution,
  server startup, browser actions that run a model, Azure access/inference/
  export/spend, hosted third-party services, published prompt/schema/version
  changes, historical-run changes, delegation and Git publication.
* Cost/recovery: no model/Azure cost; documentary updates only. Preserve
  current runtime and historical decisions; unresolved compatibility becomes
  an explicit implementation gate rather than a claimed successful test.

## S-038 Revision 1 Local CopilotKit Compatibility Slice

* Status: completed; explicitly approved on 2026-11-04 at 10:37 +01:00
  in Q-040. Local authority is consumed. S-037 alone did not authorize it.
* Outcome: [A-025](../implementation/log.md#a-025---s-038-local-copilotkit-compatibility-slice)
  records build/type-check, 12 SDK tests, 3 actual-Python wire tests,
  30 targeted Python tests, 10 documentary checks and browser acceptance.
  Temporary fixture servers/data were stopped/removed. No live verification.
* Resolved candidate: select available stable react-core 1.82.0, whose
  published manifest confirms v2 exports and AG-UI JS 1.0.2. The configured
  feed returns 404 for analysis candidate 1.84.1; direct public npm fails
  TLS. This is an explicit final-pin selection within the candidate gate,
  not a registry/TLS change, prerelease adoption or proven API compatibility.
* Objective: prove a small CopilotKit v2 chat/transport/contextual-card slice
  against the actual guarded Python AG-UI backend before replacing the
  existing interface. This is not a new project or a new runtime agent.
* Inputs: [S-037 analysis](../research/analysis.md#s-037-copilotkit-integration-analysis),
  [proposed D-019](../decisions.md#d-019---copilotkit-chat-first-presentation-proposal),
  Q-038/Q-039 and existing S-036 technical evidence.
* Scope: after explicit approval, add a dedicated frontend manifest/lock,
  React/TypeScript build and focused tests, compatible CopilotKit/AG-UI
  dependencies, a case-bound direct local-development transport and one
  styled CopilotKit chat/view with contextual comparison/proposal rendering.
  Update only necessary UI metadata/test fixture/documentation surfaces.
  Test through the existing guarded endpoint; do not construct another
  native model/function loop or make a permanent parallel legacy UI.
* Candidate baseline: observed react-core 1.84.1 and AG-UI JS 1.0.2.
  Verify actual package availability, peers, API exports and licensing
  before choosing the final lockfile. Preserve all proven Python pins.
  The npm TLS failure is an explicit prerequisite; no certificate bypass,
  unapproved registry/account change or silent version substitution.
* Local targets: this repository's application and temporary loopback test
  service with visibly simulated upstream responses. No tenant/subscription
  resource or real model endpoint operation is in scope.
* Included tests: build/type-check; actual Python SSE through the selected
  JS SDK; multiple turns with only new user input on the wire; local token/
  Origin protection; custom final-validation event; error and cancellation;
  zero automatic inference on mount/reload/case switch or decision-only
  actions; contextual cards that remain inactive before final validation;
  one offline exact-approval reservation/read-back; targeted Python and
  browser regressions. Verify no unapproved hosted-service network traffic.
* Acceptance: the documented SDK extension points work without private
  patches; success is gated by application validation; card callbacks use
  trusted existing backend actions; no automatic continuation/replay occurs.
  Record actual resolved versions, measured behavior, license/network
  findings and remaining UX work. Stop bounded test servers afterward.
* Excluded: full-interface replacement before this gate passes; production
  hosting, Intelligence, built-in model agents, frontend approval tools,
  A2UI/MCP Apps, Azure authentication/inference/export/spend, published agent
  changes, Python SDK upgrades, historical-run migration/reset/rebind,
  delegation, infrastructure/IAM/account changes, commits and pushes.
* Cost/risk: local package/build/test work only; no model/Azure cost.
  Dependencies and browser lifecycle may expose incompatibility. If blocked,
  preserve the original runtime, report exact evidence and request a revised
  scope instead of adding cloud services or weakening guards.

## S-039 Revision 1 Default CopilotKit UI Replacement

* Status: superseded before execution by revision 2 after explicit user
  correction on 2026-11-04 at 11:26 +01:00. Offline-only/default-case
  presentation is not an acceptable final delivery.
* Objective: activate the verified CopilotKit direction as the single local
  user-facing interface, retiring the bespoke static client rather than
  retaining two permanent UIs.
* Inputs: S-038 [executed evidence](../research/evidence.md#s-038---executed-local-copilotkit-compatibility-evidence),
  D-019, Q-038's UX requirements and unchanged native runtime safeguards.
* Proposed scope after approval: default frontend/static-asset routing and
  build prerequisites in the existing Python launcher; remove the previous
  static HTML/JS/CSS client; include relevant frontend source/lockfile/served
  build identity in candidate provenance without hashing caches/modules as
  application source; finish durable contextual card/decision presentation
  and clear connection/disabled states. Update related tests/documentation.
* UX: chat first, current evidence-backed human cards, separate explicit
  Continue, readable decision receipts/history, secondary diagnostics and
  no automatic inference on startup/reload/switch/decision-only actions.
  Preserve backend exact proposal and eligibility checks. Do not silently
  add a model approval tool or change the managed agent contract.
* Local targets: application source, dependency lock already selected,
  fresh temporary synthetic cases and bounded loopback fixture services.
  No Azure tenant/subscription operation is in scope.
* Included tests/acceptance: build/type-check and targeted Python/JS/wire/
  browser tests; default launch/missing-build behavior; frontend drift blocks
  rather than silently rebinding old cases; one complete offline case;
  persistent contextual actions/receipts across reload; Stop/error behavior;
  no duplicate context, cross-case leakage, automatic model calls or
  unapproved external traffic. Keyboard/focus/mobile accessibility checks
  and screenshots support a subsequent user UX review, not assumed approval.
* Excluded: real Azure authentication/inference/export/spend, agent prompt/
  schema/version changes, hosted CopilotKit services, production hosting,
  Python upgrades, historical-run migration/reset/rebind, IAM/infrastructure,
  automatic decision-and-continue behavior, delegation, commits and pushes.
* Cost/recovery: local build/test work only; preserve existing business/native
  runtime behavior and historical artifacts. Switch only after default-path
  tests pass; no permanent legacy fallback. A blocked new requirement needs
  a revised scope rather than hidden cloud access or weakened controls.

## S-039 Revision 2 Real Foundry Chat as the Single Interface

* Status: completed through Q-041 and
  [A-026](../implementation/log.md#a-026---s-039-real-foundry-chat-replacement);
  authority consumed. User UX acceptance remains a separate judgment.
* Confirmed user requirements: one real CopilotKit chat, no old UI coupling,
  no simulated application responses and no prerequisite case-creation UI.
  Opening the application presents an enabled question composer; the first
  explicit user submission creates internal state and the actual managed
  Foundry conversation and streams the real answer.
* Scope: replace default static routing/launcher with the existing built
  CopilotKit frontend; remove the previous `supply_chain/web` client and its
  serving/fingerprint references; remove preview-specific production UX.
  Wire first-submit initialization without a model call on page mount,
  losing the first question, duplicate requests or invented assistant text.
  Persist actual history/decisions with source/lockfile/build provenance.
  Keep synthetic business data, trusted human actions and native safeguards.
* Runtime behavior: use the existing real managed-agent factory only in the
  application. Missing configuration/build fails with actionable errors,
  not a working-looking simulated or inference-disabled chat.
  Simulated upstream responses remain in automated tests only.
  No new native model/tool loop, frontend approval tool or agent publication.
* Local verification: build/type-check; targeted Python/JS/wire/browser tests
  of first-question submission, persistence, cards, Stop/errors, isolation,
  strict CSP and absence of automatic inference. Passing mocks alone does
  not satisfy final acceptance.
* Proposed live verification: existing project
  `https://ai-aif-demo-01.services.ai.azure.com/api/projects/ai-aif-demo-prg-01`,
  existing configured identity/tenant, deployment `gpt-6.1-sol`, managed
  `supply-chain-resilience-advisor` exact version `3`. Verify binding and
  prerequisites using existing access; no resource/IAM creation.
* Live acceptance: submit one real investigation/comparison question through
  the default UI, with at most five native model requests and ten tools.
  Reconcile real usage, actual managed conversation identity, incremental
  text and validated completion. Stop at the human choice; do not invent
  a preference, approve a proposal or execute a reservation in this check.
* Proposed monitoring: 30,000 aggregate tokens and EUR 2 conservative model
  estimate, subject to Q-041. Usage is observed after responses; these are
  application stop thresholds, not a guaranteed Azure billing cap.
  No automatic inference retries or telemetry export in this verification.
* Excluded: new infrastructure/services, APIM, hosted CopilotKit, deployment,
  IAM/account changes, published prompts/schemas/versions, historical-run
  migration/reset/rebind, reservation approval inferred from this task,
  Azure conversation deletion, delegation, commits and pushes.
* Recovery: preserve old run artifacts read-only; do not rebind drifted
  sessions. Record any started/uncertain real conversation without replay.
  Stop bounded verification services afterward; retain a single documented
  real application launch path, not a permanent old/simulated fallback.

## S-035 Revision 1 Local Testing UI Design

* Status: completed as local/public design on 2026-11-04; Q-035 selected
  `full_human_controlled`. No application implementation is authorized.
* Objective: define one learning-first interface increment for the existing
  managed advisor and Agent Framework runtime, not a new agent application.
* Scope: existing UI research, relevant public documentation, local runtime
  compatibility inspection and canonical design/question/plan tracking.
  Q-035 settles read-only chat versus the human-controlled complete demo.
* Recommendation: local browser UI with chat, visible tool activity,
  evidence, run/trace IDs and explicit human selection/exact-proposal
  approval. Reuse existing guards and persistence; do not move reasoning
  or authorization into frontend workflow code.
* Integration choice: compare the framework development UI and AG-UI
  integration against the actual installed runtime before selecting.
  Do not assume a protocol supplies token streaming or approval semantics.
* Acceptance: record the chosen UI scope, compatible integration approach,
  exclusions and one bounded implementation contract for user approval.
* Excluded: application edits, dependency installation, server startup,
  authenticated Azure access, inference/export/spend, deployment/IAM,
  historical-run transitions, commits/pushes and delegation.
* Cost/recovery: no model or Azure cost for design; preserve current runtime
  and historical artifacts. Implementation and live tests need separate consent.

## S-036 Revision 1 Local Human-Controlled Testing UI

* Status: superseded before approval by revision 2. The user explicitly
  requires AG-UI and real streaming on 2026-11-04 at 09:38 +01:00.
* Objective: a small local browser interface for the actual managed advisor,
  preserving agent-led reasoning, trusted human decisions and validated evidence.
* Proposed approach: FastAPI backend and static HTML/CSS/JavaScript served
  from the same loopback origin. No React build pipeline or AG-UI adapter
  in this first increment. This is a lab simplicity recommendation, not
  a claim that Microsoft mandates a bespoke UI.
* Reason: native DevUI targets generic development/debugging; the application
  additionally owns exact-proposal decisions, evidence validation and durable
  uncertainty stops. The documented AG-UI path streams agent execution,
  while current safety middleware explicitly rejects streaming. Do not bypass
  those controls or bolt a second runtime onto them to obtain a chat screen.
* Scope: add a local UI entry point and static assets under
  `src/supply-chain-resilience`; extract the existing guarded managed chat
  service from CLI ownership where necessary, reuse `agent.py`, conversation,
  session, locks, domain/store and observability. Update only directly related
  requirements, tests, README and canonical tracking.
* Features: new synthetic case, chat, tool-status timeline, current/historical
  evidence, option selection, exact-proposal details and approve/reject controls,
  usage/limits and run/conversation/trace IDs. Show progress separately from
  the final answer; no unvalidated final answer or claimed token streaming.
* Human boundary: choice and exact-proposal approve/reject are explicit backend
  actions, never inferred from chat, browser-supplied state or model text.
  After a human action, a visible separate continue action runs the agent;
  button clicks alone do not automatically incur inference.
* Local boundary: loopback bind, same-origin/Host/Origin checks and explicit
  local action authorization against cross-site requests; no permissive CORS.
  Credentials and target configuration stay server-side. The client cannot
  select arbitrary filesystem paths, endpoints, roles or remote tools.
* Runtime behavior: serialize mutations per case, preserve existing locks,
  exact-version/drift/usage/uncertainty checks and zero automatic retries.
  Own one telemetry provider at server startup and flush on shutdown, not
  per browser message. Do not reuse the CLI's per-process lifecycle unchanged.
  Tracing remains off unless explicitly configured for synthetic data.
* Dependencies: compatible FastAPI/ASGI server pins in an appropriate
  optional UI manifest; install into the application environment only after
  updating the manifest. Do not upgrade the proven framework stack.
* Validation included: offline native-framework/service-boundary tests,
  backend input/origin/decision/concurrency/uncertainty tests, browser checks
  against test-only synthetic service responses, regression tests, documentary
  checks and a local smoke server stopped after validation.
  Simulated browser tests must not be presented as live Foundry inference.
* Acceptance: usable full-case UI with unchanged safeguards and explicit
  backend errors; no secrets in browser responses or tracking; no duplicate
  runtime loop, fake live success or hidden automatic model requests.
* Excluded: authenticated Azure access, real inference/trace export/spending,
  deployment/new infra/IAM/account changes, new agent versions, production
  identity/multi-user hosting, multi-agent orchestration, historical-run
  migration/reset/rebind, commits/pushes and delegation.
* Cost/recovery: local code/dependencies only. No paid validation authorized.
  Preserve old artifacts, use fresh test cases and stop uncertain turns.
  A real UI-to-Foundry walkthrough requires a separate bounded authorization.

## S-036 Revision 2 AG-UI Testing Interface and Native Streaming

* Status: completed on 2026-11-04; Q-037 local authority consumed.
  Acceptance: [A-023](../implementation/log.md#a-023---s-036-ag-ui-and-native-streaming).
  No live inference/export authorization was granted or exercised.
* Requirement: user's explicit AG-UI and streaming choice supersedes the
  revision 1 bespoke non-streaming recommendation. Q-035's complete
  human-controlled case remains the functional scope.
* Objective: a local browser AG-UI client connected to the existing managed
  Foundry advisor through Microsoft Agent Framework's AG-UI integration,
  with actual incremental model output and tool events over SSE.
  Do not simulate streaming by splitting an already completed answer.
* Scope: compatible optional AG-UI/backend/frontend dependencies, local UI
  and integration service, existing runtime/conversation/session/observability
  adaptations, CLI compatibility, focused tests and related documentation.
  Use the official integration where compatible, not an independent model loop.
  Evaluate exact installed APIs and package bounds before installation.
  Stop for a revised contract if the proven framework pins must change.
* Streaming safeguards: account per actual model request, reconcile terminal
  usage/status, assemble complete tool call arguments and validate the whole
  batch before any tool effects. Preserve call-ID validation, sequential
  dispatch, fatal latches, human gates and no model retries/settlement bypass.
* UI semantics: show incremental text as provisional, not validated evidence.
  Validate the completed structured answer before marking the turn successful
  or presenting current/historical evidence as authoritative. The current
  JSON message/evidence output requires an explicit incremental rendering
  strategy; never display JSON fragments as a purported validated answer.
  Do not change published instructions/schema/version under this contract.
* Human boundary: preserve explicit backend option selection and exact-ID
  approve/reject; AG-UI messages, frontend tools, state and forwarded properties
  cannot grant capabilities. Continue inference only through a visible action.
* Failure/lifecycle: cancellation, browser disconnect, incomplete stream or
  missing terminal usage cannot clear uncertainty or trigger replay. Preserve
  durable effects and reload checks. Own shared telemetry at server startup/
  shutdown, keep per-agent content isolation and avoid duplicate trace providers.
* Local boundary: loopback-only, trusted server configuration, same-origin
  and action protection, no permissive CORS, browser credentials or arbitrary
  filesystem/endpoint/role/tool selection. No production/multi-user hosting.
* Validation included: native streaming framework tests with simulated service
  boundary; assert incremental delivery before terminal completion, split tool
  arguments, invalid/forbidden batches, final evidence, usage, cancellation,
  disconnect, approval gates, trace isolation and session reload.
  Browser/AG-UI protocol tests and existing regressions must pass.
  Local test servers are stopped after validation.
* Acceptance: actual AG-UI event exchange and real incremental processing,
  preserved controls and explicit failures. Offline fixtures are labeled
  simulations, not proof of live Foundry streaming.
* Excluded: authenticated Azure access, real inference/export/spend, new
  agent versions, infrastructure/IAM/account changes, deployment, historical
  run migration/reset/rebind, commits/pushes and delegation.
* Cost/recovery: local code/dependencies only; no paid validation. Preserve
  old artifacts and stop uncertain cases. A real streaming Foundry walkthrough
  needs separate bounded authorization after offline acceptance.

## S-034 Revision 1 Shared Observability with Per-Agent Policy

* Status: completed on 2026-11-04; Q-034's synthetic-content and bounded
  live/Insights authority is consumed. All seven expected spans are ingested.
  See [A-022](../implementation/log.md#a-022---s-034-shared-per-agent-observability).
* Authority: user explicitly requests implementation, shared across agents,
  with per-agent logging choices and no unnecessary framework.
* Objective: one shared OTel/Azure Monitor setup and a small explicit policy
  for each agent: disabled, metadata, or explicitly opted-in synthetic content.
* Local scope: shared observability module, advisor factory policy, CLI
  bootstrap/lifecycle and correlation, dependency manifest/application environment,
  offline capture/privacy/flush/error tests, README and tracking.
* Simplicity: no registry, superclass, plugin system, second agent, automatic
  evaluator, telemetry provisioning or extra instrumentation layers.
* Privacy: framework content settings are process-global in the installed
  package. Do not toggle them per agent or let one agent enable payload capture
  for others; keep shared setup safe and enforce explicit per-agent policy.
  Never print connection strings or export credentials, authorization headers,
  real data, entire session state or tracking documents.
* Acceptance: actual in-memory spans demonstrate per-agent isolation, model/
  tool/run/conversation correlation, selected content policy and shutdown flush.
  Existing business/human/evidence/uncertainty behavior remains unchanged.
  Export failure is explicit, never a successful trace-visibility claim.
* Live scope if explicitly chosen in Q-034: same S-032 project/tenant/model/
  managed advisor v3, read linked Insights configuration without exposing it,
  one fresh read-only conversation/run with at most five model requests and
  ten tools, 4,096 output tokens per request, post-response 30,000-token/
  EUR 2 monitoring. Query only the associated trace/run IDs for ingestion
  verification. No proposals, approvals, execution or historical-run resume.
* Cost/risk: local dependencies must satisfy pinned framework constraints;
  Azure export incurs existing Insights ingestion/retention charges and
  the optional validation has model spend. Confirm destination and content
  policy before authenticated access or export.
* Recovery: correct only implementation defects; stop uncertain model calls
  without retry/rebind. Do not replay old writes or broaden cloud permissions.
* Excluded: infrastructure/IAM/account changes, new agent versions, UI,
  run migration/deletion/rebinding, commits/pushes and undeclared cloud access.

## S-033 Revision 1 Trace Visibility Diagnosis

* Status: completed, 2026-11-04; user's diagnostic request only
* Scope: current application source/package inspection and fresh public
  tracing documentation; no authenticated Azure access, code or installs.
* Result: local metadata exists, but no configured OpenTelemetry SDK/provider/
  Azure Monitor exporter in the application. Waiting alone cannot export
  missing spans. Typical 2-5 minute ingestion guidance applies after setup.
* Evidence: [S-033](../research/evidence.md#s-033---why-live-conversations-are-not-visible-as-foundry-traces).
* Proposed next activity: a bounded observability increment before UI work,
  with declared exporter destination/content policy, compatible dependencies,
  CLI flush and one separately approved new trace-validation case.
  No implementation, telemetry export or live test is authorized here.

## S-032 Revision 1 Fresh Live Framework Validation

* Status: completed on 2026-11-04; Q-031 authority consumed.
  Q-032 selected STANDARD; Q-033 separately approved the exact proposal.
  [A-021](../implementation/log.md#a-021---s-032-live-framework-validation)
  records successful real invocation, one reservation and verified final
  current/historical evidence; nine requests/twelve tools/37,168 tokens.
* Objective: verify the actual Agent Framework path against the unchanged
  managed advisor v3, not merely offline service simulations.
* Target: project
  `https://ai-aif-demo-01.services.ai.azure.com/api/projects/ai-aif-demo-prg-01`,
  tenant `db60e921-9c3c-4fd4-98d1-4445db7ab425`, deployment `gpt-6.1-sol`,
  agent `supply-chain-resilience-advisor`, exact version `3`.
* Scope: tenant-bound authenticated checks, exact published-definition
  verification, one new framework conversation and new local synthetic run
  under `artifacts/local/supply-chain-s032`; CLI/model interaction and
  inspection of metadata, usage, evidence and durable SQLite outcome.
* Limits: 20 cumulative model requests, 20 tools, 4,096 output tokens per
  request; aggregate 100,000-token/EUR 10 post-response monitoring.
  Conservative estimate uses EUR 20 per million tokens, not actual billing.
* Human gates: pause for STANDARD/EXPRESS preference; independently pause
  for approval/rejection of the exact resulting proposal. Operational test
  consent grants neither choice nor execution approval.
* Acceptance: actual managed-version response, framework-chosen tool use,
  exact grounded facts, persisted continuation/usage, human-gated one-time
  synthetic reservation and mandatory current post-write read-back with
  historical evidence correctly separated. No shipping or real data.
* Recovery: stop on unexpected identity/definition drift, failed/uncertain
  request or tool/evidence failure. Inspect durable effects locally; no
  blind retry, session rebind/reset or automatic model/thread repair.
  Report defects before any source/dependency change.
* Excluded: publication/new agent versions, provisioning/IAM, login-account
  changes, UI/AG-UI, external telemetry, installs, old-run migration/deletion/
  resume,   source changes, commits and pushes. No operational work preceded consent.

### Proposed Next Activity After S-032

Design a bounded local testing interface for the now live-verified framework
agent: chat, observable tool activity, explicit option/approval controls and
current/historical evidence. Select direct integration versus AG-UI based
on the agreed learning goals. This is a proposal only, not UI implementation,
deployment, package installation or another live conversation.

## S-031 Revision 1 Explicit Agent Factory

* Status: completed locally, 2026-11-04; Q-030 authority consumed.
  See [A-020](../implementation/log.md#a-020---s-031-explicit-agent-factory)
  for offline execution and editor-validation evidence.
* Authority: user's 08:47 +01:00 acceptance of the single proposed factory/
  conversation separation, not a new cloud operation
* Objective: expose managed-agent composition in `agent.py` through a
  `create_agent` function returning the actual `FoundryAgent`.
* Scope: extract construction and bindings from the conversation class;
  update CLI/test callers, source-layout documentation and tracking.
  Keep conversation state, human events, guards and evidence in the
  conversation module. Do not add a custom agent wrapper or compatibility alias.
* Acceptance: actual framework offline tests, schemas/version/options,
  exact human approval, cumulative limits, evidence and persistence remain
  valid; source hashing includes the new module. Documentary checks pass.
* Risk/recovery: imports/callback binding can break during extraction;
  correct only this refactor and verify with existing tests. Preserve
  drift checks and all historical artifacts rather than rebinding old runs.
* Excluded: dependencies, Azure/authentication/inference/publication,
  UI, runtime behavior changes, session migration, commits and pushes.

## S-030 Revision 1 Direct Agent Framework Migration

* Status: completed locally; Q-029 authority consumed. Actual framework
  execution, native sessions and 105 offline application tests verified in
  [A-019](../implementation/log.md#a-019---s-030-direct-agent-framework-migration).
  Editor type-check could not complete because of environment/transport
  issues; this limitation is recorded, not reported as a clean check.
* Objective: one Agent Framework runtime connected to the existing managed
  prompt-agent identity, not a local replacement agent or parallel legacy loop.
* Git scope: create local `feat/agent-framework` from the currently clean
  `main`; no stash, history rewrite, commit or push.
* Local source scope: application dependency manifest/environment, shared
  runtime replacement, advisor tool bindings/capability/evidence adapter,
  durable framework sessions, CLI, regression suites and directly related docs.
* Dependency scope: published Foundry adapter 1.16.0 requires Projects below
  2.8.0; use compatible pinned Projects 2.7.0/core 1.24.0/OpenAI adapter
  1.18.0 generation, retaining compatible identity/OpenAI pins. Install only
  after manifest change and verify the resolved environment with `pip check`.
* Acceptance: actual framework execution/function invocation exercised with
  offline service responses; managed-agent binding and exact tool schemas;
  trusted human selection/approval, single durable reservation, mandatory
  post-write result, current/historical evidence, cumulative request/tool/
  usage limits, metadata-only correlation, persistence/drift and uncertainty
  stops. SDK-free business suite and documentary checks must remain valid.
* Retirement: remove custom generic model/function loop and incompatible
  tests/API surfaces. Do not retain a selectable fallback or migrate/alter
  actual old runs. Preserve source-independent domain/store/data safeguards.
* Cost/risk: no model spend; SDK/API and framework middleware differences
  require local validation. Existing cloud compatibility is not claimed
  without a later separately authorized live case.
* Recovery: correct only migration-related defects; if a verified framework
  limitation blocks required safety, record it and stop rather than bypassing
  a guard or reinstating a silent fallback. Retain the local branch for review.
* Excluded: UI/AG-UI implementation, authenticated Azure access, inference,
  publication, provisioning/IAM, external telemetry, run-data deletion/reset/
  rebind, installation outside the application environment, commits/pushes.

### Proposed Next Activity After S-030

Verify one fresh bounded live conversation through the framework using the
unchanged managed v3 definition, a new native-format local directory and
separate operational consent. Define request/tool/token/spend limits before
authenticated access; human option selection and exact-proposal approval
remain independent. Do not resume or migrate S-026. This activity has not
started and is not authorized by local S-030 completion.

## Earlier Milestone Planning History

Current planning qualification: the S-022 fixed-flow implementation is a
verified baseline, not fulfillment of the agent-led experience requested
on 2026-11-03. See the proposed S-024 increment below and
[S-023 findings](../research/evidence.md#s-023---agent-led-design-and-prompt-lifecycle-review).
No earlier consumed approval is extended to that increment.

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

## S-026 Revision 1 Proposed Live Conversational Validation

* Status: stopped at nine requests and superseded by revision 2's explicit
  allowance extension. Q-024 authorized the original declared cloud case.
* Objective: publish the locally tested agent-led definition and verify one
  real synthetic conversation with the application-side tool dispatcher.
* Target: existing project
  `https://ai-aif-demo-01.services.ai.azure.com/api/projects/ai-aif-demo-prg-01`,
  tenant `db60e921-9c3c-4fd4-98d1-4445db7ab425`,
  deployment `gpt-6.1-sol`, agent `supply-chain-resilience-advisor`.
* Authorized actions if confirmed: verify explicit tenant/current deployment
  and existing latest definition; stop on unexpected drift. Create at most
  one candidate agent version, read it back and verify the full definition.
  The new version becomes latest for the named endpoint; retain v1/v2.
  Create one conversation and one fresh local synthetic candidate session
  under ignored `artifacts/local/supply-chain-s026`. No existing run overwrite.
* Test: user-level supplier-delay message; let the agent choose fact/tool
  order, explain alternatives and request preference. Ask the user for the
  actual one-case choice, record it through the human event, then continue
  conversationally to an exact proposal. Ask separately for exact-proposal
  approval/rejection. Only if approved may the same conversation request
  the synthetic reservation and read its durable result.
* Global limits: 10 model requests, 20 function calls, 4,096 requested output
  tokens per response; 100,000 aggregate tokens and EUR 10 monitored after
  actual usage, not hard pre-call cutoffs. No SDK automatic retries.
* Pricing: retain the documented conservative EUR 5/20 per-million estimate,
  not actual billing; no new pre-count requirement. Stop on missing usage.
* Acceptance: actual definition/version verified; genuine function calls and
  exact authoritative evidence; choice/approval outside model authority;
  no reservation before approval; inspect local trace and durable SQLite
  result from a separate process. Report actual tools/order, requests/tokens,
  estimate, outcome and limitations, not a general quality certification.
* Local scope: candidate CLI/runtime, state/trace and canonical tracking;
  narrowly related compatibility corrections with offline regression checks
  only if a concrete failure requires them. Never retry an uncertain call
  or blindly repeat a write to fix a validation failure.
* Excluded: new infrastructure or model deployments, IAM, harness/hosted
  migration, other agents, API/MCP, Azure telemetry export, paid evaluation
  or optimizer jobs, installations, deletion/cleanup, commits/pushes.
* Recovery: preserve agent versions/conversation/local evidence on failure;
  reconcile durable state, record blocker and stop. No automatic rollback,
  new version, new session or extra test beyond the above allowance.
* Consent boundary: agreeing to this technical test is not a permanent
  planner preference or approval of a not-yet-created business proposal.

## S-026 Revision 2 Proposed Request-Allowance Extension

* Status: blocked at final-answer acceptance; live attempt ended and
  authority consumed. Q-026 authorized this revision and Q-027 independently
  approved the exact proposal. Revision 1 history is retained.
* Observed reason: actual agent refreshed snapshot, policy and comparison
  before creating the STANDARD proposal. Cumulative usage is 9 requests,
  7 tools, 22,345 tokens, estimate EUR 0.4469; fully reconciled, no write.
* Change: allow 20 cumulative model requests for this same case, retaining
  20 tools, 100,000-token/EUR 10 post-response thresholds, output limit and
  no automatic retries. Never reset the 9 requests or create another session.
* Local correction: separate the advisor's maximum request policy from the
  historical ten-request baseline, persist an explicit per-session allowance
  defaulting to ten, and regression-test both limits and restoration.
  No new cloud definition/version or prompt change.
* Explicit source transition if approved: audit that the current turn is
  complete/reconciled, proposal remains unapproved and no request exists;
  after local tests, rebind only this session's source-content hash and
  allowance. Record old/new hashes in the log. Do not clear uncertainty,
  alter evidence/call IDs/usage, or silently migrate any other run.
* Existing source hash: `d87f70f707ec149ea0909ce73c18874c9e2dc14d35af6c2e2e60d23809667e9b`
* Business action remains independent: Q-027 asks exact approval/rejection of
  proposal `bf144275-ec8f-4ad3-bdd2-b63b9ff4616f`.
* All unchanged target, exclusions, evidence and recovery requirements of
  revision 1 apply. If the extension is declined, stop before a model
  execution that cannot complete its required read-back within the allowance.
* Actual outcome: reservation and post-write read-back verified, but final
  evidence included authentic pre-write facts invalidated by the application,
  triggering `ungrounded_answer`. Exactly one request, source 80/70/10,
  destination 20. Fourteen requests, eleven tools, 48,338 tokens. Preserve
  failed-turn stop; no retry or automatic source/session transition.

## S-027 Revision 1 Proposed Local Evidence-Handoff Correction

* Status: local implementation authorized by the user's 2026-11-03
  17:02 +01:00 request; Q-028 clarifies historical/current output semantics.
  No cloud or stopped-session recovery authority.
* Objective: correct the S-026 historical/current evidence mismatch without
  disguising old stock as current or relying on model-copied current facts.
* Local scope: advisor response contract/adapter, directly related session
  handling if required, regression tests and documentation.
* Acceptance: reproduce the observed historical snapshot + policy + valid
  durable-result case; distinguish historical explanation from current
  authoritative outcome, reject invented/altered evidence, and preserve
  approval, single-execution and mandatory post-write read-back guards.
  Existing baseline behavior and all relevant tests must remain intact.
* Risk/recovery: a contract change may require a new local definition hash
  and subsequent separately authorized publication. Preserve old versions
  and stopped S-026 state; do not rebind or resume that executed session.
* Excluded: authenticated Azure access, publication, inference, new runs,
  clearing S-026 stop flags, stock changes, dependencies, IAM, commit/push.
* A later bounded live validation would require its own explicit contract;
  this proposal does not authorize it.

### Revision 2 Accepted Local Scope

Status: completed locally; authorization consumed. All 95 combined tests,
34 independent SDK-free tests and ten documentary/link checks passed.
The originally failing live-shaped case now separates authentic historical
facts from the mandatory current read-back. The old drivers are retired,
useful safety coverage targets the active path, and the published definition
is unchanged. No cloud run, data deletion or stopped-session transition.
See [A-018](../implementation/log.md#a-018---s-027-revision-2-evidence-separation-and-legacy-retirement).

Q-028 explicitly selects separate historical/current evidence and adds
deletion of obsolete implementation code. Preserve revision 1 above as the
original correction proposal; its cloud exclusions and acceptance remain.

* Implement application-owned separation, retaining unchanged tool objects
  and mandatory current post-write read-back. Preserve the two-key model
  response contract and published prompt/schema/definition.
* Persist history with existing session decisions; never rewrite or resume
  the stopped S-026 run. Add regression tests for the observed failure,
  changed/unknown facts, refreshed state, persistence and mandatory read-back.
* Trace legacy callers before deleting retired drivers and their direct
  tests. Retain active business/manual tools, shared runtime, useful runtime
  regression checks and historical prompt assets; repair current docs and
  mark historical source references as retired without erasing decisions.
* No run-data deletion, cloud access, publication, inference, dependency
  installation, IAM, commit or push. Validate locally with the relevant
  Python suites and documentary/link checks.

## S-025 Revision 1 Proposed Multi-Agent-Ready Source Layout

* Status: completed; Q-023 explicitly approved with agent-specific tool ownership.
  [A-016](../implementation/log.md#a-016---s-025-revision-1-multi-agent-ready-source-layout)
  records 99 passing combined tests, independent SDK-free tests and
  documentary checks. Approval consumed; no cloud work authorized.
* Objective: prepare the solution source layout for multiple distinct agents,
  while implementing and running only the existing resilience advisor.
* Scope: move advisor definition, prompt assets, specialized conversation
  controls and tool schemas/dispatcher under
  `src/supply-chain-resilience/supply_chain/agents/resilience_advisor`;
  place its evaluation dataset under `evals/resilience_advisor`. Update
  package initializers, imports, asset paths, source hashing, related tests,
  README and affected tracking links.
* Shared boundaries: leave reusable Responses runtime, business rules/store
  and solution data outside the per-agent package. The runtime depends only
  on a dispatcher contract, not this advisor's tools. A future actually shared
  tool can be extracted without duplicating domain/data operations.
  The application session/CLI can still know the sole advisor explicitly.
* Excluded: new agents, orchestrator, handoff, registry/plugin framework,
  new dependencies, cloud access/publication/inference, IAM, resource changes,
  telemetry export, existing-run migration/reset/deletion and commits/pushes.
* Acceptance: unchanged instruction/definition hashes for historical v1/v2
  and the current candidate; nested agent source participates in drift checks;
  all 96 current tests, independent SDK-free tests and documentary/link checks
  pass. Do not claim multi-agent behavior from source layout alone.
* Cost/risk: no model spend; risks are broken imports/assets or incomplete
  provenance after moves. Verify these locally and retain existing run artifacts.
* Recovery: no cloud state changes; correct imports/assets locally, never
  silently migrate old candidate fingerprints to bypass drift checks.

## S-024 Revision 1 Proposed Local Agent-Led Increment

* Status: completed locally; user's 2026-11-03 16:22 +01:00 "procedi"
  authorized this single increment, not cloud publication or execution.
  Actual files, 96 passing tests and limits are in
  [A-015](../implementation/log.md#a-015---s-024-revision-1-agent-led-local-candidate);
  implementation consent is consumed.
* Objective: make the single managed agent the conversation/case coordinator,
  expose code responsibilities and establish a minimal prompt-as-code baseline.
* Expected result: a locally tested candidate definition/runtime and synthetic
  evaluation cases; the existing cloud v2 remains unchanged.
* Scope: `src/supply-chain-resilience` agent-definition/instruction assets,
  generic runtime, CLI, tool/approval boundary, synthetic scenario data,
  tests/evaluation cases and README; directly related canonical project
  tracking. Reuse existing domain/store functions and dependencies.
* Intended organization: a small agent module, explicit text instructions,
  a generic runtime, existing tools/store/domain modules, scenario fixture
  and evaluation data. Exact filenames follow the implementation's simplest
  coherent layout; do not introduce a framework or one directory per class.
* Behavior: user messages drive tool use; only pending human decisions block
  continuation. Retain trusted exact selection/approval, stale checks,
  reservation idempotency, cumulative budgets and explicit-error behavior.
  Do not hardcode a tool sequence or treat model claims as human approval.
* Prompt provenance: stable source file, instruction/schema hashes and
  candidate configuration references; no fake cloud version or clean commit.
* Excluded: authenticated Azure access, new agent versions/conversations,
  inference, cloud evaluations/optimizer, harness/hosted migration, APIs/MCP,
  telemetry export, IAM, resource changes, dependency installation, Git
  commits/pushes and deletion/reset of existing run artifacts.
* Acceptance: existing applicable business/SDK tests pass; preserve the
  historical fixed-flow contract separately where necessary. Add tests for
  generic continuation, more than one valid tool order, missing-preference
  and approval pause/resume, no unauthorized effects, exact result grounding,
  fixture/provenance loading and prompt/schema drift. Add a small versioned
  scenario/rubric set; label offline model fixtures as simulations, not live
  model-quality evidence. Run repository documentary/link checks.
* Cost/risk: no model spend; risks are behavioral regression and accidental
  endpoint-definition drift. Do not publish, and refuse mismatched live
  definitions. Retain v1/v2 artifacts and the S-022 run.
* Recovery: candidate remains local/unpublished; no cloud rollback needed.
  Preserve old scenario and business invariants and distinguish incompatible
  session formats explicitly rather than silently migrating completed runs.

This was one cohesive local increment, not a renewed discovery questionnaire.
Live publication and model-quality validation still require a later bounded
contract; no such execution is authorized by this completed step.

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
