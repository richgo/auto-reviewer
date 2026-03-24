"""Provider-neutral transport contracts for model interaction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Protocol


@dataclass(frozen=True)
class CompletionRequest:
    prompt: str
    system: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    response_format: Optional[str] = None


@dataclass(frozen=True)
class CompletionResponse:
    text: str
    model: Optional[str]
    provider: str
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


class LLMTransport(Protocol):
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Execute a provider-neutral completion request."""
