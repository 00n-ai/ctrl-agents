# Testing

## Positive cases

- task is clear and bounded
- controller selects the right next agent
- agents stay within role
- tools return usable results
- parser extracts needed fields
- validator passes grounded output
- trace records each step
- memory persists checkpoints
- final answer is released only after convergence

## Negative cases

- task is ambiguous or unbounded
- controller loops without progress
- agent outputs unsupported claims
- tool returns unparseable output
- parser fails and no fallback exists
- validator passes weak evidence
- trace is missing or incomplete
- memory is updated without a checkpoint
- final answer is released before validation

## Required test cases

1. single-question answer with citations
2. conflicting evidence requiring retry
3. malformed text requiring parser fallback
4. policy violation blocked by validator
5. rollback from failed convergence
6. comparison against single-agent baseline
