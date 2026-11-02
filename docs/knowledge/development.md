---
title: Agent development and hosting
description: Practical paths for prompt agents, hosted containers, and external runtimes on Foundry new.
ms.date: 2026-11-02
status: research-baseline
---

## Choose what to own

| Path                       | Main benefit                               | Our additional responsibilities                      |
| -------------------------- | ------------------------------------------ | ---------------------------------------------------- |
| Prompt agent               | Managed runtime and declarative definition | Tool contracts, permissions, datasets, and quality   |
| Hosted Agent Service       | Custom code with managed hosting           | Containers, dependencies, logic, RAI, and policies   |
| External runtime + Foundry | Application control and portability        | Hosting, state, identity, networking, and operations |

Sources: [S01](../research/sources.md#s01), [S03](../research/sources.md#s03),
[S33](../research/sources.md#s33).

Do not choose a container solely because the solution is multi-agent.
Choose one when you need explicit orchestration, middleware, libraries,
application policies, or process control that cannot be expressed in
the prompt definition alone.

## Prompt agent path

The new quickstart uses `AIProjectClient`, an agent definition, and
version creation. In Python, the definition is
`PromptAgentDefinition`; names may differ in other SDKs.
Invocation uses Responses and the conversation management provided
by the chosen path.
Source: [S02](../research/sources.md#s02).

Proposed workflow:

1. Choose a supported model deployment and project endpoint.
2. Define instructions, tools, and expected outputs in source control.
3. Create an agent version through compatible APIs.
4. Assign the required runtime permissions, separate from developer permissions.
5. Run happy paths, deny paths, and offline evaluations.
6. Connect tracing before adding more agents.

A function call from the model does not imply execution on the Foundry server.
In the prompt path with function calling, the client may need to execute
the function and return its output. Distinguish a local function tool from
a managed tool or remote MCP.
Source: [S32](../research/sources.md#s32).

## Hosted agent path

Code is packaged in an image, stored in Azure Container
Registry, and run by Agent Service. Python and C# are documented,
with protocol libraries independent of the chosen framework.
Sources: [S03](../research/sources.md#s03), [S04](../research/sources.md#s04).

The platform describes VM-isolated sandboxes per session, not a set of
shared replicas to size. CPU and memory are allocated per session.
Scaling to zero after idle does not necessarily mean the session
has ended or its data has been deleted.
Source: [S03](../research/sources.md#s03).

### Protocols and state

| Protocol    | Documented use                            | State to manage carefully                          |
| ----------- | ----------------------------------------- | -------------------------------------------------- |
| Responses   | Conversations, streaming, and background  | Conversation, session, and response                |
| Invocations | Custom payloads, webhooks, and custom SSE | Contract and application sessions                  |
| WebSocket   | Bidirectional streaming and voice         | Connections, reconnection, and lifecycle           |
| A2A         | Delegation between agents                 | Identity, capabilities, and cross-service failures |

Source: [S03](../research/sources.md#s03). A2A is not required to call
multiple agents in the same process.

The hosted page distinguishes:

* Sessions with a persisted filesystem and restoration after idle
* Conversations with history independent of compute
* A state store for application JSON items and framework checkpoints

At the time of review, the idle timeout is configurable from 2-240 minutes,
with a default of 15; sessions are deleted after 30 days of inactivity.
These are properties of the documented runtime, not sufficient privacy
policies for the demo. Check history, stores, logs, and downstream data separately.
Source: [S03](../research/sources.md#s03).

Background execution and resilience are not synonyms. A process may continue
after a request without being able to resume correctly after a crash.
Checkpoints and idempotency of external actions require testing.

### Deployment and updates

Documented paths: azd, Python/C# SDKs, VS Code, and Foundry tools.
The SDK path requires an existing project and model deployment;
it is not equivalent to the full provisioning provided by the azd path.
Source: [S04](../research/sources.md#s04).

Hosted versions are immutable snapshots of the image, resources, variables,
and protocols. The endpoint routes 100% of traffic to one version; native
traffic splitting between versions is not supported in the reviewed guide.
Proposal: smoke tests on a separate target and a controlled switch, not a
pipeline promising unverified percentage-based canary deployment.
Source: [S03](../research/sources.md#s03).

Do not load trusted code or instructions from paths that session uploads
can modify. `$HOME`/user files must not change program behavior
merely because a file is present.
Source: [S03](../research/sources.md#s03).

## External path with Responses

The quickstart describes an ephemeral agent: instructions, model, and tools
live in code, with no persisted agent resource to create.
The project endpoint exposes the Foundry API surface; it is not interchangeable
with the Azure OpenAI endpoint, which focuses on OpenAI capabilities.
Source: [S33](../research/sources.md#s33).

The runtime could be a container on Container Apps or another
service selected after the spike. This is a design option,
not a claim that all hosted features transfer to that environment.

## Minimum toolchain matrix to pin

| Documentation path       | Requirements observed on the page                  |
| ------------------------ | -------------------------------------------------- |
| Prompt Python new        | `azure-ai-projects>=2.3.0`                         |
| Python tracing           | Python 3.10+, `azure-ai-projects>=2.0.0`           |
| Hosted Python quickstart | Python 3.13+, `azure-ai-projects>=2.3.0`           |
| Hosted C# source deploy  | .NET 10, Projects 2.1.0-beta.4                     |
| Toolbox C#               | Coordinated Projects/Agents/Extensions preview set |

Sources: [S02](../research/sources.md#s02), [S04](../research/sources.md#s04),
[S13](../research/sources.md#s13), [S18](../research/sources.md#s18).

These are observed requirements, not a ready-to-use lockfile. Before writing
code, pin exact compatible versions, including exporters,
Agent Framework, and protocol libraries. Do not install independent
"latest" packages and assume compatibility.

## Lab proposal

Compare .NET and Python using the same vertical slice:
one request, one authorized tool, one deny, and a complete trace.
Python provides a direct research/evaluation path; .NET is a
natural choice if the reuse target is an enterprise C# solution.
The choice should weigh familiarity, required SDKs, and supportability,
not the number of samples found.
