import assert from "node:assert/strict";
import { test } from "node:test";
import { RunAgentInputSchema } from "@ag-ui/core/schemas";
import { CopilotKitCore } from "@copilotkit/core";
import { z } from "zod";
import { bootstrapSchema, caseSchema } from "../src/api.ts";
import type { CaseView } from "../src/api.ts";
import { CaseAgent, ValidatedRun } from "../src/transport.ts";

const origin = process.env.UI_FIXTURE_URL;
if (!origin || new URL(origin).hostname !== "127.0.0.1") {
  throw new Error("Set UI_FIXTURE_URL to the explicitly offline loopback fixture.");
}
const base = origin;
const bootstrap = bootstrapSchema.parse(await (await fetch(`${base}/api/bootstrap`)).json());
assert.equal(bootstrap.service_mode, "offline-test-fixture", "Never execute this suite against real Foundry.");
const headers = { "Content-Type": "application/json", "X-Local-Token": bootstrap.action_token, Origin: base };
const interactionKind = (view: CaseView) => view.interaction?.kind ?? null;
async function create() {
  return caseSchema.parse(await (await fetch(`${base}/api/cases`, { method: "POST", headers, body: "{}" })).json());
}
async function inspect(id: string) {
  return caseSchema.parse(await (await fetch(`${base}/api/cases/${id}`)).json());
}

test("actual CopilotKit core automatically continues two native human tools over Python SSE", async () => {
  let view = await create();
  assert.equal(interactionKind(view), null);
  const requests: unknown[] = [];
  const transport = new CaseAgent({
    url: `${base}/api/cases/${view.id}/run`, threadId: view.id, headers,
    fetch: async (url, init) => {
      if (typeof init.body !== "string") throw new Error("Expected JSON body");
      requests.push(JSON.parse(init.body));
      return fetch(url, init);
    },
  });
  const core = new CopilotKitCore({ agents__unsafe_dev_only: { advisor: transport } });
  const agent = core.getAgent("advisor");
  assert.ok(agent instanceof CaseAgent);
  agent.onValidated = async () => { view = await inspect(view.id); };
  let decisions = 0;
  async function act(body: object, callId: string) {
    const before = requests.length;
    const usage = JSON.stringify(view.usage);
    const result = await fetch(`${base}/api/cases/${view.id}/actions`, {
      method: "POST", headers, body: JSON.stringify({ ...body, tool_call_id: callId }),
    });
    assert.equal(result.status, 200, await result.clone().text());
    view = caseSchema.parse(await result.json());
    assert.equal(requests.length, before);
    assert.equal(JSON.stringify(view.usage), usage, "A decision alone cannot infer.");
    decisions++;
    return view.pending_human?.receipt;
  }
  const premature = await fetch(`${base}/api/cases/${view.id}/actions`, {
    method: "POST", headers, body: JSON.stringify({ action: "select", option: "STANDARD" }),
  });
  assert.equal(premature.status, 409);
  core.setTools([
    { name: "request_transfer_choice", type: "human-in-the-loop", agentId: "advisor",
      parameters: z.object({ question: z.string() }),
      handler: async (_args, { toolCall }) => {
        assert.equal(interactionKind(view), "select");
        return act({ action: "select", option: "STANDARD" }, toolCall.id);
      } },
    { name: "request_transfer_approval", type: "human-in-the-loop", agentId: "advisor",
      parameters: z.object({ question: z.string(), proposal_id: z.string() }),
      handler: async (args, { toolCall }) => {
        assert.equal(interactionKind(view), "approve");
        assert.equal(args.proposal_id, view.decisions.proposal_id);
        return act({ action: "approve", proposal_id: args.proposal_id, confirm: true }, toolCall.id);
      } },
  ]);
  agent.addMessage({ id: crypto.randomUUID(), role: "user", content: "Quali opzioni abbiamo?" });
  await core.runAgent({ agent });
  assert.equal(decisions, 2);
  assert.equal(view.running, false);
  assert.equal(view.blocked, null);
  assert.equal(interactionKind(view), null);
  assert.deepEqual(view.snapshot.source, { warehouse: "W-B", on_hand: 80, reserved: 70, available: 10 });
  assert.deepEqual(view.snapshot.local, { warehouse: "W-A", on_hand: 20 });
  assert.equal(requests.length, 3);
  for (const body of requests) assert.equal(RunAgentInputSchema.parse(body).messages.length, 1);
  assert.deepEqual(view.history.map(entry => entry.role), ["user", "assistant", "tool", "assistant", "tool", "assistant"]);
  const roles = requests.map(body => RunAgentInputSchema.parse(body).messages[0].role);
  assert.deepEqual(roles, ["user", "tool", "tool"]);
  assert.equal(agent.messages.filter(message => message.role === "user").length, 1);
});

test("local action token, Origin and raw whole-history boundaries remain enforced", async () => {
  assert.equal((await fetch(`${base}/api/cases`, { method: "POST", body: "{}" })).status, 403);
  assert.equal((await fetch(`${base}/api/cases`, {
    method: "POST", headers: { ...headers, Origin: "https://not-local.example" }, body: "{}",
  })).status, 403);
  const view = await create();
  const response = await fetch(`${base}/api/cases/${view.id}/run`, {
    method: "POST", headers, body: JSON.stringify({
      threadId: view.id, runId: crypto.randomUUID(), tools: [], state: {}, context: [], forwardedProps: {},
      messages: [
        { id: "a", role: "user", content: "Old" },
        { id: "b", role: "user", content: "New" },
      ],
    }),
  });
  assert.equal(response.status, 409);
  assert.equal((await inspect(view.id)).history.length, 0);
});

test("abort is never reported as validated and the durable uncertain case cannot replay", async () => {
  const view: CaseView = await create();
  const agent = new CaseAgent({ url: `${base}/api/cases/${view.id}/run`, threadId: view.id, headers });
  agent.addMessage({ id: crypto.randomUUID(), role: "user", content: "Inspect then stop." });
  const validation = new ValidatedRun(view.id, crypto.randomUUID());
  try {
    await agent.runAgent({ runId: validation.runId }, {
      ...validation.subscriber(),
      onTextMessageContentEvent: () => { agent.abortRun(); },
    });
  } catch (error) { assert.ok(error instanceof Error); }
  assert.throws(() => validation.assertComplete());
  const stopped = await inspect(view.id);
  assert.ok(stopped.blocked);
  assert.equal(stopped.interaction, null);
});
