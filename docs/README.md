---
title: Knowledge base map
description: Reading paths and document boundaries for the Foundry lab.
ms.date: 2026-11-02
status: research-baseline
---

## Study path

| Order | Document                                           | Question it answers                                              |
| ----- | -------------------------------------------------- | ---------------------------------------------------------------- |
| 1     | [Recent findings](research/findings-2026-11-02.md) | What affects the solution choice?                                |
| 2     | [Platform](knowledge/platform.md)                  | What is Foundry and what does it manage?                         |
| 3     | [Development](knowledge/development.md)            | How do you create, run, and deploy an agent?                     |
| 4     | [Orchestration](knowledge/orchestration.md)        | When do you need multiple agents and how do you coordinate them? |
| 5     | [Tools and MCP](knowledge/tools-mcp.md)            | When do you need an MCP server?                                  |
| 6     | [Security](knowledge/security.md)                  | Who can do what, on which data?                                  |
| 7     | [Observability](knowledge/observability.md)        | How do you reconstruct an entire request?                        |
| 8     | [GenAIOps](knowledge/genaiops.md)                  | How do you measure, release, and correct?                        |
| 9     | [Responsible AI](knowledge/responsible-ai.md)      | What risks remain and how are they managed?                      |
| 10    | [Candidate use case](demo/use-case.md)             | Which demo makes these aspects verifiable?                       |
| 11    | [Roadmap and spikes](demo/validation-roadmap.md)   | What evidence is needed before implementation?                   |

## Provenance and maintenance

For guided work, use the
[Foundry AI Engineer in VS Code](engineering/copilot-guide.md).
The guide covers the assistant architecture, Copilot sources, startup
instructions, and testing. Do not confuse it with the demo runtime agents.

The [source register](research/sources.md) is the single location for public
URLs. The [method](research/method.md) defines the evidence hierarchy,
statuses, and update rules.

The guides are reasoned syntheses, not copies of the original pages.
Sections titled "Proposal" describe possible lab decisions,
not Microsoft guarantees.

## Useful distinctions

* Foundry Agent Service and Microsoft Agent Framework are not the same product.
* A containerized agent is not automatically a Foundry hosted agent.
* The MCP protocol is not an authorization system.
* A call that completes without errors does not prove that the task is correct.
* Content filtering does not replace authorization, RAI, or data isolation.
* A trace ID is not a credential and does not authorize operations.
* Dashboard availability does not guarantee telemetry coverage.

These distinctions guide all lab proposals.
