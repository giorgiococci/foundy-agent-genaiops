---
name: "foundry-guided-engineering"
description: "Step-by-step Foundry guidance: use case analysis, targeted questions, planning, approvals, and persistent tracking."
user-invocable: true
disable-model-invocation: false
---

# Foundry Guided Engineering

## Overview

Manage the documentation workflow and authorizations for the Foundry AI
Engineer role. Use this skill to start or resume a Foundry use case,
record questions/answers and decisions, and plan or execute a single
agreed step. Keep the context inline, not in a forked skill.

The skill is not an autonomous orchestrator and does not create a
Foundry solution merely upon receiving its description.

## Prerequisites

* Project workspace accessible for reading and writing
* Foundry AI Engineer principal role selected
* Structured tool for questions and confirmations available (`ask_user` in Copilot)
* Project knowledge and constraints provided by the coordinator

If a prerequisite is missing, report the blocker without inventing approvals.
Tracking requires no Azure services, credentials, or packages.

The principal explicitly allows Copilot's native `ask_user` tool.
Check the live tool inventory and use tool discovery if available before
declaring structured questions unavailable; deferred is not the same as absent.
The host must also support interactive user input: an allowlist entry cannot
create a capability the host does not expose.
If the tool is still unavailable, preserve the open question and report the
checks performed. Do not silently substitute text-only confirmation, broaden
the tool allowlist, or treat a failed/cancelled call as consent.

## Quick Start

1. Identify the tracking project. If the use case or project to resume
   is missing, ask a targeted question before choosing it.
2. For a new use case, derive a stable slug, show where documents will
   be saved, and create only the necessary state, questions, and initial analysis.
3. When resuming, reread the state, open questions, effective decisions,
   current plan, and latest outcome. Summarize progress.
4. Apply the principal's phase and the next step contract. No operational
   approval automatically survives a new chat, pause, scope revision,
   or ambiguous error.

## Parameters Reference

| Input      | Source                               | Default                                 |
| ---------- | ------------------------------------ | --------------------------------------- |
| Workspace  | Opened and verified folder           | Current workspace                       |
| Project ID | Confirmed use case or user choice    | None; do not reuse an arbitrary project |
| Phase      | Persisted state and current request  | Discovery for a new project             |
| Activity   | Step contract                        | No execution authorized                 |
| Autonomy   | Confirmed preference                 | `single-step`                           |
| Knowledge  | References provided by the principal | Read the index and relevant sections    |

## Persistent Tracking

Use one root per project: `.copilot-tracking/projects/<project-id>`.
The project ID contains no variable dates, separators, or `..`; do not
create a new folder every turn. If the slug exists, verify that it is
the same use case before updating it.

Projects with `kind: customization-setup` document assistant configuration:
they are not Foundry use cases to resume implicitly.
Use `kind: foundry-solution` for a new solution.

Canonical destinations, relative to the project root:

| Document       | Path                    |
| -------------- | ----------------------- |
| State          | `state.md`              |
| Questions      | `questions.md`          |
| Decisions      | `decisions.md`          |
| Analysis       | `research/analysis.md`  |
| Research       | `research/evidence.md`  |
| Plan           | `plan/plan.md`          |
| Implementation | `implementation/log.md` |
| Review         | `reviews/review.md`     |

Templates are resources, not documents that have already been completed:

* [State](./assets/state.template.md)
* [Questions and answers](./assets/questions.template.md)
* [Decisions](./assets/decisions.template.md)
* [Analysis](./assets/analysis.template.md)
* [Research](./assets/research.template.md)
* [Plan](./assets/plan.template.md)
* [Implementation](./assets/implementation.template.md)
* [Review](./assets/review.template.md)

Fill in placeholders before saving actual documents. Create documents
when needed; do not populate empty folders or outcomes of future activities.
Every actual document has a title, description, and updated date.
Write project documents in English; label translated historical answers
as translations rather than verbatim quotations.

### State and History

State summarizes the phase, step/revision, outcome, blocker, and next point.
It does not replace evidence and is not an authorization token.
Use these step states:

* `proposed`: scope presented, not approved
* `approved`: explicit consent to the current revision, not yet started
* `in-progress`: execution of the approved step only
* `completed`: criteria verified; authorization consumed
* `blocked`: a condition prevents further progress
* `cancelled`: the user interrupted or rejected the step

A step's `completed` status does not complete the entire project.
When proposing a subsequent step, assign a new ID and `proposed` status.

Preserve previous records. A later correction to an answer supersedes
the previous one with a reference; it does not delete it.
The same applies to requirements, plans, and decisions.

### Questions and Answers

Before asking, save the Q-ID, reason, alternatives, recommendation,
affected decisions, and `open` status. After the answer, record the
date, faithful answer with sensitive data redacted, interpretation,
and `answered`, `deferred`, or `cancelled` status.

Do not record suggested wording, an unaccepted default, or an inference
as the user's answer. Do not request credentials, secrets, or PII
in the form; request secure references or configuration outside chat.

### Decisions and Sources

Use IDs Q-001 for questions, RQ-001 for requirements, D-001 for decisions,
S-001 for steps, and A-001 for executions. Each is unique within its project.
Every step revision increments `revision`.

Link the decision, questions/answers, requirements, alternatives, sources,
and consequences. Distinguish `proposed`, `accepted`, `superseded`, and
`rejected` status. If a new choice conflicts with an accepted decision,
document the impact and ask for confirmation before changing the work.

Research records the URL/section, date, facts, and limitations; local
references do not replace fresh verification when the decision depends
on releases, quotas, or actual availability.

## Step Contract and Approval

Before acting, present:

1. ID, revision, objective, and expected outcome.
2. In-scope files, resources, subscription/environment, and actions.
3. Excluded actions and operations with side effects.
4. Included tests and acceptance criteria.
5. Cost/risk, prerequisites, and a relevant recovery strategy.

For a simple analysis requested by the user, necessary public/local
reading and tracking updates are part of that analysis. Confirmation
is not required for every read, but this does not authorize code,
state-changing commands, or authenticated tenant access.

Record actual consent with the answer/reference, step, revision,
scope, and date. Approval of a plan applies to the plan; each operational
activity requires a separate contract.

Before the first side effect, verify that consent, revision, and scope
match and that no pause or requirement change has intervened.
An old `approved` value on disk is insufficient after resuming: reconfirm it.

A generic confirmation may apply only to the single unambiguous step
just presented, without cloud/spending/IAM/destruction/remote Git.
Those operations require explicit consent and declared targets.
Do not combine provisioning, deployment, and cleanup under one "proceed".

Delegation is one of the actions to declare in the contract. No
specialist may broaden authorization or approve the next step.

## Execution and Closure

1. Record `in-progress` and work only within the approved scope.
2. Save the result, changed files, checks, outcome, and limitations.
3. If a test fails, report it. Fix only defects within scope; return
   to the user for new files/resources or choices.
4. Mark `completed` only if the criteria are proven; otherwise mark `blocked`.
5. Consume the approval and save the summary before proposing anything else.
6. Propose only one next step and stop without starting it.

Before a question, save the context needed to resume it.
Before ending the turn, update at least the state and relevant register.
If writing fails, make the failure to persist explicit and stop work:
do not claim that nonexistent documents have been saved.

## Script Reference

This skill has no execution scripts: use the Markdown templates.
Package structural tests are described in the repository usage guide;
they do not replace testing a Copilot session.

## Troubleshooting

* Missing skill: check its name/directory, target, availability, and a fresh chat.
* Multiple candidate projects: ask which to resume instead of choosing the latest.
* Tracking inconsistent with chat: report the discrepancy and ask for confirmation.
* Questions unavailable: block the workflow; do not presume consent.
  Verify `ask_user` is allowed, discoverable, and exposed by the interactive
  host. Follow the [capability check](../../../docs/engineering/copilot-guide.md#structured-questions-and-confirmations)
  before retrying in a fresh session; do not approve the pending step during
  a capability-only test.
* Stop during execution: start nothing else; report operations already
  started and any safe shutdown actions needed. Do not promise to undo side effects.

## Attribution

Workflow specific to Foundry Multi-Agent Lab, based on the user's
confirmed requirements. Product and customization sources are recorded
in the repository research guides.
