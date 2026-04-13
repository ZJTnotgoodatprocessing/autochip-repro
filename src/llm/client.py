"""LLM client — wraps Anthropic SDK with relay base_url support and retry logic."""

import os
import time
import anthropic

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Retry config for transient API errors (503, model_not_found, connection errors)
_MAX_RETRIES = 3
_BACKOFF_SECONDS = [2, 5, 10]


class APIError(Exception):
    """Raised when the LLM API fails after all retries are exhausted."""

    def __init__(self, message: str, error_type: str = "unknown", original: Exception | None = None):
        super().__init__(message)
        self.error_type = error_type
        self.original = original


def get_model_name() -> str:
    """Return the active model name (env var > default constant)."""
    return os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)


def _get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    base_url = os.environ.get("ANTHROPIC_BASE_URL")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
    kwargs: dict = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return anthropic.Anthropic(**kwargs)


def _is_retryable(exc: Exception) -> bool:
    """Check if an exception is a transient error worth retrying."""
    # Anthropic SDK HTTP errors
    if isinstance(exc, anthropic.APIStatusError):
        status = exc.status_code
        msg = str(exc).lower()
        # Relay-side server / availability errors that are often transient
        if status in (429, 500, 502, 503, 504, 529):
            return True
        # model_not_found from relay/distributor is transient
        if "model_not_found" in msg:
            return True
        if "no available channel" in msg:
            return True
        return False
    # Connection-level errors
    if isinstance(exc, anthropic.APIConnectionError):
        return True
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

    # Exhausted retries — classify the error
    error_type = _classify_error(last_exc)
    raise APIError(
        f"API call failed after {_MAX_RETRIES} retries: {last_exc}",
        error_type=error_type,
        original=last_exc,
    )


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


def _extract_text(response) -> str:
    """Extract text from Anthropic response content robustly.

    Some relay / SDK edge cases may return blocks without a usable `.text`.
    In that case, return an empty string so downstream code treats it as a
    generation failure rather than crashing.
    """
    content = getattr(response, "content", None) or []
    texts: list[str] = []
    for block in content:
        text = getattr(block, "text", None)
        if isinstance(text, str) and text:
            texts.append(text)
    return "\n".join(texts)


def generate(prompt: str, *, model: str | None = None, temperature: float = 0.7) -> str:
    """Send a single user prompt to the LLM and return the text response.

    Raises APIError if the call fails after retries.
    """
    client = _get_client()
    model = model or get_model_name()

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
    messages: list[dict],
    *,
    model: str | None = None,
    temperature: float = 0.7,
) -> str:
    """Send a multi-turn conversation to the LLM and return the assistant's text.

    Raises APIError if the call fails after retries.
    """
    client = _get_client()
    model = model or get_model_name()

    def _do_call():
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=temperature,
            messages=messages,
        )
        return _extract_text(response)

    return _call_with_retry(_do_call)
