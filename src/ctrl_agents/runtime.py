from __future__ import annotations

"""Runtime layer for ctrl-agents.

The runtime layer provides simple, explicit execution primitives:
- ToolRuntime wraps callable tools
- AgentRuntime executes a role handler
- ValidatorRuntime applies release gates
- ControllerRuntime runs a workflow across agents
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .llm import OllamaModelRuntime
from .spec import AgentSpec, ContextPack, PolicySpec, State, Task, TraceEntry, WorkflowSpec


class ToolFn(Protocol):
    def __call__(self, payload: dict[str, Any]) -> Any: ...


@dataclass
class ToolRuntime:
    name: str
    description: str = ""
    fn: ToolFn | None = None

    def call(self, payload: dict[str, Any]) -> Any:
        if self.fn is None:
            raise ValueError(f"tool {self.name!r} has no implementation")
        return self.fn(payload)


@dataclass
class AgentRunResult:
    text: str
    tool_calls: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRuntime:
    spec: AgentSpec
    handler: Callable[[ContextPack, dict[str, ToolRuntime]], AgentRunResult | str] | None = None
    model_runtime: OllamaModelRuntime | None = None
    tools: dict[str, ToolRuntime] = field(default_factory=dict)

    def render_prompt(self, context: ContextPack) -> str:
        template = self.spec.prompt.user_template.strip()
        if not template:
            return (
                f"Objective: {context.task.objective}\n"
                f"Constraints: {', '.join(context.task.constraints) if context.task.constraints else 'none'}\n"
                f"Expected output: {context.task.expected_output or 'plain text'}\n"
                f"Checkpoint: {context.state.checkpoint or 'start'}\n"
                f"Confidence: {context.state.confidence}\n"
                f"Evidence: {' | '.join(context.evidence) if context.evidence else 'none'}\n"
                f"Memory: {' | '.join(context.memory) if context.memory else 'none'}"
            )
        return template.format(
            objective=context.task.objective,
            constraints=", ".join(context.task.constraints),
            expected_output=context.task.expected_output,
            checkpoint=context.state.checkpoint,
            confidence=context.state.confidence,
            evidence=" | ".join(context.evidence),
            memory=" | ".join(context.memory),
        )

    def run(self, context: ContextPack) -> AgentRunResult:
        if self.handler is not None:
            result = self.handler(context, self.tools)
            if isinstance(result, str):
                return AgentRunResult(text=result)
            return result
        if self.model_runtime is None:
            raise ValueError(f"agent {self.spec.name!r} has no handler or model runtime")
        prompt = self.render_prompt(context)
        return AgentRunResult(text=self.model_runtime.generate(prompt))


@dataclass
class ValidationResult:
    passed: bool
    notes: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class ValidatorRuntime:
    rules: list[str] = field(default_factory=list)

    def validate(self, text: str, state: State, task: Task) -> ValidationResult:
        notes: list[str] = []
        passed = True
        confidence = state.confidence

        if not text.strip():
            return ValidationResult(False, ["empty output"], 0.0)

        if task.expected_output and task.expected_output.lower() not in text.lower():
            passed = False
            notes.append("missing expected output marker")
            confidence = min(confidence, 0.3)

        for rule in self.rules:
            if rule and rule.lower() not in text.lower():
                passed = False
                notes.append(f"missing rule: {rule}")

        if "citation" in " ".join(self.rules).lower() and "[" not in text and "http" not in text:
            passed = False
            notes.append("missing citation-like evidence")
            confidence = min(confidence, 0.4)

        return ValidationResult(passed=passed, notes=notes, confidence=confidence)


@dataclass
class RunResult:
    final_text: str
    state: State
    traces: list[TraceEntry] = field(default_factory=list)
    validation: ValidationResult | None = None


@dataclass
class ControllerRuntime:
    workflow: WorkflowSpec
    agents: dict[str, AgentRuntime]
    validator: ValidatorRuntime | None = None
    policy: PolicySpec = field(default_factory=PolicySpec)

    def run(self, task: Task, state: State | None = None) -> RunResult:
        current_state = state or State(checkpoint="start")
        traces: list[TraceEntry] = []
        final_text = ""
        validation: ValidationResult | None = None

        steps = list(self.workflow.steps)
        for index, step in enumerate(steps):
            agent = self.agents[step.agent]
            context = ContextPack(task=task, state=current_state)
            result = agent.run(context)
            final_text = result.text
            traces.append(
                TraceEntry(
                    step=step.name,
                    agent=agent.spec.name,
                    status="pass",
                    input=task.objective,
                    output=result.text,
                )
            )
            current_state.checkpoint = step.name
            current_state.evidence.extend([line for line in result.text.splitlines() if line.strip()])

            is_last_step = index == len(steps) - 1
            if self.validator is not None and is_last_step:
                validation = self.validator.validate(result.text, current_state, task)
                traces.append(
                    TraceEntry(
                        step=f"{step.name}:validation",
                        agent="validator",
                        status="pass" if validation.passed else "fail",
                        input=result.text,
                        output="; ".join(validation.notes),
                    )
                )
                current_state.confidence = validation.confidence
                if not validation.passed:
                    break

        return RunResult(final_text=final_text, state=current_state, traces=traces, validation=validation)
