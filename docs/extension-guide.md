# Extension guide

## Adding a new workflow

1. define the goal
2. choose the agents
3. define the step order
4. decide where validation happens
5. define what gets traced
6. write a smoke test

## Adding a new agent role

A new agent should have:
- a narrow purpose
- a dedicated prompt
- a limited tool set
- a clear output contract
- a defined memory scope

Suggested roles:
- research
- skeptic
- validator
- synthesizer
- memory manager
- JSON extractor

## Adding a tool

A tool should be:
- deterministic when possible
- narrow in scope
- easy to log
- explicit about failure

Tools should not call other tools unless the behavior is documented.

## Adding persistence

If you need durable state, add:
- checkpoint writes
- memory writes
- trace entries
- recovery paths

## Adding richer parsing

The framework prefers text parsing first. If you need structure:
1. try labeled text
2. try regex
3. try a dedicated JSON extractor
4. only then add heavier parsing logic

## Adding evaluation

Evaluation should compare:
- answer quality
- trace completeness
- validation success
- runtime cost
- failure recovery behavior

## Documentation rule

Every new component should answer:
- what it is
- what it does
- what it consumes
- what it emits
- how to test it
