from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ctrl_agents.modeling import ModelRegistry, build_model_runtime
from ctrl_agents.spec import ModelSpec


class DummyBackend:
    def __init__(self):
        self.prompts = []

    def generate(self, prompt: str, *, system_prompt: str = "", options=None) -> str:
        self.prompts.append((prompt, system_prompt, options or {}))
        return "dummy answer"


def test_build_model_runtime_selects_registered_provider():
    registry = ModelRegistry()
    registry.register("dummy", lambda spec, opts: DummyBackend())
    runtime = build_model_runtime(ModelSpec(name="x", provider="dummy"), system_prompt="sys", registry=registry)

    assert runtime.generate("hello") == "dummy answer"


def test_build_model_runtime_rejects_unknown_provider():
    try:
        build_model_runtime(ModelSpec(name="x", provider="missing"))
    except ValueError as e:
        assert "unknown model provider" in str(e)
    else:
        raise AssertionError("expected ValueError")


if __name__ == "__main__":
    test_build_model_runtime_selects_registered_provider()
    test_build_model_runtime_rejects_unknown_provider()
    print("all modeling tests passed")
