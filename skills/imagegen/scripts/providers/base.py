"""Base provider interface for image generation."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from skills.imagegen.telemetry import TelemetryCollector


class BaseProvider(ABC):
    """Abstract base class for image generation providers.

    All image generation providers must inherit from this class
    and implement the required methods. Providers should also
    override capability properties to accurately describe their
    features.

    Examples:
        >>> class MyProvider(BaseProvider):
        ...     @property
        ...     def supports_editing(self) -> bool:
        ...         return True
        ...
        ...     async def generate(self, prompt, output_path, **kwargs):
        ...         # Implementation here
        ...         pass
    """

    def __init__(self, model: str, api_key: str, telemetry: Optional["TelemetryCollector"] = None):
        """Initialize provider with model and API key.

        Args:
            model: Model identifier (e.g., "gemini-2.5-flash-image")
            api_key: API key for authentication
            telemetry: Optional telemetry collector for metrics tracking
        """
        self.model = model
        self.api_key = api_key
        self.telemetry = telemetry

    @abstractmethod
    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate image from text prompt.

        Args:
            prompt: Text description of image to generate
            output_path: Where to save the generated image
            **kwargs: Provider-specific options
        """
        pass

    @abstractmethod
    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit image(s) with text prompt.

        Args:
            prompt: Text description of the edit to make
            output_path: Where to save the edited image
            input_images: List of input images
            **kwargs: Provider-specific options
        """
        pass

    @property
    def supports_editing(self) -> bool:
        """Whether this provider supports image editing.

        Override this if the provider doesn't support editing operations.

        Returns:
            bool: True if provider supports edit(), False otherwise
        """
        return True

    @property
    def supports_batch(self) -> bool:
        """Whether this provider supports batch generation.

        Batch generation allows generating multiple images in a single
        API call, which can be more efficient and cost-effective.

        Returns:
            bool: True if provider supports batch operations

        Note:
            Future enhancement - batch support not yet implemented in base
        """
        return False

    @property
    def max_resolution(self) -> str:
        """Maximum supported image resolution.

        Returns:
            str: Maximum resolution (e.g., "1K", "2K", "4K")

        Note:
            Override this in provider implementations to indicate capability
        """
        return "1K"

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """List of supported aspect ratios.

        Returns:
            list[str]: Supported aspect ratios (e.g., ["1:1", "16:9"])

        Note:
            Override this in provider implementations with actual supported ratios
        """
        return ["1:1"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(model={self.model!r})>"
