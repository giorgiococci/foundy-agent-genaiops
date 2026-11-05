import { HttpAgent } from "@ag-ui/client";
import type { AgentSubscriber, HttpAgentConfig, RunAgentParameters, RunAgentResult } from "@ag-ui/client";
import type { RunAgentInput } from "@ag-ui/core";
import { validatedOutcome } from "./api.ts";
import type { ValidatedOutcome } from "./api.ts";
import type { z } from "zod";

export class CaseAgent extends HttpAgent {
  onValidated?: (outcome: ValidatedOutcome) => Promise<void>;
  lastFailure: Error | undefined;

  override async runAgent(parameters: RunAgentParameters = {}, subscriber?: AgentSubscriber): Promise<RunAgentResult> {
    const runId = parameters.runId ?? crypto.randomUUID();
    const validation = new ValidatedRun(this.threadId, runId);
    const subscription = this.subscribe(validation.subscriber());
    try {
      const result = await super.runAgent({ ...parameters, runId }, subscriber);
      validation.assertComplete();
      if (validation.answer) await this.onValidated?.(validation.answer);
      return result;
    } catch (error) {
      this.lastFailure = error instanceof Error ? error : new Error(String(error));
      throw error;
    } finally { subscription.unsubscribe(); }
  }

  protected override requestInit(input: RunAgentInput): RequestInit {
    if (input.threadId !== this.threadId || Object.keys(input.state).length
      || input.tools.some(tool => !["request_transfer_choice", "request_transfer_approval"].includes(tool.name))
      || input.context.length || Object.keys(input.forwardedProps).some(key => key !== "__copilotkitRequestId")
      || input.resume?.length || ("parentRunId" in input && input.parentRunId)) {
      throw new Error("Unsupported client authority, context, state or resume.");
    }
    const humanCalls = new Set(input.messages.flatMap(message => message.role === "assistant"
      ? (message.toolCalls ?? []).filter(call =>
        ["request_transfer_choice", "request_transfer_approval"].includes(call.function.name)).map(call => call.id)
      : []));
    const message = [...input.messages].reverse().find(message =>
      message.role === "user" || message.role === "tool" && humanCalls.has(message.toolCallId));
    if (!message || !["user", "tool"].includes(message.role) || typeof message.content !== "string"
      || !message.content.trim() || message.content.length > 8000) {
      throw new Error("Submit one new plain-text user message or native human tool result.");
    }
    return {
      ...super.requestInit(input),
      credentials: "same-origin",
      body: JSON.stringify({
        threadId: this.threadId, runId: input.runId,
        messages: [message], state: {}, tools: [], context: [], forwardedProps: {},
      }),
    };
  }

  override clone(): CaseAgent {
    const config: HttpAgentConfig = {
      url: this.url, headers: { ...this.headers }, fetch: this.fetch,
      threadId: this.threadId, agentId: this.agentId,
      initialMessages: structuredClone(this.messages),
      initialState: structuredClone(this.state),
    };
    const clone = new CaseAgent(config);
    clone.onValidated = this.onValidated;
    return clone;
  }
}

export class ValidatedRun {
  readonly caseId: string;
  readonly runId: string;
  answer: z.infer<typeof validatedOutcome> | undefined;
  finished = false;
  failure: Error | undefined;

  constructor(caseId: string, runId: string) {
    this.caseId = caseId;
    this.runId = runId;
  }

  subscriber(): AgentSubscriber {
    return {
      onCustomEvent: ({ event }) => {
        if (!["validated_answer", "validated_pause"].includes(event.name)) return;
        if (this.answer || this.finished || this.failure) {
          this.failure = new Error("Unexpected repeated validation.");
          return;
        }
        const parsed = validatedOutcome.safeParse(event.value);
        if (!parsed.success || (event.name === "validated_pause") !== (parsed.data.status === "awaiting_human")) {
          this.failure = new Error("Invalid application outcome validation.");
          return;
        }
        this.answer = parsed.data;
      },
      onRunFinishedEvent: ({ event, outcome }) => {
        if (!this.answer || this.failure || this.finished || outcome !== "success"
          || event.threadId !== this.caseId || event.runId !== this.runId) {
          this.failure = new Error("Run ended without matching application validation.");
          return;
        }
        this.finished = true;
      },
      onRunErrorEvent: ({ event }) => {
        this.failure = new Error(`${event.code ?? "run_error"}: ${event.message}`);
      },
      onRunFailed: ({ error }) => { this.failure = error; },
    };
  }

  assertComplete(): void {
    if (this.failure) throw this.failure;
    if (!this.finished || !this.answer) {
      throw new Error("Unvalidated or interrupted stream. Inspect case state; do not retry automatically.");
    }
  }
}
