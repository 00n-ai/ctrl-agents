# CLI

## What it does

The CLI runs a small demo controller against Ollama and prints:
- final answer
- checkpoint
- confidence
- validation status
- trace summary

## Usage

From the repo root:

```bash
PYTHONPATH=src python3 -m ctrl_agents.cli "Explain feedback control"
```

After installation:

```bash
ctrl-agents "Explain feedback control"
```

Options:
- `--model` — Ollama model name
- `--base-url` — Ollama server URL
- `--system-prompt` — system instruction for synthesis
- `--trace-json` — print trace entries as JSON

## Behavior

The CLI is intentionally small:
1. build a demo task
2. build a demo controller
3. run the workflow
4. print the result

It is a reference implementation, not a full production orchestrator.
