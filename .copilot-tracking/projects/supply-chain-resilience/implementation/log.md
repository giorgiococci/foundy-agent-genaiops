---
title: "Implementation of supply-chain-resilience"
description: "Authorized local business-tool implementation, module boundaries and verified test evidence."
ms.date: "2026-11-05"
---

## Activity Log

## A-033 - S-048 Existing Demo Reader Assignment

* Date: 2026-11-05
* Status: completed under Q-051/Q-052; authority consumed.
* Authority: Q-051 confirms exact synthetic UPN aliases in the existing
  demo domain and authorizes S-048 revision 1 checks and memberships.
* Matrix: UserDemo01 to SCR Planning Readers (10) only; UserDemo02 to
  SCR Procurement Readers (11) only.
* Exclusions: account/credential/license/role/consent/policy changes, folder
  ACL changes, deletion, sign-in, runtime/Foundry work and Git publication.
* S-047 credential material remains untouched and is not used for these users.
* Preflight: exact approved Graph UPNs resolve to enabled Member accounts;
  each non-paginated transitive directory-role read returns zero roles.
* Browser: previous page no longer exists. Opening the exact approved site
  redirects to the expected tenant sign-in. No SharePoint write occurred.
* Limitation: initial assignedLicenseSkuIds projection returns a null element,
  so it is not used as proof of license availability or count.
* Resumed browser preflight verifies the same approved owner and web ID;
  groups 10/11/4/5 are empty, group 3 contains only the existing owner.
  Neither demo user is a site principal. Both folder ACLs are unique and
  exactly match A-031's owner/Read matrix. No SharePoint write yet.
* Actual writes after successful preflight: two ensureuser POSTs create
  site-local principals 12 (UserDemo01) and 13 (UserDemo02); neither is
  IsSiteAdmin. These are not new Entra users.
* Exactly two group-user POSTs return HTTP 201: principal 12 to group 10,
  principal 13 to group 11. No retries, extra grants or other mutations.
* Verification: each user's site groups contain exactly its agreed reader
  group, each reader group has exactly its intended member, and both
  site-admin flags remain false. Owners retain only existing principal 6;
  Members/Visitors remain empty.
* Folder read-back exactly matches A-031: General unique ACL principal IDs
  3/6 Full Control and 10/11 Read; Restricted Procurement unique ACL IDs
  3/6 Full Control and 11 Read. No folder permission mutation occurred.
* Final exact-user Graph read-back confirms enabled Member state and zero
  assigned licenses for each user. The earlier null projection was not
  interpreted as a license; a direct collection-count check resolves it.
* Source refresh: LE09 SharePoint REST permission documentation retrieved
  2026-11-05, updated 2026-10-28; REST remains supported despite retirement
  of SharePoint Add-ins. No retired add-in authentication was adopted.
* Limitations: active-role checks do not prove PIM eligibility; no reader
  sign-in, license assignment, document retrieval or Foundry OBO test.
  All S-047 encrypted credentials remain untouched and unused.

## A-032 - S-047 Entra Demo Users and Reader Membership

* Date: 2026-11-04
* Authority: Q-050 approve_proposed_aliases, enabled_dpapi_force_change,
  create_users_assign_groups_no_licenses; S-047 revision 1.
* Status: blocked; authority paused pending permission resolution and renewed
  execution confirmation.
* Target: existing demo tenant and approved SharePoint site; proposed
  aliases scr-planner-demo and scr-procurement-demo.
* Scope: at most two new enabled standard users, distinct encrypted local
  temporary credentials, first-sign-in change, planner in site group 10
  only and procurement in site group 11 only; targeted verification.
* Excluded: licenses/purchases, admin/Foundry roles, consent, elevation,
  MFA/security-policy changes, existing-account resets, deletion, user
  sign-in, runtime integration, inference and Git publication.
* Verified preflight: current CLI operator and tenant match the approved
  target; intended domain is in organization.verifiedDomains; both exact
  proposed user paths return 404. Same approved SharePoint owner session
  confirms the two expected reader groups are empty.
* Secure preparation: two distinct cryptographically generated temporary
  passwords, each exported as DPAPI-protected PSCredential CLIXML outside
  the repo. Directory inheritance disabled; only current Windows SID has
  filesystem access. Import/decryption was checked without printing values.
  No plaintext credential file, password process argument, environment
  variable, transcript or token output was produced.
* Actual request: exactly one Graph POST /users for scr-planner-demo,
  enabled Member with forceChangePasswordNextSignIn=true. Response is
  HTTP 403, error code Authorization_RequestDenied. No create retry;
  scr-procurement-demo create was not attempted.
* Post-failure verification: both exact user paths still return 404.
  Groups 10/11 each have zero members. No users, licenses, roles or
  SharePoint memberships were created/assigned.
* Role diagnosis: GET /me/transitiveMemberOf/microsoft.graph.directoryRole
  succeeds without pagination and returns Global Reader only. No active
  write-capable user administrator role was observed; eligibility via PIM
  was not queried, activated or inferred.
* Corrected preflight-only issues: organization.verifiedDomains contains
  verifiedDomain objects, which have no isVerified property. Checked the
  official schema and corrected the membership test before any POST.
  Initial browser CDP connection timed out; a read reconnected normally,
  and the owner/group preflight then succeeded.
* Preserved partial local files: scr-planner-demo.credential.clixml and
  scr-procurement-demo.credential.clixml under LOCALAPPDATA/
  FoundryMultiAgentLab/credentials/supply-chain-resilience-s047.
  These passwords currently authenticate no created account. Do not register
  or upload encrypted credential files, print passwords, or overwrite them
  during an unapproved retry.
* Next: user resolves the least-privileged directory role prerequisite
  through the normal admin/PIM process. A role grant/activation or different
  operator is outside this authority. Renew create/membership confirmation
  after the pause. Sources: [LE10](../../../../docs/research/sources.md#le10---entra-test-user-provisioning).

## A-031 - S-046 SharePoint Knowledge Site Provisioning

* Date: 2026-11-04
* Authority: Q-049 authorize_site_groups_upload_acl; S-046 revision 1.
* Status: completed; Q-049 authority consumed.
* Target:
  <https://mngenvmcap946525.sharepoint.com/sites/supply-chain-resilience-lab>.
* Scope: at most one non-group-associated site, two empty site-local reader
  groups, two folder ACLs, four approved DOCX uploads and read-back.
* User explicitly defers reader assignments and requests no document edits.
  No Entra objects, consent, elevation, other-site ACLs, deletion, application
  changes, model inference, publication or Git operations authorized.
* Actual creation: one SPSiteManager create, HTTP 200, SiteStatus=2.
  Non-group-associated team site, English locale; current verified demo
  caller is owner. No duplicate creation or Microsoft 365 group/Team.
* Resource IDs: site collection 4537546e-3503-4516-ae2f-ac7a2b080681;
  web 8855d547-8567-411a-8d37-696f7443b1ed; default Documents library
  3ce69324-7957-4d71-9cba-79483257c95e. These are configuration identifiers,
  not credentials or test-user identities.
* Created empty site-local groups: SCR Planning Readers, ID 10;
  SCR Procurement Readers, ID 11. Both prohibit member-edited membership,
  join requests and automatic acceptance.
* Actual ACLs: General uniquely grants Read to groups 10/11. Restricted
  Procurement uniquely grants Read to group 11 only. Associated owners group
  and authenticated site owner retain Full Control. Exact principal counts
  and role IDs were checked, not inferred from a successful POST.
* Uploads: two approved DOCX files in each folder via normal browser file
  input. Final read-back proves all four inherit their respective folder
  permissions and no unexpected folder grants were added. PDFs/sources
  are local only. No external/anonymous/tenant-wide grant was created.
* Content read-back: each authenticated browser GET of the remote DOCX
  package was checked. word/document.xml SHA256 exactly equals the local
  approved body, covering all text and tables. Package sizes/hashes changed
  after SharePoint processing, so binary package identity is not claimed.
* Recorded remote evidence:

```json
[
  {
    "source_id": "SCR-K001",
    "name": "Disruption Response Guide.docx",
    "folder": "General",
    "remote_bytes": 54658,
    "remote_package_sha256": "c0f51dc53a5f84afc46b57168eb2b905ecba185d069cbd4f4eb241ed3b295826",
    "word_body_sha256": "f3cbbd01ef9d0824dfc1c84ac05624b2ff1012a5c8b44dc8512c9ad32f2dafba"
  },
  {
    "source_id": "SCR-K002",
    "name": "Transfer Evaluation Guide.docx",
    "folder": "General",
    "remote_bytes": 54613,
    "remote_package_sha256": "d0ab201fab44ccd9501f0d10a770d39f276d4c6bf1d611a409e6062349d4fc5b",
    "word_body_sha256": "83aba1df3fc2f8a16bb9b5ceffba894e9e8347354e8db8c500f49436f75d7d49"
  },
  {
    "source_id": "SCR-K003",
    "name": "Supplier Recovery Conditions.docx",
    "folder": "Restricted Procurement",
    "remote_bytes": 54725,
    "remote_package_sha256": "1a8da4e31321d73fd9ffd2a980fc0a5d1318531ebb65ab872464bfaa43f7ede1",
    "word_body_sha256": "6842f9e1e7865181e59770a508f5720d38afc36624535637c2a688ab33b02419"
  },
  {
    "source_id": "SCR-K004",
    "name": "Commercial Escalation Guide.docx",
    "folder": "Restricted Procurement",
    "remote_bytes": 54932,
    "remote_package_sha256": "a5cc1dbf9deecbefb316217d267ea14045fc4ecdb92cde9180a8017e10d5fc36",
    "word_body_sha256": "f9bcd5fee6b730a059cfd5cb7162e226411b146abe2cd13b382a8f95cccecfd3"
  }
]
```

* Resolved verification issues: compact modern UI used an unlabeled upload
  button; actual snapshot reference selected it. CLI Graph binary read-back
  returned Forbidden; no new consent or different identity was used.
  Browser-native download-event capture timed out. Same-origin browser GET
  succeeded with the existing owner session; bounded ZIP decompression and
  Web Crypto verified the approved Word-body hashes without exporting tokens.
* Cleanup: removed only the empty named local readback scratch directory.
  Existing local source/DOCX/PDF deliverables and created site are retained.
* Limitations: no group users assigned, no actual non-admin allow/deny test,
  no indexing-readiness/citation measurement and no Foundry OBO integration.
  Owner access to both folders is expected, not evidence of failed trimming.
* Sources: [LE08-LE09](../../../../docs/research/sources.md#le08---sharepoint-site-provisioning).

## A-030 - S-045 Synthetic SharePoint Corpus and Preflight

* Date: 2026-11-04
* Authority: Q-047 drafts_and_targeted_readonly_preflight; Q-048
  approve_english_outline and browser sign-in confirmation.
* Status: completed; S-045 authority consumed.
* Deliverables: four Word documents and four PDFs, with matching Markdown
  build sources, under session files/sharepoint-knowledge. General contains
  Disruption Response Guide and Transfer Evaluation Guide. Restricted
  Procurement contains Supplier Recovery Conditions and Commercial
  Escalation Guide. These are local organizational labels, not local ACLs.
* All content is synthetic, English, version 0.1, dated 04 November 2026,
  labeled Synthetic demo draft. No actual commercial/customer data.
  Current tools remain authoritative for live facts and business actions.
* Verification: all four strict Word builds pass; PDFs exported through
  Word; all eight final pages visually reviewed; exactly two pages and one
  criteria table per document. DOCX lengths total 213,016 bytes.
  Source IDs/status labels present; tenant/account strings absent from
  visible content; restricted example references absent from General files.
  This content-separation check is not a permissions or retrieval test.
* Resolved: first exports had mostly empty third pages. Shortened prose
  without changing the approved outline; final page budgets pass.
* Preflight: CLI tenant matches requested demo tenant; Graph root discovery
  succeeds. SharePoint REST CLI authentication fails. After user signs in,
  browser GET confirms the expected account and reads root rights.
  IsSiteAdmin=false only describes this root site, not tenant eligibility.
* Proposed site status GET initially returned XML; explicit OData-Version
  header produced JSON with SiteStatus=0, Not Found. No create was attempted.
* No SharePoint/Entra write, upload, new consent, package installation,
  account change, runtime change, publication, inference or Git publication.
* Next: S-046/Q-049 exact site/group/folder/upload contract; no inherited
  operational authority. Real reader membership and OBO tests remain pending.

## A-029 - S-043 Readable Data-Driven Explanations

* Date: 2026-11-04 at 14:19 +01:00
* Authority: Q-045 `local_and_one_publication_no_inference`.
* Status: completed; Q-045 authority consumed.
* Scope: S-043 revision 1; generic explanation prompt, authoritative
  calendar/currency/labels, native human-card rendering, offline regression
  checks, one existing-advisor version publication/read-back, local `.env`.
* No model inference, approval/reservation, infrastructure/IAM, account
  changes, user-server termination, delegation or Git publication.
* Implemented: scenario v2 has an explicit fixed calendar reference,
  currency and arbitrary ID-to-label map; validated planning context is
  persisted per snapshot and copied into exact proposals. All relevant
  business tools expose context, and order/receipt/option/proposal dates
  are computed using the declared consecutive-calendar-day convention.
  Approval/digest/current-facts guards cover context as well as amounts.
* Prompt: generic writing guidance only, no fixture IDs, dates, currency or
  canned business answer. Missing context is acknowledged, not invented.
  Human cards reuse the native Markdown renderer, supplied dates/currency/
  labels and plain-language margins. Removed fixed "boards", "fictional
  units, not euros" and day-only rendering where authoritative context exists.
* Checks: 164 Python tests, including 11 new context/alternate-data/frozen
  approval tests; 16 frontend tests, including alternate USD/leap-day labels;
  three actual offline CopilotKit core/Python SSE integrations; build and
  TypeScript checks pass. No dependency changes were needed.
* Browser fixture: Markdown emphasis and two real list items render in the
  human question. Choice cards show correct November dates, EUR amounts and
  descriptive names; EXPRESS click automatically resumes to the exact
  proposal with the same context. Pending-approval reload adds zero model
  requests and 390px has no horizontal overflow. No real Foundry model run.
* Resolved validation issues: an overlapping build and asset-fingerprinting
  test run caused a Windows EPERM/missing-build failure. Rebuilt separately,
  then reran against stable assets. Two assertions still expected the old
  fixture sentence; updated them to the new shared Markdown fixture text.
  Final suites pass. Browser's Markdown emphasis is a Streamdown span, not
  a strong tag; verified its actual DOM and list items.
* Pylance: changed runtime files have no errors; store retains a pre-existing
  contextmanager Iterator-return deprecation hint. Syntax checks pass.
* Publication preflight: existing CLI tenant/subscription match Q-045,
  v4's complete definition hash matches S-041, model and eight tool schemas
  are unchanged. Current official AgentsOperations create_version reference
  and AI application best practices were consulted.
* Published exactly one version: `5`; complete read-back equals local
  definition, SHA-256
  `6cd734d3e53a0765ae7d5b437eec0381d1f2debe353189c8b313deb90a2bc752`.
  Minimal evidence: `artifacts/local/s043-publication.json`.
  Model requests: zero. Existing v4/earlier versions are unchanged.
* Activation: updated local ignored `.env`, shared `.env.example` and
  README to v5. Restart the user-owned server and choose New chat; no
  historical session rebinding or migration system was introduced.
* Cleanup: stopped only the owned `s043-offline` fixture and removed its
  inspected exact `artifacts/local/s043-offline-ui` directory. Existing real
  cases, publication proof and user-owned servers remain untouched.
* Limitation: actual v5 model phrasing has not been evaluated; publication
  read-back and deterministic/offline compatibility do not guarantee prose
  quality. User review remains the next step, not additional paid work.
* Final gates: all 10 customization/Markdown/link checks and `git diff
  --check` pass. The default launcher loads local `.env` v5 and constructs
  the real app successfully with the server runner mocked; no conversation
  or inference is created. Existing LF-to-CRLF notices remain informational.

## A-028 - S-041 Native Human Handoff Migration

* Date: 2026-11-04 at 12:20 +01:00
* Authority: Q-044 `approve_native_migration_publish_live_express`.
* Status: completed; Q-044 operational authority consumed.
* Scope/limits: S-041 revision 1 execution contract; one managed version,
  one fresh real conversation, 10 requests/20 tools/40,000 tokens/EUR 2
  estimated monitoring. EXPRESS preference only; no proposal approval.
* Preserve existing dirty worktree, published v3 and historical conversations.
* Local gates: 114 focused Python tests and 14 frontend tests pass.
  Build/type-check passes; the three actual JS/Python wire tests pass again
  against the final backend. Core automatically handles two genuine human
  results; the wire roles are user/tool/tool, never invented user text.
* Browser: fresh test page verifies Send/Enter, native choice, one-click
  continuation, exact checkbox approval, one reservation/read-back and
  reload of pending approval with unchanged model usage. Waited for the
  validated terminal, not merely provisional success text.
* Guard coverage includes whole-batch checks, durable native identity,
  stale/cross-case/forged/duplicate result refusal, incomplete human-receipt
  persistence, uncertainty and no automatic reload inference.
* Cloud prerequisite: existing CLI tenant/subscription matches Q-044;
  SDK read confirms advisor v3 uses the existing `gpt-6.1-sol` and six tools.
  AI application best practices consulted; no tenant/account/IAM change.
* Implementation: two request-only declaration tools, updated managed
  prompt/schema, typed durable human request/receipt state, native tool-result
  input, same server-owned AgentSession, single-use phase validation,
  checked pause versus final outcome and core-driven frontend handlers.
  CLI decisions use exact native IDs; `resume` sends a stored tool result.
  The launcher requires an exact version instead of assuming historical v3.
* Compatibility details: the adapter drops orphan results, so rebuild its
  input from the actual stored assistant call plus checked receipt; never
  fabricate a call. Core inserts the human result beside its call and can
  leave later assistant narration, so project the latest genuine user/human
  result rather than blindly the last message. Preserve the transport
  failure latch even when the SDK/core catches callback errors.
* Publication: exactly one new version, `4`, returned and read-back verified
  against the complete candidate definition; SHA-256
  `81043bf9ea20b5e3d69909ce90ce160c95936c175d3f591d136b85bc5ee1aa69`.
  Existing v3 remains unchanged. No new resource, deployment or IAM change.
* Real browser case: `0cbdedf0-d8b8-4d1f-9da3-b6665ad81b9b`, managed
  conversation `conv_07d7a6ec7b59c5ff00HtPrP4ZVS4zLGhCAnOIIh6fRxLlm2x3v`.
  One actual Italian user question, one authorized EXPRESS response as a
  native tool result, then an Italian exact-proposal approval request.
  Durable history roles: user/assistant/tool/assistant, no invented text.
* Live usage: 4 model requests, 6 tools (including the two human requests),
  7,301 input + 459 output = 7,760 reconciled tokens, EUR 0.1552 conservative
  estimate, not invoiced cost. Both HTTP legs finish with a checked native
  pause. No further inference, approval, rejection or reservation.
* Actual pending proposal: `dd003838-cca7-4311-a382-ee88b2b85bf8`;
  native call `call_7qd3dUtnGjSZzvVb9wcE0O5m`. Source stock remains
  80 on hand / 30 reserved / 50 available; destination remains 20.
  One observed action POST took 485.5 ms, not an inference latency benchmark.
* Reload: same real service conversation and pending call, no extra model
  request, approval still unchecked/disabled, zero Continue buttons, no
  horizontal overflow at 390px. A fresh Python process reloads the durable
  state and passes readiness without a model call.
* Validation: build/type-check; 114 Python tests; 14 frontend tests; three
  final actual core/Python SSE tests. Pylance syntax checks for the native
  conversation and HTTP boundary pass with an explicit workspace root.
  Full live approval/reservation is deliberately not claimed.
* Cleanup: all bounded fixture/live servers stopped; exact S-041 offline
  fixture directory removed. Real local state and minimal publication/live
  evidence retained under `artifacts/local`; no cloud deletion, commit or push.
  Remaining limitations: direct local-development provider, large bundle
  warning, no new telemetry export or production/multi-user certification.
* Final documentary gates: all 10 customization/Markdown/link checks pass;
  `git diff --check` passes, with only existing LF-to-CRLF conversion notices.

## A-027 - S-040 Conversational Decision Handoff Analysis

* Date: 2026-11-04
* Authority: Q-042, S-040 revision 1, local/public analysis only.
* Status: completed; Q-042 analysis authority consumed.
* Objective: verify native structured human handoff and define the concrete
  replacement for separate Continue and fabricated user text.
* Excluded: application/runtime/environment edits, model/server execution,
  authenticated access, publication, deployment and Git changes.
* Findings: native declaration-only functions, v2 human `respond` and core
  follow-up support exist in the installed versions. Managed Foundry v3
  cannot acquire new tool schemas from the frontend. Native approval is
  supported, but its default AG-UI authority store is process-local.
* Recommendation: two model-requested human tools, checked durable receipts,
  native function-output continuation and explicit waiting/final states.
  Replace current text-only/replay/lifecycle assumptions, not merely the
  Continue button. Preserve backend human authority and language.
* Deliverables: concrete contract, alternatives, source register/evidence,
  proposed D-020, architecture question Q-043 and conditional S-041 scope.
* Subsequent answer: Q-043 `native_human_tools` accepts D-020's architecture.
  S-041 remains proposed and unstarted; no operational consent was requested
  or received through that architecture question.
* Documentary checks: all 10 customization/Markdown/link tests passed;
  `git diff --check` passed. Existing LF-to-CRLF notices are warnings, not
  test failures. No application tests were rerun for documentary-only edits.
* Boundary: documentary/source findings only. No native scenario or latency
  measurement, no code/package/environment edit, no server/auth/model call,
  publication, deployment or Git operation. Runtime activation still requires
  separately approved new managed definition and actual verification.

## A-026 - S-039 Real Foundry Chat Replacement

* Date: 2026-11-04
* Authority: S-039 revision 2 and Q-041 `approve_real_ui_and_live_check`
* Status: completed; Q-041 authority consumed
* Scope: one real default CopilotKit UI, first-question initialization,
  retirement of old static client, provenance/persistence and bounded
  real read-only browser verification. No publication or new services.
* Live limits: five native model requests, ten tools, 30,000 aggregate
  tokens and EUR 2 post-response estimated monitoring; no automatic retry,
  selection, approval, reservation or telemetry export.
* Local implementation: root serves the sole built CopilotKit application;
  old static files/routes removed. First explicit question initializes local
  business state and starts the managed conversation once. Reload restores
  history without inference; historical human cards/receipts remain visible.
* Startup rejects missing real configuration or frontend build. The launcher
  has no simulated/disabled application mode. Test injection remains only in
  the dedicated offline fixture.
* Frontend source, manifest, dependency lock and binary-safe served-build
  hashes are persisted for UI sessions. Drift blocks mutation without
  rebinding historical records. Verification limits are persisted and tested.
* Checks before cloud execution: frontend build/type-check and 12 SDK tests;
  77 focused Python tests; three actual JS/Python AG-UI wire tests; ten
  documentary/link tests. Pylance syntax checks pass for launcher/session/UI;
  all nine resolved `create_app` call sites are signature-compatible.
* Browser: first Send/Enter works, exactly one run on first question, human
  selection/approval alone do not infer, checkbox gates exact approval,
  two historical cards survive reload, no reload runs, no page errors or
  external resource requests, no horizontal overflow at 390px. Clean
  three-turn STANDARD fixture ends unblocked with source 80/70/10.
* An initial browser check reloaded after provisional final text rather than
  validated completion. The post-write turn correctly remained uncertain,
  with one preserved reservation and no replay. A separate fresh case,
  waiting for validation before reload, completes successfully.
* Corrected one documentary anchor after replacing the preview heading;
  all documentary checks then pass. Vite large-chunk warnings remain.
* Refreshed official [Agent Framework AG-UI guidance](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/)
  on 2026-11-04 and Azure MCP AI application best practices. No SDK/API,
  managed agent definition, model or deployment changes were introduced.
* Real verification: the default application starts in `managed-foundry`
  mode, with an empty chat list and enabled first-question composer.
  Exactly one browser run submits the explicit investigation question,
  verifies the exact published advisor v3 definition and opens the actual
  Foundry conversation through the existing native factory.
* Retained local case:
  `artifacts/local/supply-chain-s039-live/20d9028a-25b1-41c4-af71-30bf9b975f6e`.
  Actual service conversation:
  `conv_0626c304938af3bb00fOHiBmyFQeoxuYCf0a8U8DAzvmIQycpK`.
  Browser run: `09e044ab-aa1e-4ba2-8777-9ff528cbcea0`.
  No historical run was resumed or rebound.
* Actual model usage: two model requests, three tools, 2,419 input and
  1,048 output tokens; 3,467 aggregate, reconciled. Conservative estimated
  model cost EUR 0.06934, not an invoice. Persisted limits are 5/10/30,000/
  EUR 2, and telemetry is off.
* Real SSE: 69 text-content events; first text approximately 12.86 seconds
  after the request begins, successful terminal at 26.91 seconds.
  `validated_answer` precedes `RUN_FINISHED`. The initial browser wait's
  ten-second timeout did not cancel or replay the turn; the same run
  completes successfully.
* Actual final state: `running=false`, no block, a persisted user question
  and validated assistant answer, comparison cards waiting for human
  selection. Selection/proposal remain null; approval/rejection false.
  Source remains on-hand 80/reserved 30/available 50, destination on-hand
  20. No proposal, reservation or physical operation was made.
* Live reload restores the real conversation/history/cards with zero new
  browser runs and unchanged reconciled usage. No page errors, external
  browser requests or horizontal overflow at 390px.
* Additional offline browser regressions verify invalid final output,
  Stop, uncertainty after reload, zero replay, new-chat isolation and inert
  user HTML. Both failure paths show no eligible action card.
* Bounded servers stopped; exact dedicated offline fixture directories
  removed. The actual live case and cloud conversation are retained.
  No publication, IAM/resource/account changes, telemetry export,
  delegation, commit or push occurred.
* Completion is the tested real application delivery, not inferred final
  user UX approval, production certification or completion of the project.

## A-025 - S-038 Local CopilotKit Compatibility Slice

* Date: 2026-11-04
* Authority: S-038 revision 1 and Q-040 at 10:37 +01:00
* Status: completed; local authority consumed, no cloud/full-replacement authority
* Initial package gate: configured feed returns 404 for 1.84.1 and exposes
  stable 1.82.0 with v2 exports, MIT and AG-UI client/core 1.0.2.
  Public npm query fails TLS. No registry/certificate change.
  Select 1.82.0 for actual compatibility tests, not the prerelease latest tag.
* Recovery: leave the current active UI/runtime unchanged until this bounded
  slice passes; retain historical cases without migration/rebinding.

Added the pinned React/TypeScript/Vite
[frontend](../../../../src/supply-chain-resilience/frontend) and lockfile,
using CopilotKit's v2 styled view/message/composer components. A public
HttpAgent extension projects only the new trailing user message; the SDK
handles SSE and message reconstruction. Clone preserves the binding and
token; client tools/state/context/forwarded authority remain forbidden.
The run validator explicitly latches failures because SDK subscriber
exceptions need not reject its promise.

The [backend](../../../../src/supply-chain-resilience/supply_chain/ui.py)
projects human-card eligibility from the latest validated current evidence
and snapshot/decision state, then repeats the check at action time. A local
repro showed premature selection previously returned 200; it now returns
409 until a validated comparison exists. Existing CLI decisions and native
tool reasoning are unchanged. No model approval tool or new agent stage.

The fixture optionally serves `/copilot/`, invalid final answers and actual
inference-disabled configuration. The normal launcher/interface is not yet
replaced. New preview code is not yet part of production candidate frontend
fingerprints; default routing/provenance and durable card receipts belong
to proposed S-039, not a live S-038 claim.

Verification:

* Exact published dependencies install and deduplicate through the configured
  feed. All install scripts/audit/funding disabled. Lockfile package URLs
  have no embedded credentials or query parameters; license metadata retained.
* Type-check and Vite production build pass; large-chunk warnings remain.
  Main emitted JS chunk is about 2,270 kB / 663 kB gzip, not a whole-app
  transfer measurement. No production optimization or security audit claim.
* Twelve JS SDK tests pass, three actual Python SSE integration tests pass,
  and thirty targeted Python UI/native-streaming tests pass.
* Browser complete STANDARD case uses exactly three explicit run requests,
  including reload/reselection, and ends unblocked with six history entries,
  W-B 80 on hand / 70 reserved / 10 available, W-A 20.
* Cards appear after validation, not provisional tool output. Selection and
  approval do not infer; approval requires exact confirmation. Keyboard Send,
  disabled startup, invalid answer, Stop/uncertainty, case isolation, inert
  user HTML and no horizontal overflow at 390 pixels were exercised.
* Final clean browser paths report no console/page errors or external
  requests. Keep strict CSP; disabling Vite asset inlining fixed a blocked
  embedded font without adding a data-font/inline-script allowance.
* Browser harness lacks request-context cookie support; a delayed interception
  experiment stalled and was removed. Normal read/reload/switch flows were
  rerun. No claim of exhaustive slow-network race coverage.
* Ten documentary/link checks and whitespace pass. All three temporary
  loopback servers were stopped and only their exact S-038 fixture data
  directories removed. Dependencies/build outputs remain for reproducibility.

No Azure authentication/model/export/spend, hosted onboarding, published
agent changes, historical-run mutation, delegation, commits or pushes.
Only [S-039 revision 1](../plan/plan.md#s-039-revision-1-default-copilotkit-ui-replacement)
is proposed next, awaiting separate explicit approval.

## A-024 - S-037 Complete CopilotKit Analysis

* Date: 2026-11-04
* Authority: explicit user request for complete CopilotKit analysis; Q-039
* Status: completed as analysis; authority consumed, no implementation approval
* Type: analysis/tracking only, not application implementation
* Deliverable: [S-037 analysis](../research/analysis.md#s-037-copilotkit-integration-analysis)

Inspected actual guarded UI/conversation/persistence boundaries, published
package manifests/declarations, licensing and official Microsoft/CopilotKit/
AG-UI documentation. Compared documented startup/HITL/history semantics with
the current server's single-message, no-client-authority and final-validation
contract. Recorded exact installed Python/Node metadata without network
model operations. Public npm reads failed TLS through PowerShell and curl;
versioned CDN metadata and repository manifests remained readable.
No environment configuration was changed to conceal that limitation.

Produced a target chat-first UX, local deployment/build design, version/
product boundary matrix, human-card and success semantics, privacy/
telemetry considerations, change surfaces and measurable acceptance gates.
Proposed D-019 and one bounded S-038 local compatibility slice; neither
proposal is implementation approval. The existing managed agent and
published response contract are unchanged.

No application edits, packages installed/executed, servers started, browser
actions, authenticated tenant access, real inference/export/spend, hosted
service onboarding, historical-run changes, delegation or Git publication.

All ten documentary/link checks and patch whitespace pass. Existing runtime
tests were not rerun because this activity changed only documentation and
performed metadata inspection. No SDK-wire, package-resolution or live
compatibility result is invented.
Only [S-038 revision 1](../plan/plan.md#s-038-revision-1-local-copilotkit-compatibility-slice)
is proposed next, awaiting explicit operational approval.

## A-023 - S-036 AG-UI and Native Streaming

* Date: 2026-11-04
* Authority: S-036 revision 2 and Q-037 (`approve_local_agui_streaming`)
* Status: completed; local authority consumed, no live authorization
* Branch: existing `feat/agent-framework`; no commits or pushes
* Decision: [D-018](../decisions.md#d-018---local-ag-ui-interface-with-native-streaming)

Added optional AG-UI 1.7.1, FastAPI 0.141.0 and Uvicorn 0.38.0, retaining
the proven framework/Foundry/OpenAI/Projects pins. Installation and package
compatibility checks passed. Native `FoundryAgent` owns streaming and all
model/tool continuation. Terminal response and whole-batch reconciliation
precede tool effects; argument fragments are assembled natively. Fatal tool
failures still latch before framework settlement can issue another request.

Shared managed-version/native-conversation binding now serves both CLI and
UI. The official AG-UI adapter runs through a small guarded transport binding
that retains the server-owned framework session and final evidence validation.
The renderer decodes only incremental top-level message text, including
split escapes, and handles intermediate native commentary separately.
Validated-answer and successful terminal events are withheld on failure.

The same-origin static browser UI adds fresh synthetic cases, real event
consumption, provisional text, tool activity, evidence, snapshot, IDs/limits
and separate trusted selection/approve/reject/Continue controls.
Loopback Host/Origin/action-token checks reject cross-site operations.
Client histories, tools, state, resume and forwarded properties cannot
grant execution authority. Reused AG-UI run IDs are refused. Per-case locks
and checkpointing retain uncertain turns and any committed reservations.
Static assets/entry points and optional UI SDK versions participate in
provenance checks; no historical run was reset or rebound.

One provider/exporter belongs to the server lifecycle; tracing remains off
by default. A native AG-UI-span test exposed the adapter's local thread-ID
override of managed conversation telemetry. The shared allowlisted exporter
now retains the trusted service conversation identity. Existing tracing
policies and native spans remain in use; no global sensitive capture.

Initial UI tests caught an incorrect expectation that all `CUSTOM` events
indicate success: the adapter legitimately emits tool-related custom events.
The test now specifically rejects `validated_answer` on failure.
Browser testing exposed a case-switch/create race; controls are now busy
until the new case loads, and the empty selector option is disabled.
Additional test-fixture naming/discovery and expected-error-code failures
were corrected without relaxing application safeguards.

Browser verification uses a test-only loopback server and visibly labeled
offline service responses, not a fake production agent mode. The full
STANDARD case produced one reservation with source 80/70/10, destination 20,
seven simulated model requests, six tools and restored validated history.
Text reached the browser before completion while approval remained disabled.
Stop stream retained a blocked case, uncertain usage and unchanged stock.
Mobile width 390 pixels had no horizontal overflow.

No Azure authentication/access, paid inference/export, agent publication,
infrastructure/IAM/account change, APIM, old-run mutation or delegation occurred.
Live streaming/trace ingestion is not claimed.

Final acceptance:

* All 150 combined Python tests pass: 116 framework/advisor/observability/
  native-streaming/UI checks plus 34 SDK-free business/tool checks.
  The 34 SDK-free checks also passed independently without the SDK environment.
* The 28 streaming/UI tests include native split arguments, all-batch
  refusal before effects, terminal/call-ID mismatch, missing usage, failed/
  incomplete terminal responses, fatal tool latches, invalid final evidence,
  exact human approval/rejection, replay refusal, dependency drift, native
  trace correlation and disconnects before and after a committed reservation.
  Resource-close failure cannot emit success or clear an uncertain turn.
* Ten documentary/link tests, JavaScript syntax, entry-point help,
  `pip check` and `git diff --check` pass.
* Final-source browser recheck passes the complete STANDARD path and reload:
  no inference on selection (two requests) or approval (four requests);
  completion uses seven simulated requests/six tools, one reservation and
  durable source 80/70/10, destination 20. No application error is displayed.
  Provisional text arrives before terminal validation; Stop disables retry
  and retains uncertain usage. Width 390 pixels has no horizontal overflow.
* Independent real-loopback HTTP SSE consumption confirms six text events,
  first text at 1.65 seconds and clean successful EOF at 3.18 seconds,
  with validated-answer and final `RUN_FINISHED`. This tests actual local
  transport with explicitly simulated upstream service I/O.
* All temporary servers are stopped; only their dedicated
  `artifacts/local/s036-browser-tests` directory was removed.
* Pylance reports unresolved optional framework/UI imports under the editor's
  different interpreter. Do not claim a full dependency-aware static type
  check; actual imports and execution pass in the pinned application environment.

The next possible increment is one separately authorized bounded live
streaming UI walkthrough. It was not started.

## A-022 - S-034 Shared Per-Agent Observability

* Date: 2026-11-04
* Authority: S-034 revision 1 and Q-034 (`synthetic_content`, `live_readonly`)
* Status: completed; local checks and full live trace ingestion verified
* Branch: existing `feat/agent-framework`; no commits or pushes

Added shared trace setup, task-local off/metadata/content policy, native
span correlation, bounded synthetic turn/tool payload capture and allowlisted
export. Native framework sensitive recording remains globally disabled.
The advisor owns its policy; no agent registry, base class or second agent
was introduced. CLI tracing defaults to off and flushes on both success
and errors. Export failure is explicit; it must never replay an inference.
Linked destination credentials, raw session state and exception messages
are not exported. Automatic logging/HTTP/metric instrumentation, auxiliary
exporter workers and offline retry storage are not enabled.

Added compatible OTel SDK 1.45.1 and Azure Monitor exporter 1.0.0b58
(beta) after manifest changes. The configured package feed lacked SDK
1.45.2; installing compatible 1.45.1 succeeded and `pip check` is clean.
Persisted lower per-run request/tool/token/spend limits for the authorized
case; defaults and existing business/human/evidence guards remain unchanged.

All 85 framework/advisor/observability tests pass, including 14 new tracing
tests; all 34 independent SDK-free tests and ten documentary/link tests
pass. In-memory export proves actual native agent/chat/tool spans, shared
trace/run/conversation/managed-version correlation, concurrent policy
isolation, off suppression, selected content, redaction/truncation and
explicit failure/flush lifecycle. A sampler regression initially discarded
creation-time native tool attributes; returning the input attributes from
the sampler fixed the cause and the native-span assertions now pass.
Pylance verifies syntax and three compatible advisor-constructor call sites.
Its selected interpreter still cannot resolve `agent_framework.observability`;
no complete dependency-aware editor type-check is claimed.

Read-only Azure preflight verifies the declared tenant and subscription.
The SDK identifies linked Insights `ai-ai-demo-01` in `rg-ai-demo`, app ID
`b9fddc55-43ec-4cfa-afcb-92e25e345f48`. The connection string is not printed
or persisted. A guessed resource-group lookup failed; subsequent exact-name
discovery also exposed an unrelated stale CLI default group. An empty
process-local default resolved the named account without changing user
configuration or account selection.

One new read-only S-034 case and trace-scoped ingestion verification remain
pending; no live inference or export success is claimed at this checkpoint.
S-026 and S-032 artifacts remain unchanged.

The first CLI attempt stopped during destination discovery, before creating
any Foundry conversation or invoking a model/tool. SDK 2.7's convenience
method accepts only `ApiKeyCredentials`; the actual linked AppInsights
connection uses discriminator `ProjectManagedIdentity` and stores
`ApplicationInsightsConnectionString` in metadata. Only credential types/
presence flags were inspected, never the value.
Shared discovery now uses public `connections.list/get(include_credentials=True)`
and explicitly supports that observed layout plus typed API-key credentials.
Missing/ambiguous/unsupported layouts fail closed. Two regression tests
cover the actual SDK models and layouts; all 87 framework/advisor/tracing
tests now pass, including 16 observability tests.

The unused local run `801e1dbf-695a-4c7b-83f3-872e23997437` in
`artifacts/local/supply-chain-s034` is preserved with zero requests/tools,
`running=false` and no native conversation. It is not rebound after the fix.
The sole actual live case will use a fresh `supply-chain-s034-trace` directory;
no failed inference is retried and no historical artifacts are changed.

### S-034 Live Acceptance and Closure

The fresh source-bound run is `3d76b303-14d3-49f4-9bbc-30ab9d9a89e6`,
source hash `4515903c0d2dc2c9010437d98ce2bf51e9ac25fdffa41bdea94dfe5b8c98eaa2`.
Its persisted limits are five requests, ten tools, 30,000 total tokens,
4,096 output per request and EUR 2 post-response monitoring.
Exact managed v3 definition verification passed before creating conversation
`conv_071fdfaffd6a052400gEPfRdg7iCInnGw43WZQGaH93cVqDQ1k`.
The agent called snapshot/policy/comparison and returned a grounded comparison
requesting human preference. It created no proposal or reservation.

Trace `cc4f5d7e2c1e90743c06f80ccfbf0001` was exported with content mode.
The linked Application Insights resource is:
`/subscriptions/39a7dab3-b9c0-4eeb-a13b-5dfac542c2fd/resourceGroups/rg-ai-demo/providers/microsoft.insights/components/ai-ai-demo-01`.
Queries were scoped to this exact operation ID and a one-hour time window,
projecting metadata/content-presence flags rather than message/tool payloads.
The first query used workspace table names in resource context and failed
semantically; App Insights `requests`/`dependencies` tables are correct here.
Initial queries found three spans. After allowing ingestion delay, the direct
Application Insights query API returned all seven, with executable assertions:

| Span | Count | Verified content |
| ---- | ----- | ---------------- |
| `supply_chain.turn` | 1 | Synthetic input and validated output |
| `invoke_agent supply-chain-resilience-advisor` | 1 | Metadata only |
| `chat gpt-6.1-sol-2026-09-29` | 2 | Metadata and native usage |
| `execute_tool` | 3 | Exact call IDs, arguments and results |

Every span succeeded and carries the same run/conversation and managed
`supply-chain-resilience-advisor:3` identity. Parent IDs form the turn/agent/
model-and-tool hierarchy. Content on the turn and tools is intentional;
intermediate native chat content and system instructions are not captured.
The actual backend ingestion is verified; the portal UI was not opened.

Independent read-only SQLite checks assert zero proposals and requests;
W-B stays 80 on hand / 30 reserved / 50 available and W-A 20.
There is no selected option, approval or proposal ID. Native reload/readiness
passes, `running=false` and usage is reconciled. Eleven local metadata events
include exactly one `telemetry.started` trace reference and no human decision.

Actual usage: two model requests, three tools, input 2,405/output 956 =
3,361 tokens. Conservative upper model estimate EUR 0.06722, not an invoice
and excluding Insights ingestion/retention. All declared bounds hold.
An added threaded batch-export regression verifies all seven spans still
export after leaving the task-local agent scope; all 17 observability tests pass.

Final application checks pass: 88 framework/advisor/tracing tests and 34
SDK-free tests on the independent interpreter (122 total). All ten repository
documentary/link tests, `pip check` and whitespace checks pass. The link test
caught a relative-path depth error in D-017; its targeted correction is
verified. Final runtime-source/SDK provenance still matches the live run,
without rebind. Pylance verifies generated syntax and all nine CLI chat call
sites; the documented unresolved framework import in its editor environment
prevents claiming a complete dependency-aware editor type-check.

S-034 revision 1 is completed and its authority is consumed. No additional
live turn/query follows automatically. No agent publication, infrastructure/
IAM/account change, UI, historical-run reset/rebind, commit or push occurred.

## A-021 - S-032 Live Framework Validation

* Date: 2026-11-04
* Authority: Q-031 explicit operational consent, S-032 revision 1
* Status: completed; bounded live STANDARD case passed end to end
* Scope: existing managed advisor v3, approved project/tenant/deployment,
  one new framework conversation and synthetic local run; no publication

CLI tenant check matches the declared tenant and subscription
`39a7dab3-b9c0-4eeb-a13b-5dfac542c2fd`; no account selection/login change.
Initialized new `artifacts/local/supply-chain-s032` without overwrite:
run `4be32fdd-8618-4cff-9814-a1129005df69`, source hash
`93acfc813cfcaef9cad816982abf1c53a7c7ee302bf77081187513e494d2aab2`,
definition hash `46e916cf4ce54c524d41472d24e506d83d26eea91c9b1d001623502fed254da2`.
Exact v3 definition verification succeeded before framework conversation creation.
Conversation: `conv_01eac5775d3b907400OGYGM6XDDrp4uzxBGT7nDIU7ABOxd3ig`.

The actual agent requested snapshot, policy and comparison in one model batch;
local functions executed sequentially through framework middleware. The next
response correctly explained shortage 40, delayed assembly day 7, STANDARD
90/day 3/margins 0/1 and EXPRESS 95/day 2/margins 1/2, then requested human
preference. All three evidence objects matched real outputs.
No proposal or request exists; source 80/30/50 and destination 20 unchanged.

First-turn usage: two model requests, three tools, input 2,435/output 1,095,
total 3,530 tokens, conservative upper estimate EUR 0.0706.
Local reload/readiness passes; native conversation persisted, `running=false`,
usage reconciled. Metadata trace confirms correlated service/tool calls.
The framework's warning about omitting local tool declarations is expected:
the stored managed definition owns schemas, local functions supply dispatch.
Pause for Q-032; no selection or approval is inferred from older runs.

Q-032 explicitly selected STANDARD. Recorded the trusted local selection,
then continued the same conversation. The agent refreshed snapshot/policy/
comparison and created proposal `8cf76b82-25fd-40d6-98f6-795a5d3a43fa`:
40 BOARD-1 W-B to W-A, cost 90, arrival day 2, completion day 3.
It returned exact grounded details and waited for human approval.
Durable lookup confirms proposed status, approved=false, no request or stock
mutation. Source remains 80/30/50; destination 20.
Cumulative usage: five requests, seven tools, input 11,823/output 2,297,
total 14,120 tokens, estimated upper cost EUR 0.2824; usage reconciled.
Pause for Q-033 exact-ID approval; the one-case preference does not authorize
reservation.

Q-033 explicitly approved the exact proposal and synthetic reservation.
Recorded human approval through the local application operation, then
continued the same managed-v3 conversation. The agent chose snapshot,
policy and comparison refresh, then `execute_approved_transfer`, followed
by `read_transfer_result`. Its final answer passed application validation,
returning one exact current durable result and three separately labeled
historical fact objects. It correctly distinguished reservation from
shipping/receipt and planned dates from completed events.

Final request: `beb714bc-e587-4c45-8486-e7796962e3dd`.
Read-only SQLite confirms exactly one proposal and one request. Stock is
W-B 80 on hand / 70 reserved / 10 available; W-A remains 20. Snapshot
pending-request count is one. Trace assertions confirm human approval
precedes execution, which precedes completed durable read-back; the execution
tool was called exactly once.

Final cumulative usage: nine model requests, twelve tools, input 33,484/
output 3,684 = 37,168 tokens. Conservative upper estimate EUR 0.74336,
not actual billing. All usage is reconciled, `running=false`, native session
reload/readiness passes and all declared operational limits were respected.
The 44 local metadata events contain no prompt/arguments/result/message
payload fields. All ten documentary/link checks passed.

S-032 revision 1 is completed for this positive live case; its authority is
consumed. No further model turn or operation follows automatically.
No source/dependency change was needed, no publication/provisioning/IAM
change or run reset/retry occurred. S-026 and its historical failed acceptance
remain untouched. This proves this managed-v3 framework integration and
current/historical handoff for one case, not general model quality or UI support.
The one proposed next activity is bounded local testing-UI design, without
implementation, hosting or cloud spend unless separately authorized.

## A-020 - S-031 Explicit Agent Factory

* Date: 2026-11-04
* Authority: Q-030, user's acceptance of the single local design recommendation
* Status: local refactor verified on the existing `feat/agent-framework` branch
* Scope: factory extraction, callers/tests, source-layout documentation and tracking

The new [agent module](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/agent.py)
exposes `create_agent(project, agent_version, conversation=...) -> FoundryAgent`.
It composes the managed version, exact local function implementations, middleware,
limits and retry configuration. The returned object is the framework agent,
not a custom agent class or wrapper.

[AdvisorConversation](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
retains interaction state, human decisions, guarded dispatch and current/historical
evidence. Its public `invoke_tool` callback connects those controls to the factory.
Removed its construction method; there is no alias or parallel creation path.
CLI and all ten test/helper factory callers use the new module. Managed
definition, prompts, tool schemas, dependencies and runtime behavior are unchanged.

Verification:

* All 71 framework/runtime/advisor tests passed in 3.009 seconds through the
  extracted factory, including actual offline function invocation, serialized
  HTTP requests, exact human gates, budgets, evidence and native-session restore
* Extended the existing provenance regression to cover `agent.py` as well as
  `tools.py`; the focused regression passed after that test change
* All 15 current application/test Python files parsed under the application
  interpreter; Pylance also reports no syntax errors in the new factory module
* Pylance reports all ten factory call sites compatible, but renders external
  SDK types as `Any`; this is not a clean dependency-aware editor type-check
* No remaining Python references to the retired `build_agent` or private
  `_invoke_tool` entry points
* All ten documentary/link checks passed; `git diff --check` reports no
  whitespace errors

Existing uncommitted S-030 changes were retained. No Azure access, inference,
publication, dependency installation, old-session migration/rebinding, commit
or push occurred. Existing session source hashes intentionally drift after
the extraction; no historical run was adjusted to bypass that protection.
S-031 local approval is consumed. A fresh bounded live framework case remains
the one proposed next activity and requires separate operational consent.

## A-019 - S-030 Direct Agent Framework Migration

* Date: 2026-11-03
* Authority: Q-029, S-030 revision 1 local-only contract
* Branch: `feat/agent-framework`, created from the clean `main`
* Status: application implementation and offline integration verified
* Boundary: no authenticated Azure access, inference, publication, UI,
  actual-run migration/retry/deletion, commit or push

### Single Framework Runtime

Replaced the generic custom Responses loop with the actual Microsoft
`FoundryAgent`. The [advisor](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
owns its managed-agent construction, exact local `FunctionTool` bindings and
business capability/evidence adapter. The framework executes functions and
continues the conversation. There is no custom model loop or fallback.
The [shared runtime module](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
now contains cumulative budget/call policy and framework middleware only.

Chat middleware checkpoints each service request before I/O, reconciles
raw SDK response usage/status and validates the whole function batch before
any effect. Function middleware validates unused call IDs, emits metadata,
checks authoritative results and propagates fatal failure. Calls are locally
sequential. A failure latch prevents the framework's hosted-conversation
settlement request from making extra I/O; no automatic recovery is attempted.
Expected and unexpected function errors stop rather than becoming recoverable
model inputs. Model request default remains ten, with explicit allowance up
to twenty; tool/token/output/spend limits remain unchanged.

The asynchronous [CLI](../../../../src/supply-chain-resilience/advisor_demo.py)
uses tenant-bound credentials and an async Projects client with retries off.
It retrieves the exact published version, checks its complete definition,
then supplies versioned `agent_reference` through the framework's non-preview
project endpoint. A newer latest version does not silently substitute for
the requested one. No publication API is implemented. Native framework
conversation creation is checkpointed, bound and reused.

The [session adapter](../../../../src/supply-chain-resilience/supply_chain/session.py)
persists actual `AgentSession.to_dict()` state and restores it using
`from_dict()`, alongside current/historical facts, exact human decisions,
call IDs, counters and source/asset/SDK provenance. Its new
`supply-chain-framework-1` format rejects old runs without migration.
Local inspection of those historical artifacts uses their recorded
JSON/SQLite, not a legacy runtime path. Failed turns remain blocked.

### Dependencies and Regression Evidence

Updated the [manifest](../../../../src/supply-chain-resilience/requirements-foundry.txt)
before installing only in the application's existing environment:
framework core 1.24.0, Foundry 1.16.0, OpenAI adapter 1.18.0, Projects 2.7.0,
Identity 1.27.0 and OpenAI 3.38.0. Projects 2.7.0 satisfies the adapter's
declared `<2.8.0` ceiling. `pip check` reports no broken requirements.

Validation:

* All 105 combined application tests passed in 11.590 seconds
* All 34 SDK-free business/manual tests passed independently in 3.018 seconds
* All ten repository documentary/link checks passed; `git diff --check`
  reports no whitespace errors
* Actual framework function invocation is exercised, not replaced by a mocked
  `agent.run`; network/service responses alone are simulated
* Real OpenAI HTTP serialization verifies version reference, conversation,
  matching tool outputs and absence of local tool declarations in requests
* A real SDK HTTP 503 fixture makes exactly one request despite a client
  fixture initially configured for retries; uncertain usage blocks continuation
* Whole-batch capability/argument/call-ID/tool-count guards, trusted exact
  selection/approval, stale approval, idempotency, mandatory read-back,
  current/historical evidence and failure stops pass
* Native session round-trip, bound conversation creation/reuse, cumulative
  counters/call IDs, metadata-only trace and old-format refusal pass
* All 14 current application/test Python files parsed under the application
  interpreter; no remaining executable `AgentRuntime`, `AdvisorLimits` or
  application-level model loop was found
* Existing prompt/schema/definition fingerprint tests pass unchanged

An initial full test process ended without a result (exit 1073807364).
Focused rerun and subsequent full 105-test run passed.
Initial targeted failures exposed framework `list[Content]` result handling
and incomplete service-conversation fixtures; both were corrected and covered.

Editor validation limitation: Pylance selected Python 3.14 rather than the
application environment and reported `reportMissingImports` for framework/
async Azure modules. An environment-update tool reported success but the
next environment query still showed 3.14. Package inventory independently
confirmed the modules in the application environment. Subsequent Pylance
syntax requests failed at MCP transport initialization; no clean Pylance
type-check result is claimed. Runtime signatures and all migrated call
surfaces are exercised by the passing tests; interpreter-based syntax passes.

S-026 artifacts were not rewritten, rebound, migrated, resumed or retried.
Their failed live acceptance remains historical, not superseded by offline
tests. The managed v3 prompt and schemas are unchanged. A fresh bounded live
framework case is the one proposed next activity, requiring separate consent.
No new inference or successful live migration is claimed.

## A-018 - S-027 Revision 2 Evidence Separation and Legacy Retirement

* Date: 2026-11-03
* Authority: user's 17:02 +01:00 local correction request and Q-028's explicit
  historical/current choice plus obsolete-code deletion request
* Status: local implementation verified; no further live validation claimed
* Scope: advisor evidence/persistence, retired local drivers, tests and docs

### Evidence Correction

The observed failure is reproduced by an offline test: read snapshot,
policy and comparison before execution, execute the exact human-approved
proposal, read its durable result, then include those unchanged earlier
facts alongside the current result. Before the fix it raises the same
`ungrounded_answer`; after the fix it completes with separate collections.

The [advisor](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
archives successful tool results when superseded or invalidated. Historical
facts persist with human decisions, using an empty default for older records;
this is not a source-hash migration or a means of reconstructing missing facts.
Python classifies the model's exact returned objects into `answer.evidence`
(current) and `answer.historical_evidence` (historical), leaving the message
unchanged. The model still returns exactly `message` and `evidence`.

Only actual locally recorded tool results can match either collection.
Changed or invented objects fail. A historical result cannot satisfy a
required current operation result or replace the mandatory post-write lookup.
Execution invalidates earlier comparison/read obligations as well as facts,
avoiding a stale comparison requirement after that comparison has been
removed from the current cache. This does not prescribe a reasoning workflow.

Regression checks cover authentic history with current read-back, modified
history, omission of the current result, refreshed snapshots, durable history
restoration and older records without invented history. Existing forged
approval, wrong ID, rejection, stale facts, duplicate execution and interrupted
write checks remain. Free-text correctness is not semantically certified.

### Retired Executable Paths

After confirming no active advisor/session import depends on them, removed:

* Historical read-only adapter `supply_chain/foundry.py` and `foundry_demo.py`
* Historical staged adapter `supply_chain/walkthrough.py` and `walkthrough_demo.py`
* Their retired-path suites `tests/foundry_adapter_tests.py` and
  `tests/walkthrough_tests.py`
* Legacy definition factories/profile generation and the unused shared-runtime
  result hook/called-tool accumulator

Useful SDK response fixtures and transport/usage/batch/call-ID/error checks
now live in [runtime tests](../../../../src/supply-chain-resilience/tests/runtime_tests.py)
against the current advisor. Cloud binding/version reuse guards are covered
in [advisor tests](../../../../src/supply-chain-resilience/tests/advisor_tests.py),
with mocked clients only. This avoids preserving a dead implementation just
to test shared safeguards. The SDK-free manual tool adapter, business
capabilities, explicit historical prompt assets and actual run evidence remain.
Historical links below now identify retired source paths instead of linking
to nonexistent files; their original outcomes and decisions remain unchanged.

Validation:

* The failing reproduction passed after the correction
* All 95 combined tests passed in 4.095 seconds; the lower total reflects
  retirement of obsolete driver-specific tests, not removal of active guards
* Pylance reports all eight current definition-factory call sites compatible;
  advisor diagnostics contain no items
* All 34 SDK-free tests passed independently in 2.313 seconds
* All ten documentary/link checks passed; retired implementation references
  no longer create broken links
* Changed application Python files have no syntax errors; no remaining
  Python references to the retired adapters/factories/hooks were found
* Current and historical prompt/schema/definition hashes still pass their
  existing regression assertions; no new publication is needed solely for
  this local adapter change

S-026 remains a failed historical live acceptance with one completed synthetic
reservation. Its session, stop flag, counters, source hash, database, events
and cloud version were not rewritten or retried. A new live case using the
unchanged v3 definition requires separate operational authorization.
Read-only inspection confirmed original 14/11/48,338 counters, source binding,
one request and 80/70/10 stock; session, SQLite and trace bytes were unchanged
by that inspection. The published definition fingerprint remains
`46e916cf4ce54c524d41472d24e506d83d26eea91c9b1d001623502fed254da2`.
No authenticated Azure access, inference, installation, commit or push occurred.

## A-017 - S-026 Live Agent-Led Validation

* Date: 2026-11-03
* Status: blocked at final-answer acceptance; live attempt ended and
  operational authority consumed. No automatic retry or rollback.
* Authority: Q-024 publication and bounded live case; Q-025 STANDARD choice;
  Q-026 revision 2 allowance/local correction; independent Q-027 exact approval
* Target: existing project/deployment, same agent version 3 and conversation
* No new provisioning, IAM, prompt change, telemetry export, commit or push

Version 3 was published and its complete definition read back before inference.
The first natural-language turn used snapshot/policy/comparison, then asked
for a preference: four requests, three tools, 6,104 tokens, no effects.
After Q-025's trusted STANDARD selection, a second conversational message
caused a fresh read of those three tools, proposal creation and a stop for
approval. No fixed propose-stage model command was used.

The exact proposal is `bf144275-ec8f-4ad3-bdd2-b63b9ff4616f`: STANDARD,
40 BOARD-1 W-B to W-A, cost 90, arrival 2/completion 3, snapshot 1/P-1:1.
At the pause, 9 requests/7 tools/22,345 tokens had been consumed,
conservative estimate EUR 0.4469. Independent local inspection confirmed
fully reconciled usage, `running=false`, no request, unapproved proposal
and stock 80/30/50 at W-B, 20 at W-A.

Q-026 explicitly extended the same run to 20 cumulative requests, not twenty
additional requests. Historical `RunLimits` still defaults/caps at ten;
the advisor subclass permits twenty while its session defaults to ten.
The allowance is persisted and restored. Initial CLI setup accepts explicit
10/20; it never changes an existing session's allowance automatically.
All 101 tests passed in 3.849 seconds, including actual twenty-versus-
twenty-first simulated request enforcement, legacy cap rejection and
restoration retaining nine requests and seen call IDs.

The authorized local-source transition changes only this clean session's
source fingerprint and allowance, with all bindings, usage, decisions and
seen call IDs retained. It is not an automatic migration or a means of
clearing uncertain operations. All other drift checks remain in force:

* Old source: `d87f70f707ec149ea0909ce73c18874c9e2dc14d35af6c2e2e60d23809667e9b`
* New source: `ff5fc9ca7047961e84904b7355cc8166fe50ec9a9389522396bd3ee78ab26f14`
* Instructions/schema/full cloud definition remain unchanged

Q-027 independently approves the exact proposal, not a future proposal,
shipment or receipt. Human-path approval and agent-requested execution/
read-back were the next authorized actions at that checkpoint.

### Actual Action and Final-Answer Failure

The human-only CLI recorded approval before model continuation; trace event
34 is `human.approved`, preceding execution at event 45. The agent chose
snapshot, policy, execution, then durable-result read-back, without a fixed
application execution-stage command. Exactly one proposal and one request
exist. The request is `682a1ce9-1600-4e75-bae9-c0338df29f82`, bound to the
exact approved STANDARD proposal. Snapshot advanced to version 2:
W-B on-hand/reserved/available 80/70/10; W-A remains 20.
No shipping, receipt, purchasing or factory scheduling occurred.

The final model response was rejected with `ungrounded_answer`; CLI exit 1.
Read-only retrieval of the existing response
`resp_09d5d47071f1bef3006aea038f03f48190b00355a300d6214c` and bounded
conversation-item inspection required no additional model inference.
All three evidence objects match actual earlier function outputs exactly:
pre-write snapshot 1, policy, and the correct post-write durable result.
The prose describes the reservation and before/after values accurately.
The failure is therefore a temporal evidence-contract mismatch, not observed
fabricated tool data or failed execution: the application invalidates cached
read results after a write, while the model also copied those historical
facts into its final evidence. This does not justify accepting stale facts
as current state or disabling the guard.

Separate-process reconciliation verified:

* One proposal/request, correct IDs, source 80/70/10, destination 20
* Human approval precedes the single execution; subsequent result read-back
* All eleven tool starts/completions have matched unique call IDs
* All 53 local events share run/conversation correlation and contain no raw
  prompts, arguments, model text or tool-result payloads
* Fourteen model requests, eleven tools; 45,189 input + 3,149 output =
  48,338 tokens, estimate EUR 0.96676, not invoice
* Usage reconciled; `running=true` retained as the failed-turn stop flag,
  not evidence of an active process. No flags cleared or write retried.

The 101 offline tests passed; all ten documentary/link checks and changed
application Python syntax checks passed before closure. These checks do
not turn the failed live final-answer contract into a successful test.
No new version, prompt change or recovery operation was performed to mask it.
The next proposed local increment is to correct the historical/current
evidence handoff with regression coverage; any publication and further live
case require a separate operational contract.

## A-016 - S-025 Revision 1 Multi-Agent-Ready Source Layout

* Date: 2026-11-03
* Authority: Q-023 explicitly approved the local reorganization, with the
  clarification that tools can be agent-specific or shared.
* Status: completed; local approval consumed
* Scope: source ownership/imports/assets/provenance/tests/documentation only

The [resilience advisor package](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor)
now owns its definition, conversational controls, prompts and six tool
contracts/dispatcher. Its
[evaluation cases](../../../../src/supply-chain-resilience/evals/resilience_advisor/cases.json)
are grouped by agent. Package initializers do not eagerly load the SDK.
The [root package](../../../../src/supply-chain-resilience/supply_chain/__init__.py)
retains SDK-free tool convenience exports for existing callers.

The [shared runtime](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
depends only on a small structural `FunctionDispatcher` protocol, not the
advisor or a concrete business tool session. Agent-specific approval handlers
and historical baseline adapters explicitly retain their business store/actor.
Domain rules, store transactions and solution data are reused without copying.
No shared-tool directory is invented before actual reuse; a later agent can
own different schemas/permissions or reuse an extracted common capability.
The application session/CLI still explicitly binds the single advisor.

All imports, asset paths, applicable historical links and README were updated.
Source hashing now includes nested agent Python modules, rather than only
root-level package files. Existing candidate source hashes are not rewritten
or silently migrated; drift still blocks continuation while local inspection
remains available. No persisted run artifacts were changed.

Validation:

* All 99 combined tests passed in 3.946 seconds: the previous 96 and three
  additional source-layout/decoupling regression tests
* All 34 SDK-free tests passed independently
* All 10 repository documentary/link checks passed
* Captured pre-move candidate instruction, tool-schema and full-definition
  hashes match after relocation; exact historical v1/v2 instruction hashes
  also still match
* A simulated nested tool-source change changes source provenance and
  triggers `candidate_drift`; no actual source modification is used by the test
* A dispatcher without advisor/store members works with the shared runtime
* Pylance conversation diagnostics returned no items; runtime diagnostics
  contain only unused-parameter hints in its pre-existing extension hooks

This is multi-agent-ready organization, not multi-agent orchestration,
delegation or identity isolation. Only the original advisor exists.
No prompt behavior, schema, dependency, cloud definition, tenant context,
inference, telemetry export, commit or push changed.
The next proposed activity remains separately authorized candidate publication
and bounded live conversational validation; it was not started.

## A-015 - S-024 Revision 1 Agent-Led Local Candidate

* Date: 2026-11-03
* Authority: user's 16:22 +01:00 "procedi" confirms the single local
  increment presented after S-023. This is free-form consent, not an
  invented native-form answer or new cloud approval.
* Status: local implementation verified; no publication or inference
* Accepted direction: D-013, RQ-011...RQ-014, existing Python/managed-agent
  choice and unchanged synthetic stock/approval invariants

### Implemented Boundaries

* [Agent definitions](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/definition.py)
  load explicit text instructions and bind tools/model. No deployment logic.
* [Advisor instructions](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/prompts/advisor.txt)
  cover investigation, uncertainty, planner preference, external approval,
  failure/reconciliation, language and exact-evidence output.
* [Generic runtime](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
  owns Responses continuation, call IDs, usage/limits and metadata events.
  Supply-chain instructions and required read-tool sequences are absent.
* [Conversation](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/conversation.py)
  accepts arbitrary planner messages; guards capabilities using trusted human
  decisions, not comparison/proposal/execution reasoning phases.
* [Candidate session](../../../../src/supply-chain-resilience/supply_chain/session.py)
  persists decisions, synthetic evidence, seen call IDs, usage and asset
  references. Exclusive locking and checkpoint-before-request semantics
  block blind retries after interrupted/failed turns.
* [Candidate CLI](../../../../src/supply-chain-resilience/advisor_demo.py)
  provides local definition/init/inspect/select/approve/reject commands and
  a future guarded chat path. It contains no agent publication command.
  Chat verifies the full latest definition/version before opening the
  Responses client; historical cloud v2 is not a matching candidate.
* [Scenario](../../../../src/supply-chain-resilience/data/scenario.json)
  and [loader](../../../../src/supply-chain-resilience/supply_chain/data.py)
  separate versioned initial snapshot facts from code. The small fixed
  product/order/cost model remains explicit in the existing domain module;
  no ERP abstraction, alternate data service or ORM was introduced.
* [Evaluation asset](../../../../src/supply-chain-resilience/evals/resilience_advisor/cases.json)
  defines ten synthetic scenarios/rubrics, not measured model outcomes.
* [README](../../../../src/supply-chain-resilience/README.md)
  distinguishes the unpublished candidate from real historical baseline
  evidence and explains local preparation versus future authorized chat.

The existing tool schemas, business arithmetic, SQLite transactions and
human-only approval store were reused. The historical fixed-flow drivers
remain available and their sessions are not migrated.
The read-only and walkthrough instruction assets exactly preserve committed
v1/v2 content: regression SHA-256 values were independently derived from
the committed source and match the extracted files.
No `.replace` construction of workflow instructions remains.

### GenAIOps and Provenance

The stable candidate instruction path is tracked as source, without copied
numbered candidate files or a templating dependency. Candidate state records
instruction/schema/definition hashes, source-content hash, exact SDK versions,
scenario/evaluation hashes and actual remote bindings only when verified.
These content references are not a clean-commit claim, signed release or
fabricated Foundry version. Model deployment is configuration; resolved
model version and publication evidence await an authorized cloud step.

Any detected code/prompt/schema/scenario/evaluation/SDK drift blocks
resumption rather than silently changing the running candidate. Prompt
changes in the portal do not synchronize into Git. The existing latest-version
guard remains; no historical-version routing or automatic rollback is claimed.

### Validation and Limits

The combined suite passed 96 tests, including 26 new offline candidate tests
and all 70 historical tests. The 34 SDK-free business tests independently
passed with terminal Python. `pip check` found no broken requirements.
All 10 documentary/link checks passed.

Candidate cases use real SDK Response objects and real local SQLite effects
with a simulated model. They verify:

* Multiple read-tool orders, partial investigation and tool-free clarification
* Explicit human selection, exact proposal/approval and rejection without writes
* Forbidden self-approval, wrong IDs/options and stale facts
* Exact evidence preservation, mandatory read-back after execution, and a
  pre-execution result read not satisfying post-execution confirmation
* One effect for duplicate execution and persistent reconciliation after
  a lost response, without another model request
* Shared budgets, restored call IDs, metadata-only trace correlation, command
  locking, version-format rejection, prompt/schema/SDK drift and no overwrite
* No Azure authentication from local commands and no Responses client opened
  when the existing cloud definition does not match the candidate

Pylance syntax checks passed for conversation, session and CLI. Initial syntax
tool calls required an explicit workspace root; after supplying it, all three
checks passed. Editor diagnostics reported `reportMissingImports` for Azure
Projects imports in agent/CLI while execution/imports succeeded in the pinned
application-local environment. No editor-interpreter setting was changed and
no fully clean strict workspace type-check is claimed.

Free-text message correctness is not certified by JSON/evidence validation.
No live candidate conversation, model-quality score, optimizer, cloud
evaluation, new agent version/conversation or telemetry export was run.
Trusted local files/demo roles are not a production authorization boundary.
One proposal is allowed per candidate session; rejection does not silently
create a replacement proposal. The existing completed S-022 artifacts were
not reset, migrated or removed.
No dependencies, environment configuration, cloud resources, IAM, APIs/MCP,
harness/hosted runtime, Git commits or pushes changed.

The next proposed activity is bounded candidate publication and live
conversational validation; operational targets/limits and business approval
must be confirmed separately. Local S-024 implementation consent is consumed.

## A-014 - S-022 Revision 1 Complete Human-Gated Walkthrough

* Date: 2026-11-03
* Authorization: Q-020 explicitly approved implementation, one workflow version,
  one live synthetic case and local metadata-only tracing. Q-021 selected
  EXPRESS only for this case. Q-022 separately approved the exact proposal
  and synthetic reservation. No answer inferred from implementation consent.
* Status: completed; live and local acceptance verified, authorization consumed
* Identity: `supply-chain-resilience-advisor`, workflow version `2`, same
  existing project and `gpt-6.1-sol` deployment. Read-only version `1` retained.
* Conversation: `conv_0492c8bfd1d8311400NkVZtm61THqvWjwXjqoRmDf8V11OUHvm`
* Run correlation ID: `fff4d313-f9d5-4e46-ab47-853b65cb7ae1`
* Proposal: `4113e1b5-55a0-4137-b1e3-4d5481adcf3b`
* Durable request: `6c0fdd7f-66c1-4a08-906e-c8fef52a82ed`

### Implemented Surfaces

The paths below describe the S-022 implementation at that time. The old
drivers were retired in S-027; shared safeguards now live in the
[current runtime](../../../../src/supply-chain-resilience/supply_chain/runtime.py)
and current advisor tests.

* Shared loop (`supply_chain/foundry.py`, retired):
  reuse of request accounting, call-ID continuation, batch validation and
  explicit-error behavior; optional metadata-only event callback
* Workflow stages (`supply_chain/walkthrough.py`, retired):
  human-selected option and exact approved proposal checks independent of
  model instructions; no model approval tool
* Staged CLI (`walkthrough_demo.py`, retired):
  durable session and SQLite state, atomic session-file replacement,
  exclusive command lock, persistent shared usage and uncertainty flags
* Workflow tests (`tests/walkthrough_tests.py`, retired):
  success, rejection without reservation, early execution/self-approval
  rejection, wrong IDs/options, duplicate proposal prevention, shared budgets,
  state/trace restoration and confirmation/uncertainty guards
* Baseline CLI (`foundry_demo.py`, retired):
  explicitly rejects a different latest named-endpoint version rather than
  silently invoking the new workflow definition as read-only v1
* Adapter regression tests (`tests/foundry_adapter_tests.py`, retired)
  and [README](../../../../src/supply-chain-resilience/README.md) updated

No new dependency, framework, MCP/API server, workflow engine, cloud
infrastructure, IAM mutation, hosted runtime or Copilot harness was added.
The active named endpoint now uses the workflow version; local dispatch
still enforces current-stage tool permissions.

### Actual Live Evidence

The same retained conversation completed three model stages:

| Stage | Cumulative model requests | Cumulative tool calls | Cumulative tokens |
| ----- | ------------------------- | --------------------- | ----------------- |
| Comparison | 4 | 3 | 3,658 |
| EXPRESS proposal | 6 | 4 | 6,865 |
| Human-approved execution and read-back | 9 | 6 | 13,738 |

Final reported usage is 12,919 input and 819 output tokens, with no
unreconciled request. Conservative application model-cost estimate is
EUR 0.27476, not actual invoiced cost. All configured bounds/monitoring
thresholds stayed clear; no automatic retries.

The model created the selected EXPRESS proposal through its function tool:
40 BOARD-1 from W-B to W-A, cost 95, arrival day 1, completion day 2.
Before approval the source remained reserved 30. The user asked for
clarification rather than selecting in the first form; the process paused,
clarified one-case semantics and waited for explicit EXPRESS selection.
The subsequent exact-proposal approval was recorded outside the model.
The model then called execution and durable-result lookup, returning exact
authoritative tool JSON rather than an invented successful action.

A separate CLI `result` process confirmed snapshot version 2, source on-hand
80, reserved 70, available 10 and destination on-hand 20. SQL inspection found
exactly one proposal and one request. No shipment or receipt was claimed.

Durable local session:
`artifacts/local/supply-chain-s022` (ignored by Git, deliberately retained).
The metadata-only JSONL trace contains 36 events: nine model start/end pairs,
six function start/end pairs, and six lifecycle events.
Verified matching unique function call IDs, consistent run/conversation IDs,
durations, and `human.approved` before `execution.started`.
The lifecycle is comparison ready, planner selected, proposal ready,
human approved, execution started, execution completed.
No prompts, function arguments, tool results, model text or credentials
are recorded in these trace events. This is not a distributed OpenTelemetry
trace or Azure Monitor export.

### Validation and Limits

The initial combined implementation run passed all 67 tests before the live
case. The final combined suite passed **70 tests in 4.338 seconds**, including
the latest-version regression and preparation reuse/conflict checks.
`pip check` reported no broken requirements. All **10 repository documentary
and link checks** passed. Preparation reuses a matching workflow version for
a separately authorized fresh session rather than producing duplicate
versions; unrelated definitions are never silently overwritten. No second
live session was started to validate this offline-tested reuse path.
Editor problem checks on the shared loop, workflow and staged CLI returned
no errors; this is not a claim of a separately configured strict type check.

Negative/rejection/idempotence cases are offline evidence; only the approved
positive EXPRESS case ran live. Demo actors and trusted local state files
are not real multi-user identity enforcement. One pending synthetic transfer
is requested/reserved, not physically shipped. The session is completed and
retained for inspection; no reset, cancellation or further inference is implied.
No resource deletion, real data, telemetry export, paid evaluation, commit
or push occurred.

The approved S-022 increment and this exact synthetic business approval are
consumed. No further model calls or resource changes are authorized by
completion. A proposed next activity is a user-led demonstration/review of
the completed flow; Copilot harness study remains a separate future topic.

## A-013 - S-020 Revision 2 Successful Live Read-Only Case

* Date: 2026-11-03
* Authorization: Q-019 native confirmation returned true after the explicit
  revised target, limits and post-response monitoring contract
* Status: completed; this single-run authorization is consumed
* Reused agent `supply-chain-resilience-advisor` version `1` and existing
  `gpt-6.1-sol`, model version `2026-09-29`, GlobalStandard, in the approved
  existing project. No agent/version creation or mutation.
* Created and retained conversation
  `conv_0c9bfd4440046b6b009z6TCANKGYxuSL8kTUa2qI506VmAhJxG`;
  no old conversation deletion or automatic cleanup.
* Live CLI exited 0 with `status: completed`. Real calls covered
  `read_planning_snapshot`, `read_transfer_policy` and
  `compare_transfer_options`. Function outputs continued the same conversation.
* Actual model-reported usage: four generation requests, three dispatched
  function calls, 2,577 input tokens, 420 output tokens, 2,997 total;
  no unreconciled usage.
* Application conservative model-cost estimate: EUR 0.05994, charging every
  reported token at the higher EUR 20/million estimate rate. Not an invoice
  or exact contracted price. All configured monitoring thresholds stayed clear.
* Returned structured options exactly matched authoritative tool output:
  quantity 40 for both; STANDARD cost 90, arrival day 2, completion day 3,
  margins C-1/C-2 of 0/1; EXPRESS cost 95, arrival day 1, completion day 2,
  margins 1/2. Both feasible under ceiling 100.
* Explanation inspection: correctly identified shortage 40, source available
  50 excluding unrelated reservations, supplier day 6 delay and the extra
  cost 5 for one extra margin day. It left selection to the planner and did
  not claim proposal creation, approval, execution or stock movement.
* `baseline_unchanged: true`: read-back snapshot equaled the initial synthetic
  baseline. Viewer actor and registered read-only tool subset were used.
  Temporary local database was removed by its context manager.
* No mandatory token-count endpoint, write tool, stock mutation, provisioning,
  IAM change, telemetry export, paid evaluation, dependency change or Git
  mutation. No automatic retries or additional test cases.
* Limitations: this proves one baseline live function-calling case, not live
  human approval/action, full tracing, negative-case cloud evaluation, real
  production authorization or universal SDK/model compatibility.
* Next proposed activity: the complete interactive planner-selection and
  human-approved action flow with trace visibility, under a separate bounded
  contract. Not started or authorized by this completed case.

## A-012 - Relaxing the Mandatory Token Pre-Count

* Date: 2026-11-03
* Authorization: user's explicit 15:09 request to relax the prerequisite;
  no new cloud operation or unlimited spending inferred
* Status: completed, local implementation and validation only
* Removed `responses.input_tokens.count` from the request path; no alternate
  route or guessed input count is substituted
* Preserved ten generation requests, twenty function calls, requested 4,096
  output tokens per response, no automatic retries and read-only tool access
* Aggregate 100,000 tokens and estimated EUR 10 are now monitoring thresholds
  checked against actual returned usage; a request can cross a threshold,
  at which point the loop stops. No hard pre-request budget guarantee.
* Missing/lost/invalid usage is explicitly unreconciled and cannot silently
  retry. Summary identifies `post_response_monitoring` enforcement.
* Updated adapter tests and README. All 56 combined Python tests passed in
  2.657 seconds. Tests include an unavailable counter that must never be
  called, actual-usage thresholds and uncertain-request reporting.
* No model call, conversation creation, cloud resource mutation, dependency
  installation, IAM change, commit or push occurred.
* Mandatory-pre-count blocker removed locally; a live function-loop result
  remains unverified. Earlier pre-count/reservation records are historical.

## A-011 - S-021 Revision 2 Meaningful Agent Identity

* Date: 2026-11-03
* Authorization: explicit Q-018 answer to change the name and delete the old
  agent; replacement creation/verification precedes deletion
* Status: completed; cloud result verified, local checks recorded below
* Target: same existing project as S-020; no subscription or IAM changes
* Created `supply-chain-resilience-advisor` version `1` using the previous
  version's exact prompt-agent definition; read-back equality verified
* Deleted only `supply-chain-readonly-847751e8dee6`, without force;
  response reported `deleted: true`, and subsequent lookup returned not-found
* Retained the historical conversation. No conversation creation, inference,
  tool dispatch, stock mutation, resource provisioning or other deletion
* Initial attempt failed before project access because Azure CLI was absent
  from the current process PATH. Verified its known installation and added
  that directory to the retry process PATH only; no global environment or
  login mutation.
* Updated the live CLI to get the explicit semantic name/version and verify
  its definition, never create random agent identities. Added a mocked CLI
  reuse regression test and updated README.
* Authorization consumed: yes. S-020 remains blocked by token-count HTTP 405;
  this naming change does not authorize an inference retry.
* Portal clarification: function specifications are server-side, Python
  implementations remain local; portal chat alone cannot execute them.
* Validation: all 56 combined Python tests passed in 2.895 seconds and all
  10 documentary/link checks passed. The new mocked CLI test initially failed
  because its conversation ID fixture was a mock rather than a string;
  corrected that fixture and reran the full Python suite successfully.

The local business milestone is completed. S-020 subsequently implemented
the SDK adapter, passed offline tests, verified the existing deployment and
created one real agent/version and conversation. The live function loop is
blocked before inference by the service's token-count HTTP 405, as recorded
in A-010. No completed real-agent comparison or trace is claimed.

## A-010 - S-020 Revision 1 Preflight Blocker

* Date: 2026-11-02
* Status: blocked before inference; not completed. The initial identity
  blocker was resolved; the latest blocker is the token-count API's HTTP 405.
* Authorization: explicit Q-015 approval of S-020 revision 1, targeting only
  Q-014's existing project and deployment, with ten model requests, twenty
  function calls, 100,000 aggregate input/output tokens and a 10 EUR ceiling
* Actual local actions: created
  [requirements-foundry.txt](../../../../src/supply-chain-resilience/requirements-foundry.txt),
  created the application-local ignored `.venv`, and installed the declared
  SDK dependencies there; no global installation or shell login change
* Installed runtime facts: `azure-ai-projects` 2.10.0, `azure-identity` 1.27.0,
  `openai` 3.38.0 on Python 3.12.10. This is not a successful live compatibility
  certification or a full dependency lock.
* Auth check: existing Azure CLI account reported enabled. No token, key,
  account dump or credential was recorded.
* Read-only project action: `AIProjectClient` with existing
  `AzureCliCredential` attempted `project.deployments.list()` against the
  exact approved endpoint. The service returned a tenant-mismatch error.
  No deployment metadata was successfully obtained.
* Outcome: stopped at the authentication blocker. No agent/version,
  conversation, inference, model deployment, IAM change, stock mutation,
  telemetry export, deletion or Git operation occurred.
* Code/tests: no Foundry adapter or new adapter tests created yet. Existing
  local business code was not changed; its previous 34-test result remains
  historical, not a new S-020 validation run.
* Pricing limitation: the public pricing page confirms deployment-type and
  model distinctions, but the directly retrieved table contains price
  placeholders. Search snippets are not sufficient evidence for this actual
  deployment's EUR rate. No safe cost estimate is certified.
* Recovery: Q-016 requests the correct existing directory/CLI context and
  explicit same-target retry. No automatic account switching or tenant
  enumeration. The local virtual environment is retained, not deleted.
* Authorization state: no further cloud action until the authentication
  blocker is resolved and continuation reconfirmed; Q-015's approved scope
  and limits do not expand.

Commands executed:

```powershell
python -m venv src\supply-chain-resilience\.venv
src\supply-chain-resilience\.venv\Scripts\python.exe -m pip install -r src\supply-chain-resilience\requirements-foundry.txt
az account show --query "{state:state}" --output json --only-show-errors
```

SDK introspection verified the installed `FunctionTool`,
`PromptAgentDefinition`, `create_version` and `get_openai_client` interfaces.
It did not create an agent. The lookup failure prevents determining the
underlying model/version, deployment type, region, actual price or quota.

### A-010 Interrupted Tenant Retry

Q-016 supplied an explicit directory identifier and authorized retrying the
same project's read-only metadata lookup. That value was passed explicitly
to `AzureCliCredential`, without modifying the global login/account state.
The ten-second credential subprocess timeout expired before metadata could
be read. A same-context retry with a sixty-second credential timeout was
interrupted. At 17:39 +01:00 the user challenged the tenant selection.

All further cloud activity stopped. A subsequent process-session check
reported no active PowerShell sessions. No successful deployment metadata,
agent/version, conversation or inference is claimed. Q-017 preserves the
dispute and requests clarification; Q-016 is not treated as continuing
authorization to retry the disputed directory.

The user subsequently confirmed the same directory value and specified the
intended account. Comparing only the cached CLI account with those inputs
returned false for both tenant and user equality, with the account enabled.
Only Boolean comparison results are retained; the personal account name is
not stored. No Foundry request or global authentication change occurred.
The active blocker is correction of the CLI user/directory context, followed
by explicit continuation within the unchanged S-020 limits.

### A-010 Corrected Preflight and Adapter Preparation

The user confirmed completing the corrected login and explicitly authorized
resuming S-020 with the same limits. Cached CLI identity equality checks then
passed, and the exact deployment lookup succeeded: `gpt-6.1-sol`,
version `2026-09-29`, publisher OpenAI, SKU `GlobalStandard`, capacity 100.
No global login state was changed by the assistant.

Added SDK adapter `supply_chain/foundry.py`, live CLI `foundry_demo.py` and
offline SDK tests `tests/foundry_adapter_tests.py` (these historical paths
were subsequently retired in S-027; current runtime checks were retained).
Pinned direct dependencies to installed Projects 2.10.0, Identity 1.27.0 and
OpenAI 3.38.0. SDK imports remain outside the business package's normal imports.

The first SDK-test run failed because the installed response model requires
`cache_write_tokens` in its usage details; the offline fixture was corrected.
Then all 21 SDK tests passed. The 34 SDK-free business/CLI tests also passed.
This is offline adapter evidence, not live function-calling success.

Direct official pricing HTML and ECB exchange-rate evidence now support
conservative model estimate rates of EUR 5 input and EUR 20 output per
million, covering both published context tiers. At 100,000 total tokens,
charging all tokens at the higher rate estimates at most EUR 2 before
account-specific billing differences, within the EUR 10 approved allowance.
See the [source evidence](../research/evidence.md#s-020-fresh-source-check-and-preflight-boundary).
This does not certify negotiated prices or an instant billing cutoff.
Creation of the one demo agent/version and conversation and the bounded
live test are next within the reconfirmed existing contract; no result is
claimed before execution.

### A-010 Live Attempt and Token-Count Blocker

The final combined offline suite passed **55 tests** in 2.954 seconds, and
`pip check` reported no broken requirements. The existing SDK-free suite
also passed independently with terminal Python. No static type checker or
Pylance diagnostics were run.

After confirming corrected-login consent, exact deployment metadata and
conservative prices, the one authorized run used the explicit project,
deployment and tenant context. The service created:

* Agent name: `supply-chain-readonly-847751e8dee6`
* Agent version: `1`
* Conversation: `conv_03047129d38afdfd00nbRimtiK1xgyUhPZ5EMSGamwMdOV8jlb`

The agent definition contains only snapshot, policy and comparison functions.
No proposal, approval or transfer-action function was registered for this slice.
The agent/version and conversation were intentionally retained, as cleanup
was excluded from the approval.

The first `responses.input_tokens.count` returned HTTP 405. The explicit-error
path stopped the run before `responses.create`. Observed counters:

| Counter | Observed value |
| ------- | -------------- |
| Generation requests | 0 |
| Function dispatches | 0 |
| Reported model input/output tokens | 0 / 0 |
| Unreconciled generation reservations | 0 |
| Application model-cost estimate | EUR 0 |

These are execution counters, not a statement from Azure billing.
No stock mutation or model/tool result occurred. Temporary local stores were
removed by their owning context manager. No default demo database was reset.
No retries or additional agents/conversations were started after this error.

The installed client exposes token counting, but that does not prove service
support on this project's route. Do not disable the guard or quietly replace
it with a token guess. Live inference, real call-ID continuation and final
business-answer acceptance remain unverified.

Authorization is suspended at this compatibility error; resource deletion,
duplicate creation and another live attempt are not automatically authorized.
The proposed next activity is a bounded compatibility correction for counting
tokens and resuming the existing agent/conversation, with a revised contract
if the enforcement approach changes. It has not started.

Final documentary validation: all 10
`node --test scripts\test-copilot-customizations.mjs` checks passed,
including metadata, local links and anchors. S-020 remains blocked despite
the passing local checks; no successful live function loop is claimed.

## A-009 - S-019 Revision 2

* Authorization: the user's explicit 2026-11-02 16:59 +01:00 implementation
  request after the Q-013 pause and clarification. The
  [question history](../questions.md#q-013-clarification-followed-by-implementation-consent)
  records the actual scope; the earlier paused form is not consent.
* Organization constraint: at 17:06 +01:00 the user requested well-organized
  code from the outset without overengineering (faithful English translation).
  This refined the authorized local implementation, not its cloud boundary.
* Status: completed; runtime and documentary criteria verified.
* Runtime: terminal Python 3.12.10 and SQLite 3.49.1. No dependency installation,
  environment change or editor-interpreter claim.
* Authorization consumed: yes. No subsequent implementation or cloud activity
  is authorized by this completed increment.

### Actual Files and Organization

The [application directory](../../../../src/supply-chain-resilience) contains
one small package and a manual CLI adapter. A future SDK driver is deliberately
not implemented. Package responsibilities are:

| File | Implemented responsibility |
| ---- | -------------------------- |
| [domain.py](../../../../src/supply-chain-resilience/supply_chain/domain.py) | Synthetic snapshot, local actor fixtures, shared feasibility/cost/margin rules |
| [store.py](../../../../src/supply-chain-resilience/supply_chain/store.py) | SQLite schema, transactions, exact-proposal approval, durable request and reservation |
| [tools.py](../../../../src/supply-chain-resilience/supply_chain/agents/resilience_advisor/tools.py) | Six strict JSON function specifications and explicit-error dispatcher |
| [package exports](../../../../src/supply-chain-resilience/supply_chain/__init__.py) | Stable entry points shared by callers |
| [demo.py](../../../../src/supply-chain-resilience/demo.py) | Thin manual CLI; demo role selection is not authentication |
| [domain tests](../../../../src/supply-chain-resilience/tests/test_domain.py) | Pure scenario arithmetic and fixture validation |
| [workflow tests](../../../../src/supply-chain-resilience/tests/test_workflow.py) | Approval, persistence, dispatch, concurrent/failed/repeated requests and CLI |
| [test package](../../../../src/supply-chain-resilience/tests/__init__.py) | Root-level standard-library test discovery |
| [README](../../../../src/supply-chain-resilience/README.md) | Tested commands, synthetic scenario, boundaries and future function-calling exposure |
| [local ignore rules](../../../../src/supply-chain-resilience/.gitignore) | Exclude local SQLite files and journals |

The initial single module was split without changing tool names, argument
contracts, CLI commands or scenario values. No HTTP/MCP server, framework,
repository interface, container, workflow engine or production identity layer
was added. Business calculations are shared by comparison and write checks.
The dispatcher returns explicit errors for corrupt stored outcomes rather
than reporting success or silently substituting data.
Related state, question history, analysis and plan version 2 were updated.

### Commands and Observed Results

From the repository root:

```powershell
python -B -m unittest discover -s src\supply-chain-resilience -p "test_*.py" -v
```

Final runtime run: **34 tests passed in 4.095 seconds**, exit code 0.
Earlier runs passed 32 tests before the module split and 33 afterwards;
the final run includes the durable subprocess CLI walkthrough.

Verified acceptance:

* Exact transfer quantity 40, STANDARD 90 and EXPRESS 95, ceiling equality
  and schedule margins 0/1 versus 1/2.
* No-impact, unavailable stock, missing policy and infeasible budget outcomes.
  No invented policy defaults or automatic option selection.
* Strict model arguments; caller-owned actor context; no approval tool.
  Missing, stale, changed or mismatched approval prevents execution.
* Approval/proposal creation does not reserve stock. One successful request
  leaves source on-hand/reserved/available at 80/70/10 and W-A at 20.
* Twelve concurrent requests for the same proposal produce one durable
  request and eleven idempotent repeats. Stock is reserved once.
* Failed request insertion rolls back the reservation. Corrupt stored JSON
  and invalid recorded outcomes return explicit errors, not successful fallbacks.
* Independent CLI processes initialize a temporary database, compare both
  costs, propose, reject execution before approval, require explicit approval
  confirmation, execute, repeat idempotently and retrieve the persistent result.
  A subsequent comparison reports the existing pending transfer.
* Initialization cannot overwrite an existing store; missing stores are not
  silently created on read. Temporary test databases are cleaned by the tests.

Repository documentary/link validation:

```powershell
node --test scripts\test-copilot-customizations.mjs
```

All **10 tests passed**, exit code 0, including Markdown metadata, local links
and anchors. Python imports and execution were exercised; no static type
checker or Pylance diagnostics were run.

### Limitations and Next Point

This is a reusable local business-tool increment, **not a live Foundry demo**.
The JSON definitions have not been instantiated with or validated against a
Foundry SDK. No live function call IDs, conversation continuation, model-loop
limits, real authentication, traces or cloud evaluation have been verified.
Role fixtures and fingerprints are not real IAM or tamper-resistant credentials.
No default demonstration database, Azure resource, API/MCP endpoint, Git commit
or push was created.

One proposed next activity: S-020 revision 1, connect these same functions to
the real managed Foundry prompt agent, after explicitly agreeing the target,
model, permissions and bounded call budget. Status: proposed; its operational
contract is not approved and it is not started. Provisioning, IAM changes
and cleanup remain outside the proposal.
