# API reference

## Modules

### `ctrl_agents.spec`
Dataclasses that define the framework’s abstract model.

### `ctrl_agents.runtime`
Minimal runtime objects that execute agents, tools, validation, and controller loops.

### `ctrl_agents.llm`
Local LLM clients and model runtimes, starting with Ollama.

### `ctrl_agents.parsing`
Helpers for converting plain text into fields and extracting JSON blocks when needed.

### `ctrl_agents.examples`
Example agent factories for quick experimentation.

## Core types

### `Task`
Represents the unit of work.

Fields:
- `objective: str`
- `constraints: list[str]`
- `expected_output: str`

Usage:
```python
from ctrl_agents.spec import Task

task = Task(
    objective="answer the question",
    constraints=["plain text", "cite sources"],
    expected_output="answer",
)
```

### `ModelSpec`
Stores model configuration.

Fields:
- `name`
- `temperature`
- `max_tokens`
- `context_window`

### `PromptSpec`
Stores system and user prompt templates.

### `ToolSpec`
Describes a tool contract.

### `AgentSpec`
Describes a reusable agent role.

Fields:
- `name`
- `purpose`
- `model`
- `prompt`
- `tools`
- `memory_scope`
- `output_contract`

### `WorkflowStep`
One step in a workflow graph.

Fields:
- `name`
- `agent`
- `entry_condition`
- `exit_condition`

### `WorkflowSpec`
Ordered workflow definition.

### `State`
Current run state.

Fields:
- `checkpoint`
- `confidence`
- `objections`
- `evidence`

### `ContextPack`
The per-step context bundle.

### `TraceEntry`
An audit record for a step.

### `PolicySpec`
Guardrail rules for the run.

### `EvaluatorSpec`
Rubric for comparing runs.

## Runtime classes

### `ToolRuntime`
Wraps a callable tool implementation.

Method:
- `call(payload: dict[str, Any]) -> Any`

### `AgentRuntime`
Executes a role handler with a context pack and tool map.

Method:
- `run(context: ContextPack) -> AgentRunResult`

### `ValidatorRuntime`
Applies simple rule-based validation.

Method:
- `validate(text, state, task) -> ValidationResult`

### `ControllerRuntime`
Runs a workflow across registered agents.

Method:
- `run(task, state=None) -> RunResult`
+
+### LLM classes
+
+#### `ChatMessage`
+Simple role/content message for chat APIs.
+
+#### `OllamaResponse`
+Response wrapper returned by `OllamaClient`.
+
+#### `OllamaClient`
+Calls the Ollama REST API.
+
+Method:
+- `chat(messages, model=None, options=None) -> OllamaResponse`
+
+#### `OllamaModelRuntime`
+Plain-text generation wrapper around `OllamaClient`.
+
+Method:
+- `generate(prompt, options=None, model=None) -> str`
+
+#### `OllamaAgentRuntime`
+Prompt-driven convenience wrapper around `OllamaModelRuntime`.
+
+Method:
+- `run(prompt: str) -> str`

### `RunResult`
Final result of a controller run.

Fields:
- `final_text`
- `state`
- `traces`
- `validation`

## Parsing helpers

### `parse_labeled_text(text)`
Convert `key: value` lines into a dictionary.

### `extract_json_block(text)`
Extract a fenced JSON block if present.

## Example usage

```python
from ctrl_agents.parsing import parse_labeled_text
from ctrl_agents.runtime import ControllerRuntime
```
