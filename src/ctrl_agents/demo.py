from __future__ import annotations

"""Demo controller configurations for ctrl-agents.

This module provides a small end-to-end example that:
- gathers evidence from the repository docs
- synthesizes an answer with a selected model provider
- keeps the answer grounded in the repo instead of generic outside analogies
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .modeling import build_model_runtime
from .runtime import AgentRunResult, AgentRuntime, ControllerRuntime, ToolRuntime, ValidatorRuntime
from .spec import AgentSpec, ModelSpec, PolicySpec, PromptSpec, Task, WorkflowSpec, WorkflowStep


@dataclass
class DemoConfig:
    provider: str = "ollama"
    model: str = "llama3.1"
    base_url: str = "http://localhost:11434"
    system_prompt: str = (
        "You are a concise assistant for the ctrl-agents repository. "
        "Use only the provided repo-doc evidence. If evidence is insufficient, say so. "
        "Keep the answer plain text and grounded in the cited docs."
    )
    temperature: float = 0.2
    max_tokens: int = 1024


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _search_repo_docs(query: str, *, max_hits: int = 8) -> str:
    tokens = [token.lower() for token in query.split() if token.strip()]
    docs_dir = _repo_root() / "docs"
    hits: list[str] = []

    priority_docs: list[Path] = []
    query_joined = " ".join(tokens)
    doc_priority_map = {
        "controller": ["architecture.md", "components.md", "developer-guide.md", "api.md"],
        "workflow": ["architecture.md", "components.md", "testing.md"],
        "validator": ["testing.md", "components.md", "architecture.md", "api.md"],
        "trace": ["trace-format.md", "architecture.md", "components.md", "developer-guide.md"],
        "memory": ["architecture.md", "components.md", "developer-guide.md"],
        "model": ["llms.md", "modeling.md", "api.md"],
        "ollama": ["llms.md", "modeling.md", "api.md"],
        "cli": ["cli.md", "developer-guide.md", "api.md"],
        "demo": ["cli.md", "developer-guide.md", "api.md"],
        "prompt": ["prompts.md", "developer-guide.md", "api.md"],
    }

    for key, filenames in doc_priority_map.items():
        if key in query_joined:
            for filename in filenames:
                path = docs_dir / filename
                if path.exists() and path not in priority_docs:
                    priority_docs.append(path)

    if not priority_docs:
        priority_docs = sorted(docs_dir.glob("*.md"))

    for path in priority_docs:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        local_hits = 0
        for idx, line in enumerate(lines, start=1):
            lower = line.lower()
            if tokens and not any(token in lower for token in tokens):
                continue
            snippet = line.strip()
            if not snippet:
                continue
            hits.append(f"{path.relative_to(_repo_root())}:{idx}: {snippet}")
            local_hits += 1
            if len(hits) >= max_hits:
                return "\n".join(hits)
        if local_hits == 0:
            for idx, line in enumerate(lines[:3], start=1):
                snippet = line.strip()
                if snippet:
                    hits.append(f"{path.relative_to(_repo_root())}:{idx}: {snippet}")
            if len(hits) >= max_hits:
                return "\n".join(hits[:max_hits])

    if hits:
        return "\n".join(hits[:max_hits])
    return f"No direct repo-doc match for: {query}"


def build_repo_research_agent() -> AgentRuntime:
    spec = AgentSpec(
        name="research",
        purpose="gather repo evidence before synthesis",
        model=ModelSpec(name="local-research", provider="none"),
        prompt=PromptSpec(
            system=(
                "You are the research agent for ctrl-agents. "
                "Return only repo evidence, with file:line references. "
                "Do not answer the question directly."
            ),
            user_template="Question: {objective}\nConstraints: {constraints}\nExpected output: {expected_output}",
        ),
    )

    def handler(context, tools: dict[str, ToolRuntime]) -> AgentRunResult:
        search = tools["search"].call({"query": context.task.objective})
        text = "\n".join(
            [
                "evidence:",
                str(search),
            ]
        )
        return AgentRunResult(text=text, tool_calls=["search"])

    return AgentRuntime(
        spec=spec,
        handler=handler,
        tools={"search": ToolRuntime(name="search", description="Search repo docs", fn=lambda payload: _search_repo_docs(payload["query"]))},
    )


def build_synthesis_agent(config: DemoConfig, *, opener: Any | None = None) -> AgentRuntime:
    """Build a prompt-driven synthesis agent backed by the configured provider."""

    spec = AgentSpec(
        name="synthesis",
        purpose="turn repo evidence into a final answer",
        model=ModelSpec(
            name=config.model,
            provider=config.provider,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        ),
        prompt=PromptSpec(
            system=config.system_prompt,
            user_template=(
                "Objective: {objective}\n"
                "Constraints: {constraints}\n"
                "Expected output: {expected_output}\n"
                "Checkpoint: {checkpoint}\n"
                "Confidence: {confidence}\n"
                "Repo evidence:\n{evidence}\n"
                "Memory: {memory}\n"
                "Instructions: answer only from the repo evidence above. "
                "If the evidence is insufficient, say 'answer: insufficient evidence'. "
                "Keep the answer short and grounded."
            ),
        ),
    )
    model_runtime = build_model_runtime(
        spec.model,
        system_prompt=spec.prompt.system,
        runtime_options={"base_url": config.base_url, "opener": opener},
    )
    return AgentRuntime(spec=spec, model_runtime=model_runtime)


def build_demo_controller(config: DemoConfig, *, opener: Any | None = None) -> ControllerRuntime:
    """Build a small controller that gathers repo evidence before synthesis."""

    research_agent = build_repo_research_agent()
    synthesis_agent = build_synthesis_agent(config, opener=opener)
    workflow = WorkflowSpec(
        steps=[
            WorkflowStep(name="research", agent="research"),
            WorkflowStep(name="synthesis", agent="synthesis"),
        ]
    )
    return ControllerRuntime(
        workflow=workflow,
        agents={"research": research_agent, "synthesis": synthesis_agent},
        validator=ValidatorRuntime(rules=["answer"]),
        policy=PolicySpec(rules=["plain_text", "evidence_before_release"]),
    )


def build_demo_task(prompt: str) -> Task:
    return Task(
        objective=prompt,
        constraints=["plain text", "show evidence from repo docs"],
        expected_output="answer",
    )
