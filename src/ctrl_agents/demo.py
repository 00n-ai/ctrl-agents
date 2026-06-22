from __future__ import annotations

"""Demo controller configurations for ctrl-agents.

This module provides a small end-to-end example that uses a local Ollama
model for synthesis. It is intentionally simple so developers can copy it as a
starting point for their own workflows.
"""

from dataclasses import dataclass
from typing import Any

from .llm import OllamaClient, OllamaModelRuntime
from .runtime import AgentRuntime, ControllerRuntime, ToolRuntime, ValidationResult, ValidatorRuntime
from .spec import AgentSpec, ModelSpec, PolicySpec, PromptSpec, Task, WorkflowSpec, WorkflowStep


@dataclass
class DemoConfig:
    model: str = "llama3.1"
    base_url: str = "http://localhost:11434"
    system_prompt: str = "You are a concise assistant that answers with evidence and plain text."
    temperature: float = 0.2
    max_tokens: int = 1024


def build_ollama_synthesis_agent(config: DemoConfig, *, opener: Any | None = None) -> AgentRuntime:
    """Build a prompt-driven synthesis agent backed by Ollama."""

    client = OllamaClient(
        model=config.model,
        base_url=config.base_url,
        opener=opener or OllamaClient(model=config.model).opener,
    )
    model_runtime = OllamaModelRuntime(client=client, system_prompt=config.system_prompt)
    spec = AgentSpec(
        name="synthesis",
        purpose="turn evidence into a final answer",
        model=ModelSpec(
            name=config.model,
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
    return AgentRuntime(spec=spec, model_runtime=model_runtime)


def build_demo_controller(config: DemoConfig, *, opener: Any | None = None) -> ControllerRuntime:
    """Build a small controller that uses Ollama for the final synthesis step."""

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
