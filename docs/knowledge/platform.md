---
title: Microsoft Foundry and capability maturity
description: A taxonomy distinguishing services, runtimes, frameworks, and features.
ms.date: 2026-11-02
status: research-baseline
---

## Mental model

Microsoft Foundry brings together development, models, tools, and operations.
Foundry Agent Service is the managed service for agents. Microsoft Agent
Framework is a library for building agents and workflows, usable with
Foundry and other providers. The framework is not the hosting platform.
Sources: [S01](../research/sources.md#s01), [S05](../research/sources.md#s05).

Separate five layers:

1. Application: user interface, authentication, and use-case APIs.
2. Orchestration: routing, specialist agents, state, approvals, and limits.
3. Inference: model, deployment, parameters, and invocation protocol.
4. Capability: tools, data, policies, identity, and business contracts.
5. Operations: tracing, evaluations, releases, incidents, and costs.

Separating these layers is a lab design convention.
A layer may be managed by Foundry or by our code.

## Execution options

| Option                   | Definition and responsibility                            | Source                            |
| ------------------------ | -------------------------------------------------------- | --------------------------------- |
| Prompt agent             | Persisted configuration: instructions, model, and tools  | [S02](../research/sources.md#s02) |
| Voice-based prompt agent | Managed voice orchestration with Voice Live              | [S01](../research/sources.md#s01) |
| Hosted agent             | Containerized code run by Agent Service                  | [S03](../research/sources.md#s03) |
| External ephemeral agent | Definition in code, calls to the project's Responses API | [S33](../research/sources.md#s33) |

Voice is not required for the current objectives. An external runtime can
run locally or on a hosting service selected later; it does not automatically
benefit from the session management, identities, or guardrails
specific to hosted Foundry.

## Documented maturity matrix

| Capability                                 | Evidence in the baseline                     | Proposed treatment                       |
| ------------------------------------------ | -------------------------------------------- | ---------------------------------------- |
| Prompt agent / Projects 2.x                | Documented; global GA is not attested here   | Possible baseline; verify chosen APIs    |
| Hosted runtime                             | Documented; overall GA not attested          | Spike before choosing hosting            |
| Hosted .NET source deployment              | Prerelease package in the quickstart         | Isolate toolchain and pin versions       |
| Foundry visual workflow                    | Preview; retirement announced for 2026-12-01 | Do not adopt for new development         |
| Agent Framework workflow graph             | Documented for the listed SDKs               | Orchestration candidate                  |
| Python functional workflow                 | Experimental                                 | Not needed for the first baseline        |
| Agent Framework Go                         | Public preview                               | Not the lab's first choice               |
| Foundry SDK GenAI tracing                  | Experimental preview                         | Spike, pinning, and telemetry tests      |
| Monitor, recurring eval, scans, and alerts | Elements marked preview                      | Not the only operational control plane   |
| Agentic guardrails / tool intervention     | Explicit preview                             | Additional defense, not authorization    |
| Copilot harness for prompt agents          | Explicit preview                             | Separate experimental track              |
| Agent optimizer                            | Preview in the Agent Service overview        | Later study; promotion subject to review |

Sources: [S01](../research/sources.md#s01), [S02](../research/sources.md#s02),
[S03](../research/sources.md#s03), [S04](../research/sources.md#s04),
[S05](../research/sources.md#s05), [S06](../research/sources.md#s06),
[S08](../research/sources.md#s08), [S14](../research/sources.md#s14),
[S18](../research/sources.md#s18), [S19](../research/sources.md#s19),
[S31](../research/sources.md#s31), [S32](../research/sources.md#s32).

## New features to study without making them mandatory

The Copilot harness keeps the resource as a prompt agent but changes the managed
runtime for multi-step workflows with tools, skills, files, and commands.
It is not a hosted container whose framework and middleware we own. In the
initial public preview, it is selected at creation; BYOM is not supported.
Source: [S31](../research/sources.md#s31).

The optimizer searches for better configurations guided by evaluations.
In the portal path for prompt agents, it does not support the Copilot harness.
Optimizing function descriptions does not evaluate the actual execution
of those functions. Our authorization and effect tests are still required.
Source: [S32](../research/sources.md#s32).

## Compatibility to verify jointly

The region choice must satisfy the intersection of runtime, model,
tools, evaluation, red teaming, networking, and residency requirements.
The hosted page also lists Italy North and European regions, but this does not
prove that an entire solution is available there.
Sources: [S03](../research/sources.md#s03), [S13](../research/sources.md#s13),
[S28](../research/sources.md#s28), [S30](../research/sources.md#s30).

Documented availability does not replace subscription quota and capacity.
No region is fixed at this stage.
