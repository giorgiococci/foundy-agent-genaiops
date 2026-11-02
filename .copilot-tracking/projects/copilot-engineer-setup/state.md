---
title: "Foundry AI Engineer Setup State"
description: "Corrected question-tool capability and the pending fresh-profile smoke test."
ms.date: "2026-11-02"
project_id: "copilot-engineer-setup"
kind: "customization-setup"
phase: "validation"
step_id: "S-002"
step_revision: 2
step_status: "completed"
autonomy: "single-step"
---

## Objective

Create the guided engineering assistant in the repository, not a Foundry
solution. The candidate use case has not been approved.

## Confirmed Choices

Copilot in VS Code; one principal, one skill, and two read-only specialists
through justified, approved delegation; one activity per confirmation.
See [questions](questions.md) and [decisions](decisions.md).
The repository is in English under Q-006/D-005.

## Previous Step S-001

Package creation and structural checks, documentation, and tracking.
Authorization: the user's request to create the agent, form choices, and
subsequent message translated as "OK, let's proceed with Copilot".
This does not authorize any Azure resource or operation.
Outcome: completed within the configuration and structural validation scope.
Authorization consumed; not reusable for S-002.

## Checks

Configuration written; original structural tests: 8 passed, 0 failed.
Editor diagnostics for the three profiles, skill, and test reported no
errors. This does not prove discovery or runtime behavior.
Testing discovery, questions, and pauses in a fresh VS Code session is
separate. The user subsequently reported a principal session that reached
supply-chain Q-007 but could not submit a structured question. This is
failure evidence, not a passing run of the behavioral suite.
After the configuration fix, the user reported a successful T13 form
round trip in a fresh corrected-principal chat through setup Q-008.

## Current Step S-002 Revision 2

Completed focused check T13: select the corrected principal in a fresh
interactive Copilot chat, ask a capability-only question, and verify the
form and returned answer. Setup Q-008 returned `passed` through a structured
form; this is user-reported runtime evidence, not an inspected trace.
The check's consent is consumed; no other activity follows automatically.
The earlier revision 1 T01...T03 proposal remains historical.
No demo code, project research, Azure access, or business approval is included.

## Language Maintenance S-003

The user's subsequent repository translation request is a separate
maintenance activity. It does not authorize S-002 or any Foundry implementation.
Progress and evidence are recorded in the [implementation log](implementation/log.md).

S-003 revision 1 is completed; its authorization is consumed.
The repository is in English and the structural suite passes 9 of 9 tests.
At S-003 closure the next proposed operational step was S-002, without consent.
Its subsequent revision 2 outcome is recorded above.

## Question Capability Maintenance, Setup S-004

Revision 1 completed under the user's explicit correction request Q-007.
The principal now explicitly permits native `ask_user`, checks discovery
before declaring it absent, and retains strict consent without a text fallback.
The skill, guide, regression tests, and setup tracking were updated.
Ten structural tests pass; scoped editor diagnostics report no errors.
Configuration-maintenance consent is consumed.

The host must still provide interactive user input. The user reports
fresh-profile T13 passing in setup Q-008. Other behavioral cases, including
T14's unavailable/cancelled path, remain unverified. This result is not
supply-chain Q-007 approval.
No personal settings, global permissions, or supply-chain approvals changed.
See the [capability check](../../../docs/engineering/copilot-guide.md#structured-questions-and-confirmations)
and [implementation evidence](implementation/log.md#a-003---structured-question-capability-fix-setup-s-004-revision-1).

## Next Point

The capability repair and focused smoke check are complete. Return to the
Foundry AI Engineer session to separately submit the existing supply-chain
Q-007 contract. Supply-chain S-004 remains proposed; no research is started
or approved by this setup test.
