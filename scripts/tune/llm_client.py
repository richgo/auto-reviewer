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


class CopilotLLMClient:
    """LLM client that routes completions through the GitHub Copilot SDK.

    Uses GitHub Copilot auth — no provider-specific API keys required.
    """

    def __init__(self, model: str, timeout: float = 120.0):
        """
        Initialize Copilot SDK client.

        Args:
            model: Copilot model identifier (e.g., "gpt-4o-mini", "gemini-2.0-flash")
            timeout: Seconds to wait for the session to become idle
        """
        self.model = model
        self.timeout = timeout

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
        return asyncio.run(self._complete_async(prompt, system))

    async def _complete_async(self, prompt: str, system: Optional[str]) -> str:
        from copilot import CopilotClient, PermissionHandler

        system_msg: Optional[Dict[str, str]] = (
            {"mode": "replace", "content": system} if system else None
        )
        client = CopilotClient()
        session = await client.create_session(
            model=self.model,
            on_permission_request=PermissionHandler.approve_all,
            system_message=system_msg,  # type: ignore[arg-type]
        )
        try:
            response = await session.send_and_wait(prompt, timeout=self.timeout)
            if response is None or response.data is None:
                raise RuntimeError(
                    f"Copilot SDK returned no response for model '{self.model}'"
                )
            return str(response.data.content)
        finally:
            await session.disconnect()
            await client.stop()


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
