from __future__ import annotations

from .runtime import AgentRunResult, AgentRuntime, ToolRuntime
from .spec import AgentSpec, ContextPack, ModelSpec, PromptSpec


def make_research_agent() -> AgentRuntime:
    spec = AgentSpec(
        name="research",
        purpose="gather evidence",
        model=ModelSpec(name="research-model"),
        prompt=PromptSpec(system="You are the research agent."),
    )

    def handler(context: ContextPack, tools: dict[str, ToolRuntime]) -> AgentRunResult:
        search = tools["search"].call({"query": context.task.objective})
        return AgentRunResult(text=f"evidence: {search}")

    return AgentRuntime(spec=spec, handler=handler, tools={})
