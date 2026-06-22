from __future__ import annotations

"""Command line entrypoint for ctrl-agents.

The CLI is intentionally minimal:
- choose a prompt
- build a demo controller
- run it through Ollama
- print the answer and trace summary
"""

import argparse
import json
from typing import Any

from .demo import DemoConfig, build_demo_controller, build_demo_task


def _default_opener(req, timeout=None):
    from urllib import request as urllib_request

    return urllib_request.urlopen(req, timeout=timeout)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ctrl-agents", description="Run ctrl-agents demos")
    parser.add_argument("prompt", help="Prompt to answer")
    parser.add_argument("--provider", default="ollama", help="Model provider name")
    parser.add_argument("--model", default="llama3.1", help="Model name")
    parser.add_argument("--base-url", default="http://localhost:11434", help="Provider base URL when applicable")
    parser.add_argument("--system-prompt", default="You are a concise assistant that answers with evidence and plain text.")
    parser.add_argument("--trace-json", action="store_true", help="Print trace entries as JSON")
    args = parser.parse_args(argv)

    config = DemoConfig(provider=args.provider, model=args.model, base_url=args.base_url, system_prompt=args.system_prompt)
    controller = build_demo_controller(config, opener=_default_opener)
    task = build_demo_task(args.prompt)
    result = controller.run(task)

    print(result.final_text)
    print()
    print(f"checkpoint: {result.state.checkpoint}")
    print(f"confidence: {result.state.confidence}")
    if result.validation is not None:
        print(f"validated: {result.validation.passed}")
        if result.validation.notes:
            print("notes:")
            for note in result.validation.notes:
                print(f"- {note}")
    print("traces:")
    if args.trace_json:
        for trace in result.traces:
            print(json.dumps(trace.__dict__))
    else:
        for trace in result.traces:
            print(f"- {trace.step} [{trace.agent}] {trace.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
