from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    objective: str
    constraints: list[str] = field(default_factory=list)
    expected_output: str = ""


@dataclass
class ModelSpec:
    name: str
    temperature: float = 0.2
    max_tokens: int = 2048
    context_window: int = 8192


@dataclass
class PromptSpec:
    system: str
    user_template: str = ""


@dataclass
class ToolSpec:
    name: str
    description: str = ""
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentSpec:
    name: str
    purpose: str
    model: ModelSpec
    prompt: PromptSpec
    tools: list[ToolSpec] = field(default_factory=list)
    memory_scope: str = "run"
    output_contract: str = "plain_text"


@dataclass
class ControllerSpec:
    name: str
    purpose: str
    agents: list[str] = field(default_factory=list)


@dataclass
class WorkflowStep:
    name: str
    agent: str
    entry_condition: str = ""
    exit_condition: str = ""


@dataclass
class WorkflowSpec:
    steps: list[WorkflowStep] = field(default_factory=list)


@dataclass
class State:
    checkpoint: str = ""
    confidence: float = 0.0
    objections: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


@dataclass
class ContextPack:
    task: Task
    state: State
    evidence: list[str] = field(default_factory=list)
    memory: list[str] = field(default_factory=list)


@dataclass
class TraceEntry:
    step: str
    agent: str
    status: str
    input: str = ""
    output: str = ""


@dataclass
class PolicySpec:
    rules: list[str] = field(default_factory=list)


@dataclass
class EvaluatorSpec:
    rubric: list[str] = field(default_factory=list)
