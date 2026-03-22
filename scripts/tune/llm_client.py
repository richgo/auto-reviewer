"""
LLM client interfaces supporting the GitHub Copilot SDK (primary) and direct provider
APIs (Anthropic, OpenAI, Google) as a fallback.
"""

import asyncio
import os
import json
from typing import Dict, List, Optional, Any
import httpx


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
    """Generic LLM client that supports Anthropic and OpenAI APIs."""
    
    def __init__(self, model: str, timeout: int = 120):
        """
        Initialize LLM client.
        
        Args:
            model: Model identifier (e.g., "claude-sonnet-4-20250514", "gpt-4o")
            timeout: Request timeout in seconds
        """
        self.model = model
        self.timeout = timeout
        self._api_key: Optional[str] = None
        self._provider: Optional[str] = None
        self._detect_provider()
    
    def _detect_provider(self) -> None:
        """Detect which API provider to use based on model and environment."""
        if "claude" in self.model.lower() or "anthropic" in self.model.lower():
            self._provider = "anthropic"
            self._api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self._api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        elif "gpt" in self.model.lower() or "openai" in self.model.lower():
            self._provider = "openai"
            self._api_key = os.getenv("OPENAI_API_KEY")
            if not self._api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
        elif "gemini" in self.model.lower():
            self._provider = "google"
            self._api_key = os.getenv("GOOGLE_API_KEY")
            if not self._api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")
        else:
            # Default to Anthropic for unknown models
            self._provider = "anthropic"
            self._api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self._api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Get completion from LLM.
        
        Args:
            prompt: User prompt
            system: System prompt (optional)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Response text from LLM
        """
        if self._provider == "anthropic":
            return self._complete_anthropic(prompt, system, max_tokens, temperature)
        elif self._provider == "openai":
            return self._complete_openai(prompt, system, max_tokens, temperature)
        elif self._provider == "google":
            return self._complete_google(prompt, system, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported provider: {self._provider}")
    
    def _complete_anthropic(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Call Anthropic API."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system:
            payload["system"] = system
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
    
    def _complete_openai(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Call OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        messages: List[Dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    def _complete_google(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Call Google Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self._api_key}"
        headers = {"Content-Type": "application/json"}
        
        content_parts = []
        if system:
            content_parts.append({"text": f"System: {system}\n\n"})
        content_parts.append({"text": prompt})
        
        payload = {
            "contents": [{"parts": content_parts}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature
            }
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
