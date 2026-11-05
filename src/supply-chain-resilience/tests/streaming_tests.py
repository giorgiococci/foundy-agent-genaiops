"""Native framework streaming at the HTTP boundary, without Azure access."""

from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
from agent_framework import AgentSession
from azure.ai.projects.aio import AIProjectClient
from openai import AsyncOpenAI
from openai.types.responses import Response

from supply_chain import DemoActor, DemoRole, DemoStore, ToolError, ToolSession
from supply_chain.agents.resilience_advisor.agent import create_agent
from supply_chain.agents.resilience_advisor.conversation import AdvisorConversation
from supply_chain.runtime import Pricing, RunLimits
from tests.runtime_tests import response


def events(result: Response, *, terminal: bool = True):
    sequence = 0
    for index, item in enumerate(result.output):
        if item.type == "function_call":
            yield {"type": "response.output_item.added", "output_index": index,
                   "sequence_number": sequence, "item": {
                       **item.model_dump(), "id": f"fc_{index}", "arguments": "", "status": "in_progress",
                   }}
            sequence += 1
            midpoint = max(1, len(item.arguments) // 2)
            for delta in (item.arguments[:midpoint], item.arguments[midpoint:]):
                yield {"type": "response.function_call_arguments.delta", "output_index": index,
                       "item_id": f"fc_{index}", "delta": delta, "sequence_number": sequence}
                sequence += 1
            yield {"type": "response.function_call_arguments.done", "output_index": index,
                   "item_id": f"fc_{index}", "name": item.name, "arguments": item.arguments,
                   "sequence_number": sequence}
            sequence += 1
        elif item.type == "message":
            text = "".join(part.text for part in item.content if part.type == "output_text")
            for start in range(0, len(text), 12):
                yield {"type": "response.output_text.delta", "item_id": item.id,
                       "output_index": index, "content_index": 0, "delta": text[start:start + 12],
                       "logprobs": [], "sequence_number": sequence}
                sequence += 1
    if terminal:
        yield {"type": f"response.{result.status}", "response": result.model_dump(),
               "sequence_number": sequence}


class EventBody(httpx.AsyncByteStream):
    def __init__(self, chunks, before_terminal=None):
        self.chunks = chunks
        self.before_terminal = before_terminal

    async def __aiter__(self):
        for event in self.chunks:
            if event["type"] == "response.completed" and self.before_terminal:
                await self.before_terminal()
            yield ("data: " + json.dumps(event) + "\n\n").encode()
            await asyncio.sleep(0)


class StreamingFoundry:
    def __init__(self, responses, *, before_terminal=None, terminal=True):
        self.requests = []
        iterator = iter(responses)

        def serve(request):
            payload = json.loads(request.content)
            self.requests.append(payload)
            assert payload["stream"] is True
            result = next(iterator)
            result = result.model_copy(update={
                "id": f"resp_{len(self.requests)}",
                "output": [
                    item.model_copy(update={"id": f"message_{len(self.requests)}_{index}"})
                    if item.type == "message" else item
                    for index, item in enumerate(result.output)
                ],
            })
            return httpx.Response(200, headers={"content-type": "text/event-stream"},
                                  stream=EventBody(events(result, terminal=terminal), before_terminal))

        self.client = AsyncOpenAI(
            api_key="offline-only", base_url="https://example.invalid", max_retries=0,
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(serve)),
        )
        self.project = MagicMock(spec=AIProjectClient)
        self.project.get_openai_client.return_value = self.client
        self.project.agents = MagicMock()


class StreamingTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.store = DemoStore(Path(temporary.name) / "planning.sqlite3")
        self.store.initialize()
        self.advisor = AdvisorConversation(
            ToolSession(self.store, DemoActor("demo-planner", DemoRole.PLANNER)),
            pricing=Pricing(Decimal("5"), Decimal("20"), "offline fixture"),
        )
        self.session = AgentSession(service_session_id="conv_offline")
        self.results = []

    async def consume(self, fixture):
        self.addAsyncCleanup(fixture.client.close)
        agent = create_agent(fixture.project, "3", conversation=self.advisor)
        return [update async for update in self.advisor.stream(
            agent, self.session, "Synthetic planner question.", self.results.append,
        )]

    async def test_native_stream_yields_before_terminal_and_validates_final_answer(self):
        received = asyncio.Event()

        async def before_terminal():
            self.assertTrue(received.is_set(), "Text must reach the consumer before terminal completion.")

        fixture = StreamingFoundry([response(text='{"message":"Progressive answer.","evidence":[]}')],
                                  before_terminal=before_terminal)
        self.addAsyncCleanup(fixture.client.close)
        agent = create_agent(fixture.project, "3", conversation=self.advisor)
        text = ""
        async for update in self.advisor.stream(agent, self.session, "Question", self.results.append):
            if update.text:
                text += update.text
                received.set()
        self.assertIn("Progressive answer", text)
        self.assertEqual(self.results[0]["answer"]["message"], "Progressive answer.")
        self.assertEqual(self.advisor.safety.usage.model_requests, 1)
        self.assertEqual(self.advisor.safety.usage.total_tokens, 120)
        self.assertFalse(self.advisor.safety.usage.usage_unreconciled)

    async def test_split_arguments_validate_whole_batch_before_native_tools(self):
        fixture = StreamingFoundry([
            response((("read_planning_snapshot", "split-1", "{}"),
                      ("compare_transfer_options", "split-2", "{}"))),
            response(text=json.dumps({
                "message": "Compared.", "evidence": [
                    self.store.compare_options(DemoActor("demo-viewer", DemoRole.VIEWER)),
                ],
            })),
        ])
        await self.consume(fixture)
        self.assertEqual(len(fixture.requests), 2)
        self.assertEqual(self.advisor.safety.usage.tool_calls, 2)
        self.assertEqual(self.results[0]["status"], "completed")

    async def test_forbidden_sibling_blocks_all_tools(self):
        fixture = StreamingFoundry([response((
            ("read_planning_snapshot", "allowed", "{}"),
            ("execute_approved_transfer", "forbidden", '{"proposal_id":"untrusted"}'),
        ))])
        with patch.object(self.advisor.session, "dispatch", wraps=self.advisor.session.dispatch) as dispatch:
            with self.assertRaises(ToolError):
                await self.consume(fixture)
            dispatch.assert_not_called()
        self.assertEqual(len(fixture.requests), 1)
        self.assertFalse(self.results)

    async def test_missing_terminal_retains_uncertain_usage(self):
        fixture = StreamingFoundry([response(text='{"message":"Partial","evidence":[]}')], terminal=False)
        with self.assertRaises(ToolError):
            await self.consume(fixture)
        self.assertTrue(self.advisor.safety.usage.usage_unreconciled)
        self.assertFalse(self.results)

    async def test_invalid_final_evidence_never_completes(self):
        fixture = StreamingFoundry([response(text='{"message":"Invented","evidence":[{"invented":true}]}')])
        with self.assertRaises(ToolError) as caught:
            await self.consume(fixture)
        self.assertEqual(caught.exception.code, "ungrounded_answer")
        self.assertFalse(self.results)

    async def test_stream_request_limit_and_failed_tool_do_not_trigger_more_network_calls(self):
        self.advisor.safety.limits = RunLimits(model_requests=1)
        fixture = StreamingFoundry([response((("read_planning_snapshot", "one-call", "{}"),))])
        with self.assertRaises(ToolError):
            await self.consume(fixture)
        self.assertEqual(len(fixture.requests), 1)
        self.assertEqual(self.advisor.safety.usage.model_requests, 1)

    async def test_fatal_streamed_tool_failure_prevents_siblings_settlement_and_retry(self):
        fixture = StreamingFoundry([response((
            ("read_planning_snapshot", "failed", "{}"),
            ("compare_transfer_options", "sibling", "{}"),
        ))])
        with patch.object(self.advisor.session, "dispatch", side_effect=RuntimeError("offline fixture")) as dispatch:
            with self.assertRaises(ToolError) as caught:
                await self.consume(fixture)
        self.assertEqual(caught.exception.code, "tool_exception")
        self.assertEqual(dispatch.call_count, 1)
        self.assertEqual(len(fixture.requests), 1)
        self.assertIsNotNone(self.advisor.safety.failure)

    async def test_missing_terminal_after_a_partial_text_never_authorizes_a_tool(self):
        fixture = StreamingFoundry([response((("read_planning_snapshot", "unfinished", "{}"),))], terminal=False)
        with patch.object(self.advisor.session, "dispatch", wraps=self.advisor.session.dispatch) as dispatch:
            with self.assertRaises(ToolError):
                await self.consume(fixture)
            dispatch.assert_not_called()
        self.assertTrue(self.advisor.safety.usage.usage_unreconciled)

    async def test_cancellation_keeps_usage_uncertain_and_closes_without_replay(self):
        arrived = asyncio.Event()

        async def hold():
            arrived.set()
            await asyncio.Future()

        fixture = StreamingFoundry([response(text='{"message":"Partial","evidence":[]}')], before_terminal=hold)
        task = asyncio.create_task(self.consume(fixture))
        await asyncio.wait_for(arrived.wait(), 5)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(self.advisor.safety.usage.usage_unreconciled)
        self.assertEqual(len(fixture.requests), 1)
        self.assertFalse(self.results)

    async def test_streamed_call_ids_must_match_the_authoritative_terminal_batch(self):
        original = events

        def altered(result, **kwargs):
            for event in original(result, **kwargs):
                if event["type"] == "response.completed":
                    event["response"]["output"][0]["call_id"] = "different-terminal-id"
                yield event

        fixture = StreamingFoundry([response((("read_planning_snapshot", "delta-id", "{}"),))])
        with patch(f"{__name__}.events", altered), patch.object(
            self.advisor.session, "dispatch", wraps=self.advisor.session.dispatch,
        ) as dispatch:
            with self.assertRaises(ToolError) as caught:
                await self.consume(fixture)
            dispatch.assert_not_called()
        self.assertEqual(caught.exception.code, "invalid_response")
        self.assertEqual(len(fixture.requests), 1)

    async def test_terminal_without_usage_and_failed_or_incomplete_responses_never_dispatch(self):
        for result, code in (
            (response().model_copy(update={"usage": None}), "missing_usage"),
            (response(status="failed"), "response_failed"),
            (response(status="incomplete"), "response_failed"),
        ):
            with self.subTest(code=code, status=result.status):
                self.advisor.safety.usage.usage_unreconciled = False
                fixture = StreamingFoundry([result])
                with patch.object(self.advisor.session, "dispatch", wraps=self.advisor.session.dispatch) as dispatch:
                    with self.assertRaises(ToolError) as caught:
                        await self.consume(fixture)
                    dispatch.assert_not_called()
                self.assertEqual(caught.exception.code, code)
                self.assertEqual(len(fixture.requests), 1)


if __name__ == "__main__":
    unittest.main()
