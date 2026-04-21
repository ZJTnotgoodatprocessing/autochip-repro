"""Provider registry — resolve LLM_PROVIDER env var to a concrete provider instance.

Usage:
    from src.llm.provider_registry import get_provider
    provider = get_provider()           # uses LLM_PROVIDER env var
    provider = get_provider("openai")   # explicit override

Supported providers:
    - "anthropic" (default): uses ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL, ANTHROPIC_MODEL
    - "openai": uses OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
"""

import os

from src.llm.base import LLMProvider

# Lazy-loaded singletons
_instances: dict[str, LLMProvider] = {}


def get_provider(provider_name: str | None = None) -> LLMProvider:
    """Return a provider instance, creating it if needed.

    Args:
        provider_name: "anthropic" or "openai". If None, reads LLM_PROVIDER
                       env var (default: "anthropic").

    Returns:
        An LLMProvider instance.
    """
    name = (provider_name or os.environ.get("LLM_PROVIDER", "anthropic")).lower()

    if name in _instances:
        return _instances[name]

    if name == "anthropic":
        from src.llm.anthropic_provider import AnthropicProvider
        _instances[name] = AnthropicProvider()
    elif name == "openai":
        from src.llm.openai_provider import OpenAIProvider
        _instances[name] = OpenAIProvider()
    else:
        raise ValueError(
            f"Unknown LLM provider: {name!r}. "
            f"Supported: 'anthropic', 'openai'. "
            f"Set LLM_PROVIDER env var or pass provider_name explicitly."
        )

    return _instances[name]
