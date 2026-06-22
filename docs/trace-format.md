# Trace format

A trace entry should capture the smallest useful explanation of a step.

## Recommended fields

- `step`
- `agent`
- `status`
- `input`
- `output`
- `timestamp` (if available)
- `notes` (if needed)

## Example

```json
{
  "step": "research",
  "agent": "research",
  "status": "pass",
  "input": "answer question",
  "output": "evidence: source1"
}
```

## Rules

- traces should be human-readable
- traces should show failures explicitly
- traces should be written at checkpoints
- traces should be enough to replay the reasoning path
