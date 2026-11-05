"""Actual native function pauses and correlated human results; upstream is offline."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent_framework import AgentSession

from supply_chain.agents.resilience_advisor.agent import create_agent
from supply_chain.domain import ToolError
from supply_chain.session import CandidateSession
from tests.runtime_tests import response
from tests.streaming_tests import StreamingFoundry


class HumanHandoffTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "case"
        self.candidate = CandidateSession.initialize(self.path, "test")
        self.candidate.framework_session = AgentSession(service_session_id="conv_offline")

    async def run_native(self, responses, message="Quali opzioni abbiamo?"):
        fixture = StreamingFoundry(responses)
        self.addAsyncCleanup(fixture.client.close)
        advisor = self.candidate.advisor
        agent = create_agent(fixture.project, "test-version", conversation=advisor)
        completed = []
        updates = [item async for item in advisor.stream(
            agent, self.candidate.framework_session, message, completed.append,
        )]
        self.assertEqual(len(completed), 1)
        return completed[0], fixture.requests, updates

    async def choice(self):
        return await self.run_native([
            response((("compare_transfer_options", "compare-1", "{}"),)),
            response((("request_transfer_choice", "choice-1",
                       '{"question":"Preferisci STANDARD o EXPRESS?"}'),)),
        ])

    async def test_native_pause_has_real_call_id_and_no_fictitious_tool_result(self):
        result, requests, _ = await self.choice()
        self.assertEqual(result["status"], "awaiting_human")
        self.assertEqual(result["human_request"]["call_id"], "choice-1")
        self.assertEqual(self.candidate.record.usage.tool_calls, 2)
        self.assertFalse(self.candidate.record.usage.usage_unreconciled)
        self.assertEqual(len(requests), 2)
        self.assertIsNone(self.candidate.advisor.decisions.selected_option)
        self.assertIsNone(self.candidate.advisor.decisions.pending.receipt)

    async def test_saved_pause_continues_same_native_conversation_with_tool_output_only(self):
        await self.choice()
        self.candidate.save()
        self.candidate = CandidateSession.load(self.path)
        receipt = self.candidate.advisor.respond("choice-1", option="EXPRESS")
        self.candidate.save()

        def replies():
            yield response((("create_transfer_proposal", "proposal-1", '{"option":"EXPRESS"}'),))
            yield response((("request_transfer_approval", "approval-1", json.dumps({
                "question": "Approvi questa proposta?",
                "proposal_id": self.candidate.advisor.decisions.proposal_id,
            })),))

        result, requests, _ = await self.run_native(replies(), self.candidate.advisor.continuation())
        self.assertEqual(result["status"], "awaiting_human")
        self.assertEqual(result["human_request"]["call_id"], "approval-1")
        first = requests[0]
        self.assertEqual(first["conversation"], "conv_offline")
        outputs = [item for item in first["input"] if item.get("type") == "function_call_output"]
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0]["call_id"], "choice-1")
        self.assertEqual(json.loads(outputs[0]["output"]), receipt)
        self.assertFalse(any(item.get("role") == "user" for item in first["input"]))
        self.assertFalse(self.candidate.advisor.decisions.approved)
        self.assertEqual(self.candidate.store.read_snapshot(self.candidate.advisor.session.actor)["source"]["reserved"], 30)

    async def test_mixed_human_and_executable_batch_fails_before_effects(self):
        with self.assertRaises(ToolError) as caught:
            await self.run_native([response((
                ("compare_transfer_options", "compare-1", "{}"),
                ("request_transfer_choice", "choice-1", '{"question":"Scegli?"}'),
            ))])
        self.assertEqual(caught.exception.code, "invalid_human_batch")
        self.assertEqual(self.candidate.record.usage.tool_calls, 0)
        self.assertEqual(self.candidate.advisor.decisions.tool_results, {})

    async def test_response_is_correlated_idempotent_and_consumed_once(self):
        await self.choice()
        advisor = self.candidate.advisor
        with self.assertRaises(ToolError):
            advisor.respond("another-case", option="EXPRESS")
        receipt = advisor.respond("choice-1", option="EXPRESS")
        self.assertEqual(advisor.respond("choice-1", option="EXPRESS"), receipt)
        with self.assertRaises(ToolError):
            advisor.respond("choice-1", option="STANDARD")
        advisor.continuation()
        with self.assertRaises(ToolError):
            advisor.continuation()

    async def test_changed_facts_cannot_authorize_the_old_question(self):
        await self.choice()
        advisor = self.candidate.advisor
        snapshot = advisor.store.read_snapshot(advisor.session.actor)
        with patch.object(advisor.store, "read_snapshot", return_value={**snapshot, "snapshot_version": 2}):
            with self.assertRaises(ToolError) as caught:
                advisor.respond("choice-1", option="EXPRESS")
        self.assertEqual(caught.exception.code, "stale_human_request")
        self.assertIsNone(advisor.decisions.selected_option)

    async def test_partial_decision_save_is_inspectable_but_not_replayable(self):
        await self.choice()
        self.candidate.advisor.select("EXPRESS")
        self.candidate.save()
        restored = CandidateSession.load(self.path)
        with self.assertRaises(ToolError) as caught:
            restored.ensure_ready()
        self.assertEqual(caught.exception.code, "uncertain_human_response")
