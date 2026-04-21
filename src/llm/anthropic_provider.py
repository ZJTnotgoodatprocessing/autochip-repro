"""Anthropic LLM provider implementation.

Wraps the Anthropic SDK with relay base_url support and retry logic.
Extracted from the original client.py for multi-provider architecture.
"""

import os
import time
import anthropic

from src.llm.base import LLMProvider
from src.llm.client import APIError  # Re-use existing error class

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Retry config for transient API errors
_MAX_RETRIES = 3
_BACKOFF_SECONDS = [2, 5, 10]


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider with relay support and retry logic."""

    def __init__(self):
        self._client: anthropic.Anthropic | None = None

    def _get_client(self) -> anthropic.Anthropic:
        if self._client is not None:
            return self._client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        base_url = os.environ.get("ANTHROPIC_BASE_URL")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self._client = anthropic.Anthropic(**kwargs)
        return self._client

    def get_model_name(self) -> str:
        return os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)

    def generate(self, prompt: str, *, model: str | None = None, temperature: float = 0.7) -> str:
        client = self._get_client()
        model = model or self.get_model_name()

        def _do_call():
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return _extract_text(response)

        return _call_with_retry(_do_call)

    def generate_with_history(
        self,
        messages: list[dict],
        *,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> str:
        client = self._get_client()
        model = model or self.get_model_name()

        def _do_call():
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=temperature,
                messages=messages,
            )
            return _extract_text(response)

        return _call_with_retry(_do_call)


# ---------- Shared helpers (same logic as original client.py) ----------

def _is_retryable(exc: Exception) -> bool:
    """Check if an exception is a transient error worth retrying."""
    if isinstance(exc, anthropic.APIStatusError):
        status = exc.status_code
        msg = str(exc).lower()
        if status in (429, 500, 502, 503, 504, 529):
            return True
        if "model_not_found" in msg:
            return True
        if "no available channel" in msg:
            return True
        return False
    if isinstance(exc, anthropic.APIConnectionError):
        return True
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True
    return False


def _classify_error(exc: Exception) -> str:
    """Return a short error type tag for reporting."""
    if isinstance(exc, anthropic.APIStatusError):
        msg = str(exc).lower()
        if "model_not_found" in msg or "no available channel" in msg:
            return "model_not_found"
        return f"http_{exc.status_code}"
    if hasattr(anthropic, "APITimeoutError") and isinstance(exc, anthropic.APITimeoutError):
        return "timeout"
    if isinstance(exc, anthropic.APIConnectionError):
        return "connection_error"
    if isinstance(exc, TimeoutError):
        return "timeout"
    return "unknown"


def _call_with_retry(fn, *args, **kwargs):
    """Call *fn* with retry logic for transient API errors."""
    last_exc = None
    for attempt in range(_MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            last_exc = exc
            if not _is_retryable(exc) or attempt >= _MAX_RETRIES:
                break
            wait = _BACKOFF_SECONDS[min(attempt, len(_BACKOFF_SECONDS) - 1)]
            print(f"    [Retry] API error (attempt {attempt + 1}/{_MAX_RETRIES}): "
                  f"{type(exc).__name__}: {str(exc)[:120]}  — retrying in {wait}s")
            time.sleep(wait)

    error_type = _classify_error(last_exc)
    raise APIError(
        f"API call failed after {_MAX_RETRIES} retries: {last_exc}",
        error_type=error_type,
        original=last_exc,
    )


def _extract_text(response) -> str:
    """Extract text from Anthropic response content robustly."""
    content = getattr(response, "content", None) or []
    texts: list[str] = []
    for block in content:
        text = getattr(block, "text", None)
        if isinstance(text, str) and text:
            texts.append(text)
    return "\n".join(texts)
