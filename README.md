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
- `src/ctrl_agents/parsing.py` — plain-text and JSON extraction helpers
- `src/ctrl_agents/examples.py` — example agent factory
- `docs/developer-guide.md` — how to extend the framework
- `docs/architecture.md` — formal architecture spec
- `docs/components.md` — component catalog and interactions
- `docs/extension-guide.md` — how to add new roles, tools, and workflows
- `docs/testing.md` — positive and negative test cases
- `docs/prompts.md` — prompt templates and message formats
- `docs/llms.md` — local LLM integration guide
- `docs/trace-format.md` — recommended trace schema
- `docs/api.md` — API reference for core types and runtime classes

## Quick start

Run the built-in smoke tests:

```bash
python3 tests/test_runtime.py
```

Read these first when extending the framework:
1. `docs/developer-guide.md`
2. `docs/architecture.md`
3. `docs/api.md`
4. `docs/testing.md`

The framework currently demonstrates:
1. a controller
2. a workflow graph
3. specialized agents
4. trace logging
5. validation at release
6. Ollama local model calls

## LLM support

The first supported model backend is Ollama.
Use it when you want a local prompt-driven agent instead of a pure handler-based one.

See `docs/llms.md` and `docs/api.md` for the integration contract.

## Status

This repository is the design + implementation scaffold for the multi-agent research experiment.
