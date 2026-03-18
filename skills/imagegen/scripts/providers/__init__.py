"""Image generation providers.

This module exports all available image generation providers and registers
them with the ProviderRouter for discovery and use.

Working Providers:
    - GoogleProvider: Fully implemented (gemini-2.5-flash-image, gemini-3-pro-image-preview)

Template Providers (Educational Examples):
    - OpenAIProvider: DALL-E 3 template
    - ReplicateProvider: FLUX/SDXL template
    - StabilityProvider: Stable Diffusion template
    - TogetherProvider: Together AI template
    - HuggingFaceProvider: Hugging Face template
"""

from skills.imagegen.providers.base import BaseProvider
from skills.imagegen.providers.google import GoogleProvider
from skills.imagegen.providers.huggingface_provider import HuggingFaceProvider
from skills.imagegen.providers.openai_provider import OpenAIProvider
from skills.imagegen.providers.replicate_provider import ReplicateProvider
from skills.imagegen.providers.stability_provider import StabilityProvider
from skills.imagegen.providers.together_provider import TogetherProvider

# Register all providers with the router
from skills.imagegen.router import ProviderRouter

# Register template providers
ProviderRouter.register_provider("openai", OpenAIProvider)
ProviderRouter.register_provider("replicate", ReplicateProvider)
ProviderRouter.register_provider("stability", StabilityProvider)
ProviderRouter.register_provider("together", TogetherProvider)
ProviderRouter.register_provider("huggingface", HuggingFaceProvider)

__all__ = [
    "BaseProvider",
    "GoogleProvider",
    "OpenAIProvider",
    "ReplicateProvider",
    "StabilityProvider",
    "TogetherProvider",
    "HuggingFaceProvider",
]
