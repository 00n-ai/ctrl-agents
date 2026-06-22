# Components

## Task
- **Purpose:** define the unit of work
- **Usage:** entry point for every run

## Model
- **Purpose:** reasoning backend
- **Usage:** configured per agent role or cost tier

## Prompt
- **Purpose:** shape behavior and output
- **Usage:** role-specific templates

## Tool
- **Purpose:** external capability
- **Usage:** retrieval, parsing, execution, validation

## Agent
- **Purpose:** reusable specialized role
- **Usage:** model + prompt + tools + output contract + memory scope

## Controller
- **Purpose:** manage workflow and convergence
- **Usage:** top-level coordinator, possibly itself an agent

## Workflow
- **Purpose:** define the step graph or state machine
- **Usage:** encode linear, branched, or looped execution

## State
- **Purpose:** track what is known right now
- **Usage:** store checkpoints, confidence, and objections

## Context Pack
- **Purpose:** provide the exact input for a step
- **Usage:** keep the agent’s view narrow and relevant

## Parser / Extractor
- **Purpose:** convert plain text into fields
- **Usage:** regex first, JSON fallback

## Validator / Judge
- **Purpose:** determine whether output is acceptable
- **Usage:** gating step before release

## Memory
- **Purpose:** durable storage across runs
- **Usage:** keep summaries, recovery points, reusable facts

## Trace
- **Purpose:** make the system inspectable
- **Usage:** log each meaningful step

## Policy
- **Purpose:** guardrails and stop conditions
- **Usage:** apply before and during execution

## Evaluator
- **Purpose:** compare runs and detect regressions
- **Usage:** benchmark prompts, models, workflows
