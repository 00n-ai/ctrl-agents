# LLM integration

## Provider-aware model layer

The framework now uses a provider-aware model component.
The controller and agents do not care which backend is used; they call a model runtime.
The model runtime selects the right backend code based on `ModelSpec.provider`.

## Concepts

### ModelSpec.provider
Controls which backend implementation is used.
Examples:
- `ollama`
- future providers such as `openai`, `anthropic`, `gemini`, or custom backends

### build_model_runtime
Create the runtime based on provider and registry.
Use it from controller code so the controller stays provider-agnostic.

### ModelRegistry
Maps provider names to backend factories.
Use it when you want to add or swap backends without changing controller logic.

### ModelRuntime
A generic wrapper around a provider backend.
Use it when you want a uniform `generate()` API across model providers.

### OllamaClient
A minimal HTTP client for the Ollama REST API.

Use it when you need to:
- call a local model
- run a chat completion
- keep the integration testable

### OllamaBackend
A provider backend that wraps `OllamaClient`.

Use it when the provider is `ollama`.

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
