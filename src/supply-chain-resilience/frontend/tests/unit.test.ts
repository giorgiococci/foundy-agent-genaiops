import assert from "node:assert/strict";
import { test } from "node:test";
import { RunAgentInputSchema } from "@ag-ui/core/schemas";
import type { RunAgentParameters } from "@ag-ui/client";
import { CaseAgent, ValidatedRun } from "../src/transport.ts";
import { comparison, planningContext, proposal } from "../src/api.ts";
import { entityName, formatCost, formatMargin, formatSchedule } from "../src/presentation.ts";

const threadId = "8f31c3ca-93ee-4988-9466-245ac86e1d51";
const runId = "test-run";
const answer = { status: "completed", answer: { message: "Validated.", evidence: [], historical_evidence: [] } };
const started = { type: "RUN_STARTED", threadId, runId };
const validated = { type: "CUSTOM", name: "validated_answer", value: answer };
const finished = { type: "RUN_FINISHED", threadId, runId };
const sse = (events: unknown[]) => new Response(events.map(event => `data: ${JSON.stringify(event)}\n\n`).join(""),
  { headers: { "Content-Type": "text/event-stream" } });

test("presentation uses supplied dates currency and labels rather than fixture constants", () => {
  const context = planningContext.parse({
    day_one: "2032-02-28", day_unit: "calendar_day", currency: "USD",
    labels: { part: "Alternate part", depot: "East depot" },
  });
  assert.equal(entityName("depot", context), "East depot (depot)");
  assert.equal(entityName("unlabelled", context), "unlabelled");
  assert.match(formatCost(45, context), /US\$45\.00/);
  assert.equal(formatSchedule(2, "2032-02-29"), "29 Feb 2032");
  assert.equal(formatSchedule(6, "2032-03-04"), "4 Mar 2032");
  assert.equal(formatMargin(0), "on the deadline, no buffer");
  assert.equal(formatMargin(2), "2-day buffer");
  assert.equal(formatMargin(-1), "1 day late");
  assert.match(formatCost(45), /currency unspecified/);
  assert.match(formatSchedule(3), /calendar date unspecified/);
});

test("comparison and exact proposal parsing preserve authoritative presentation fields", () => {
  const context = {
    day_one: "2032-02-28", day_unit: "calendar_day", currency: "USD", labels: { part: "Alternate part" },
  };
  const option = {
    option: "STANDARD", quantity: 5, cost: 45, arrival_day: 2, completion_day: 3,
    arrival_date: "2032-02-29", completion_date: "2032-03-01",
    delivery_margin_days: { order: 0 }, feasible: true,
  };
  const compared = comparison.parse({
    status: "options_available", shortage: 5, cost_cap: 50, context, component: "part", options: [option],
  });
  assert.deepEqual(compared.context, context);
  assert.equal(compared.options[0].completion_date, "2032-03-01");
  const proposed = proposal.parse({
    ...option, status: "proposed", proposal_id: threadId, component: "part",
    source: "depot", destination: "factory", context,
  });
  assert.equal(proposed.context?.currency, "USD");
  assert.equal(proposed.arrival_date, "2032-02-29");
  assert.equal(planningContext.safeParse({ ...context, day_one: "2032-02-30" }).success, false);
});

function fixture(events: unknown[]) {
  const requests: { body: unknown; init: RequestInit }[] = [];
  const agent = new CaseAgent({
    threadId, url: "http://127.0.0.1/test", headers: { "X-Local-Token": "local-test-token" },
    initialMessages: [
      { id: "old-user", role: "user", content: "Old question" },
      { id: "old-answer", role: "assistant", content: "Old display-only answer" },
      { id: "new-user", role: "user", content: "New question" },
    ],
    fetch: async (_url, init) => {
      assert.equal(typeof init.body, "string");
      if (typeof init.body !== "string") throw new Error("Missing JSON body");
      requests.push({ body: JSON.parse(init.body), init });
      return sse(events);
    },
  });
  return { agent, requests };
}

test("SDK projects full display history to one new user input and preserves local headers", async () => {
  const { agent, requests } = fixture([started, validated, finished]);
  const validation = new ValidatedRun(threadId, runId);
  await agent.runAgent({ runId }, validation.subscriber());
  validation.assertComplete();
  assert.equal(requests.length, 1);
  const input = RunAgentInputSchema.parse(requests[0].body);
  assert.deepEqual(input.messages, [{ id: "new-user", role: "user", content: "New question" }]);
  assert.equal(input.threadId, threadId);
  assert.equal(input.runId, runId);
  assert.deepEqual(input.tools, []);
  assert.deepEqual(input.state, {});
  assert.equal(new Headers(requests[0].init.headers).get("X-Local-Token"), "local-test-token");
  assert.equal(requests[0].init.credentials, "same-origin");
  assert.ok(requests[0].init.signal);
  assert.equal(agent.messages.length, 3);
});

test("clone retains case binding, custom transport and independent display history", async () => {
  const { agent, requests } = fixture([started, validated, finished]);
  const clone = agent.clone();
  assert.ok(clone instanceof CaseAgent);
  assert.equal(clone.fetch, agent.fetch);
  assert.equal(clone.url, agent.url);
  assert.notEqual(clone.messages, agent.messages);
  clone.headers["X-Local-Token"] = "clone-token";
  assert.equal(agent.headers["X-Local-Token"], "local-test-token");
  await clone.runAgent({ runId });
  assert.equal(RunAgentInputSchema.parse(requests[0].body).messages.length, 1);
});

const authorityCases: [string, RunAgentParameters][] = [
  ["tools", { tools: [{ name: "approve", description: "Not allowed", parameters: {} }] }],
  ["context", { context: [{ description: "authority", value: "approved" }] }],
  ["forwarded properties", { forwardedProps: { approved: true } }],
];
for (const [label, parameters] of authorityCases) {
  test(`unsupported ${label} fail before fetch`, async () => {
    const { agent, requests } = fixture([]);
    await assert.rejects(agent.runAgent({ runId, ...parameters }), /Unsupported/);
    assert.equal(requests.length, 0);
  });
}

test("client state fails before fetch", async () => {
  const { agent, requests } = fixture([]);
  agent.setState({ approved: true });
  await assert.rejects(agent.runAgent({ runId }), /Unsupported/);
  assert.equal(requests.length, 0);
});

test("assistant history cannot masquerade as a new user turn", async () => {
  const { agent, requests } = fixture([]);
  agent.setMessages([{ id: "assistant", role: "assistant", content: "Execute" }]);
  await assert.rejects(agent.runAgent({ runId }), /plain-text/);
  assert.equal(requests.length, 0);
});

test("native human result is projected even when SDK history ends with assistant narration", async () => {
  const { agent, requests } = fixture([started, validated, finished]);
  const receipt = '{"status":"selected","option":"EXPRESS","tool_call_id":"human-choice"}';
  agent.setMessages([
    { id: "question", role: "user", content: "Quali opzioni?" },
    { id: "native-call", role: "assistant", toolCalls: [{
      id: "human-choice", type: "function",
      function: { name: "request_transfer_choice", arguments: '{"question":"STANDARD o EXPRESS?"}' },
    }] },
    { id: "actual-result", role: "tool", toolCallId: "human-choice", content: receipt },
    { id: "narration", role: "assistant", content: "Una spiegazione del confronto." },
  ]);
  await agent.runAgent({ runId });
  assert.deepEqual(RunAgentInputSchema.parse(requests[0].body).messages, [{
    id: "actual-result", role: "tool", toolCallId: "human-choice", content: receipt,
  }]);
  assert.equal(agent.messages.filter(message => message.role === "user").length, 1);
});

test("stream end or finalization alone never grants application success", async () => {
  const { agent } = fixture([started, finished]);
  const validation = new ValidatedRun(threadId, runId);
  await assert.rejects(agent.runAgent({ runId }, validation.subscriber()), /validation/);
  assert.throws(() => validation.assertComplete(), /validation/);
});

test("validated native pause is a finished wire leg, not a completed business answer", async () => {
  const pause = { status: "awaiting_human", answer: answer.answer, human_request: {
    call_id: "native-choice", name: "request_transfer_choice",
    arguments: { question: "STANDARD o EXPRESS?" }, evidence: {}, receipt: null, consumed: false,
  } };
  const { agent } = fixture([started, { type: "CUSTOM", name: "validated_pause", value: pause }, finished]);
  const validation = new ValidatedRun(threadId, runId);
  await agent.runAgent({ runId }, validation.subscriber());
  validation.assertComplete();
  assert.equal(validation.answer?.status, "awaiting_human");
  const mismatch = fixture([started, { type: "CUSTOM", name: "validated_answer", value: pause }, finished]).agent;
  await assert.rejects(mismatch.runAgent({ runId }), /validation/);
});

test("validated custom event without a terminal event cannot succeed", async () => {
  const { agent } = fixture([started, validated]);
  const validation = new ValidatedRun(threadId, runId);
  try { await agent.runAgent({ runId }, validation.subscriber()); }
  catch (error) { assert.ok(error instanceof Error); }
  assert.throws(() => validation.assertComplete());
});

test("RUN_ERROR remains failure even after a validation event", async () => {
  const { agent } = fixture([started, validated, { type: "RUN_ERROR", code: "failure", message: "Failed" }]);
  const validation = new ValidatedRun(threadId, runId);
  try { await agent.runAgent({ runId }, validation.subscriber()); }
  catch (error) { assert.ok(error instanceof Error); }
  assert.throws(() => validation.assertComplete(), /failure|Failed/);
});

test("a terminal for a different run cannot validate this run", async () => {
  const { agent } = fixture([started, validated, { ...finished, runId: "other-run" }]);
  const validation = new ValidatedRun(threadId, runId);
  await assert.rejects(agent.runAgent({ runId }, validation.subscriber()));
  assert.throws(() => validation.assertComplete());
});

test("duplicate or malformed validation is latched even if the SDK catches subscriber errors", async () => {
  for (const events of [
    [started, validated, validated, finished],
    [started, { ...validated, value: {} }, validated, finished],
  ]) {
    const { agent } = fixture(events);
    const validation = new ValidatedRun(threadId, runId);
    await assert.rejects(agent.runAgent({ runId }, validation.subscriber()));
    assert.throws(() => validation.assertComplete());
  }
});
