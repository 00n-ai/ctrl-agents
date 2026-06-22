# ctrl-agents

A reusable framework for evidence-grounded multi-agent systems.

## Core idea

A simple question becomes a control problem once the system must show its work.
This framework treats the system as a closed-loop controller:
- **Task** defines the objective
- **Controller** manages the process
- **Workflow** defines the execution path
- **Agents** perform specialized roles
- **Tools** extend capability
- **Validator** checks grounding and policy
- **State / Memory / Trace** preserve continuity and observability

## Design principles

- plain text first, JSON only when needed
- one role per agent
- explicit validation before final release
- durable state and trace at every checkpoint
- simple components that compose into larger workflows

## Repository layout

- `src/ctrl_agents/spec.py` — framework dataclasses and abstractions
- `src/ctrl_agents/runtime.py` — controller, agent, validator, and tool runtime
- `src/ctrl_agents/llm.py` — Ollama client and model runtimes
- `src/ctrl_agents/modeling.py` — provider-aware model selection
- `src/ctrl_agents/parsing.py` — plain-text and JSON extraction helpers
- `src/ctrl_agents/examples.py` — example agent factory
- `src/ctrl_agents/demo.py` — repo-doc research + synthesis demo
- `src/ctrl_agents/cli.py` — CLI entrypoint
- `docs/current-state.md` — restart point for the project
- `docs/developer-guide.md` — how to extend the framework
- `docs/architecture.md` — formal architecture spec
- `docs/components.md` — component catalog and interactions
- `docs/extension-guide.md` — how to add new roles, tools, and workflows
- `docs/testing.md` — positive and negative test cases
- `docs/prompts.md` — prompt templates and message formats
- `docs/llms.md` — local LLM integration guide
- `docs/modeling.md` — provider-aware model selection
- `docs/cli.md` — CLI usage
- `docs/trace-format.md` — recommended trace schema
- `docs/api.md` — API reference for core types and runtime classes

## Quick start

Run the built-in smoke tests:

```bash
python3 tests/test_runtime.py
python3 tests/test_ollama.py
python3 tests/test_modeling.py
python3 tests/test_demo_cli.py
```

Run the CLI from source:

```bash
PYTHONPATH=src python3 -m ctrl_agents.cli "Explain feedback control"
```

Read these first when extending the framework:
1. `docs/current-state.md`
2. `docs/developer-guide.md`
3. `docs/architecture.md`
4. `docs/api.md`
5. `docs/testing.md`

The framework currently demonstrates:
1. a controller
2. a workflow graph
3. specialized agents
4. trace logging
5. validation at release
6. Ollama local model calls
7. a runnable CLI demo\n
## LLM support

The model layer is provider-aware.
Ollama is the first supported backend, but the controller and agent code only depend on the generic model runtime.

See `docs/llms.md`, `docs/modeling.md`, and `docs/api.md` for the integration contract.

## Status

This repository is the design + implementation scaffold for the multi-agent research experiment.
