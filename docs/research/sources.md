---
title: Source register
description: Public sources consulted and evidence limitations for the multi-agent lab.
ms.date: 2026-11-02
status: research-baseline
---

## Reading rules

Baseline entries have the consultation date **2026-11-02**.
Follow-up entries specify their own consultation dates. `updated_at`
indicates the page's editorial date, not the feature release.
"Not established" means that no GA/preview status is assigned without
specific evidence. Learn sources are product documentation; S09 is
an application-pattern blog. The limitations of this research are in the
[method](method.md).

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
