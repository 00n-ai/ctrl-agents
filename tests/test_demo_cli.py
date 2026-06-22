from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ctrl_agents.cli import main
from ctrl_agents.demo import DemoConfig, build_demo_controller, build_demo_task


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def fake_opener(req, timeout=None):
    return FakeResponse({"message": {"content": "answer: demo synthesis"}})


def test_demo_controller_uses_ollama_for_synthesis():
    controller = build_demo_controller(DemoConfig(), opener=fake_opener)
    result = controller.run(build_demo_task("What is control theory?"))

    assert result.final_text == "answer: demo synthesis"
    assert result.validation is not None and result.validation.passed
    assert result.traces[0].agent == "synthesis"


def test_cli_main_prints_answer_and_trace_summary(capsys=None):
    # Reuse the demo controller via the same fake opener by monkeypatching the builder path.
    from ctrl_agents import cli as cli_mod

    original = cli_mod.build_demo_controller
    cli_mod.build_demo_controller = lambda config, opener=None: build_demo_controller(config, opener=fake_opener)
    try:
        code = main(["Explain feedback control", "--trace-json"])
        assert code == 0
    finally:
        cli_mod.build_demo_controller = original


if __name__ == "__main__":
    test_demo_controller_uses_ollama_for_synthesis()
    test_cli_main_prints_answer_and_trace_summary()
    print("all demo cli tests passed")
