import { createContext, useContext, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  CopilotChatAssistantMessage, CopilotChatInput, CopilotChatMessageView, CopilotChatView, CopilotKitProvider, useAgent,
  useCopilotKit, useHumanInTheLoop,
} from "@copilotkit/react-core/v2";
import type { CopilotChatAssistantMessageProps, CopilotChatMessageViewProps } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { api, bootstrapSchema, caseSchema, comparison, proposal, historyMessages } from "./api.ts";
import type { Bootstrap, CaseView, HumanAction } from "./api.ts";
import { CaseAgent } from "./transport.ts";
import { entityName, formatCost, formatMargin, formatSchedule } from "./presentation.ts";
import "@copilotkit/react-core/v2/styles.css";
import "./style.css";

const errorText = (error: unknown) => error instanceof Error ? error.message : String(error);
type Respond = (result: unknown) => Promise<void>;
const CardContext = createContext<{
  view: CaseView; busy: boolean; act: (action: HumanAction, callId: string, respond?: Respond) => void;
} | null>(null);

function DecisionCard({ toolCallId, respond }: { toolCallId: string; respond?: Respond }) {
  const context = useContext(CardContext);
  const [confirm, setConfirm] = useState(false);
  if (!context) return null;
  const { view, act } = context;
  const entry = view.history.find(item => item.role === "assistant" &&
    item.result.status === "awaiting_human" && item.result.human_request.call_id === toolCallId);
  if (entry?.role !== "assistant") return <p role="status">Validating the advisor's question…</p>;
  const evidence = entry.result.answer.evidence;
  const compared = evidence.map(value => comparison.safeParse(value)).find(value => value.success);
  const proposed = evidence.map(value => proposal.safeParse(value)).find(value => value.success);
  const interaction = proposed?.success ? { kind: "approve" as const, evidence: proposed.data } :
    compared?.success ? { kind: "select" as const, evidence: compared.data } : null;
  if (!interaction) return null;
  const active = !context.busy && !view.blocked && view.interaction?.tool_call_id === toolCallId &&
    view.interaction.kind === interaction.kind;
  const currentProposal = interaction.kind === "approve" &&
    interaction.evidence.proposal_id === view.decisions.proposal_id;
  const decided = interaction.kind === "select" ? Boolean(view.decisions.selected_option) :
    currentProposal && (view.decisions.approved || view.decisions.rejected);
  return <section className="decision-card" aria-label="Human decision">
    <span className="eyebrow">{active ? "YOUR DECISION · ADVISOR CONTINUES AFTER YOUR ANSWER" : "RECORDED CONTEXT"}</span>
    <div className="advisor-question">
      <CopilotChatAssistantMessage.MarkdownRenderer content={entry.result.answer.message} />
    </div>
    {interaction.kind === "select" ? <>
      <h2>Choose cost or schedule margin</h2>
      <p>Recover {interaction.evidence.shortage} {interaction.evidence.component
        ? entityName(interaction.evidence.component, interaction.evidence.context) : "components"}.
        {" "}Spending ceiling: {formatCost(interaction.evidence.cost_cap, interaction.evidence.context)}.</p>
      <div className="options">{interaction.evidence.options.map(option => <div key={option.option}>
        <h3>{option.option}</h3>
        <p>Quantity: {option.quantity} · {formatCost(option.cost, interaction.evidence.context)}</p>
        <p>Arrival: {formatSchedule(option.arrival_day, option.arrival_date)}
          {" · "}completion: {formatSchedule(option.completion_day, option.completion_date)}</p>
        <p>Customer margins: {Object.entries(option.delivery_margin_days)
          .map(([customer, days]) => `${entityName(customer, interaction.evidence.context)}: ${formatMargin(days)}`).join("; ")}</p>
        {active && <button disabled={!option.feasible}
          onClick={() => act({ action: "select", option: option.option }, toolCallId, respond)}>Choose {option.option}</button>
        }
      </div>)}</div>
    </> : <>
      <h2>Review the exact proposal</h2>
      <p>{interaction.evidence.quantity} {entityName(interaction.evidence.component, interaction.evidence.context)}
        {" · "}{entityName(interaction.evidence.source, interaction.evidence.context)}
        {" → "}{entityName(interaction.evidence.destination, interaction.evidence.context)} · {interaction.evidence.option}</p>
      <p>{formatCost(interaction.evidence.cost, interaction.evidence.context)}
        {" · "}arrival: {formatSchedule(interaction.evidence.arrival_day, interaction.evidence.arrival_date)}
        {" · "}completion: {formatSchedule(interaction.evidence.completion_day, interaction.evidence.completion_date)}</p>
      <p>Approval permits a source reservation, not physical shipping.</p>
      <code>{interaction.evidence.proposal_id}</code>
      {active && <><label className="confirmation"><input type="checkbox" checked={confirm}
        onChange={event => setConfirm(event.target.checked)} />I confirm this exact proposal.</label>
      <div className="actions">
        <button disabled={!confirm} onClick={() => act({
          action: "approve", proposal_id: interaction.evidence.proposal_id, confirm: true,
        }, toolCallId, respond)}>Approve proposal</button>
        <button className="secondary" onClick={() => act({
          action: "reject", proposal_id: interaction.evidence.proposal_id,
        }, toolCallId, respond)}>Reject proposal</button>
      </div></>}
    </>}
    {decided && <p className="receipt">{interaction.kind === "select"
      ? `${view.decisions.selected_option} selected.`
      : view.decisions.approved ? "Exact proposal approved." : "Proposal rejected."}</p>}
  </section>;
}

function AdvisorMessage(props: CopilotChatAssistantMessageProps) {
  return <CopilotChatAssistantMessage {...props} toolbarVisible={false} />;
}
const AdvisorMessageWithSlots = Object.assign(AdvisorMessage, CopilotChatAssistantMessage);

function MessageList(props: CopilotChatMessageViewProps) {
  return <CopilotChatMessageView {...props} messageFeedback={false}
    assistantMessage={AdvisorMessageWithSlots} />;
}
const DecisionMessages = Object.assign(MessageList, { Cursor: CopilotChatMessageView.Cursor });

function HumanTools() {
  useHumanInTheLoop({
    name: "request_transfer_choice", agentId: "advisor",
    description: "Ask for the human's transfer preference.",
    parameters: z.object({ question: z.string() }),
    render: ({ toolCallId, respond }) => <DecisionCard toolCallId={toolCallId} respond={respond} />,
  }, []);
  useHumanInTheLoop({
    name: "request_transfer_approval", agentId: "advisor",
    description: "Request a human decision on the exact proposal.",
    parameters: z.object({ question: z.string(), proposal_id: z.string() }),
    render: ({ toolCallId, respond }) => <DecisionCard toolCallId={toolCallId} respond={respond} />,
  }, []);
  return null;
}

function Conversation({ initial, bootstrap, onBusy, firstQuestion }: {
  initial: CaseView; bootstrap: Bootstrap; onBusy: (busy: boolean) => void; firstQuestion?: string;
}) {
  const { agent, isReady } = useAgent({ agentId: "advisor" });
  const { copilotkit } = useCopilotKit();
  const [view, setView] = useState(initial);
  const [busy, setBusy] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const busyRef = useRef(false);
  const runnerActive = useRef(false);
  const mounted = useRef(true);
  const firstSubmitted = useRef(false);
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [status, setStatus] = useState(bootstrap.inference_enabled
    ? initial.pending_human && !initial.pending_human.consumed
      ? initial.pending_human.receipt ? "Decision saved; continuation was interrupted. Inspect diagnostics; no automatic replay."
        : "Awaiting your answer. The advisor continues after your decision."
      : "Ready. Send a question to call the advisor."
    : "Case loaded. Model calls are disabled by server configuration.");
  const [uncertain, setUncertain] = useState(false);
  const base = `/api/cases/${view.id}`;
  const disabled = !isReady || busy || Boolean(view.blocked) || uncertain || !bootstrap.inference_enabled ||
    Boolean(view.pending_human && !view.pending_human.consumed);

  useEffect(() => {
    mounted.current = true;
    if (!(agent instanceof CaseAgent)) throw new Error("Expected the guarded case transport.");
    agent.onValidated = async outcome => {
      await refresh(false);
      if (!mounted.current) return;
      setStreaming(false); lock(false);
      setStatus(outcome.status === "awaiting_human"
        ? "Awaiting your answer. The advisor continues after your decision."
        : "Validated · backend evidence checks and successful stream completion.");
    };
    const subscription = agent.subscribe({
      onRunInitialized: () => {
        if (mounted.current) {
          lock(true); setStreaming(true);
          setStatus("Advisor responding · provisional stream, awaiting application validation.");
        }
      },
    });
    return () => {
      mounted.current = false; agent.onValidated = undefined;
      subscription.unsubscribe(); copilotkit.stopAgent({ agent });
    };
  }, [agent, copilotkit]);

  function lock(value: boolean) {
    busyRef.current = value; setBusy(value); onBusy(value);
  }

  async function refresh(messages = true) {
    const next = caseSchema.parse(await api(base, bootstrap.action_token));
    if (mounted.current) {
      setView(next);
      if (messages) agent.setMessages(historyMessages(next));
    }
  }

  async function act(action: HumanAction, callId: string, respond?: Respond) {
    if (busyRef.current || view.blocked || uncertain) return;
    lock(true); setError(""); setStatus("Recording your decision…");
    try {
      const next = caseSchema.parse(await api(`${base}/actions`, bootstrap.action_token,
        { ...action, tool_call_id: callId }));
      setView(next);
      const receipt = next.pending_human?.receipt;
      if (!receipt || next.pending_human?.call_id !== callId) throw new Error("Missing authoritative decision receipt.");
      setStatus("Decision recorded. Waiting for the advisor's response…");
      if (respond) {
        await respond(receipt);
      } else {
        if (runnerActive.current) throw new Error("Human handler is not ready. Inspect the saved decision; do not replay.");
        agent.addMessage({ id: crypto.randomUUID(), role: "tool", toolCallId: callId, content: JSON.stringify(receipt) });
        void run();
      }
    } catch (failure) {
      setError(errorText(failure)); setUncertain(true); lock(false);
    }
  }

  async function run() {
    if (runnerActive.current) return;
    runnerActive.current = true;
    if (agent instanceof CaseAgent) agent.lastFailure = undefined;
    lock(true); setStreaming(true); setError("");
    setStatus("Streaming · provisional text, awaiting application validation.");
    try {
      await copilotkit.runAgent({ agent, runId: crypto.randomUUID() });
      if (agent instanceof CaseAgent && agent.lastFailure) throw agent.lastFailure;
      if (mounted.current) {
        setInput("");
      }
    } catch (failure) {
      if (mounted.current) {
        setUncertain(true);
        setError(`${errorText(failure)} No automatic replay. Inspect this case or start a new one.`);
        setStatus("Not validated · interrupted or failed turn.");
      }
    } finally {
      runnerActive.current = false;
      if (mounted.current) {
        try { await refresh(); } catch (failure) { setUncertain(true); setError(errorText(failure)); }
        setStreaming(false); lock(false);
      }

    }
  }

  async function send(text: string) {
    if (disabled || busyRef.current || runnerActive.current || !text.trim()) return;
    agent.addMessage({ id: crypto.randomUUID(), role: "user", content: text });
    setInput("");
    await run();
  }

  useEffect(() => {
    if (isReady && firstQuestion && !firstSubmitted.current) {
      firstSubmitted.current = true;
      void send(firstQuestion);
    }
  }, [isReady, firstQuestion]);

  return <CardContext value={{ view, busy: busy || uncertain,
    act: (action, callId, respond) => { void act(action, callId, respond); } }}>
    <HumanTools />
    <div className="status" role="status">{view.blocked ? `Blocked: ${view.blocked.message}` : status}</div>
    {error && <div className="error" role="alert">{error}</div>}
    <CopilotChatView className="chat" messages={agent.messages} isRunning={streaming}
      messageView={DecisionMessages} welcomeScreen={false} suggestions={[]}
      inputValue={input} onInputChange={setInput}
      onSubmitMessage={text => { void send(text); }}
      onStop={() => { setUncertain(true); copilotkit.stopAgent({ agent }); }}
      input={{
        textArea: { disabled, maxLength: 8000, placeholder: "Ask about the synthetic supply delay…" },
        sendButton: { disabled: streaming ? false : disabled || !input.trim() },
        addMenuButton: () => null,
        startTranscribeButton: () => null,
      }}
    />
    <details className="diagnostics">
      <summary>Diagnostics and validated evidence</summary>
      <pre>{JSON.stringify({
        case: view.id, managed_conversation: view.conversation_id,
        decisions: view.decisions, snapshot: view.snapshot, result: view.result,
        usage: view.usage, limits: view.limits, events: view.events,
      }, null, 2)}</pre>
    </details>
  </CardContext>;
}

function CaseChat({ initial, bootstrap, onBusy, firstQuestion }: {
  initial: CaseView; bootstrap: Bootstrap; onBusy: (busy: boolean) => void; firstQuestion?: string;
}) {
  const agents = useMemo(() => ({
    advisor: new CaseAgent({
      url: `/api/cases/${initial.id}/run`, threadId: initial.id,
      headers: { "X-Local-Token": bootstrap.action_token },
      initialMessages: historyMessages(initial),
    }),
  }), [initial.id, bootstrap.action_token]);
  return <CopilotKitProvider agents__unsafe_dev_only={agents} agentId="advisor"
    enableInspector={false} showIntelligenceIndicator={false} learning={false}>
    <Conversation initial={initial} bootstrap={bootstrap} onBusy={onBusy} firstQuestion={firstQuestion} />
  </CopilotKitProvider>;
}

function App() {
  const [bootstrap, setBootstrap] = useState<Bootstrap>();
  const [view, setView] = useState<CaseView>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [input, setInput] = useState("");
  const [firstQuestion, setFirstQuestion] = useState<string>();
  const starting = useRef(false);
  useEffect(() => {
    void api("/api/bootstrap", "").then(async value => {
      const configuration = bootstrapSchema.parse(value);
      setBootstrap(configuration);
      const id = new URL(location.href).searchParams.get("chat");
      if (id) {
        setBusy(true);
        const restored = caseSchema.parse(await api(`/api/cases/${encodeURIComponent(id)}`, configuration.action_token));
        setView(restored);
        setBusy(false);
      }
    })
      .catch(failure => { setBusy(false); setError(errorText(failure)); });
  }, []);

  async function begin(text: string) {
    if (!bootstrap || busy || starting.current || !text.trim()) return;
    starting.current = true;
    setBusy(true); setError("");
    try {
      const next = caseSchema.parse(await api("/api/cases", bootstrap.action_token, {}));
      history.replaceState(null, "", `/?chat=${next.id}`);
      setFirstQuestion(text);
      setView(next);
      setInput("");
    } catch (failure) { setError(errorText(failure)); setBusy(false); }
    finally { starting.current = false; }
  }
  return <main>
    <header>
      <div><span className="eyebrow">FOUNDRY AGENT LAB</span>
        <h1>Supply chain resilience</h1>
        <p>Synthetic planning. Agent-led reasoning. Human-controlled decisions.</p></div>
      {(view || error) && <button className="secondary" disabled={busy || !bootstrap} onClick={() => {
        history.replaceState(null, "", "/");
        setView(undefined); setFirstQuestion(undefined); setInput(""); setError("");
      }}>New chat</button>}
    </header>
    <div className="connection">{!bootstrap ? "Reading local configuration…" :
      bootstrap.service_mode === "offline-test-fixture"
        ? "OFFLINE SIMULATION · Real Agent Framework / AG-UI, simulated upstream responses. No Foundry calls."
        : !bootstrap.inference_enabled
          ? "Model calls disabled by server configuration. Typing cannot enable them."
          : `Microsoft Foundry · managed advisor v${bootstrap.agent_version} · ${bootstrap.deployment} · real model responses, synthetic business data.`}</div>
    {error && <div className="error" role="alert">{error}</div>}
    {view && bootstrap ? <CaseChat key={view.id} initial={view} bootstrap={bootstrap} onBusy={setBusy}
      firstQuestion={firstQuestion} /> :
      <section className="welcome"><h2>Investigate a supply delay, one decision at a time</h2>
        <p>Ask your question to start. Your first message opens a real Foundry conversation.
          The advisor will explain the alternatives before you choose.</p>
        <CopilotChatInput value={input} onChange={setInput} onSubmitMessage={text => { void begin(text); }}
          textArea={{ disabled: busy || !bootstrap || Boolean(error), maxLength: 8000, placeholder: "Ask about the supply delay…" }}
          sendButton={{ disabled: busy || !bootstrap || Boolean(error) || !input.trim() }}
          addMenuButton={() => null} startTranscribeButton={() => null} />
        <p className="quiet">Opening this page does not call a model. Decisions remain yours.</p>
      </section>}
    <footer>CopilotKit v2 · AG-UI streaming · Microsoft Agent Framework · local development app</footer>
  </main>;
}

const root = document.getElementById("root");
if (!root) throw new Error("Application root is missing.");
createRoot(root).render(<App />);
