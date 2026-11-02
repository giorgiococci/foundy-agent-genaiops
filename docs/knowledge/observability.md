---
title: End-to-end observability
description: OpenTelemetry, Application Insights, dashboards, privacy, and multi-agent correlation tests.
ms.date: 2026-11-02
status: research-baseline
---

## Three layers to connect

1. Runtime: requests, dependencies, exceptions, latency, and availability.
2. Agentic process: steps, model/tool calls, budgets, and approvals.
3. Outcome: task correctness, groundedness, policy compliance, and business impact.

Traces and operational metrics cover behavior; evaluations
measure quality against explicit criteria. A run without exceptions
can still be semantically wrong.
Sources: [S18](../research/sources.md#s18),
[S19](../research/sources.md#s19), [S21](../research/sources.md#s21).

## Documented path

Foundry describes server-side tracing in the portal and client-side tracing
to add visibility into our code. Exports can go to
Application Insights, the console, or compatible OTLP backends.
The Foundry SDK's GenAI instrumentation is in experimental preview.
Source: [S18](../research/sources.md#s18).

For Python, the guide requires opting in with
`AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` before
`AIProjectInstrumentor` instrumentation. Other languages have
specific configurations; do not translate options by analogy.
Source: [S18](../research/sources.md#s18).

Agent Framework emits traces, metrics, and logs following the OTel GenAI
semantic conventions. The guide warns that instrumenting both client and
agent can duplicate information, especially sensitive data.
Source: [S20](../research/sources.md#s20).

Proposal: one exporter/configurator per process, with instrumentation
scope coverage verified. Do not enable all libraries
at once without checking for duplicate spans and token counts.

## Proposed multi-agent trace

```text
request
  authenticate-and-authorize
  workflow
    evidence-agent
      model-call
      search-policy
    analysis-agent
      model-call
      get-case
    join-and-validate
    create-proposal
  response

approval-request
  validate-approver
  validate-proposal
  execute-idempotent-command
```

Human approval time must not inflate the latency of the first
result. Two traces can be connected through run/proposal IDs and span
links, rather than a single span kept open for hours. IDs provide correlation,
not authorization.

W3C `traceparent`/`tracestate` propagation is documented in the Foundry
guide, with Python-specific configuration and standard
Activity behavior in .NET. This does not prove that every MCP, queue, or A2A hop is connected.
An actual test through the chosen services is required.
Source: [S18](../research/sources.md#s18).

## Lab telemetry contract

Proposed attributes, in the application namespace `lab.*` to avoid inventing
standard OTel attributes:

| Field                     | Purpose                             | Precaution                                        |
| ------------------------- | ----------------------------------- | ------------------------------------------------- |
| `lab.run_id`              | Correlate the business request      | Do not use as a secret or permission              |
| `lab.agent_version`       | Identify runtime configuration      | Use the resolved version, not a generic alias     |
| `lab.tool_schema_version` | Reconstruct the tool contract       | Avoid the complete schema in the span             |
| `lab.policy_version`      | Reconstruct a decision              | No sensitive rule details                         |
| `lab.authz_decision`      | Allow/deny with a reason code       | No bearer tokens or claim dumps                   |
| `lab.outcome`             | Success, denied, incomplete, failed | Distinguish expected denies from technical errors |
| `lab.dataset_version`     | Correlate an offline evaluation     | Evaluation runs only                              |
| `lab.release_id`          | Join traces, code, and manifest     | Cardinality limited to releases                   |

For model, tokens, and latency, reuse the OTel fields supported by
the chosen version. Do not copy names from an experimental convention without
pinning its version and mapping.

High-cardinality identifiers, such as run/proposal IDs, belong
in traces or audit records, not in aggregate metric dimensions.
Do not record chain-of-thought; outcomes, evidence, external decisions,
and reason codes are sufficient.

## Telemetry privacy

The Foundry guide notes that content recording can capture prompts,
responses, and tool arguments. In Python, the documented option is
`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`, disabled
by default; other SDKs use their own options.
Source: [S18](../research/sources.md#s18).

Proposal: content OFF even in cloud demos; any debugging should use
synthetic data, be explicit and time-limited, and include deletion verification.
Also check decorators and custom spans: capturing parameters or return
values can reintroduce data that the GenAI flag does not record.

Baggage is disabled by default in the Python guide and can expose
PII. Do not add tokens, names, email addresses, document text, or ACLs.
Source: [S18](../research/sources.md#s18).

Redaction must happen before export. A query that hides
an already ingested value does not remove it from storage.
Define retention, access, and deletion for logs and derived datasets.

## Dashboards and access

The Agent Monitoring Dashboard uses the Application Insights instance linked
to the project. The guide distinguishes tokens, latency, run success, evaluation,
and red team. Metric views and recurring evaluation, scan, and
alert features are marked preview.
Source: [S19](../research/sources.md#s19).

Access to telemetry and, for log-based views, to the corresponding
workspace is required. The guides reference Log Analytics Reader and, for
protected tables, Privileged Monitoring Data Reader. A Foundry role alone
does not demonstrate access to logs.
Sources: [S18](../research/sources.md#s18),
[S19](../research/sources.md#s19).

Proposal without APIM: App Insights/Azure Monitor remain the
baseline backend. The Foundry dashboard is an additional view to verify.
Do not introduce AI Gateway as a prerequisite for monitoring
an external runtime; if native integration requires an out-of-scope
path, retain OTel/App Insights visibility and declare the gap.

## Proposed metrics and alerts

* p50/p95 latency of the first result, separate from HITL waiting time
* Errors by dependency, throttling, retries, and timeouts
* Tokens by agent/model, runs, and tool calls
* Denies by reason code and attempted unauthorized actions
* Percentage of tasks completed correctly on the dataset
* Count of business effects and prevented replays
* Runs missing expected telemetry and exporter failures

Do not use the dashboard guide's 10 seconds or 95% as an SLA.
These are general diagnostic guidelines, not targets for this workflow.
Source: [S19](../research/sources.md#s19).

Proposal: alert on exporter failures and unavailable audit; business
changes must fail explicitly if they cannot
record the required audit. For reads, define and report
degradation instead of producing false observability evidence.

## Required tests

1. Reconstruct a happy path and a deny from request to backend.
2. Verify parent/child relationships or span links across processes, not just the same run ID.
3. Simulate timeouts and 429 responses and observe retries within limits.
4. Confirm that metrics and costs do not count the same spans twice.
5. Search for a synthetic canary in logs, traces, errors, and artifacts: zero occurrences.
6. Disable the exporter/backend and verify degradation reporting.

None of these tests were performed during the research phase.
