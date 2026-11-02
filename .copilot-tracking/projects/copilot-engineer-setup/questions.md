---
title: "Setup Questions and Answers"
description: "The user's actual preferences, harness clarification, and authorized resumption."
ms.date: 2026-11-02
---

## Translation Provenance

The questions and answers below were originally recorded in Italian.
English renderings preserve their meaning and authorization scope;
quoted answers are translations, not verbatim English user messages.

## Q-001 - Location and Environment

* Date: 2026-11-02
* Reason: choose the scope and compatible customization format
* Form question, translated: where and for which environment
* Answer, translated: "In this repository, for the Copilot harness in VS Code"
* Status: answered; confirmed after clarification Q-004
* Decision: D-001 and D-004

## Q-002 - Composition

* Date: 2026-11-02
* Reason: choose the complexity and delegation boundaries
* Form question, translated: assistant structure
* Answer, translated: "One principal + one skill + two read-only specialists on justified request"
* Status: answered
* Interpretation: a stable principal; optional specialists, not an autonomous team
* Decision: D-002

## Q-003 - Pace

* Date: 2026-11-02
* Reason: distinguish activity-level and phase-level autonomy
* Form question, translated: how far to advance after approval
* Answer, translated: "One bounded activity, then a summary and fresh confirmation"
* Status: answered
* Decision: D-003

## Q-004 - Clarification Requested by the User

* Date: 2026-11-02
* Origin: user request, not a question posed by the principal
* Request, translated summary: explain Local vs Copilot before continuing
* Effect: creation paused before writing the profiles
* Explanation provided: harness/model/workspace distinction,
  customization compatibility, and independence from Autopilot
* Status: answered; sources in the [guide](../../../docs/engineering/copilot-guide.md)

## Q-005 - Resumption

* Date: 2026-11-02
* Origin: explicit user confirmation after Q-004
* Answer, translated: "OK, let's proceed with Copilot"
* Interpretation: resume the requested setup using Copilot and the
  previously expressed composition/pace preferences; do not implement a Foundry use case
* Status: answered
* Reference: S-001 revision 1

## Q-006 - Repository Translation Request

* Date: 2026-11-02
* Origin: explicit user request, not a question posed by the principal
* Request, translated summary: translate the entire repository into English
* Status: answered by the request itself; no additional preference inferred
* Interpretation: translate repository content, including profiles,
  templates, tracking, and test messages; preserve technical contracts
  and the meaning of historical decisions
* Reference: S-003 revision 1; D-005

## Q-007 - Restore Structured Questions

* Date: 2026-11-02
* Origin: explicit user request, not a question posed by the principal
* Request, translated summary: how do we fix the missing capability and
  give the Foundry AI Engineer access to structured questions?
* Status: answered by the request itself
* Interpretation: correct the repository-scoped customization, related
  documentation, and regression tests; preserve explicit consent and the
  paused supply-chain step. No fallback policy or global permissions were approved.
* Reference: setup S-004 revision 1; D-006

## Q-008 - Fresh-Profile Capability Check

* Date: 2026-11-02
* Reason: a static allowlist check cannot prove the selected principal
  can open an interactive form and receive the actual answer.
* Question: after selecting the corrected principal in a fresh Copilot chat,
  does the capability-only test produce a real form and return the answer?
* Alternatives: passed, still missing/failing, or deferred
* Recommendation: test only the form round trip, without resuming the project
  or submitting supply-chain Q-007.
* Status: answered on 2026-11-02
* User answer: `passed`; no additional details provided
* Interpretation: the user reports that a real form appeared in a fresh
  corrected-principal chat and the agent received the answer. This is
  user-reported T13 evidence, not direct inspection of that session's trace.
  It does not approve any business step or verify the other behavioral cases.
* Reference: setup S-002 revision 2, T13; not supply-chain S-004
