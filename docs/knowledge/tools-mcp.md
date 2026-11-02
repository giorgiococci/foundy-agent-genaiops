---
title: Tools, MCP, and Toolbox
description: Capability contracts, MCP integration, and criteria for avoiding an unnecessary server.
ms.date: 2026-11-02
status: research-baseline
---

## What MCP solves

Foundry documents connections to MCP servers and a Toolbox that exposes
tools through a managed MCP endpoint. MCP provides an integration
contract; it does not decide which records a user may read or modify.
Sources: [S12](../research/sources.md#s12),
[S13](../research/sources.md#s13).

| Integration            | Prefer it when                                       | Limitation to manage                         |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------- |
| Typed local function   | A capability belongs to a single runtime             | Coupling and process identity                |
| Foundry managed tool   | The required capability is already supported         | Model/region/auth constraints                |
| Business API / OpenAPI | A reliable application contract already exists       | Authorization and error handling             |
| Custom MCP server      | Reuse and an explicit capability boundary are needed | Server, auth, lifecycle, versions, and tests |

The table proposes selection criteria, not a product requirement.

## Toolbox does not mean APIM

Toolbox is a Foundry capability for curating tools, authentication,
and versions behind a managed endpoint. For hosted agents with Agent Framework,
the guide recommends `FoundryToolbox` in Python or `AddFoundryToolboxes`
in .NET, rather than assuming a generic MCP client is equivalent.
Source: [S13](../research/sources.md#s13).

APIM is not required in the Toolbox path studied here.
Any AI Gateway/external onboarding paths that require it
are out of scope. End-to-end compatibility without APIM must
be verified in the spike.

## Connection identity

The documentation lists `none`, `custom-keys`, `oauth2`,
`user-entra-token`, `project-managed-identity`, and `agentic-identity`.
Actual support depends on the tool type.
Source: [S11](../research/sources.md#s11).

* `oauth2` uses a user authorization flow; Foundry manages the resulting
  credentials and refresh according to the documented path.
* `user-entra-token` forwards an Entra token to the service for the
  downstream audience, representing the authenticated user.
* Project or agent identity enables application operations,
  but does not by itself reconstruct an individual user's permissions.

Do not generically call every passthrough "OBO". The hosted page
explicitly describes interactive OBO scenarios, but the implementation
of the selected path must be verified. Do not forward a received bearer
token to a different audience.
Sources: [S03](../research/sources.md#s03),
[S11](../research/sources.md#s11).

## Proposed tool contract

Prefer capabilities such as `get_case(case_id)`, `search_policy(query)`,
and `create_case_note(case_id, proposal_id, idempotency_key)`.
Do not expose `execute_sql`, `fetch_any_url`, `run_shell`, or
`tenant_id`, `account_url`, `container` parameters freely chosen by the model.

Each tool must declare inputs, outputs, required identity, accessible
data, preconditions, side effects, timeouts, and limits. A syntactically
valid ID still requires record-level authorization.

The endpoint and resource are bound server-side. Identity context
comes from verified tokens and middleware, not agent-generated JSON.
This applies the pattern in
[S09](../research/sources.md#s09) to the future demo.

## Proposed MCP flow

1. The runtime authenticates the caller to the intended endpoint.
2. Toolbox/the connection applies the supported auth mode.
3. The MCP server validates the credentials and context actually received.
4. Application policy resolves the capability, user, and data scope.
5. The tool validates the schema and parameters and accesses the backend with least privilege.
6. The server records the decision and outcome without sensitive payloads.

> [!IMPORTANT]
> Do not assume that all identities traverse every hop.
> If the server sees only a shared identity, it cannot distinguish
> specialists by their name in the prompt or by an untrusted header.

The token identifies the principal actually authenticated. Authorizing
the original caller as well requires verifiable propagation
or separate identities/connections. An `agent-name` header is
diagnostic metadata, not proof.

## Different approvals

Keep OAuth consent, MCP invocation approval, and business approval
of a change separate. Authorizing a connection
does not approve all future actions performed through that connection.
Source for the MCP path: [S12](../research/sources.md#s12).

The demo must not disable approvals globally to smooth out
the happy path. Reads can be automatic after policy checks;
changes require the proof of approval defined by the domain.

## Networking and failures

The MCP guide includes private endpoints with specific networking
prerequisites, including a dedicated/delegated subnet in the documented path.
Exposing a local server publicly is not enough to call it "enterprise".
Sources: [S12](../research/sources.md#s12),
[S15](../research/sources.md#s15).

Proposal: pin the schema and server version, allowlist destinations,
set timeouts and a maximum response size, and fail closed.
An auth error or required consent must be visible to the caller,
not translated into an empty result and then "no data found".

A tool result is untrusted data: text retrieved from a document
or note cannot change instructions, permissions, or destinations.
