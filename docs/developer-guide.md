# Developer guide

## What this repo is

`ctrl-agents` is a lightweight framework scaffold for building evidence-grounded multi-agent workflows.
It is intentionally small and explicit:
- one task enters the system
- a controller coordinates the run
- agents handle specialized roles
- tools extend capability
- validators gate release
- traces make the run inspectable

## Mental model

Think of the framework as a closed loop:

1. task enters
2. controller builds a workflow
3. controller dispatches a specialized agent
4. agent calls tools if needed
5. output is parsed when structure is required
6. validator checks grounding and policy
7. state and memory are updated
8. trace is recorded
9. controller continues or stops

## Project structure

- `src/ctrl_agents/spec.py` — dataclasses describing the system
- `src/ctrl_agents/runtime.py` — controller, agent, validator, and tool runtime
- `src/ctrl_agents/llm.py` — Ollama client and model runtimes
- `src/ctrl_agents/parsing.py` — plain-text and JSON extraction helpers
- `src/ctrl_agents/examples.py` — example agent factory
- `src/ctrl_agents/demo.py` — demo controller using Ollama for synthesis
- `src/ctrl_agents/cli.py` — CLI entrypoint
- `tests/test_runtime.py` — smoke tests and usage examples
- `tests/test_ollama.py` — Ollama integration smoke test
- `tests/test_demo_cli.py` — CLI/demo smoke test
- `docs/` — conceptual and implementation documentation

## How to extend the framework

### Add a new agent

1. define an `AgentSpec`
2. choose execution mode:
   - handler-based for deterministic logic
   - Ollama-backed for prompt-driven reasoning
3. create a handler function or model runtime
4. add any tools the agent needs
5. register the agent in the controller
6. add a workflow step that invokes it
7. add a test that proves the agent stays within role

### Add a local model

1. create or register a provider backend
2. call `build_model_runtime(...)`
3. attach the resulting runtime to an `AgentRuntime`
4. keep the prompt plain-text and parseable
5. add a smoke test with a fake opener or fake backend before relying on a live server
6. if you need a full demo path, use the repo-doc research step in `src/ctrl_agents/demo.py`
7. expose it via `src/ctrl_agents/cli.py`

### Add a new tool

1. wrap the capability in a `ToolRuntime`
2. give it a narrow input payload
3. make failure explicit
4. return structured, loggable output
5. add trace coverage if the tool changes workflow behavior

### Add a new workflow stage

1. add a `WorkflowStep`
2. decide what agent owns the step
3. define entry/exit conditions in docs
4. update controller expectations
5. add positive and negative test cases

### Add a new validator rule

1. add the rule string or validation logic
2. decide whether it is a hard fail or soft note
3. update the test cases
4. document the behavior in `docs/testing.md`

## Output conventions

- plain text is the default output format
- keep outputs labeled and parseable
- use JSON only when a downstream parser truly needs it
- if parsing plain text fails, add a dedicated extractor instead of forcing JSON everywhere

## Trace conventions

Every meaningful step should log:
- step name
- agent name
- input summary
- output summary
- status

This matters because the framework is designed for inspection and teaching, not just runtime output.

## Testing conventions

The repo currently uses smoke tests that can run with plain Python.
When a richer test environment is available, add `pytest`-based tests for:
- positive path
- negative path
- parsing fallback
- validation failure
- rollback / retry behavior

## Common developer mistakes

- letting one agent do multiple jobs
- hiding state instead of logging it
- making JSON the default output format
- skipping validation before release
- writing tools with unclear side effects
- forgetting to document the negative cases
