"""
LLM client interface for benchmark/tuning calls.
Uses GitHub Copilot SDK as the unified transport.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from benchmark.copilot_client import CopilotSDKClient, CopilotTransport
from llm.transport import CompletionRequest, CompletionResponse, LLMTransport


class CopilotLLMClient:
    """LLM client that routes completions through the GitHub Copilot SDK.

    Uses GitHub Copilot auth — no provider-specific API keys required.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        timeout: float = 120.0,
        transport: Optional[LLMTransport] = None,
    ):
        """
        Initialize Copilot SDK client.

        Args:
            model: Optional Copilot model identifier. When unset, the SDK default is used.
            timeout: Seconds to wait for the session to become idle
        """
        self.model = model
        self.timeout = timeout
        self._transport = transport or CopilotTransport(timeout=int(timeout))

    def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """
        Send a completion request via the Copilot SDK.

        Args:
            prompt: User prompt
            system: Optional system prompt
            max_tokens: Accepted for interface compatibility; not forwarded to the SDK
            temperature: Accepted for interface compatibility; not forwarded to the SDK
            **kwargs: Accepts extra keyword arguments for interface compatibility

        Returns:
            Response text from the model
        """
        response = self._transport.complete(
            CompletionRequest(
                prompt=prompt,
                system=system,
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        )
        return response.text


class LLMClient:
    """Sync interface expected by tune/benchmark modules."""

    def __init__(
        self,
        model: Optional[str] = None,
        timeout: int = 120,
        transport: Optional[LLMTransport] = None,
    ):
        self.model = model
        self.timeout = timeout
        self._transport = transport or _CopilotTransport(timeout=timeout)

    def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> str:
        target_model = model or self.model
        response = self._transport.complete(
            CompletionRequest(
                prompt=prompt,
                system=system,
                model=target_model,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format=response_format,
            )
        )
        return response.text


class _CopilotTransport:
    """Internal adapter that satisfies the shared LLM transport contract."""

    def __init__(self, timeout: int):
        self._copilot = CopilotSDKClient(timeout=timeout)

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        text = self._copilot.complete(
            model=request.model,
            prompt=request.prompt,
            system=request.system,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return CompletionResponse(
            text=text,
            model=request.model,
            provider="copilot",
            usage={},
            raw=None,
        )
