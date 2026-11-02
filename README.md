---
title: Foundry Multi-Agent Lab
description: Knowledge base and lab for a multi-agent demo on Microsoft Foundry with verifiable controls.
ms.date: 2026-11-02
status: research-baseline
---

## Goal

Study Microsoft Foundry and build a demonstrable multi-agent solution,
not a chatbot with multiple prompts. The lab must make authorization,
quality, observability, Responsible AI, and lifecycle management visible.

The first deliverable is an English knowledge base with **33 sources**, documented
facts, trade-offs, and checks to perform before implementation.
Sources consulted: **November 2, 2026**.

> [!IMPORTANT]
> The documentation announces the retirement of Foundry visual workflows on
> **December 1, 2026** and recommends Microsoft Agent Framework for new workflows.
> They are not the recommended foundation for this demo.
> Source: [S08](docs/research/sources.md#s08).

## Where to start

1. Read the [knowledge base map](docs/README.md).
2. Review the [platform and feature maturity](docs/knowledge/platform.md).
3. Compare [development and hosting options](docs/knowledge/development.md).
4. Read about [security](docs/knowledge/security.md),
   [observability](docs/knowledge/observability.md), and
   [GenAIOps](docs/knowledge/genaiops.md).
5. Assess the [candidate use case and architecture](docs/demo/use-case.md).
6. Use the [validation path](docs/demo/validation-roadmap.md)
   to decide on the stack and first increment.

## Guided AI Engineer in VS Code

The [Foundry AI Engineer](.github/agents/foundry-ai-engineer.agent.md)
guides the work with focused questions and only one authorized activity
at a time. It uses one skill and two optional read-only specialists.

The [usage guide](docs/engineering/copilot-guide.md) describes Copilot target
selection, sources, limitations, and testing in a new chat.
Analysis, decisions, answers, and results are retained in the
[project memory](.copilot-tracking/README.md).

Setting up the assistant does not approve or start the candidate demo use case.

## Scope

| Included in the research                           | Not included at this stage                          |
| -------------------------------------------------- | --------------------------------------------------- |
| Prompt agents, hosted agents, external runtimes    | Application code or already deployed infrastructure |
| Microsoft Agent Framework and multi-agent patterns | Final choice of language, model, and region         |
| MCP, Toolbox, identity, and authorization          | Access to real data, tenants, or credentials        |
| Tracing, monitoring, evaluations, and CI/CD        | Measured benchmarks or guaranteed monthly costs     |
| RAI, red teaming, and data management              | Security or compliance certification                |
| Demo alternatives and acceptance criteria          | APIM and APIM-dependent components                  |

APIM is excluded by choice. Identity, RBAC, the runtime, and application
services remain responsible for the required controls. An AI Gateway is not
introduced as an alternative way to require APIM.

## Current structure

```text
README.md
.github/
  agents/
  skills/foundry-guided-engineering/
  copilot-instructions.md
.copilot-tracking/
  README.md
  projects/
scripts/
  test-copilot-customizations.mjs
docs/
  README.md
  research/
    method.md
    sources.md
    findings-2026-11-02.md
  knowledge/
    platform.md
    development.md
    orchestration.md
    tools-mcp.md
    security.md
    observability.md
    genaiops.md
    responsible-ai.md
  demo/
    use-case.md
    validation-roadmap.md
  engineering/
    copilot-guide.md
```

Code, infrastructure, and dataset folders will be created when they have
content and an approved architectural choice. There are no placeholder scaffolds.

## How to interpret the information

* Citations `S01`...`S33` refer to the
  [source register](docs/research/sources.md), with URLs and evidence limitations.
* A documented feature is not automatically GA, available in your region,
  or included in the installed SDK version.
* The demo recommendations and thresholds are lab proposals.
* Tenant checks are still pending. No runtime result has been
  simulated or presented as measured.

The Git repository is local. No remotes, commits, or Azure resources have been created.
The [update method](docs/research/method.md) defines how to maintain
this baseline without turning it into a collection of unverified links.
