---
title: "Foundry AI Engineer Analysis"
description: "Requirements, alternatives, sources, and limitations of the assistant setup."
ms.date: 2026-11-02
---

## Explicit Requirements

* RQ-001: guide the user from a use case description to a Foundry solution.
* RQ-002: use the knowledge base and explain options and trade-offs.
* RQ-003: ask targeted questions rather than fill ambiguities with assumptions.
* RQ-004: proceed step by step, not build everything autonomously.
* RQ-005: save analysis, plans, questions/answers, and results in documents.
* RQ-006: repository configuration for Copilot in VS Code.
* RQ-007: one principal, one skill, and two optional read-only specialists.
* RQ-008: one bounded activity per approval.

RQ-001...RQ-005 derive from the user's initial request.
RQ-006...RQ-008 are confirmed in the [question register](../questions.md).
These are setup requirements, not requirements for the future Foundry solution.

## Alternatives Considered

A single prompt is too closely tied to one invocation.
A single agent can be sufficient but mixes role, procedure, and templates.
A principal and skill preserve separation and progressive loading.
Two optional specialists add context isolation without turning the
workflow into autonomous orchestration.

## Sources and Compatibility

Public research on 2026-11-02 using sources C01...C08 in the
[Copilot guide](../../../../docs/engineering/copilot-guide.md).
Evidence: harness vs workspace distinction, Copilot-specific schema,
tool aliases, skill loading, subagent cost and context, and separation
of tool availability from approvals.

The current reference does not support `agents` and `handoffs` for the
Copilot target. An explicit protocol is used, acknowledging that it is
not a technical allowlist. Profiles avoid unnecessary MCP, models, and hooks.

## Non-Goals

No Azure provisioning, candidate use case implementation, personal
settings changes, commits/pushes, or claims of deterministic enforcement
through the prompt alone.

## Required Checks

Structural tests do not prove discovery or model behavior.
A fresh Copilot chat and cases T01...T12 from the guide are needed.
Installing components or bypassing policies is not part of the authorized setup.

## Language Maintenance Requirement

RQ-009: translate the entire repository into English, from the explicit
request recorded as Q-006. This changes presentation and the profile
language default, not technical contracts or historical approvals.
