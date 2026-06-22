from __future__ import annotations

"""Generic model selection and provider-aware runtimes.

The framework routes model calls through a provider registry so the same agent
can target Ollama today and another backend later without changing controller
logic.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .llm import ChatMessage, OllamaClient
from .spec import ModelSpec


class ModelBackend(Protocol):
    def generate(self, prompt: str, *, system_prompt: str = "", options: dict[str, Any] | None = None) -> str: ...


@dataclass
class OllamaBackend:
    client: OllamaClient

    def generate(self, prompt: str, *, system_prompt: str = "", options: dict[str, Any] | None = None) -> str:
        messages: list[ChatMessage] = []
        if system_prompt:
            messages.append(ChatMessage(role="system", content=system_prompt))
        messages.append(ChatMessage(role="user", content=prompt))
        response = self.client.chat(messages, options=options)
        return response.text


BackendFactory = Callable[[ModelSpec, dict[str, Any]], ModelBackend]


@dataclass
class ModelRuntime:
    spec: ModelSpec
    backend: ModelBackend
    system_prompt: str = ""
    default_options: dict[str, Any] = field(default_factory=dict)

    def generate(self, prompt: str, *, options: dict[str, Any] | None = None) -> str:
        merged = dict(self.default_options)
        if options:
            merged.update(options)
        return self.backend.generate(prompt, system_prompt=self.system_prompt, options=merged)


@dataclass
class ModelRegistry:
    factories: dict[str, BackendFactory] = field(default_factory=dict)

    def register(self, provider: str, factory: BackendFactory) -> None:
        self.factories[provider] = factory

    def build(self, spec: ModelSpec, *, runtime_options: dict[str, Any] | None = None, system_prompt: str = "") -> ModelRuntime:
        runtime_options = runtime_options or {}
        if spec.provider not in self.factories:
            raise ValueError(f"unknown model provider: {spec.provider}")
        backend = self.factories[spec.provider](spec, runtime_options)
        return ModelRuntime(
            spec=spec,
            backend=backend,
            system_prompt=system_prompt,
            default_options=dict(spec.options),
        )


DEFAULT_MODEL_REGISTRY = ModelRegistry()


def _build_ollama_backend(spec: ModelSpec, runtime_options: dict[str, Any]) -> ModelBackend:
    client = OllamaClient(
        model=spec.name,
        base_url=runtime_options.get("base_url", "http://localhost:11434"),
        timeout_seconds=runtime_options.get("timeout_seconds", 120),
        opener=runtime_options.get("opener", OllamaClient(model=spec.name).opener),
    )
    return OllamaBackend(client=client)


DEFAULT_MODEL_REGISTRY.register("ollama", _build_ollama_backend)


def build_model_runtime(
    spec: ModelSpec,
    *,
    system_prompt: str = "",
    runtime_options: dict[str, Any] | None = None,
    registry: ModelRegistry | None = None,
) -> ModelRuntime:
    registry = registry or DEFAULT_MODEL_REGISTRY
    return registry.build(spec, runtime_options=runtime_options, system_prompt=system_prompt)
