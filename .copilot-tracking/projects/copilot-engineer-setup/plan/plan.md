---
title: "Copilot Setup Plan"
description: "Scope of the requested activity and separate runtime smoke testing."
ms.date: 2026-11-02
plan_version: 1
status: recorded
---

## Nature of the Plan

A record of the setup requested by the user, not a fabricated approval
of a previously presented plan. Preferences are in the question register;
resumption was the message translated as "OK, let's proceed with Copilot".

## S-001 - Configure and Validate the Package

* Revision: 1
* Objective: make the principal, skill, and two specialists available
* Scope: profiles, templates, minimal instructions, guide, setup tracking,
  and local structural tests
* Included actions: public research, file edits, Node tests, and diagnostics
* Exclusions: Foundry solution, Azure, secrets, installations, personal
  permissions, commits/pushes, and operational delegation to specialists
* Criteria: consistent frontmatter, restricted tools, resolvable links,
  templates present, and consent/pause/resume described without automatic progression
* Cost: no Azure resources; normal use of the session model
* Recovery: correct or remove only files introduced by the setup,
  without touching the existing knowledge base

## S-002 - Smoke-Test a New Session

Status: proposed, not executed and not implicitly authorized by S-001.
The user selects the principal and describes a synthetic use case.
First check: T01...T03 and tracking verification. Other cases follow
as bounded activities, not autonomous execution of the entire suite.

## Dependencies

S-002 depends on S-001 structural checks and availability of the
Copilot target, tools, and skill in the user's editor.

## S-003 - Translate the Repository

Revision: 1. Separate maintenance activity explicitly requested after
the original setup, recorded as Q-006/D-005. It does not execute S-002.

Scope: translate all repository documentation, instructions, profiles,
skill resources, tracking, and test messages. Preserve paths, source
URLs, identifiers, technical requirements, and approval history.
Use bounded parallel translation work for independent document groups.

Validation: run the existing structural suite, check translated anchors
and residual non-English prose, and verify profile language consistency.
No Azure access, package installation, personal permission changes,
commit, or push.

Execution status: completed. S-003 revision 1 authorization is consumed.
Validation results are recorded in the
[implementation log](../implementation/log.md#a-002---repository-translation-s-003-revision-1).
This completion does not approve the proposed S-002 runtime test.

## S-004 - Restore Structured Question Capability

Revision: 1. Scope: principal tool list and discovery instructions, the
shared skill's capability checks, related guide, structural regression
tests, and setup tracking. Authorization: the user's explicit correction
request, recorded in setup Q-007. No specialist delegation.

Acceptance: explicitly allow native Copilot `ask_user` without wildcard
access; distinguish deferred tools from absent tools; preserve open
questions and approval boundaries; document host prerequisites and a
fresh-profile test; pass the repository structural suite and editor checks.

Exclusions: changes to personal settings, host/plugin implementation,
text-only fallback, new MCP servers, package installation, cloud operations,
and starting or approving supply-chain S-004.

Outcome: completed within repository-configuration scope. Ten structural
tests pass and scoped editor diagnostics report no errors. Consent consumed.
Fresh-profile runtime behavior is separate; see setup Q-008.

## S-002 Revision 2 - Focused Question-Tool Smoke Test

Status: completed, user-reported pass through setup Q-008 on 2026-11-02.
This revision narrows the runtime check to T13:
select the corrected principal in a fresh interactive Copilot chat,
open a real question, and verify that the actual answer returns.
Revision 1's broader T01...T03 proposal remains historical, not a passing report.

Do not resume a Foundry project or approve its pending research question
during this test. The user voluntarily ran the focused check and returned `passed` through
Q-008. No session trace was inspected. The check does not authorize the
remainder of T01...T14 or supply-chain Q-007, and its consent is consumed.
