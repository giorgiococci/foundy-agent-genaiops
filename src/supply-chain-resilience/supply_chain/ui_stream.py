"""AG-UI transport binding; the native Foundry agent still owns all execution."""

from __future__ import annotations

import json
from collections.abc import Awaitable, Mapping
from contextlib import aclosing
from typing import Any, Literal, overload

from agent_framework import AgentResponse, AgentResponseUpdate, AgentSession, Content, Message, ResponseStream
from agent_framework.foundry import FoundryAgent
from agent_framework_ag_ui import AgentFrameworkAgent

from .domain import ToolError
from .session import CandidateSession


class MessagePrefix:
    """Decode only a top-level JSON message string, including incomplete escapes."""

    def __init__(self) -> None:
        self.buffer = ""
        self.emitted = ""

    def push(self, text: str) -> str:
        self.buffer += text
        if len(self.buffer) > 200_000:
            raise ToolError("invalid_answer", "Streamed answer exceeds the local display bound.")
        source = self.buffer.lstrip()
        if not source.startswith("{"):
            return ""
        position = 1
        decoder = json.JSONDecoder()
        prefix = ""
        try:
            while position < len(source):
                position = self._whitespace(source, position)
                key, end = decoder.raw_decode(source, position)
                position = self._whitespace(source, end)
                if source[position] != ":":
                    break
                position = self._whitespace(source, position + 1)
                if key == "message":
                    if source[position] != '"':
                        break
                    prefix = self._string_prefix(source[position:])
                    break
                _, position = decoder.raw_decode(source, position)
                position = self._whitespace(source, position)
                if source[position] != ",":
                    break
                position += 1
        except (json.JSONDecodeError, IndexError):
            return ""
        if not prefix.startswith(self.emitted):
            raise ToolError("invalid_answer", "Streamed message attempted to rewrite its displayed prefix.")
        delta = prefix[len(self.emitted):]
        self.emitted = prefix
        return delta

    @staticmethod
    def _whitespace(source: str, position: int) -> int:
        while position < len(source) and source[position].isspace():
            position += 1
        return position

    @staticmethod
    def _string_prefix(source: str) -> str:
        end = 1
        while end < len(source):
            if source[end] == '"':
                break
            if source[end] == "\\":
                if end + 1 >= len(source):
                    break
                if source[end + 1] == "u":
                    if end + 6 > len(source):
                        break
                    try:
                        code = int(source[end + 2:end + 6], 16)
                    except ValueError:
                        break
                    if 0xD800 <= code <= 0xDBFF:
                        if end + 12 > len(source) or source[end + 6:end + 8] != "\\u":
                            break
                        end += 12
                        continue
                    end += 6
                    continue
                end += 2
                continue
            end += 1
        try:
            return json.loads(source[:end] + '"')
        except json.JSONDecodeError:
            return ""


class AdvisorUIBinding:
    """Bind the official AG-UI adapter to one server-owned, guarded case."""

    id = "supply-chain-resilience-advisor"
    name = "supply-chain-resilience-advisor"
    description = "Human-controlled synthetic supply-chain case"

    def __init__(self, candidate: CandidateSession, agent: FoundryAgent, message: str | Message) -> None:
        self.candidate = candidate
        self.agent = agent
        self.message = message
        self.answer: dict[str, object] | None = None
        self.native_response: AgentResponse | None = None

    def create_session(self, *, session_id: str | None = None) -> AgentSession:
        return AgentSession(session_id=session_id)

    def get_session(self, service_session_id: str, *, session_id: str | None = None) -> AgentSession:
        return AgentSession(session_id=session_id, service_session_id=service_session_id)

    @overload
    def run(
        self, messages=None, *, stream: Literal[False] = False, session=None,
        function_invocation_kwargs=None, client_kwargs=None, tools=None, options=None,
    ) -> Awaitable[AgentResponse]: ...

    @overload
    def run(
        self, messages=None, *, stream: Literal[True], session=None,
        function_invocation_kwargs=None, client_kwargs=None, tools=None, options=None,
    ) -> ResponseStream[AgentResponseUpdate, AgentResponse]: ...

    def run(
        self, messages=None, *, stream: bool = False, session=None,
        function_invocation_kwargs: Mapping[str, Any] | None = None,
        client_kwargs: Mapping[str, Any] | None = None,
        tools=None, options=None,
    ) -> Awaitable[AgentResponse] | ResponseStream[AgentResponseUpdate, AgentResponse]:
        if not stream:
            raise ToolError("unsupported_transport", "The AG-UI binding requires streaming.")

        def complete(answer: dict[str, object]) -> None:
            self.answer = answer

        def native_complete(response: AgentResponse) -> None:
            self.native_response = response

        async def updates():
            native_session = self.candidate.framework_session
            if native_session is None or not native_session.service_session_id:
                raise ToolError("missing_conversation", "No server-bound managed conversation.")
            parser = MessagePrefix()
            message_key = None
            source = self.candidate.advisor.stream(
                self.agent, native_session, self.message, complete, native_completed=native_complete,
            )
            async with aclosing(source):
                async for update in source:
                    contents = []
                    for content in update.contents:
                        if content.type == "text":
                            key = (update.response_id, update.message_id)
                            if key != message_key:
                                parser = MessagePrefix()
                                message_key = key
                            delta = parser.push(content.text or "")
                            if delta:
                                contents.append(Content.from_text(delta))
                        elif content.type in ("function_call", "function_result", "usage"):
                            contents.append(content)
                    if contents:
                        yield AgentResponseUpdate(
                            contents=contents, role=update.role, response_id=update.response_id,
                            message_id=update.message_id, agent_id=update.agent_id,
                        )

        def finalizer(updates):
            if self.answer is None or self.native_response is None:
                raise ToolError("invalid_answer", "The streamed turn did not pass final validation.")
            return self.native_response

        return ResponseStream(updates(), finalizer=finalizer)

    def adapter(self) -> AgentFrameworkAgent:
        return AgentFrameworkAgent(self, emit_messages_snapshot=False)
