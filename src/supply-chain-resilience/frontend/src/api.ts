import { z } from "zod";
import type { Message } from "@ag-ui/core";

export const validatedAnswer = z.object({
  status: z.literal("completed"),
  answer: z.object({
    message: z.string().min(1),
    evidence: z.array(z.record(z.unknown())),
    historical_evidence: z.array(z.record(z.unknown())),
  }),
}).passthrough();

export const humanRequest = z.object({
  call_id: z.string().min(1),
  name: z.enum(["request_transfer_choice", "request_transfer_approval"]),
  arguments: z.object({ question: z.string().min(1), proposal_id: z.string().optional() }),
  evidence: z.record(z.unknown()),
  receipt: z.record(z.unknown()).nullable(),
  consumed: z.boolean(),
});
export const validatedPause = z.object({
  status: z.literal("awaiting_human"),
  answer: validatedAnswer.shape.answer,
  human_request: humanRequest,
}).passthrough();
export const validatedOutcome = z.discriminatedUnion("status", [validatedAnswer, validatedPause]);
export type ValidatedOutcome = z.infer<typeof validatedOutcome>;

export const bootstrapSchema = z.object({
  action_token: z.string().min(1),
  cases: z.array(z.string().uuid()),
  inference_enabled: z.boolean(),
  service_mode: z.enum(["offline-test-fixture", "managed-foundry"]),
  agent_version: z.string().min(1),
  deployment: z.string().min(1),
  telemetry: z.string(),
});

const optionSchema = z.enum(["STANDARD", "EXPRESS"]);
export const planningContext = z.object({
  day_one: z.string().date(),
  day_unit: z.literal("calendar_day"),
  currency: z.string().regex(/^[A-Z]{3}$/),
  labels: z.record(z.string().min(1)),
});
export type PlanningContext = z.infer<typeof planningContext>;
export const comparison = z.object({
  status: z.literal("options_available"),
  shortage: z.number(),
  cost_cap: z.number(),
  component: z.string().optional(),
  context: planningContext.optional(),
  options: z.array(z.object({
    option: optionSchema,
    quantity: z.number(),
    cost: z.number(),
    arrival_day: z.number(),
    completion_day: z.number(),
    arrival_date: z.string().date().optional(),
    completion_date: z.string().date().optional(),
    delivery_margin_days: z.record(z.number()),
    feasible: z.boolean(),
  })),
});
export const proposal = z.object({
  status: z.literal("proposed"),
  proposal_id: z.string().uuid(),
  option: optionSchema,
  quantity: z.number(),
  component: z.string(),
  source: z.string(),
  destination: z.string(),
  cost: z.number(),
  arrival_day: z.number(),
  completion_day: z.number(),
  context: planningContext.optional(),
  arrival_date: z.string().date().optional(),
  completion_date: z.string().date().optional(),
});
export const caseSchema = z.object({
  id: z.string().uuid(),
  run_id: z.string(),
  conversation_id: z.string().nullable(),
  running: z.boolean(),
  blocked: z.object({ code: z.string(), message: z.string() }).nullable(),
  decisions: z.object({
    selected_option: optionSchema.nullable(),
    proposal_id: z.string().nullable(),
    approved: z.boolean(),
    rejected: z.boolean(),
  }),
  interaction: z.discriminatedUnion("kind", [
    z.object({ kind: z.literal("select"), history_index: z.number().int(), evidence: comparison, tool_call_id: z.string() }),
    z.object({ kind: z.literal("approve"), history_index: z.number().int(), evidence: proposal, tool_call_id: z.string() }),
  ]).nullable(),
  pending_human: humanRequest.nullable(),
  history: z.array(z.discriminatedUnion("role", [
    z.object({ role: z.literal("user"), content: z.string(), request_id: z.string() }),
    z.object({ role: z.literal("assistant"), result: validatedOutcome }),
    z.object({ role: z.literal("tool"), content: z.string(), request_id: z.string(), tool_call_id: z.string() }),
  ])),
  snapshot: z.record(z.unknown()),
  result: z.record(z.unknown()).nullable(),
  usage: z.record(z.unknown()),
  limits: z.record(z.unknown()),
  events: z.array(z.record(z.unknown())),
});

export type Bootstrap = z.infer<typeof bootstrapSchema>;
export type CaseView = z.infer<typeof caseSchema>;
export type HumanAction =
  | { action: "select"; option: "STANDARD" | "EXPRESS" }
  | { action: "approve"; proposal_id: string; confirm: true }
  | { action: "reject"; proposal_id: string };

export async function api(path: string, token: string, body?: object): Promise<unknown> {
  const response = await fetch(path, {
    method: body === undefined ? "GET" : "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", "X-Local-Token": token },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    const failure = z.object({ error: z.object({ code: z.string(), message: z.string().optional() }) })
      .safeParse(await response.json());
    throw new Error(failure.success
      ? `${failure.data.error.code}: ${failure.data.error.message ?? "Operation refused."}`
      : `HTTP ${response.status}: unexpected server error response.`);
  }
  return response.json();
}

export function historyMessages(view: CaseView): Message[] {
  return view.history.map((entry, index): Message => {
    const id = `${view.id}:history:${index}`;
    if (entry.role === "tool") return { id, role: "tool", toolCallId: entry.tool_call_id, content: entry.content };
    if (entry.role === "user") return { id, role: "user", content: entry.content };
    if (entry.result.status === "awaiting_human") {
      const request = entry.result.human_request;
      return { id, role: "assistant", content: "", toolCalls: [{
        id: request.call_id, type: "function",
        function: { name: request.name, arguments: JSON.stringify(request.arguments) },
      }] };
    }
    return { id, role: "assistant", content: entry.result.answer.message };
  });
}
