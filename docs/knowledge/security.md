---
title: Security and least privilege
description: Identity, capabilities, authorization, trust boundaries, and negative tests for the demo.
ms.date: 2026-11-02
status: research-baseline
---

## Guiding principle

The agent proposes a call. The system authorizes the operation.
The model is not a trusted source for principal, tenant, scope, or approval.

The starting blog proposes narrow capability contracts, appropriate identities,
server-side resource binding, and deny-path tests. These are application
patterns that complement platform controls.
Source: [S09](../research/sources.md#s09).

## Separate identities

| Identity                 | Responsibility                              | Must not implicitly become                        |
| ------------------------ | ------------------------------------------- | ------------------------------------------------- |
| Developer/deployer       | Create resources, versions, and assignments | A runtime identity with administrative privileges |
| End user                 | Request and approve within their rights     | The owner of all project data                     |
| Project managed identity | Intended infrastructure operations          | User or agent authority in every tool             |
| Hosted agent identity    | Inference and assigned runtime access       | Unlimited access to downstream services           |
| Tool/backend identity    | Minimum access to service data              | A privileged proxy for any request                |

Hosted documentation describes a dedicated Entra identity per agent and
distinguishes the runtime identity from the project managed identity, also
used for infrastructure operations such as registry access.
Source: [S03](../research/sources.md#s03).

Tool connections support different modes, including project identity,
agentic identity, and user tokens. You must test which principal
actually reaches the tool, not infer it from the interface.
Source: [S11](../research/sources.md#s11).

### Foundry roles

The current guide distinguishes management and consumption roles, including
Foundry Agent Consumer. Recent role renaming may leave
samples or screenshots with previous names; check role definitions and scopes.
Agent scope is described for access to the agent endpoint, not for
all data accessed by the agent.
Source: [S10](../research/sources.md#s10).

Do not assign Owner/Contributor to the runtime to get past a 403 error.
Identify the minimum operation, principal, and scope. Broad provisioning
instructions in quickstarts are not a production IAM model.

## Three complementary layers

1. Exposing only the necessary tools to the model reduces the surface.
2. Authorizing the action, resource, and user server-side prevents misuse.
3. Restricting the downstream identity with RBAC contains the impact of errors.

Hiding `delete_case` from the tool list does not prevent an
overprivileged credential from deleting a record through another path.
An Azure read role does not by itself implement business
authorization between users sharing the same resource.
Sources: [S09](../research/sources.md#s09),
[S10](../research/sources.md#s10).

## Proposed capability contract

For each operation, record:

* Permitted authenticated principals and token audience
* Business action and authorized resource/partition
* Need for delegated user identity
* Conditions, limits, and policy version
* Permitted effects and approval requirements
* Audit evidence, timeouts, and error behavior

Tenant, user, and agent identity must be resolved from verified credentials.
Do not trust custom headers or model arguments. If the path
uses a shared connection that loses the original identity, do not
implement false per-agent security based on the specialist's name.

The server binds endpoints, accounts, and containers to trusted configuration.
Business IDs and paths must be validated against traversal, unauthorized
resources, and out-of-scope references.
Pattern source: [S09](../research/sources.md#s09).

## Initial demo threat model

The table is a proposed threat model, not an audit of existing code.

| Threat                            | Trust boundary                 | Control to implement and test                     |
| --------------------------------- | ------------------------------ | ------------------------------------------------- |
| Prompt injection in a note        | Retrieved data -> instructions | Untrusted data, narrow tools, external policy     |
| Confused deputy                   | Agent -> privileged tool       | Verified principal and server-side business scope |
| Access to another user's case     | Tool -> record                 | Record ACL/ownership, not just ID validation      |
| SSRF or exfiltration via URL      | Tool parameter -> network      | No arbitrary URLs, allowlist, and egress controls |
| Write without approval            | Proposal -> executor           | Approval record bound to the action               |
| Replay after timeout              | Client retry -> side effect    | Idempotency and state reconciliation              |
| Leakage in traces                 | Application -> telemetry       | Content capture off, redaction, restricted access |
| Upload that changes configuration | Session filesystem -> program  | Trusted paths separate from uploads               |
| Compromised dependency            | Build -> runtime image         | Pinned versions, scanning, provenance, and digest |
| Costly loop or fan-out            | Orchestrator -> models/tools   | Deadlines, application quotas, and kill switch    |

Product references: [S03](../research/sources.md#s03),
[S09](../research/sources.md#s09), [S14](../research/sources.md#s14),
[S15](../research/sources.md#s15), [S18](../research/sources.md#s18).

## Approvals and effects

Proposal: the server stores an approval with the proposal ID, hash of the
approved content, target, action, approver, expiration, and status.
The LLM cannot issue a valid approval. Changing the proposal
invalidates the previous approval.

The executor checks current authorization, preconditions, and idempotency
before the effect. Reusing the same key for the same operation
may return the already recorded outcome, but does not create a second effect.
A key reused with a different payload is rejected.

Resuming after a checkpoint must preserve these constraints. Do not promise
exactly-once execution merely because a persistent workflow is available.

## Networking without APIM

The documented default for Agent Service is public. Public egress,
BYO VNet, and managed VNet are distinct choices. A private endpoint
protects ingress according to configuration; it does not isolate egress by itself.
Source: [S15](../research/sources.md#s15).

Two-profile proposal:

* Study profile: synthetic data only, authenticated endpoints, no anonymous
  access to business tools, and destination restrictions in code
* Hardening profile: private access and egress controls verified for
  the project, registry, data, and tools; costs and dependencies documented

No security equivalence is claimed between the two profiles. Authenticated
public networking is not private networking. Excluding APIM does not remove
the need for auth, rate limiting, validation, audit, and data isolation.

## Credentials and supply chain

In the cloud, prefer explicit credentials appropriate for the runtime; avoid
unintended fallbacks in the development credential chain. The framework guide warns about
`DefaultAzureCredential` in production.
Source: [S20](../research/sources.md#s20).

Do not put secrets in images, prompts, tool arguments, traces, or Git files.
For hosted agents, the guide recommends managed identity, connections, and secret stores,
not secrets in container environment variables.
Source: [S03](../research/sources.md#s03).

Proposal: reproducible builds, immutable digests, pinned dependencies,
image scanning, and review of schema/tool changes. A new
tool or scope is an authorization change that must be reviewed.

## Proposed mandatory negative tests

1. Missing or expired token, wrong audience or issuer: authentication denied.
2. Valid principal without the capability: denied before data access.
3. Case outside ownership/scope: no data, no side effects.
4. Forged `tenant_id` or `agent_name`: no change to effective rights.
5. Arbitrary accounts/containers/paths: rejected or impossible under the contract.
6. Read-only agent attempting a write: application and IAM denial.
7. Document ordering data exfiltration: no calls outside the allowlist.
8. Missing or expired approval, or approval for another proposal: no changes.
9. Retry and replay: at most one business effect per approved operation.
10. Sensitive canary in payloads: absent from traces, logs, and publishable artifacts.

Each test must verify both the application outcome and backend state.
An "unauthorized" message is not enough if a write has already occurred.
