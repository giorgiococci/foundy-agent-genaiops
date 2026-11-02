---
title: Guided Work Tracking
description: Documented project memory and approvals for the Foundry AI Engineer.
ms.date: 2026-11-02
---

## Purpose

Analysis, questions, answers, decisions, plans, and outcomes are project
documents, not memory entrusted solely to chat.
The protocol and templates are in the
[guided engineering skill](../.github/skills/foundry-guided-engineering/SKILL.md).

## Organization

Each project uses a stable root:

```text
.copilot-tracking/projects/<project-id>/
  state.md
  questions.md
  decisions.md
  research/
    analysis.md
    evidence.md
  plan/
    plan.md
  implementation/
    log.md
  reviews/
    review.md
```

The layout is a convention: create documents when needed, not all on
the first turn. A project does not change folders with each chat.
IDs and revisions link requirements, questions, decisions, authorizations,
and results.

## Existing Projects

* [Foundry AI Engineer setup](projects/copilot-engineer-setup/state.md):
  assistant configuration, not a Foundry solution.
* [Supply-chain resilience](projects/supply-chain-resilience/state.md):
  manufacturing context and mixed audience selected; discovery in progress,
  scenario and architecture not approved.

No implementation has started. The original
[candidate use case](../docs/demo/use-case.md) remains unapproved.

## Use Case Discovery

The [demo selection record](discovery/use-case-selection.md) retains the
comparison and initial answers that led to the supply-chain direction.
It is not an approved solution or an implementation project. The selected
project links back to this record rather than replacing its history.

## Resuming and Authorizations

A new chat reads state and relevant documents, summarizes progress, and
reconfirms the next operational step. The state file is not an authorization
token. Historical consent does not authorize new side effects.

The user approves a single bounded activity, not the entire backlog.
A plan can be approved without authorizing its execution.
A scope or revision change requires updated consent.

## What to Save

Save technical rationale, alternatives, relevant answers, sources,
decisions, and repeatable evidence. Preserve history and identify
supersessions. Record `not-run` when a check has not been performed.

Keep documents in English. Historical user answers translated from
another language must be labeled as translations, not verbatim quotations.
Translation does not change their meaning, approval scope, or status.

Do not save secrets, tokens, unnecessary PII, complete transcripts, or
internal reasoning. Sensitive results belong in an authorized store,
with only a secure reference in tracking.

Sanitized documents can be versioned. This folder is not ignored by Git,
so redaction before writing is essential.
