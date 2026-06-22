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


class FakeOpener:
    def __init__(self, content: str = "answer: demo synthesis"):
        self.content = content
        self.requests: list[dict] = []

    def __call__(self, req, timeout=None):
        body = json.loads(req.data.decode("utf-8"))
        self.requests.append({"url": req.full_url, "body": body, "timeout": timeout})
        return FakeResponse({"message": {"content": self.content}})


def test_demo_controller_uses_repo_evidence_before_synthesis():
    opener = FakeOpener()
    controller = build_demo_controller(DemoConfig(), opener=opener)
    result = controller.run(build_demo_task("Explain why the controller matters"))

    assert result.final_text == "answer: demo synthesis"
    assert result.validation is not None and result.validation.passed
    assert [trace.agent for trace in result.traces] == ["research", "synthesis", "validator"]
    assert opener.requests
    prompt = opener.requests[0]["body"]["messages"][-1]["content"]
    assert "Repo evidence:" in prompt
    assert "docs/" in prompt
    assert "controller" in prompt.lower() or "validator" in prompt.lower()


def test_cli_main_prints_answer_and_trace_summary(capsys=None):
    from ctrl_agents import cli as cli_mod

    fake_opener = FakeOpener()
    original = cli_mod.build_demo_controller

    def patched_build_demo_controller(config, opener=None):
        return build_demo_controller(config, opener=fake_opener)

    cli_mod.build_demo_controller = patched_build_demo_controller
    try:
        code = main(["Explain feedback control", "--trace-json"])
        assert code == 0
    finally:
        cli_mod.build_demo_controller = original


if __name__ == "__main__":
    test_demo_controller_uses_repo_evidence_before_synthesis()
    test_cli_main_prints_answer_and_trace_summary()
    print("all demo cli tests passed")
