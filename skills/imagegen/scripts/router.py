"""Provider routing and selection logic."""

from typing import Optional

from skills.imagegen.config import ImageGenConfig
from skills.imagegen.providers.base import BaseProvider
from skills.imagegen.providers.google import GoogleProvider


class ProviderRouter:
    """Routes image generation requests to appropriate providers.

    The router acts as a factory, selecting and instantiating the correct
    provider based on configuration and availability. It provides a central
    point for provider discovery and selection strategies.

    Examples:
        >>> router = ProviderRouter(config)
        >>> provider = router.get_provider("google")
        >>> provider.generate("a sunset", Path("output.png"))
    """

    # Registry of available provider classes
    # Templates will be added as they're imported
    PROVIDER_CLASSES: dict[str, type[BaseProvider]] = {
        "google": GoogleProvider,
        "google-pro": GoogleProvider,
    }

    def __init__(self, config: ImageGenConfig):
        """Initialize router with configuration.

        Args:
            config: ImageGenConfig containing provider configurations
        """
        self.config = config

    def get_provider(self, name: Optional[str] = None) -> BaseProvider:
        """Get provider instance by name or use default.

        Args:
            name: Provider name (e.g., "google", "openai"). If None, uses
                  the default provider from config.

        Returns:
            BaseProvider: Instantiated provider ready for use

        Raises:
            ValueError: If provider name is unknown or API key is missing

        Examples:
            >>> provider = router.get_provider()  # Uses default
            >>> provider = router.get_provider("google-pro")  # Specific provider
        """
        provider_name = name or self.config.default_provider

        # Get provider configuration
        try:
            provider_config = self.config.get_provider_config(provider_name)
        except KeyError:
            available = ", ".join(self.config.providers.keys())
            raise ValueError(f"Unknown provider: {provider_name}\nAvailable providers: {available}")

        # Check if provider is in registry
        if provider_name not in self.PROVIDER_CLASSES:
            raise ValueError(
                f"Provider '{provider_name}' is not implemented.\n"
                f"Implemented providers: {', '.join(self.PROVIDER_CLASSES.keys())}"
            )

        # Get API key
        api_key = provider_config.get_api_key()
        if not api_key:
            raise ValueError(
                f"API key not found for provider '{provider_name}'.\n"
                f"Please set environment variable: {provider_config.api_key_env}\n"
                f"Example: export {provider_config.api_key_env}='your-api-key-here'"
            )

        # Instantiate provider
        provider_class = self.PROVIDER_CLASSES[provider_name]
        return provider_class(model=provider_config.model, api_key=api_key)

    def get_available_providers(self) -> list[dict]:
        """List all providers with availability status.

        Returns information about all configured providers including
        whether they're implemented and have API keys available.

        Returns:
            list[dict]: List of provider info dicts with keys:
                - name: Provider name (str)
                - model: Model identifier (str)
                - available: Whether API key is set (bool)
                - implemented: Whether provider code exists (bool)
                - api_key_env: Environment variable name (str)
                - enabled: Whether provider is enabled in config (bool)

        Examples:
            >>> providers = router.get_available_providers()
            >>> for p in providers:
            ...     if p['available'] and p['implemented']:
            ...         print(f"Ready to use: {p['name']}")
        """
        providers = []

        for name, pconfig in self.config.providers.items():
            # Check if implemented
            implemented = name in self.PROVIDER_CLASSES

            # Check if API key is available
            available = bool(pconfig.get_api_key())

            # Get enabled status (defaults to True if not specified)
            enabled = getattr(pconfig, "enabled", True)

            providers.append(
                {
                    "name": name,
                    "model": pconfig.model,
                    "available": available,
                    "implemented": implemented,
                    "api_key_env": pconfig.api_key_env,
                    "enabled": enabled,
                }
            )

        return providers

    @classmethod
    def register_provider(cls, name: str, provider_class: type[BaseProvider]) -> None:
        """Register a new provider class.

        This allows dynamic registration of providers at runtime,
        useful for plugins or extensions.

        Args:
            name: Provider name to register
            provider_class: Provider class to register

        Examples:
            >>> ProviderRouter.register_provider("custom", CustomProvider)
        """
        cls.PROVIDER_CLASSES[name] = provider_class
