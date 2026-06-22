"""ctrl-agents framework scaffold."""

from .demo import DemoConfig, build_demo_controller, build_demo_task, build_ollama_synthesis_agent
from .llm import ChatMessage, OllamaAgentRuntime, OllamaClient, OllamaModelRuntime, OllamaResponse
from .modeling import DEFAULT_MODEL_REGISTRY, ModelBackend, ModelRegistry, ModelRuntime, OllamaBackend, build_model_runtime
from .parsing import extract_json_block, parse_labeled_text
from .runtime import (
    AgentRunResult,
    AgentRuntime,
    ControllerRuntime,
    RunResult,
    ToolRuntime,
    ValidationResult,
    ValidatorRuntime,
)
from .spec import *  # noqa: F401,F403
