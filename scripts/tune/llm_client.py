"""
LLM client interface for benchmark/tuning calls.
Uses GitHub Copilot SDK as the unified transport.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from benchmark.copilot_client import CopilotSDKClient


class LLMClient:
    """Sync interface expected by tune/benchmark modules."""

    def __init__(self, model: str, timeout: int = 120):
        self.model = model
        self.timeout = timeout
        self._copilot = CopilotSDKClient(timeout=timeout)

    def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None,
    ) -> str:
        target_model = model or self.model
        return self._copilot.complete(
            model=target_model,
            prompt=prompt,
            system=system,
            max_tokens=max_tokens,
            temperature=temperature,
        )
