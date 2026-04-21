"""OpenAI LLM provider implementation.

Supports OpenAI API and any OpenAI-compatible endpoint (e.g., DeepSeek, OpenRouter).
"""

import os
import time

from src.llm.base import LLMProvider
from src.llm.client import APIError

DEFAULT_MODEL = "gpt-4o"

_MAX_RETRIES = 3
_BACKOFF_SECONDS = [2, 5, 10]


class OpenAIProvider(LLMProvider):
    """OpenAI-compatible provider with retry logic.

    Environment variables:
        OPENAI_API_KEY: API key (required)
        OPENAI_BASE_URL: Base URL override for compatible endpoints (optional)
        OPENAI_MODEL: Default model name (optional, defaults to gpt-4o)
    """

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            import openai
        except ImportError:
            raise RuntimeError(
                "openai package not installed. Run: pip install openai"
            )
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment")
        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self._client = openai.OpenAI(**kwargs)
        return self._client

    def get_model_name(self) -> str:
        return os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)

    def generate(self, prompt: str, *, model: str | None = None, temperature: float = 0.7) -> str:
        client = self._get_client()
        model = model or self.get_model_name()

        def _do_call():
            response = client.chat.completions.create(
                model=model,
                max_tokens=4096,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content or ""

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
            response = client.chat.completions.create(
                model=model,
                max_tokens=4096,
                temperature=temperature,
                messages=messages,
            )
            return response.choices[0].message.content or ""

        return _call_with_retry(_do_call)


def _is_retryable(exc: Exception) -> bool:
    """Check if an exception is a transient error worth retrying."""
    try:
        import openai
        if isinstance(exc, openai.RateLimitError):
            return True
        if isinstance(exc, openai.APIStatusError):
            if exc.status_code in (429, 500, 502, 503, 504):
                return True
        if isinstance(exc, openai.APIConnectionError):
            return True
    except ImportError:
        pass
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True
    return False


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

    raise APIError(
        f"API call failed after {_MAX_RETRIES} retries: {last_exc}",
        error_type="unknown",
        original=last_exc,
    )
