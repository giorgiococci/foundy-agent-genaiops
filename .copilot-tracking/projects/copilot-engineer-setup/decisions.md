---
title: "Setup Decisions"
description: "Confirmed choices and reasoned implementation decisions for the assistant."
ms.date: 2026-11-02
---

## D-001 - Repository Scope

Status: accepted by the user in Q-001.
Profiles and the skill live in the repository, not in the personal profile.
Consequence: shareable, versionable configuration.

## D-002 - Principal, Skill, and Two Specialists

Status: accepted by the user in Q-002.
Specialists are read-only and used through justified, approved delegation.
A single agent was the simpler alternative; the skill separates protocol
and templates, while specialists isolate extensive research and reviews.
No autonomous implementer is introduced.

## D-003 - Single-Step Autonomy

Status: accepted by the user in Q-003.
Every execution has a scope and revision. After reporting and saving
results, the principal stops. Approving a plan does not execute the backlog.

## D-004 - Copilot Harness

Status: accepted by the user in Q-005, after clarification Q-004.
This is not equivalent to the Cloud target. Files use `github-copilot`.
Personal settings and runtime permissions are not changed.

## Setup Implementation Choices

These are not additional preferences attributed to the user:

* Omit `agents` and `handoffs` for Copilot compatibility.
* Declare the skill inline and use documented tool aliases.
* Do not pin unrequested models or reasoning effort.
* Do not add preview hooks without a dedicated increment.
* Keep memory in Markdown and templates, without an external database.

Rationale and sources: [analysis](research/analysis.md).

## D-005 - English Repository

Status: accepted through the user's explicit translation request Q-006.
All repository prose, profile instructions, templates, and test messages
are translated to English. Historical answers remain clearly labeled
translations; their decision status and approval scope do not change.

Implementation consequence: English replaces the previous Italian default
in the profiles. The principal may still answer in another language when
explicitly requested, while project documents remain in English.
No change to the guided workflow, specialist tools, or Azure scope.

## D-006 - Explicit Native Question Capability

Status: accepted as the targeted correction requested in Q-007.
The principal's scoped tool list explicitly permits native Copilot `ask_user`.
It checks the live inventory and available discovery before declaring the
capability absent. The native name is documented by the SDK user-input tests;
it is not a guessed Local client-tool reference.

Retain the existing strict structured-confirmation requirement. No text-only
fallback, wildcard tool access, specialist capability expansion, SDK host
implementation, personal settings, or business-step approval is introduced.
The session host must still expose interactive user input.

Evidence and limitations: [guide C03](../../../docs/engineering/copilot-guide.md#c03),
[C09](../../../docs/engineering/copilot-guide.md#c09), and
[C10](../../../docs/engineering/copilot-guide.md#c10).
A fresh-profile capability check was required because schema validation alone
cannot demonstrate that the host provides the handler. The user subsequently
reported that focused check passing in Q-008; other behavioral tests remain
unverified.
