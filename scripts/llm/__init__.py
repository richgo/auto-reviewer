"""Shared LLM transport interfaces for pipeline stages."""

from .transport import CompletionRequest, CompletionResponse, LLMTransport

__all__ = ["CompletionRequest", "CompletionResponse", "LLMTransport"]

