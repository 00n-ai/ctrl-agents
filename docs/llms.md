# LLM integration

## Ollama first

The framework starts with Ollama because it is a local, simple, and testable way to call an LLM.
It is the first model integration layer for the framework.

## Concepts

### OllamaClient
A minimal HTTP client for the Ollama REST API.

Use it when you need to:
- call a local model
- run a chat completion
- keep the integration testable

### OllamaModelRuntime
A plain-text model wrapper around `OllamaClient`.

Use it when you want a reusable runtime that can generate text from a prompt.

### OllamaAgentRuntime
A convenience wrapper for a prompt-driven Ollama agent.

Use it when the workflow does not need a full custom handler.

## Endpoint

The client uses:
- `POST /api/chat`

Example payload:

```json
{
  "model": "llama3.1",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "stream": false
}
```

## Typical usage

```python
from ctrl_agents.llm import OllamaClient, OllamaModelRuntime

client = OllamaClient(model="llama3.1")
model = OllamaModelRuntime(client=client, system_prompt="You are a helpful agent.")
text = model.generate("Explain the task.")
```

## Development rule

Keep the Ollama layer small:
- no hidden prompt magic
- no automatic tool use
- no implicit workflow logic
- just model I/O

The controller and workflow stay separate.
