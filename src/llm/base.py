"""Abstract base class for LLM providers.

All provider implementations (Anthropic, OpenAI, etc.) must inherit from
LLMProvider and implement the generate() and generate_with_history() methods.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract interface for LLM API providers."""

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the active model name for this provider."""
        ...

    @abstractmethod
    def generate(self, prompt: str, *, model: str | None = None, temperature: float = 0.7) -> str:
        """Send a single user prompt and return the text response.

        Args:
            prompt: The user prompt to send.
            model: Override the default model name.
            temperature: Sampling temperature.

        Returns:
            The generated text response.

        Raises:
            APIError: If the call fails after retries.
        """
        ...

    @abstractmethod
    def generate_with_history(
        self,
        messages: list[dict],
        *,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> str:
        """Send a multi-turn conversation and return the assistant's text.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            model: Override the default model name.
            temperature: Sampling temperature.

        Returns:
            The generated text response.

        Raises:
            APIError: If the call fails after retries.
        """
        ...
