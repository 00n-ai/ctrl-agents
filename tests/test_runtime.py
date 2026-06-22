from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ctrl_agents.parsing import extract_json_block, parse_labeled_text
from ctrl_agents.runtime import AgentRunResult, AgentRuntime, ControllerRuntime, ToolRuntime, ValidatorRuntime
from ctrl_agents.spec import AgentSpec, ModelSpec, PolicySpec, PromptSpec, Task, WorkflowSpec, WorkflowStep


def make_agent(name: str, text: str, tools=None):
    spec = AgentSpec(
        name=name,
        purpose=name,
        model=ModelSpec(name="test-model"),
        prompt=PromptSpec(system=f"system {name}"),
    )

    def handler(context, tool_map):
        if tool_map and "echo" in tool_map:
            tool_map["echo"].call({"value": context.task.objective})
        return AgentRunResult(text=text)

    return AgentRuntime(spec=spec, handler=handler, tools=tools or {})


class FakeModelRuntime:
    def __init__(self, text: str):
        self.text = text
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.text


def test_controller_runs_and_validates_positive_path():
    task = Task(objective="answer question", expected_output="answer")
    workflow = WorkflowSpec(
        steps=[
            WorkflowStep(name="research", agent="research"),
            WorkflowStep(name="final", agent="final"),
        ]
    )
    research = make_agent("research", "evidence: source1\nanswer: draft")
    final = make_agent("final", "answer: final answer with citation [source1]")
    controller = ControllerRuntime(
        workflow=workflow,
        agents={"research": research, "final": final},
        validator=ValidatorRuntime(rules=["answer", "citation"]),
        policy=PolicySpec(rules=["plain_text"]),
    )

    result = controller.run(task)

    assert result.final_text.startswith("answer:")
    assert result.validation is not None and result.validation.passed
    assert len(result.traces) >= 3
    assert result.state.checkpoint == "final"


def test_controller_stops_on_validation_failure():
    task = Task(objective="answer question", expected_output="answer")
    workflow = WorkflowSpec(steps=[WorkflowStep(name="research", agent="research")])
    research = make_agent("research", "draft without the required marker")
    controller = ControllerRuntime(
        workflow=workflow,
        agents={"research": research},
        validator=ValidatorRuntime(rules=["answer"]),
    )

    result = controller.run(task)

    assert result.validation is not None and not result.validation.passed
    assert result.traces[-1].status == "fail"


def test_agent_runtime_can_use_ollama_model_runtime():
    task = Task(objective="summarize the evidence", constraints=["plain text"], expected_output="answer")
    workflow = WorkflowSpec(steps=[WorkflowStep(name="final", agent="final")])
    spec = AgentSpec(
        name="final",
        purpose="final synthesis",
        model=ModelSpec(name="llama3.1"),
        prompt=PromptSpec(system="You are the final agent.", user_template="Objective={objective}\nEvidence={evidence}"),
    )
    fake_model = FakeModelRuntime("answer: done")
    agent = AgentRuntime(spec=spec, model_runtime=fake_model)
    controller = ControllerRuntime(workflow=workflow, agents={"final": agent}, validator=ValidatorRuntime(rules=["answer"]))

    result = controller.run(task)

    assert result.final_text == "answer: done"
    assert fake_model.prompts and "Objective=summarize the evidence" in fake_model.prompts[0]


def test_parse_labeled_text_and_json_block():
    text = """answer: hello\nconfidence: high\n```json\n{"a": 1}\n```"""
    parsed = parse_labeled_text(text)
    data = extract_json_block(text)

    assert parsed["answer"] == "hello"
    assert data == {"a": 1}


if __name__ == "__main__":
    test_controller_runs_and_validates_positive_path()
    test_controller_stops_on_validation_failure()
    test_agent_runtime_can_use_ollama_model_runtime()
    test_parse_labeled_text_and_json_block()
    print("all tests passed")
