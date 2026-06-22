from __future__ import annotations

"""Local LLM clients and model runtimes.

This module starts with Ollama because it is the easiest local model runtime
for development and experimentation. The implementation is intentionally small:
- an HTTP client that talks to the Ollama REST API
- a model runtime wrapper that returns plain text
- injectable HTTP behavior for testability
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol
from urllib import request as urllib_request
import json


class MessageLike(Protocol):
    role: str
    content: str


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class OllamaResponse:
    text: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class OllamaClient:
    """Small Ollama HTTP client.

    The client uses the Ollama chat endpoint:
    POST {base_url}/api/chat

    It is designed to be injectable so tests can run without a live Ollama
    process.
    """

    model: str
    base_url: str = "http://localhost:11434"
    timeout_seconds: int = 120
    opener: Callable[..., Any] = urllib_request.urlopen

    def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        options: dict[str, Any] | None = None,
    ) -> OllamaResponse:
        payload = {
            "model": model or self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
        }
        if options:
            payload["options"] = options

        data = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(
            f"{self.base_url.rstrip('/')}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.opener(req, timeout=self.timeout_seconds) as response:
            body = response.read().decode("utf-8")
        raw = json.loads(body)
        text = raw.get("message", {}).get("content", "")
        return OllamaResponse(text=text, raw=raw)


@dataclass
class OllamaModelRuntime:
    """Plain-text model runtime backed by Ollama."""

    client: OllamaClient
    system_prompt: str = ""

    def generate(
        self,
        prompt: str,
        *,
        options: dict[str, Any] | None = None,
        model: str | None = None,
    ) -> str:
        messages = []
        if self.system_prompt:
            messages.append(ChatMessage(role="system", content=self.system_prompt))
        messages.append(ChatMessage(role="user", content=prompt))
        response = self.client.chat(messages, model=model, options=options)
        return response.text


@dataclass
class OllamaAgentRuntime:
    """Convenience wrapper for an Ollama-backed agent.

    This is useful when a workflow wants a reusable agent that is mostly
    prompt-driven rather than tool-driven.
    """

    name: str
    model: OllamaModelRuntime

    def run(self, prompt: str) -> str:
        return self.model.generate(prompt)
