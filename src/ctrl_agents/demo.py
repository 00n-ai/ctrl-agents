from __future__ import annotations

"""Demo controller configurations for ctrl-agents.

This module provides a small end-to-end example that uses a local Ollama
model for synthesis. It is intentionally simple so developers can copy it as a
starting point for their own workflows.
"""

from dataclasses import dataclass
from typing import Any

from .modeling import build_model_runtime
from .runtime import AgentRuntime, ControllerRuntime, ValidatorRuntime
from .spec import AgentSpec, ModelSpec, PolicySpec, PromptSpec, Task, WorkflowSpec, WorkflowStep


@dataclass
class DemoConfig:
    provider: str = "ollama"
    model: str = "llama3.1"
    base_url: str = "http://localhost:11434"
    system_prompt: str = "You are a concise assistant that answers with evidence and plain text."
    temperature: float = 0.2
    max_tokens: int = 1024


def build_ollama_synthesis_agent(config: DemoConfig, *, opener: Any | None = None) -> AgentRuntime:
    """Build a prompt-driven synthesis agent backed by the configured provider."""

    spec = AgentSpec(
        name="synthesis",
        purpose="turn evidence into a final answer",
        model=ModelSpec(
            name=config.model,
            provider=config.provider,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        ),
        prompt=PromptSpec(
            system=config.system_prompt,
            user_template=(
                "Objective: {objective}\n"
                "Constraints: {constraints}\n"
                "Expected output: {expected_output}\n"
                "Checkpoint: {checkpoint}\n"
                "Confidence: {confidence}\n"
                "Evidence: {evidence}\n"
                "Memory: {memory}\n"
            ),
        ),
    )
    model_runtime = build_model_runtime(
        spec.model,
        system_prompt=spec.prompt.system,
        runtime_options={"base_url": config.base_url, "opener": opener},
    )
    return AgentRuntime(spec=spec, model_runtime=model_runtime)


def build_demo_controller(config: DemoConfig, *, opener: Any | None = None) -> ControllerRuntime:
    """Build a small controller that uses the configured model provider for synthesis."""

    synthesis_agent = build_ollama_synthesis_agent(config, opener=opener)
    workflow = WorkflowSpec(steps=[WorkflowStep(name="synthesis", agent="synthesis")])
    return ControllerRuntime(
        workflow=workflow,
        agents={"synthesis": synthesis_agent},
        validator=ValidatorRuntime(rules=["answer"]),
        policy=PolicySpec(rules=["plain_text", "evidence_before_release"]),
    )


def build_demo_task(prompt: str) -> Task:
    return Task(
        objective=prompt,
        constraints=["plain text", "show evidence if available"],
        expected_output="answer",
    )
