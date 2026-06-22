# Architecture Spec

## System contract

The system must:
- start from a task
- route through a controller
- run agents through a workflow
- keep outputs readable by default
- validate before final release
- persist state and trace

## Primary abstractions

- Task
- Model
- Prompt
- Tool
- Agent
- Controller
- Workflow
- State
- Context Pack
- Parser / Extractor
- Validator / Judge
- Memory
- Trace
- Policy
- Evaluator

## Control-theory mapping

- setpoint: grounded answer with evidence
- controller: orchestrator
- plant: multi-agent workflow
- sensors: retrieval, critique, validation
- state estimator: memory + checkpointing
- error signal: missing evidence, contradictions, weak grounding
- corrective action: re-plan, re-retrieve, re-validate, revise

## Execution loop

1. accept task
2. build context pack
3. dispatch agent
4. invoke tools
5. parse output
6. validate result
7. update state
8. persist trace
9. continue or stop

## Output policy

- default to plain text
- use labeled sections for structure
- use JSON only when a downstream consumer needs it
- if text parsing fails, route to a dedicated JSON extractor
