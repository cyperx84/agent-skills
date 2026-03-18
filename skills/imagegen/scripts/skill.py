"""ImageGen skill implementation."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from agent.skills.base import BaseSkill, tool_schema
from skills.imagegen.config import ImageGenConfig
from skills.imagegen.providers.base import BaseProvider
from skills.imagegen.router import ProviderRouter


class ImageGenSkill(BaseSkill):
    """Multi-provider image generation and editing skill.

    Supports multiple image generation providers including Google Gemini,
    OpenAI DALL-E, Replicate, Stability AI, Together AI, and Hugging Face.

    Currently working:
        - Google Gemini (gemini-2.5-flash-image, gemini-3-pro-image-preview)

    Template providers (educational examples):
        - OpenAI DALL-E 3
        - Replicate (FLUX, SDXL)
        - Stability AI (SD3, SDXL)
        - Together AI (FLUX)
        - Hugging Face (community models)
    """

    def __init__(self, skill_path: Optional[Path] = None):
        """Initialize skill.

        Args:
            skill_path: Optional path to skill directory
        """
        super().__init__(skill_path)
        self._config: Optional[ImageGenConfig] = None
        self._router: Optional[ProviderRouter] = None

    @property
    def name(self) -> str:
        return "imagegen"

    @property
    def config(self) -> ImageGenConfig:
        """Get skill configuration."""
        if self._config is None:
            self._config = ImageGenConfig.load()
        return self._config

    @property
    def router(self) -> ProviderRouter:
        """Get provider router."""
        if self._router is None:
            self._router = ProviderRouter(self.config)
        return self._router

    def get_tools(self) -> list[Callable]:
        """Return list of tool functions."""
        return [
            self.generate_image,
            self.edit_image,
            self.list_providers,
        ]

    def _get_provider(self, name: Optional[str] = None) -> BaseProvider:
        """Get provider instance by name via router.

        Args:
            name: Provider name. Uses default if not specified.

        Returns:
            Provider instance

        Raises:
            ValueError: If provider not found or API key missing
        """
        return self.router.get_provider(name)

    def _generate_filename(self, prompt: str, extension: str = ".png") -> str:
        """Generate filename from prompt.

        Args:
            prompt: Image prompt
            extension: File extension

        Returns:
            Generated filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create slug from prompt
        slug = re.sub(r"[^\w\s-]", "", prompt.lower())
        slug = re.sub(r"[-\s]+", "_", slug)
        slug = slug[:50]  # Limit length

        pattern = self.config.filename_pattern
        filename = pattern.format(timestamp=timestamp, prompt_slug=slug)

        return f"{filename}{extension}"

    @tool_schema(
        prompt={
            "type": "string",
            "description": "Text description of the image to generate",
            "required": True,
        },
        provider={
            "type": "string",
            "description": "Provider (google, google-pro)",
            "required": False,
        },
        output_path={
            "type": "string",
            "description": "Output directory or file path",
            "required": False,
        },
        aspect_ratio={
            "type": "string",
            "description": "Aspect ratio (1:1, 16:9, 9:16, etc.)",
            "required": False,
        },
        resolution={"type": "string", "description": "Resolution (1K, 2K, 4K)", "required": False},
    )
    async def generate_image(self, args: dict[str, Any]) -> dict[str, Any]:
        """Generate an image from a text prompt.

        Args:
            args: Tool arguments containing prompt and options

        Returns:
            Result dict with generated image path and markdown
        """
        prompt = args.get("prompt")
        if not prompt:
            return {
                "content": [{"type": "text", "text": "Error: prompt is required"}],
                "is_error": True,
            }

        provider_name = args.get("provider")
        output_path = args.get("output_path")
        aspect_ratio = args.get("aspect_ratio", "1:1")
        resolution = args.get("resolution", "1K")

        try:
            provider = self._get_provider(provider_name)

            # Determine output path
            if output_path:
                out_path = Path(output_path)
                if out_path.is_dir() or not out_path.suffix:
                    out_path = out_path / self._generate_filename(prompt)
            else:
                out_dir = self.config.ensure_output_dir()
                out_path = out_dir / self._generate_filename(prompt)

            # Generate image
            await provider.generate(
                prompt=prompt,
                output_path=out_path,
                aspect_ratio=aspect_ratio,
                image_size=resolution,
            )

            # Generate markdown
            markdown = f"![{prompt[:50]}]({out_path})"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Generated image: {out_path}\nMarkdown: {markdown}",
                    }
                ],
                "metadata": {
                    "image_path": str(out_path),
                    "markdown": markdown,
                    "provider": provider_name or self.config.default_provider,
                },
            }

        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error generating image: {e}"}],
                "is_error": True,
            }

    @tool_schema(
        prompt={
            "type": "string",
            "description": "Text description of the edit to make",
            "required": True,
        },
        input_images={
            "type": "array",
            "description": "List of input image paths",
            "required": True,
        },
        provider={
            "type": "string",
            "description": "Provider (google, google-pro)",
            "required": False,
        },
        output_path={
            "type": "string",
            "description": "Output directory or file path",
            "required": False,
        },
        aspect_ratio={"type": "string", "description": "Output aspect ratio", "required": False},
    )
    async def edit_image(self, args: dict[str, Any]) -> dict[str, Any]:
        """Edit an existing image with a text prompt.

        Args:
            args: Tool arguments containing prompt, input images, and options

        Returns:
            Result dict with edited image path and markdown
        """
        prompt = args.get("prompt")
        input_images = args.get("input_images", [])

        if not prompt:
            return {
                "content": [{"type": "text", "text": "Error: prompt is required"}],
                "is_error": True,
            }

        if not input_images:
            return {
                "content": [{"type": "text", "text": "Error: input_images is required"}],
                "is_error": True,
            }

        provider_name = args.get("provider", "google-pro")  # Default to pro for editing
        output_path = args.get("output_path")
        aspect_ratio = args.get("aspect_ratio", "1:1")

        try:
            provider = self._get_provider(provider_name)

            # Validate input images exist
            validated_images = []
            for img_path in input_images:
                path = Path(img_path)
                if not path.exists():
                    return {
                        "content": [
                            {"type": "text", "text": f"Error: Input image not found: {img_path}"}
                        ],
                        "is_error": True,
                    }
                validated_images.append(path)

            # Determine output path
            if output_path:
                out_path = Path(output_path)
                if out_path.is_dir() or not out_path.suffix:
                    out_path = out_path / self._generate_filename(f"edited_{prompt}")
            else:
                out_dir = self.config.ensure_output_dir()
                out_path = out_dir / self._generate_filename(f"edited_{prompt}")

            # Edit image
            await provider.edit(
                prompt=prompt,
                output_path=out_path,
                input_images=validated_images,
                aspect_ratio=aspect_ratio,
            )

            # Generate markdown
            markdown = f"![{prompt[:50]}]({out_path})"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Edited image: {out_path}\nMarkdown: {markdown}",
                    }
                ],
                "metadata": {
                    "image_path": str(out_path),
                    "markdown": markdown,
                    "provider": provider_name,
                    "input_images": [str(p) for p in validated_images],
                },
            }

        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error editing image: {e}"}],
                "is_error": True,
            }

    @tool_schema()
    async def list_providers(self, args: dict[str, Any]) -> dict[str, Any]:
        """List available image generation providers.

        Shows all configured providers with their implementation status,
        availability (API key set), and supported features.

        Returns:
            Result dict with provider information
        """
        providers = self.router.get_available_providers()

        # Separate working vs template providers
        working = [p for p in providers if p["implemented"] and p["enabled"]]
        templates = [p for p in providers if not p["implemented"] or not p["enabled"]]

        # Format as text
        lines = []

        if working:
            lines.append("✅ Working Providers (Fully Implemented):")
            for p in working:
                status = "✓ ready" if p["available"] else f"✗ missing {p['api_key_env']}"
                lines.append(f"  - {p['name']}: {p['model']} ({status})")

        if templates:
            lines.append("\n📝 Template Providers (Educational Examples):")
            for p in templates:
                has_key = "✓ key set" if p["available"] else "✗ no key"
                lines.append(f"  - {p['name']}: {p['model']} (template, {has_key})")

        lines.append("\nTo implement a template provider, see:")
        lines.append("  docs/skills/imagegen/providers/creating.md")

        return {
            "content": [{"type": "text", "text": "\n".join(lines)}],
            "metadata": {"providers": providers},
        }
