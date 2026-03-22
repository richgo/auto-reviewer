"""
Autoresearch tuning infrastructure for code review skills.

Modules:
- llm_client: Generic LLM interface (Anthropic, OpenAI, Google) and Copilot SDK client
- scorer: Binary assertion scorer
- mutator: Skill mutation strategies
- autoresearch: Main optimization loop
"""

__all__ = ["LLMClient", "CopilotLLMClient", "Scorer", "Mutator", "AutoResearcher"]

from .llm_client import LLMClient, CopilotLLMClient
from .scorer import Scorer, EvalScore, AssertionResult
from .mutator import Mutator, Mutation
from .autoresearch import AutoResearcher
