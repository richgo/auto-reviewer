#!/usr/bin/env python3
"""Small Copilot SDK wrapper shared by skill-creator scripts."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any


class CopilotSDKClient:
    """Sync helper around the async GitHub Copilot SDK."""

    def __init__(self, timeout: int = 120):
        self.timeout = timeout

    def complete(
        self,
        *,
        prompt: str,
        model: str | None = None,
        system: str | None = None,
    ) -> str:
        return asyncio.run(self._complete_async(prompt=prompt, model=model, system=system))

    async def _complete_async(self, *, prompt: str, model: str | None, system: str | None) -> str:
        try:
            from copilot import CopilotClient
        except ImportError as exc:
            raise RuntimeError(
                "github-copilot-sdk is required. Install dependencies and authenticate "
                "with `gh auth login` or set GITHUB_TOKEN."
            ) from exc

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
                        {"prompt": prompt},
                        timeout=float(self.timeout),
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

                raise RuntimeError("Copilot SDK returned no response content.")
            finally:
                await session.destroy()
        finally:
            await client.stop()

    @staticmethod
    def _extract_event_content(event: Any) -> str | None:
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
    def _github_token() -> str | None:
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token

        hosts_path = Path.home() / ".config" / "gh" / "hosts.yml"
        if not hosts_path.exists():
            return None

        current_host = None
        for line in hosts_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not line.startswith(" "):
                current_host = stripped.rstrip(":")
                continue
            if current_host != "github.com":
                continue
            if stripped.startswith("oauth_token:"):
                value = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                return value or None

        return None
