---
title: Responsible AI and data management
description: Risks, guardrails, supervision, privacy, and declared limitations for a reusable demo.
ms.date: 2026-11-02
status: research-baseline
---

## RAI is not the same as content filtering

Design must consider purpose, users, potential harms,
data, supervision, and system limitations. Microsoft provides RAI
guidance and controls, but the application owner remains responsible
for the solution and its use.
Sources: [S17](../research/sources.md#s17),
[S03](../research/sources.md#s03).

Proposal: no real decisions about health, hiring, credit,
disciplinary matters, or physical safety. The candidate use case works on
synthetic tickets and allows at most an approved note in a demo backend.

## Proposed impact assessment

Complete before implementation:

1. Purpose and permitted users.
2. Prohibited uses and decisions that remain human.
3. Data processed and excluded categories.
4. Harms from errors, abuse, omissions, or unavailability.
5. Technical and operational mitigations.
6. Metrics to verify them and the person responsible for review.
7. Procedures for contesting outcomes, escalation, and shutdown.

| Risk in the candidate use case | Proposed mitigation                                   | Evidence to collect                                 |
| ------------------------------ | ----------------------------------------------------- | --------------------------------------------------- |
| Unsupported recommendation     | Verifiable citations and abstention                   | Checks against documents and cases with no evidence |
| Bias in ticket priority        | Explicit operational criteria, no personal attributes | Pairs of equivalent cases and human review          |
| Excessive automation           | Separate proposal from execution                      | No changes without approval                         |
| Prompt injection in documents  | Untrusted inputs/tool outputs and narrow capabilities | Adversarial suite and tool denies                   |
| Privacy and leakage            | Synthetic data, minimization, access, and retention   | Canaries and artifact inspection                    |
| Operator overreliance          | UI with evidence, uncertainties, and limitations      | Operator distinguishes facts from hypotheses        |
| Inaccessible experience        | Understandable status, errors, and approvals          | UI review and keyboard path where one exists        |

Fairness and accessibility metrics require a relevant dataset and UI.
No claim is made that they have been validated at this stage.

## Documented guardrails

The Foundry guide distinguishes intervention points on user input, tool calls,
tool responses, and output. Agentic guardrails are in preview; tool calls and
tool responses are marked preview, and the matrix specifies what applies
to models or agents. Some protections do not transfer from one category
to the other. Egress control is described for hosted agents and is in preview.
Source: [S14](../research/sources.md#s14).

Text checks can detect risk categories and attacks, but
do not automatically verify that a user owns a case.
IAM policies, business policies, and RAI guardrails are complementary defenses.

Proposal: apply only guardrails supported by the chosen target and
record their version, scope, and failures. An external runtime does not
automatically inherit all Agent Service guardrails.

## Red teaming

The AI Red Teaming Agent uses PyRIT and Risk/Safety evaluations. The documentation
describes Attack Success Rate and cloud scans, including scheduled scans.
Sources: [S26](../research/sources.md#s26),
[S27](../research/sources.md#s27).

Proposed categories:

* Malicious instructions in notes, documents, and retrieval results
* Requests to read out-of-scope data or reveal prompts/credentials
* Attempts to obtain write tools from a read-only agent
* Pressure to bypass approval or fabricate a result
* Exfiltration to a controlled test endpoint, without real data
* Irrelevant or harmful content under the use-case policy

Automated scans complement, rather than replace, policy tests
and domain-relevant manual attacks. A low ASR on the sample
does not certify the absence of vulnerabilities. Tests must be authorized,
isolated, and limited to lab systems.

## Data flow and retention

The privacy page for models sold by Azure states that data is not
used to train foundation models without permission. This does not mean
zero retention or the absence of stateful features, abuse monitoring,
or processing by external tools.
Source: [S16](../research/sources.md#s16).

The residency assessment must include the model deployment type,
processing mode, and every service involved. The project's region
name is not enough to conclude where every piece of data flows.
Sources: [S16](../research/sources.md#s16),
[S03](../research/sources.md#s03).

Proposed inventory:

| Data                      | Possible destination             | Proposed lab rule                                       |
| ------------------------- | -------------------------------- | ------------------------------------------------------- |
| Requests and responses    | Conversations/runtime            | Synthetic fixtures only, verified deletion              |
| Uploads and session files | Hosted session storage           | No real files; separation from trusted code             |
| Workflow state            | Selected store/checkpoint        | Minimum necessary and no bearer tokens                  |
| Tickets and notes         | Demo backend                     | Isolated, restorable fixtures                           |
| Traces and logs           | Application Insights/workspace   | Content off, restricted access, finite retention        |
| Eval datasets and reports | Foundry/test artifacts           | Versioned, synthetic, and reviewed before adding to Git |
| Consent and credentials   | Intended connection/secret store | Never exported to datasets, traces, or source control   |

Actual retention periods must be chosen in the spike and tested per destination.
Deleting a hosted session does not demonstrate deletion of conversations,
state stores, audit records, backups, or derived datasets.
Source for the distinct concepts: [S03](../research/sources.md#s03).

## Transparency in the demo

The future interface must distinguish:

* Retrieved evidence and its provenance
* Generated hypotheses or proposals
* Missing data and reasons for abstention
* Action requested from the operator
* The effect actually executed and its status

Do not display "operation completed" when it has only been proposed.
Do not claim "secure", "compliant", or "production-ready" based
on a demo and a single scan.

A useful handover includes residual risks, failed tests, adopted previews,
owners, a shutdown procedure, and differences from a real project.
