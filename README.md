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

- `src/ctrl_agents/` — framework spec and code scaffolding
- `docs/architecture.md` — formal architecture spec
- `docs/components.md` — component catalog and interactions
- `docs/testing.md` — positive and negative test cases
- `docs/prompts.md` — prompt templates and message formats

## Quick start

This repo is currently a framework scaffold. The first implementation step is to wire:
1. a controller
2. a workflow graph
3. a small set of specialized agents
4. trace logging for every step

## Status

This repository is the design + implementation scaffold for the multi-agent research experiment.
