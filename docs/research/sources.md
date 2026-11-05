---
title: Source register
description: Public sources consulted and evidence limitations for the multi-agent lab.
ms.date: 2026-11-02
status: research-baseline
---

## Conversational human handoff research

Consulted on 2026-11-04 for S-040. This is documentary and installed-source
evidence, not a native handoff execution or a new managed-agent publication.

### CK10

* Source: [Agent Framework AG-UI human-in-the-loop](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/human-in-the-loop),
  Python sections on approval mode, interrupts and resume.
* Evidence: function approval supports `approval_mode="always_require"`;
  an approval interrupt is a waiting outcome, not application completion.
  Canonical resume carries the interrupt identity and decision without a
  fabricated user sentence.
* Limit: a Boolean tool approval does not collect an enum preference.
  Installed AG-UI 1.7.1 defaults to a process-local approval store; its
  source explicitly says it is not durable across restarts/replicas.
  Neither the tutorial nor an in-memory adapter proves our persisted
  managed-agent integration.

### CK11

* Source: [Agent Framework frontend tools](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/frontend-tools)
  and installed `agent-framework-core` 1.24.0 / `agent-framework-ag-ui` 1.7.1.
* Evidence: frontend tools return matching function results. Installed core
  accepts declaration-only `FunctionTool(func=None)` and pauses for caller
  input; the AG-UI converter uses exactly that representation. Unknown tools
  can remain fatal: allowed declaration-only calls are classified separately.
* Limit: generic tutorials do not establish dynamic tool-schema support for
  a published Foundry `agent_reference`. An application must validate incoming
  results and retain authoritative pending-call identity.

### CK12

* Source: [CopilotKit useHumanInTheLoop](https://docs.copilotkit.ai/reference/hooks/useHumanInTheLoop);
  installed react-core/core 1.82.0 v2 declarations and published source maps.
* Evidence: the hook builds on `useFrontendTool`, awaits a human `respond`
  result, and has cancellation handling. Installed core's run handler
  processes frontend handlers and schedules a follow-up when appropriate.
  This requires the core run path, not a direct bare `agent.runAgent` call.
* Identity: installed core can reuse a logical run ID for follow-ups. The
  application's current run-ID-only replay guard cannot simply be retained
  unchanged or removed; native call/phase identity must also be checked.
* Limit: hook availability and inspected continuation code are not an
  executed proof for this custom transport, final-validation latch or
  same-origin/persistence boundaries. Do not mix the v1 and v2 hook exports.

### CK13

* Source: [Foundry prompt-agent quickstart](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent)
  and installed `agent-framework-foundry` 1.16.0 managed-agent implementation.
* Evidence: the managed agent owns its definition. Installed client removes
  request `tools`, `tool_choice` and parallel-tool control when targeting an
  agent reference. Local function declarations supply dispatch/pause behavior,
  not additional schemas to that published agent.
* Consequence: two new human-request tools and changed instructions require
  a new version of the existing advisor before real use. Retain version 3
  and historical conversations; do not infer the next available version
  number or publish anything under the analysis authorization.
* Limit: package source inspection, not a new authenticated project query
  or a tenant confirmation that the proposed definition runs.

## CopilotKit complete integration analysis

Consulted on 2026-11-04 for S-037 revision 1. These are public sources,
not executed integration evidence. The
[project analysis](../../.copilot-tracking/projects/supply-chain-resilience/research/analysis.md#s-037-copilotkit-integration-analysis)
maps them to the actual guarded backend.

### CK01

* Source: [Microsoft Agent Framework AG-UI integration](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/),
  section "Build agent UIs with CopilotKit"
* Evidence: Microsoft explicitly presents CopilotKit for agent UI over
  AG-UI, with streaming, tool rendering and human interaction.
* Limit: not a Microsoft support commitment for CopilotKit, proof of our
  custom endpoint's compatibility or permission to replace application guards.

### CK02

* Sources: [Open source vs Intelligence](https://docs.copilotkit.ai/concepts/oss-vs-enterprise),
  [published react-core license](https://cdn.jsdelivr.net/npm/@copilotkit/react-core@1.84.1/LICENSE)
* Evidence: open-source SDKs and TypeScript runtime use MIT; core chat,
  AG-UI integration and application-owned persistence need no CopilotKit
  hosted service. Intelligence adds separately governed services.
* Limit: MIT does not make all branded/hosted features free or eliminate
  transitive license notices, install analytics or network-default checks.
  Published license text was inspected, not copied into project tracking.

### CK03

* Sources: [Self-managed agents](https://docs.copilotkit.ai/ag2/backend/self-managed-agents),
  [provider source](https://github.com/CopilotKit/CopilotKit/blob/main/packages/react-core/src/v2/providers/CopilotKitProvider.tsx),
  [runtime languages](https://docs.copilotkit.ai/backend/copilot-runtime)
* Evidence: direct `agents__unsafe_dev_only` is documented for local
  development. `selfManagedAgents` is labeled an Intelligence-tier route.
  The provider source exposes both and makes the distinction explicit.
  TypeScript is the runtime path documented to work without Intelligence;
  other Copilot Runtime language implementations have different requirements.
* Limit: source on `main` is mutable, not an installed version guarantee.
  Do not bypass licensing checks or present dev-only setup as production.
  The existing Python Agent Framework server is not a Copilot Runtime.

### CK04

* Sources: [react-core 1.84.1 manifest](https://cdn.jsdelivr.net/npm/@copilotkit/react-core@1.84.1/package.json),
  [core 1.84.1 manifest](https://cdn.jsdelivr.net/npm/@copilotkit/core@1.84.1/package.json),
  [matching repository manifest](https://github.com/CopilotKit/CopilotKit/blob/main/packages/react-core/package.json)
* Evidence: react-core 1.84.1 exports `/v2`, `/v2/headless` and
  `/v2/styles.css`; depends on AG-UI client/core 1.0.2. React peers
  include 18/19, Zod is `>=3.25`, and maplibre is optional.
  Core requires Node `>=20`. The manifest includes `@scarf/scarf`.
* Limit: versioned CDN package metadata, not a successful local install,
  resolved lockfile, bundle-size measurement or general support matrix.
  Public npm registry reads failed TLS with PowerShell and curl; no
  certificate bypass or registry configuration change was attempted.

### CK05

* Sources: [AG-UI client 1.0.2 manifest](https://cdn.jsdelivr.net/npm/@ag-ui/client@1.0.2/package.json),
  [published declarations](https://cdn.jsdelivr.net/npm/@ag-ui/client@1.0.2/dist/index.d.ts),
  [HttpAgent](https://docs.ag-ui.com/sdk/js/client/http-agent),
  [AbstractAgent](https://docs.ag-ui.com/sdk/js/client/abstract-agent),
  [subscriber](https://docs.ag-ui.com/sdk/js/client/subscriber)
* Evidence: client 1.0.2 declares protocol 1.0; public APIs include custom
  headers, `requestInit`, `abortRun`, `clone`, initial messages and custom/
  terminal event subscriptions. `onRunFinalized` fires after failures too.
* Limit: JS 1.0.2 versus installed Python protocol 0.1.22 is a wire-test
  requirement, not proof either of incompatibility or of compatibility.
  No JS parser or CopilotKit package was executed in S-037.

### CK06

* Sources: [v2 reference](https://docs.copilotkit.ai/reference/v2),
  [CopilotChat](https://docs.copilotkit.ai/reference/components/CopilotChat),
  [CopilotChatView](https://docs.copilotkit.ai/reference/components/CopilotChatView),
  [message view](https://docs.copilotkit.ai/reference/components/CopilotChatMessageView),
  [chat source](https://github.com/CopilotKit/CopilotKit/blob/main/packages/react-core/src/v2/components/chat/CopilotChat.tsx)
* Evidence: v2 provides reusable styled chat/view/input/message components
  and slots. High-level chat documents an initial automatic run and manages
  connection/suggestion behavior; the view can be composed independently.
* Limit: mutable docs/source and v1/v2 examples must not be mixed.
  Disable or avoid automatic operations and verify zero model requests on
  mount/reload/case switching in the selected published package.

### CK07

* Sources: [Hook selection](https://docs.copilotkit.ai/concepts/which-hook),
  [useRenderTool](https://docs.copilotkit.ai/reference/hooks/useRenderTool),
  [useHumanInTheLoop](https://docs.copilotkit.ai/reference/hooks/useHumanInTheLoop)
* Evidence: render-only hooks do not register client tool handlers.
  `useHumanInTheLoop` builds on a frontend tool and supplies a response
  callback; it is not an automatic binding to this project's action routes.
* Limit: no model-callable approval tool may be introduced implicitly.
  Rendered function completion alone is not application final validation.

### CK08

* Sources: [useAgent](https://docs.copilotkit.ai/reference/hooks/useAgent),
  [HttpAgent source](https://github.com/ag-ui-protocol/ag-ui/blob/main/sdks/typescript/packages/client/src/agent/http.ts),
  [CopilotKit Microsoft integration](https://docs.copilotkit.ai/microsoft-agent-framework)
* Evidence: agent instances hold messages/state; readiness, event
  subscriptions and case/thread isolation need explicit lifecycle handling.
  The Microsoft integration URL currently redirects to a .NET-labeled
  landing page that also describes Python AG-UI services.
* Limit: a redirected .NET starter is not authority to replace the proven
  Python agent, add another model provider/key or adopt a hosted service.

## CopilotKit local compatibility follow-up

Consulted/executed on 2026-11-04 for S-038 revision 1. This supplements,
not overwrites, the S-037 documentary candidate findings.

### CK09

* Source: configured npm feed metadata and installed
  `@copilotkit/react-core` 1.82.0, `@copilotkit/core` 1.82.0,
  `@ag-ui/client`/core 1.0.2; exact lockfile and package declarations.
* Evidence: 1.84.1 returned 404 in the configured feed; direct public npm
  returned TLS handshake failure. Stable 1.82.0 was available with the
  expected v2 exports, MIT license, React 18/19 peers and AG-UI JS 1.0.2.
  Selected that final pin explicitly, without registry/certificate changes.
* Execution: actual SDK/Python SSE compatibility, contextual human actions,
  full-history projection, terminal validation, cancellation and browser
  lifecycle were tested with synthetic upstream responses.
  See [A-025](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-025---s-038-local-copilotkit-compatibility-slice).
* Concrete SDK finding: exceptions from lifecycle subscriber callbacks
  need not reject the run promise. The client latches validation failures
  and checks them after the run instead of relying on callback exceptions.
* Packaging: install used `--ignore-scripts --no-audit --no-fund`;
  Scarf and all other dependency install scripts did not execute.
  Browser test paths observed no external requests. Vite emitted large
  chunks; these are not a measured optimized production bundle.
* Limit: no live Foundry streaming/export, full-interface activation,
  exhaustive egress/license/security/accessibility audit or production
  certification. The test-only preview is not a Copilot Runtime.

## Reading rules

Baseline entries have the consultation date **2026-11-02**.
Follow-up entries specify their own consultation dates. `updated_at`
indicates the page's editorial date, not the feature release.
"Not established" means that no GA/preview status is assigned without
specific evidence. Learn sources are product documentation; S09 is
an application-pattern blog. The limitations of this research are in the
[method](method.md).

## Learning Extension Research

This supplement records public sources checked on 2026-11-04 for possible
learning increments. It does not change the S01-S33 historical baseline or
approve a knowledge backend, new resources or runtime changes.

### LE01 - Foundry File Search

* Source: [File search tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search)
* Retrieved: 2026-11-04; page updated 2026-10-23.
* Evidence: document upload, vector-store ingestion and grounded queries are
  documented for the current agent generation. Additional charges apply.
  The current Python page describes a toolbox-based attachment path.
* Limitation: this lab's exact managed-version/Agent Framework/AG-UI path,
  citation projection, project prerequisites and actual availability have not
  been verified. This is a candidate, not an installed capability.

### LE02 - Azure AI Search Agent Tool

* Source: [Connect an Azure AI Search index](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search)
* Retrieved: 2026-11-04; page updated 2026-10-21.
* Evidence: indexed retrieval and inline citations, vector-index prerequisites
  and connection identity choices are documented. Private-network use requires
  the documented managed-identity path, not key authentication.
* Limitation: no project/index/connection, IAM or region inspection was
  performed. Do not select or provision this backend merely for a few demo files.

### LE03 - Agent Evaluators

* Source: [Agent evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators)
* Retrieved: 2026-11-04; page updated 2026-10-08.
* Evidence: evaluate system outcome and process, including tool use, not only
  final prose. Individual evaluators have distinct maturity and input contracts;
  for example Task Completion and Customer Satisfaction are marked preview.
* Limitation: no cloud evaluation was run. Existing local acceptance rubrics
  and deterministic tests are not measured model-quality scores.

### LE04 - Delegated Tool Identity and OBO

* Sources: [Foundry user delegation](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/user-delegation),
  [tool authentication](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-authentication),
  [Microsoft identity platform OBO](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow)
* Retrieved: 2026-11-04. Foundry delegation page updated 2026-10-23;
  authentication page updated 2026-10-29.
* Evidence: user delegation is distinct from app-only agent/project identity.
  Tokens are resource-audience specific. Foundry-as-actor delegation supports
  a limited set of Microsoft-owned tools, not arbitrary custom servers.
  Agent-identity-as-actor delegation and its blueprint audience have preview
  constraints. In-conversation OAuth requires actual client sign-in handling.
* Limitation: connection auth modes are not interchangeable. No current
  lab SDK/channel/consent path or multi-user runtime has been verified.

### LE05 - SharePoint Knowledge with User Permissions

* Source: [SharePoint agent tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/sharepoint)
* Retrieved: 2026-11-04; page updated 2026-10-21.
* Evidence: tool is explicitly preview; retrieves accessible documents with
  delegated identity/OBO, not app-only credentials. Same tenant for site
  and project, user access, one SharePoint tool per agent, and eligible
  Microsoft 365 Copilot licensing or configured pay-as-you-go are prerequisites.
* Limitation: neither site/license/user availability nor exact browser/
  Agent Framework/AG-UI integration is established for this lab.

### LE06 - Document ACLs and Data RLS

* Sources: [Azure AI Search document access](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview),
  [SQL row-level security](https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security?view=azuresqldb-current)
* Retrieved: 2026-11-04; search overview updated 2026-09-17.
* Evidence: security-string filters are application-enforced and API-agnostic;
  documented native document ACL/RBAC/sensitivity-label integrations are
  preview with source/API constraints. SQL RLS uses database security policies
  and predicates, not an instruction to the model.
* Limitation: OBO alone does not create per-document or row authorization.
  Copying content to an index does not prove original permission preservation.
  Shared-identity application filtering is not genuine downstream user OBO.

### LE07 - Azure SQL End-User Authentication and OBO

* Sources:
  [Azure SQL Entra authentication](https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-overview?view=azuresql),
  [OBO quickstart with Data API builder](https://learn.microsoft.com/en-us/azure/data-api-builder/quickstart/authentication-on-behalf-of)
* Retrieved: 2026-11-04. SQL authentication page updated 2026-10-19;
  OBO quickstart updated 2026-06-04.
* Evidence: SQL principals can map to Entra users/groups. The OBO example
  uses Azure SQL delegated user_impersonation permission, consent, contained
  users, and a WhoAmI/SUSER_NAME check to prove the actual caller reaches SQL.
  It explicitly contrasts end-user OBO with RLS under a shared service identity.
* Limitation: this verifies the architectural distinction, not a proven
  Python SQL driver/token path in this lab. DAB and the sample infrastructure
  are not selected, installed, cloned or provisioned. No SQL resource,
  permissions, Entra registration or driver prerequisites were inspected.

### LE08 - SharePoint Site Provisioning

* Source:
  [Create modern SharePoint sites using REST](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest)
* Retrieved: 2026-11-04. Page updated 2025-01-16.
* Evidence: SPSiteManager supports creation/status of communication sites
  and non-group-associated team sites. A delegated caller is the default
  owner when no Owner is specified. New site existence/readiness must be
  checked; a returned provisioning state is not a usable-site guarantee.
* Limitation: this is API documentation, not proof of tenant permission,
  current authentication, secure default ACLs or supported WorkIQ actions.
  No creation or deletion example was executed.

### LE09 - SharePoint Folder and Permission REST Operations

* Sources:
  [Custom permissions with REST](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/set-custom-permissions-on-a-list-by-using-the-rest-interface),
  [Folders and files with REST](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest)
* Retrieved: 2026-11-04. Both pages updated 2026-10-28.
* Evidence: folder list items, permission inheritance, role definitions and
  assignments can be inspected/changed through SharePoint REST. File content
  reads are separate from list metadata. Folder/item ACLs must be checked
  after changes rather than inferred from group names or successful writes.
* Lab evidence: S-046 applies these operations only to the new approved
  site, with an authenticated owner browser session and no add-in deployment.
* Limitation: older samples include add-in context; no retired add-in
  authentication pattern is adopted. API success does not prove end-user
  trimming, indexing or Foundry delegation. Those tests remain separate.

### LE10 - Entra Test User Provisioning

* Sources:
  [Graph user create](https://learn.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0),
  [Entra user creation prerequisites](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users),
  [verifiedDomain schema](https://learn.microsoft.com/en-us/graph/api/resources/verifieddomain?view=graph-rest-1.0)
* Retrieved: 2026-11-04. Pages updated 2026-07-04, 2026-06-15 and
  2024-11-21, respectively.
* Evidence: user create requires the intended enabled state, display name,
  mail nickname, password profile and a verified UPN domain. Appropriate
  Graph permission and operator authority are separate prerequisites;
  Entra guidance specifies User Administrator as the least-privileged
  administrator role for this task.
* Schema distinction: organization.verifiedDomains already represents
  verified domains; its verifiedDomain objects do not have isVerified.
* Lab evidence: S-047 checks target/domain/absence but first create returns
  403. Current operator's directory-role read reports Global Reader only.
  No role activation, consent, user creation or license assignment followed.
* Limitation: this does not establish eligible PIM roles or prove the Graph
  client has the required delegated write scope. Those cannot be inferred
  from SharePoint ownership or successful directory reads.

## S01

* Source: [What is Microsoft Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)
* Evidence: "Choose how to build", "Agent types", runtime, Toolbox, and integrations
* Use: taxonomy of prompt, voice-based prompt, hosted, and external Responses paths
* Limitation: the overview does not prove availability or maturity of every component

## S02

* Source: [Quickstart: Create a prompt agent](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent)
* Evidence: "Install packages and authenticate", "Create a prompt agent", "Chat with the agent"
* Metadata: `ms.date` 2026-10-26; `updated_at` 2026-10-28
* Use: Projects 2.x, agent versions, Conversations/Responses; Python >= 2.3.0 for the Projects package in the quickstart
* Limitation: quickstart requirements, not a universal minimum for every API

## S03

* Source: [Hosted agents in Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents)
* Evidence: "How it works", "Agent identity and endpoint", "Versioning", "Scaling and right-sizing", "Limits, pricing, and availability"
* Use: containers, per-session sandboxes, dedicated identity, protocols, persistent state, CPU/memory billing
* Limitation: overall GA status not established; A2A v1.0 GA and v0.3 preview are protocol labels on the page
* Note: endpoint targets one version at a time; no native traffic splitting described

## S04

* Source: [Quickstart: Deploy your first hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
* Evidence: "Prerequisites" and azd, Python, C#, VS Code paths
* Metadata: `ms.date` 2026-10-26; `updated_at` 2026-10-29
* Use: Python 3.13+, Projects >= 2.3.0; C# .NET 10 and Projects 2.1.0-beta.4 for source deployment
* Limitation: the .NET source deployment API requires a prerelease; do not extend the requirement to every .NET client

## S05

* Source: [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
* Evidence: agents, harnesses, workflows, and integrations; language tabs
* Metadata: `ms.date` 2026-10-23; `updated_at` 2026-10-28
* Use: framework distinct from the Foundry service; .NET, Python, and Go
* Limitation: Go is in public preview; feature parity across languages is not guaranteed

## S06

* Source: [Workflow concepts](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/)
* Evidence: "Workflow APIs", "Graph and runtime model", "Advanced execution"
* Metadata: `ms.date` 2026-10-22; `updated_at` 2026-10-28
* Use: graphs, executors, events, checkpoints, and experimental Python functional API
* Limitation: the framework does not automatically choose storage and external side-effect semantics

## S07

* Source: [Workflow orchestrations in Agent Framework](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/)
* Evidence: sequential, concurrent, handoff, group chat, magentic table, and HITL note
* Metadata: `ms.date` 2026-02-12; `updated_at` 2026-08-25
* Use: available patterns and support for tool approval/request info
* Limitation: support for a pattern does not imply suitability for your use case

## S08

* Source: [Build a workflow in Microsoft Foundry (Preview)](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow)
* Evidence: opening retirement notice for 2026-12-01 and Agent Framework recommendation
* Metadata: `ms.date` 2026-07-31; `updated_at` 2026-10-19
* Use: avoid new investment in the Foundry visual workflow builder
* Limitation: this is not the retirement of Microsoft Agent Framework workflows

## S09

* Source: [Designing Least-Privilege Tool Access for AI Agents with Microsoft Foundry](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/designing-least-privilege-tool-access-for-ai-agents-with-microsoft-foundry/4567029)
* Type: Microsoft Tech Community, author Abhishek Kumar; detected modification 2026-10-23
* Evidence: capability contract, identity choice, server-side binding, deny paths
* Use: least-privilege patterns and application controls complementary to RBAC
* Limitation: custom example classes, not Foundry APIs; not a GA announcement

## S10

* Source: [Role-based access control for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)
* Evidence: roles and scopes, role renaming, Foundry Agent Consumer
* Metadata: `ms.date` 2026-09-16; `updated_at` 2026-10-30
* Use: separate administration, development, and invocation
* Limitation: Agent scope is currently evaluated for access to the agent endpoint, not for every downstream operation

## S11

* Source: [Toolbox authentication in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-authentication)
* Evidence: `auth-type` table, `oauth2` / `user-entra-token` distinction
* Metadata: `ms.date` 2026-08-19; `updated_at` 2026-10-29
* Use: connections with keys, OAuth, Entra user tokens, project or agent identity
* Limitation: support depends on the tool; not all combinations are interchangeable

## S12

* Source: [Connect agents to MCP server endpoints](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
* Evidence: authentication, MCP approvals, endpoints, and private connections
* Metadata: `ms.date` 2026-10-28; `updated_at` 2026-10-29
* Use: Foundry MCP integration, OAuth consent, and network constraints
* Limitation: OAuth consent does not replace approval of a business action

## S13

* Source: [Create and manage a toolbox in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/toolbox)
* Evidence: prerequisites, tool configuration, hosted integration, and Toolbox versions
* Metadata: `ms.date` 2026-10-26; `updated_at` 2026-10-29
* Use: managed MCP endpoint; `FoundryToolbox` Python / `AddFoundryToolboxes` .NET
* Limitation: tools, models, and regions have specific compatibility requirements; .NET examples require a consistent 2.1.0-beta.4 set

## S14

* Source: [Guardrails and controls overview](https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview)
* Evidence: intervention points, model/agent applicability matrix
* Use: preview agent guardrails, controls on input/tool call/tool response/output
* Limitation: tool call/tool response and egress control are preview; egress is cited for hosted agents; not uniformly applicable to external agents

## S15

* Source: [Networking options for Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options)
* Evidence: public egress, BYO VNet, and managed VNet; ingress/egress separation
* Metadata: `ms.date` 2026-06-29; `updated_at` 2026-09-09
* Use: no implicit network privacy; an inbound private endpoint does not isolate egress
* Limitation: compatibility must be checked for the specific runtime, tool, and project

## S16

* Source: [Data, privacy, and security for Foundry Models sold by Azure](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy)
* Evidence: data use and handling of stateful features
* Metadata: `ms.date` retrieved as 2026-05-18
* Use: data not used to train foundation models without permission
* Limitation: does not imply zero retention, absence of abuse monitoring, or a guarantee for third-party tools

## S17

* Source: [Responsible AI for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/responsible-use-of-ai-overview)
* Evidence: responsibilities, risk assessment, and issue reporting
* Metadata: `ms.date` 2026-07-21; `updated_at` 2026-08-25
* Use: lifecycle-wide RAI approach, not only content filtering
* Limitation: not a certification of the solution built by the customer

## S18

* Source: [Add client-side tracing to Foundry agents](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-client-side?tabs=python%2Ccustom-attributes-python)
* Evidence: GenAI tracing, content recording, trace propagation, "Security and privacy"
* Metadata: `ms.date` 2026-09-03; `updated_at` 2026-10-21
* Use: OTel, Application Insights/OTLP, experimental opt-in, Python Projects >= 2.0.0
* Limitation: GenAI instrumentation is experimental preview; not every hop is automatically correlated

## S19

* Source: [Monitor agents with the Agent Monitoring Dashboard](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard?tabs=python)
* Evidence: metrics, "Configure settings", continuous/scheduled evaluation
* Metadata: `ms.date` 2026-09-25; `updated_at` 2026-09-30
* Use: data from linked Application Insights; metric views, recurring evaluation, red team scans, and alerts marked preview
* Limitation: 10 seconds and 95% are diagnostic guidance in the text, not SLAs or universal gates

## S20

* Source: [Agent Framework observability](https://learn.microsoft.com/en-us/agent-framework/agents/observability)
* Evidence: OTel GenAI semantic conventions, exporters, and sensitive-data warnings
* Metadata: `ms.date` 2026-10-23; `updated_at` 2026-11-01
* Use: tracing, metrics, and logs in framework code; watch for duplicate spans
* Limitation: examples with sensitive-data capture enabled are not defaults to copy into production

## S21

* Source: [Agent evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators)
* Evidence: system/process evaluators, inputs and outputs, composite evaluator
* Metadata: `ms.date` 2026-09-30; `updated_at` 2026-10-08
* Use: task completion/adherence, intent resolution, tool selection/input/success, and other metrics
* Limitation: maturity varies by evaluator; Quality Grader deprecated; do not flatten all outputs to a single scale

## S22

* Source: [Use datasets for cloud evaluation](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/cloud-evaluation-datasets)
* Evidence: JSONL/CSV upload, versioned datasets, and reuse in CI/CD
* Metadata: `ms.date` 2026-08-26; `updated_at` 2026-09-07
* Use: repeatable, versioned datasets, separate from evaluation runs
* Limitation: a versioned dataset is not necessarily representative or free of PII

## S23

* Source: [Evaluation overview](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-overview)
* Evidence: evaluation during development, CI/CD, and production traffic
* Metadata: `ms.date` 2026-10-14; `updated_at` 2026-10-17
* Use: connect offline and recurring evaluations throughout the lifecycle
* Limitation: choose the SDK path corresponding to Foundry new

## S24

* Source: [Evaluate agents with GitHub Actions](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-github-action)
* Evidence: `microsoft/ai-agent-evals` integration, reports, and statistical comparisons
* Metadata: `updated_at` retrieved as 2026-05-18
* Use: possible CI integration, not an already selected or implemented pipeline
* Limitation: verify compatibility with the new generation and authentication before adoption

## S25

* Source: [Evaluate agents with Azure DevOps](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-azure-devops)
* Evidence: Microsoft extension for offline evaluation in pipelines
* Metadata: `updated_at` retrieved as 2026-05-18
* Use: alternative to GitHub Actions
* Limitation: the lab does not need to adopt both platforms

## S26

* Source: [AI Red Teaming Agent](https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent)
* Evidence: PyRIT, adversarial scans, Attack Success Rate
* Metadata: `updated_at` retrieved as 2026-08-27
* Use: systematic risk testing and comparison over time
* Limitation: a scan does not prove the absence of vulnerabilities or harm

## S27

* Source: [Run AI red teaming in the cloud](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-ai-red-teaming-cloud)
* Evidence: cloud runs and scheduling of post-deployment scans
* Metadata: `ms.date` 2026-09-03; `updated_at` 2026-09-11
* Use: possible periodic suite in the lab
* Limitation: region, roles, costs, and target support must be verified

## S28

* Source: [Evaluation regions, limits, and virtual network support](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-regions-limits-virtual-network)
* Evidence: evaluation regions and limits, rate limits, and `retry-after`
* Metadata: `updated_at` retrieved as 2026-08-18
* Use: check compatibility and size batches and scans
* Limitation: do not reuse evaluation limits as inference quotas

## S29

* Source: [Plan and manage costs for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/manage-costs)
* Evidence: costs by model, deployment, meter, and connected services
* Use: total cost scope and spend monitoring
* Limitation: does not provide an estimate applicable to the tenant or all demo services

## S30

* Source: [Manage quota](https://learn.microsoft.com/en-us/azure/foundry/how-to/quota)
* Evidence: quota by model/region/subscription, shared quota, and deployments
* Metadata: `ms.date` 2026-07-28; `updated_at` 2026-08-13
* Use: distinguish model availability, quota, and actual capacity
* Limitation: shared quota is for temporary testing, not a production foundation

## S31

* Source: [Use the Microsoft Copilot harness with prompt agents](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/use-tools-skills-copilot-harness)
* Evidence: optional managed harness, prerequisites, and initial limitations
* Metadata: `ms.date` and `updated_at` 2026-10-29
* Use: prompt agents with managed runtime for tools/skills/files/commands; explicit preview
* Limitation: selected at creation, cannot be switched on an existing agent in the initial public preview; BYOM not supported

## S32

* Source: [Agent optimizer overview](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-optimizer-overview)
* Evidence: "Supported agent types", prompt and hosted agents, tool optimization limits
* Metadata: `ms.date` 2026-10-26; `updated_at` 2026-10-28
* Use: configuration/evaluation-driven improvement; preview indicated by overview S01
* Limitation: the portal prompt path excludes Copilot harness; improving tool descriptions does not prove execution correctness

## S33

* Source: [Build agents using the Responses API](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/responses-api)
* Evidence: ephemeral agent, project endpoint vs Azure OpenAI endpoint
* Metadata: `ms.date` 2026-10-26; `updated_at` 2026-10-28
* Use: definition in external code without a persisted agent resource
* Limitation: ephemeral pattern without Copilot harness selection or prompt-agent optimizer

## Prompt-agent definition follow-up

* Source: [Prompt agents in Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/prompt-agents)
* Consulted: 2026-11-03
* Evidence: saved definition contains model, instructions and tools; saving
  changes creates a new version; default runtime versus optional harness
* Use: separate the managed agent definition from client-side function execution
* Limitation: generic managed-tool orchestration does not imply execution of
  local Python functions; no harness migration or version-pinned route was tested

## Prompt lifecycle training follow-up

* Sources: [Manage prompts with GitHub](https://learn.microsoft.com/en-us/training/modules/prompt-versioning-genaiops/),
  [agent and prompt versioning](https://learn.microsoft.com/en-us/training/modules/prompt-versioning-genaiops/3-foundry-agents-prompt-versioning),
  [repository structure](https://learn.microsoft.com/en-us/training/modules/prompt-versioning-genaiops/4-github-repository-structure),
  [safe deployment workflow](https://learn.microsoft.com/en-us/training/modules/prompt-versioning-genaiops/5-prompt-workflow-development)
* Consulted: 2026-11-03
* Type: Microsoft Learn training, not the current SDK API contract
* Evidence: prompts as versioned assets; separate text/Markdown files;
  configuration metadata; development, validation, review and release stages
* Use: lightweight prompt-as-code practice and baseline/candidate comparison
* Limitation: the versioning unit contains `from_connection_string` and
  `create_agent` examples, not the current Projects 2.x `create_version` path.
  Adopt the lifecycle guidance, not those API snippets. File formats and
  numbered-file layouts are examples, not platform requirements.

## Evaluation targets follow-up

* Source: [Evaluate models and agents with the Foundry SDK](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/cloud-evaluation-targets)
* Consulted: 2026-11-03, alongside fresh checks of S02, S23 and S32
* Evidence: model/agent targets and runtime generation for evaluation
* Use: distinguish generated-response evaluation from deterministic tests
* Limitation: an agent-target evaluation does not prove execution of the
  application's local function dispatcher. S32 explicitly says prompt-agent
  function tools execute client-side and tool-description optimization cannot
  evaluate tool execution. No evaluation or optimizer job was launched.

## AG-UI integration follow-up

* Consulted: 2026-11-03
* Sources:
  [AG-UI integration with Agent Framework](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/),
  [getting started](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/getting-started),
  [backend tool rendering](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/backend-tool-rendering),
  [human-in-the-loop](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/human-in-the-loop),
  [security considerations](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/security-considerations)
* Evidence: Microsoft describes AG-UI as a standardized UI protocol using
  HTTP/SSE for streaming, tool events, state and human interaction. The
  overview explicitly compares direct agent use with AG-UI and says to
  consider AG-UI for relevant UI requirements, not for every application.
  CopilotKit is linked as an ecosystem UI component option, not a Microsoft
  product or a Foundry runtime.
* Python integration: the documented `agent-framework-ag-ui` package brings
  Agent Framework and its AG-UI integration. The examples create framework
  agents; they do not prove drop-in compatibility with a custom Projects
  Responses loop bound to an existing named/versioned Foundry prompt agent.
* Safety: generic approval transport does not replace business authorization.
  Microsoft recommends a trusted frontend server mediating untrusted browser
  input, server-owned instructions/tools and validation of client data.
* Limitations: no package compatibility, custom adapter, hosting, live
  integration or universal GA status was established. Language-specific
  support varies; .NET prerelease instructions must not be generalized to
  the Python package. No framework migration or implementation is approved.

## Agent Framework managed Foundry integration follow-up

* Consulted: 2026-11-03
* Source: [Microsoft Foundry Agent Service integration](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/foundry)
* Evidence: Python `FoundryAgent` connects to an existing Prompt Agent using
  project endpoint, agent name and version; stored instructions/configuration
  remain authoritative. Matching local function implementations can be
  supplied through `tools=` when their definitions already exist on the
  managed agent. Standard framework run, streaming and session APIs apply.
* Distinction: this is not the direct-model `FoundryChatClient` pattern where
  application code owns an ephemeral agent definition, and does not require
  switching to a hosted agent.
* Limitations: caller-provided model/instructions and some tool options are
  filtered or ignored for service-managed agents. The documentation does not
  prove compatibility with this repository's pinned SDKs, exact safety/budget
  behavior or AG-UI integration end to end. These need a bounded assessment.
  No packages were installed and no existing agent/session was invoked.

### Local implementation verification on 2026-11-03

Under separately authorized S-030, installed and inspected framework core
1.24.0, Foundry adapter 1.16.0 and OpenAI adapter 1.18.0 with Projects 2.7.0.
The [published package metadata](https://pypi.org/project/agent-framework-foundry/1.16.0/)
requires Projects `>=2.2.0,<2.8.0`. Dependency consistency passes locally.
Installed implementation and offline HTTP tests verify non-preview versioned
`agent_reference`, local-only exact function schemas, per-service-call chat
middleware, native session serialization and sequential local invocation.
Fatal function middleware can otherwise trigger best-effort hosted-conversation
settlement; application policy now prevents that extra request after failure.
See the [bounded findings](../../.copilot-tracking/projects/supply-chain-resilience/research/evidence.md#s-030---installed-framework-api-and-safety-verification).
No live Azure or AG-UI compatibility is claimed by this local verification.

## Framework tracing diagnostic follow-up

* Consulted: 2026-11-04, S-033 local/public diagnostic analysis only
* Sources:
  [Agent Framework observability](https://learn.microsoft.com/en-us/agent-framework/agents/observability),
  [client-side agent tracing](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-client-side),
  [tracing setup](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup),
  [agent monitoring dashboard](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard)
* Evidence: local agent/tool spans require instrumentation/provider/export
  setup; the framework does not install exporters by default. Azure Monitor
  export feeds Application Insights and Foundry trace views. Linking Insights
  and persisting a Conversation do not instrument a local application.
* Timing: the client guide states typical trace visibility in 2-5 minutes
  after setup; this is not a guaranteed SLA and cannot repair absent export.
* Privacy: full prompt/response/tool-content recording is separate from
  trace metadata and requires explicit sensitive-data consideration.
* Limitations: installed pinned packages, not current documentation alone,
  determine available APIs/dependencies. Local inspection confirms no OTel
  SDK or Azure Monitor exporter in this application's environment. No Azure
  ingestion/permissions/portal-state inspection occurred, and server-side
  trace availability is not independently established.

## Testing UI design follow-up

* Consulted: 2026-11-04, S-035 local/public design
* Sources:
  [AG-UI integration](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/),
  [DevUI](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/devui/)
* Evidence: DevUI is a standalone development/debug sample, explicitly not
  production UI. Python supports direct registration and directory discovery.
  AG-UI is an optional UI protocol with streaming/SSE, state and interaction
  features; the Python integration maps native streaming execution to events.
* Local limitation: this application's outer session/evidence/human controls
  and non-streaming safety must remain. Direct registration of the raw agent
  is not evidence that these controls are preserved. No optional UI packages
  were installed, and no integration was run during this design.
* Recommendation: one thin local browser UI for the accepted complete human
  case, with compatibility/implementation tests under separate approval.
  This is a project-specific trade-off, not a Microsoft universal best practice.

## AG-UI native streaming implementation follow-up

* Consulted: 2026-11-04 under S-036 revision 2 and Q-037 local authorization
* Official source: [AG-UI getting started](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/getting-started)
* Evidence: Python AG-UI/FastAPI integration streams standardized events over
  SSE. AG-UI is a protocol/integration, not a complete case-management UI
  or a replacement for native model/tool execution.
* Exact installed evidence: `agent-framework-ag-ui==1.7.1` supports
  framework core `>=1.22.0,<2.0.0`, AG-UI protocol `>=0.1.19,<0.2.0`,
  FastAPI `>=0.121.0,<0.142.0` and Uvicorn `>=0.30.0,<1.0.0`.
  FastAPI 0.141.0 and Uvicorn 0.38.0 installed without changing core 1.24.0,
  Foundry 1.16.0, OpenAI adapter 1.18.0 or Projects 2.7.0.
* Inspected public APIs: `AgentFrameworkAgent.run` is an async event
  generator; `EventEncoder` produces SSE; native `ResponseStream` supports
  incremental iteration and `get_final_response`. `ChatContext` update/
  result gates permit terminal authoritative-response capture and validation
  before native function invocation while allowing provisional text through.
* Observed limitation: the official adapter sets native telemetry conversation
  ID from AG-UI thread ID. Offline native-span evidence reproduced this;
  the shared exporter preserves the trusted actual managed conversation ID.
* Validation: real installed framework/adapter and OpenAI SSE types with
  simulated service I/O, explicit final validation, human actions and
  cancellation checks. See [A-023](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-023---s-036-ag-ui-and-native-streaming).
* Limitations: no live Azure inference/export, published-version change,
  production certification or support matrix. Earlier design-only statements
  about absent UI packages/non-streaming code remain historical, not current
  installed-runtime facts. Preview/experimental guidance is not a GA claim.

## Shared tracing implementation follow-up

* Consulted: 2026-11-04, S-034 and explicit Q-034 authorization
* Sources: the four official pages in the preceding diagnostic follow-up;
  [OTel SDK package](https://pypi.org/project/opentelemetry-sdk/),
  [Azure Monitor exporter](https://pypi.org/project/azure-monitor-opentelemetry-exporter/)
* Installed implementation evidence: framework core 1.24.0 uses global
  sensitive settings; native `FunctionTool`/chat/agent spans work with an
  OTel provider. SDK 1.45.1 and exporter 1.0.0b58 satisfy pinned dependencies.
  Exporter 1.0.0b58 is a beta package; do not describe it as GA.
* Implementation: shared provider, task-local per-agent policy and allowlisted
  trace export. Native sensitive capture remains off; selected synthetic
  turn/tool content is explicit. No redundant automatic instrumentation.
* Validation: in-memory native framework spans and concurrent-policy
  isolation pass. Live ingestion is separately recorded in
  [A-022](../../.copilot-tracking/projects/supply-chain-resilience/implementation/log.md#a-022---s-034-shared-per-agent-observability);
  successful local export alone is not proof of portal visibility.

## Demo discovery supporting sources

Consulted on 2026-11-02 for the pre-project demo comparison. These supplement
the S01...S33 Foundry baseline; no new runtime or architecture is approved.

* Source: [Hybrid search using vectors and full-text search in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview)
* Evidence: hybrid queries execute full-text and vector retrieval together;
  Reciprocal Rank Fusion merges the results.
* Use: candidate retrieval of versioned synthetic policy and supplier documents.
* Limitation: not a transactional operational store, business authorization
  mechanism, or proof of retrieval quality on the future demo dataset.

* Source: [What is Azure SQL Database?](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview?view=azuresql)
* Evidence: managed database engine and support for relational data.
* Use: candidate operational store for synthetic orders, inventory, proposals,
  and simulated actions.
* Limitation: service overview only; no region, SKU, price, identity model,
  application transaction design, or Foundry integration has been selected
  or tested.

* Source: [How impact analysis works (production-ready preview)](https://learn.microsoft.com/dynamics365/supply-chain/procurement/procurement-agent-impact-analysis-works)
* Evidence: confirmed delivery-date delays, quantity decreases, cancellations,
  supply-demand dependencies, downstream order impact, and no-impact cases
  with sufficient inventory buffer.
* Use: validate realistic supply-chain exception stories, not select an ERP.
* Limitation: Dynamics-specific production-ready preview and prerelease
  documentation; not a Foundry API, GA claim, mandatory Dynamics integration,
  or proof of a functioning custom agentic solution.
