"""
Copilot SDK wrapper for benchmark/tuning model calls.
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from typing import Any, List, Optional

import yaml
from copilot import CopilotClient

from llm.transport import CompletionRequest, CompletionResponse


class CopilotSDKClient:
    """Minimal sync wrapper around the async Copilot Python SDK."""

    def __init__(self, timeout: int = 120):
        self.timeout = timeout

    def list_models(self) -> List[str]:
        return asyncio.run(self._list_models_async())

    async def _list_models_async(self) -> List[str]:
        client = CopilotClient(self._client_options())
        await client.start()
        try:
            models = await client.list_models()
            return sorted(
                {
                    str(model.id)
                    for model in models
                    if getattr(model, "id", None)
                }
            )
        finally:
            await client.stop()

    def complete(
        self,
        *,
        model: Optional[str],
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        del max_tokens  # Copilot SDK model params are configured server-side per model.
        del temperature

        delay_seconds = 2
        for attempt in range(1, 4):
            try:
                return asyncio.run(
                    self._complete_once_async(model=model, prompt=prompt, system=system)
                )
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(delay_seconds)
                delay_seconds *= 2

        return ""

    async def _complete_once_async(
        self,
        *,
        model: Optional[str],
        prompt: str,
        system: Optional[str],
    ) -> str:
        client = CopilotClient(self._client_options())
        await client.start()
        try:
            session_config: dict[str, Any] = {}
            if model:
                session_config["model"] = model
            if system:
                session_config["system_message"] = {"mode": "append", "content": system}

            session = await client.create_session(session_config)
            try:
                event = await asyncio.wait_for(
                    session.send_and_wait(
                        {"prompt": prompt}, timeout=float(self.timeout)
                    ),
                    timeout=float(self.timeout) + 15.0,
                )
                content = self._extract_event_content(event)
                if content:
                    return content

                messages = await asyncio.wait_for(session.get_messages(), timeout=10.0)
                for message in reversed(messages):
                    content = self._extract_event_content(message)
                    if content:
                        return content
                return ""
            finally:
                await session.destroy()
        finally:
            await client.stop()

    @staticmethod
    def _extract_event_content(event: Any) -> Optional[str]:
        if event is None:
            return None
        data = getattr(event, "data", None)
        if data is None:
            return None

        content = getattr(data, "content", None)
        if isinstance(content, str) and content.strip():
            return content

        detailed_content = getattr(data, "detailed_content", None)
        if isinstance(detailed_content, str) and detailed_content.strip():
            return detailed_content

        result = getattr(data, "result", None)
        result_content = getattr(result, "content", None) if result is not None else None
        if isinstance(result_content, str) and result_content.strip():
            return result_content

        return None

    @staticmethod
    def _client_options() -> dict[str, Any]:
        token = CopilotSDKClient._github_token()
        if token:
            return {
                "github_token": token,
                "use_logged_in_user": False,
                "log_level": "error",
            }
        return {"use_logged_in_user": True, "log_level": "error"}

    @staticmethod
    def _github_token() -> Optional[str]:
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token

        hosts_path = Path.home() / ".config" / "gh" / "hosts.yml"
        if not hosts_path.exists():
            return None

        try:
            raw = yaml.safe_load(hosts_path.read_text(encoding="utf-8")) or {}
            return raw.get("github.com", {}).get("oauth_token")
        except Exception:
            return None


class CopilotTransport:
    """Provider-neutral transport adapter backed by CopilotSDKClient."""

    def __init__(self, client: Optional[CopilotSDKClient] = None, timeout: int = 120):
        self._client = client or CopilotSDKClient(timeout=timeout)

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        text = self._client.complete(
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
