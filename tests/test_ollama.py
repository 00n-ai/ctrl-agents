from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ctrl_agents.llm import ChatMessage, OllamaClient, OllamaModelRuntime


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_ollama_client_builds_chat_request():
    captured = {}

    def fake_opener(req, timeout=None):
        captured["url"] = req.full_url
        captured["body"] = json.loads(req.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse({"message": {"content": "hello from ollama"}})

    client = OllamaClient(model="llama3.1", opener=fake_opener)
    response = client.chat([ChatMessage(role="system", content="s"), ChatMessage(role="user", content="u")])

    assert captured["url"].endswith("/api/chat")
    assert captured["body"]["model"] == "llama3.1"
    assert captured["body"]["stream"] is False
    assert response.text == "hello from ollama"


def test_ollama_model_runtime_generates_plain_text():
    def fake_opener(req, timeout=None):
        return FakeResponse({"message": {"content": "plain text answer"}})

    client = OllamaClient(model="llama3.1", opener=fake_opener)
    runtime = OllamaModelRuntime(client=client, system_prompt="You are helpful.")

    assert runtime.generate("say hi") == "plain text answer"


if __name__ == "__main__":
    test_ollama_client_builds_chat_request()
    test_ollama_model_runtime_generates_plain_text()
    print("all ollama tests passed")
