---
title: Research and update method
description: Rules for citations, maturity, provenance, and validation of Foundry information.
ms.date: 2026-11-02
status: research-baseline
---

## Baseline and limitations

Consultation date: **2026-11-02**. Primary scope: Foundry (new),
Agent Service, and Microsoft Agent Framework. Historical Foundry (classic)
pages are not the basis for future examples.

Public Microsoft Learn pages and the blog specified by the user were
consulted. The security and AgentOps guides also incorporate delegated
specialist research using the same public sources. The register retains
the original source, not search engine answers as evidence.

No tenants, authenticated catalogs, subscriptions, deployments, negotiated
prices, or actual quota availability were queried. No agents were run.
The guidance is documentary, not a certification.

## Evidence hierarchy

1. The Microsoft Learn page specific to the feature and generation.
2. Official quickstarts and samples compatible with the SDK version under consideration.
3. Microsoft Tech Community blogs for patterns and explanations.
4. Lab proposals, explicitly identified as such.

A blog example does not prove that an API exists. In particular,
`ToolContext`, `ToolGrant`, and application controls in the least-privilege
blog are the author's examples, not classes to assume are present in the SDK.
Source: [S09](sources.md#s09).

General web searches experienced intermittent timeouts. The baseline uses
directly retrieved pages and the specific sources consulted in delegated
research; it does not claim to be a complete inventory of all releases.

## Claim labels

| Label                | Meaning                                                           |
| -------------------- | ----------------------------------------------------------------- |
| Documented           | The source describes the capability; does not imply GA            |
| Explicit preview     | The feature is marked preview in the relevant text                |
| Prerelease SDK       | The path requires an unstable package version                     |
| Retirement announced | The source announces a retirement date                            |
| Lab proposal         | Architecture, convention, or threshold chosen for the future demo |
| To be verified       | Sufficient documentary evidence or a tenant test is missing       |

> [!WARNING]
> The "Items marked preview..." banner applies to items marked as such.
> It does not automatically make every API cited on the page preview.
> Conversely, the absence of a preview tag is not proof of GA.

The status of the service, library, protocol, individual tool, and feature
can differ. There is no single "Foundry is GA" status that resolves the matrix.

## How to cite

Each group of product claims includes an `Sxx` link to the
[register](sources.md). Entries specify the title, URL, relevant section,
page date when retrieved, and verification limitations.

`ms.date` is editorial metadata; `updated_at` is the page update.
Neither is automatically the product release date.
Dates that were not retrieved are not reported.

When two sources diverge, the specific guide most relevant to the chosen
path takes precedence. The discrepancy remains an open question; it is not
hidden behind an invented "average" version.

## Proposed maintenance

* Before each milestone: reread sources for the runtimes, SDKs, and tools in use.
* Before each deployment: verify the region, model, quota, roles, and prices.
* Monthly during study: check retirements, new previews, and SDKs.
* Whenever a contract or dependency changes: update the guide and tests together.

A significant change must record:

1. Source and date of the new verification.
2. Changed claim and impact on the demo.
3. Decision: adopt, isolate behind a flag, experiment, or do not use.
4. Required technical evidence and result, when available.

## Documentary and technical checks

Documentary checks cover local links, anchors, citations, metadata,
and scope consistency. Public links remain subject to change.

Technical checks are defined in the
[roadmap](../demo/validation-roadmap.md): they must produce persistent,
repeatable evidence. The mere presence of a guide does not close a spike.

Full dumps of third-party documentation, tokens, sensitive payloads,
or real-user telemetry are not stored in the repository.
