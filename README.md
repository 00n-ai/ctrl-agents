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
- `src/ctrl_agents/parsing.py` — plain-text and JSON extraction helpers
- `src/ctrl_agents/examples.py` — example agent factory
- `docs/architecture.md` — formal architecture spec
- `docs/components.md` — component catalog and interactions
- `docs/testing.md` — positive and negative test cases
- `docs/prompts.md` — prompt templates and message formats

## Quick start

Run the built-in smoke tests:

```bash
python3 tests/test_runtime.py
```

The framework currently demonstrates:
1. a controller
2. a workflow graph
3. specialized agents
4. trace logging
5. validation at release

## Status

This repository is the design + implementation scaffold for the multi-agent research experiment.
