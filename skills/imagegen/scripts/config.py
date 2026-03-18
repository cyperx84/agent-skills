"""ImageGen skill configuration."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class ProviderConfig(BaseModel):
    """Configuration for a single provider.

    Attributes:
        model: Model identifier (e.g., "gemini-2.5-flash-image")
        api_key_env: Environment variable name for API key
        enabled: Whether this provider is enabled (templates are disabled by default)
        max_resolution: Maximum supported resolution (e.g., "1K", "2K", "4K")
        supported_operations: List of supported operations (["generate", "edit"])
        cost_per_generation: Estimated cost per image in USD (for future tracking)
    """

    model: str
    api_key_env: str = "GEMINI_API_KEY"
    enabled: bool = True
    max_resolution: Optional[str] = None
    supported_operations: list[str] = ["generate", "edit"]
    cost_per_generation: Optional[float] = None  # USD, for future cost tracking

    def get_api_key(self) -> Optional[str]:
        """Get API key from environment."""
        return os.environ.get(self.api_key_env)


class ImageGenConfig(BaseModel):
    """ImageGen skill configuration."""

    default_provider: str = "google"
    output_dir: Path = Field(default=Path("./attachments"))
    filename_pattern: str = "{timestamp}_{prompt_slug}"

    providers: dict[str, ProviderConfig] = Field(
        default_factory=lambda: {
            # Working providers (fully implemented)
            "google": ProviderConfig(
                model="gemini-2.5-flash-image",
                api_key_env="GEMINI_API_KEY",
                enabled=True,
                max_resolution="1K",
                supported_operations=["generate", "edit"],
                cost_per_generation=0.039,  # $0.039 per image
            ),
            "google-pro": ProviderConfig(
                model="gemini-3-pro-image-preview",
                api_key_env="GEMINI_API_KEY",
                enabled=True,
                max_resolution="4K",
                supported_operations=["generate", "edit"],
                cost_per_generation=0.039,  # Placeholder, actual pricing TBD
            ),
            # Template providers (not implemented, for educational purposes)
            "openai": ProviderConfig(
                model="dall-e-3",
                api_key_env="OPENAI_API_KEY",
                enabled=False,  # Template only
                max_resolution="2K",
                supported_operations=["generate", "edit"],
                cost_per_generation=0.040,  # $0.04 per 1024x1024 image
            ),
            "replicate": ProviderConfig(
                model="black-forest-labs/flux-schnell",
                api_key_env="REPLICATE_API_TOKEN",
                enabled=False,  # Template only
                max_resolution="1K",
                supported_operations=["generate"],  # No editing
                cost_per_generation=0.003,  # ~$0.003 per image
            ),
            "stability": ProviderConfig(
                model="stable-diffusion-xl-1024-v1-0",
                api_key_env="STABILITY_API_KEY",
                enabled=False,  # Template only
                max_resolution="1K",
                supported_operations=["generate", "edit"],
                cost_per_generation=0.035,  # ~$0.035 per image
            ),
            "together": ProviderConfig(
                model="black-forest-labs/FLUX.1-schnell",
                api_key_env="TOGETHER_API_KEY",
                enabled=False,  # Template only
                max_resolution="1K",
                supported_operations=["generate"],  # No editing
                cost_per_generation=0.0004,  # ~$0.0004 per image (4 steps)
            ),
            "huggingface": ProviderConfig(
                model="stabilityai/stable-diffusion-xl-base-1.0",
                api_key_env="HUGGINGFACE_API_KEY",
                enabled=False,  # Template only
                max_resolution="1K",
                supported_operations=["generate"],  # Varies by model
                cost_per_generation=0.0,  # Free tier available
            ),
        }
    )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "ImageGenConfig":
        """Load configuration from YAML file.

        Searches for .imagegen.yaml in:
        1. Provided path
        2. Current directory
        3. Home directory
        """
        search_paths = []
        if config_path:
            search_paths.append(config_path)
        search_paths.extend(
            [
                Path(".imagegen.yaml"),
                Path.home() / ".imagegen.yaml",
            ]
        )

        for path in search_paths:
            if path.exists():
                with open(path) as f:
                    data = yaml.safe_load(f)
                    if data:
                        # Convert providers to ProviderConfig
                        if "providers" in data:
                            data["providers"] = {
                                name: ProviderConfig(**pconfig)
                                for name, pconfig in data["providers"].items()
                            }
                        return cls(**data)

        return cls()

    def get_provider_config(self, name: Optional[str] = None) -> ProviderConfig:
        """Get provider configuration.

        Args:
            name: Provider name. Uses default if not specified.

        Returns:
            Provider configuration

        Raises:
            KeyError: If provider not found
        """
        provider_name = name or self.default_provider
        if provider_name not in self.providers:
            raise KeyError(f"Unknown provider: {provider_name}")
        return self.providers[provider_name]

    def ensure_output_dir(self) -> Path:
        """Ensure output directory exists and return it."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir
