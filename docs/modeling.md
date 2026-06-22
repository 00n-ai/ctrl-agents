# Model selection

## Goal

The framework should be provider-agnostic.
The controller and agents should call a generic model runtime, and the runtime should select the right backend code based on `ModelSpec.provider`.

## Core flow

1. `ModelSpec` declares the provider and model name.
2. `build_model_runtime(...)` looks up the provider in a registry.
3. The registry builds a provider backend.
4. The runtime exposes a uniform `generate()` API.
5. The agent and controller stay unchanged.

## Built-in provider

### Ollama
- provider name: `ollama`
- backend: `OllamaBackend`
- client: `OllamaClient`

## Adding a new provider

1. implement a backend with `generate(prompt, system_prompt="", options=None)`
2. register it in a `ModelRegistry`
3. set `ModelSpec.provider` to the new provider name
4. keep the controller and agents unchanged

## Why this matters

This keeps the framework flexible:
- local models today
- hosted models later
- custom backends when needed

The orchestration layer should not care which provider is underneath.
