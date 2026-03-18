"""Together AI provider (TEMPLATE - Not Implemented).

This is a template provider demonstrating how to implement image generation
with the Together AI API. Together provides fast inference for open models
including FLUX at very competitive pricing.

To implement this provider:
1. Get API key from https://api.together.xyz/settings/api-keys
2. Set environment: `export TOGETHER_API_KEY='...'`
3. Implement the methods below

API Documentation:
    https://docs.together.ai/reference/image-models
"""

from pathlib import Path
from typing import Union

from skills.imagegen.providers.base import BaseProvider


class TogetherProvider(BaseProvider):
    """Together AI image generation provider (TEMPLATE).

    Together AI provides fast, cost-effective inference for open-source
    models including FLUX.1, Stable Diffusion, and others. Known for
    excellent performance and competitive pricing.

    Key Features:
        - FLUX.1-schnell (ultra-fast, ~2s)
        - FLUX.1-dev (high quality)
        - Stable Diffusion XL
        - Very competitive pricing
        - Fast inference infrastructure
        - Simple API (similar to OpenAI)

    Models:
        - black-forest-labs/FLUX.1-schnell: Fast FLUX ($0.00001/step)
        - black-forest-labs/FLUX.1-dev: Quality FLUX
        - stabilityai/stable-diffusion-xl-base-1.0: SDXL
        - prompthero/openjourney: Midjourney-style SD

    API Pattern:
        Simple REST API with base64 response (similar to Google/Stability)
        1. POST to /inference
        2. Receive base64 encoded image in response
        3. Decode and save

    Pricing (as of 2025):
        - FLUX.1-schnell: $0.00001 per step (~$0.0004/image at 4 steps)
        - FLUX.1-dev: $0.00005 per step (~$0.0025/image at 50 steps)
        - SDXL: $0.01 per image

    Note:
        Together is one of the most cost-effective options for FLUX models.
    """

    BASE_URL = "https://api.together.xyz/v1"

    @property
    def supports_editing(self) -> bool:
        """Most Together models focus on generation."""
        return False

    @property
    def max_resolution(self) -> str:
        """Typically 1024x1024 for most models."""
        return "1K"

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """Supports various aspect ratios."""
        return ["1:1", "16:9", "9:16", "3:2", "2:3"]

    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate an image using Together AI (TEMPLATE - NOT IMPLEMENTED).

        Args:
            prompt: Text description of the image to generate
            output_path: Where to save the generated image
            **kwargs:
                width: Image width (default 1024)
                height: Image height (default 1024)
                steps: Number of inference steps (4-50)
                seed: Random seed for reproducibility
                n: Number of images to generate (default 1)

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation:
            ```python
            import httpx
            import base64

            width = kwargs.get("width", 1024)
            height = kwargs.get("height", 1024)
            steps = kwargs.get("steps", 4)  # 4 for schnell, 28+ for dev
            n = kwargs.get("n", 1)

            payload = {
                "model": self.model,
                "prompt": prompt,
                "width": width,
                "height": height,
                "steps": steps,
                "n": n,
            }

            # Add seed if provided
            seed = kwargs.get("seed")
            if seed is not None:
                payload["seed"] = seed

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/images/generations",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                data = response.json()

                # Together returns base64 encoded images
                # Format: {"data": [{"b64_json": "..."}, ...]}
                image_b64 = data["data"][0]["b64_json"]
                image_bytes = base64.b64decode(image_b64)

                # Save image
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_bytes)
            ```

        Reference:
            - Together docs: https://docs.together.ai/reference/image-models
            - FLUX schnell: Fast 4-step generation
            - FLUX dev: Higher quality, more steps
        """
        raise NotImplementedError(
            "Together AI provider is a template and not yet implemented.\n\n"
            "To implement this provider:\n"
            "1. Get your API key:\n"
            "   https://api.together.xyz/settings/api-keys\n\n"
            "2. Set environment variable:\n"
            "   export TOGETHER_API_KEY='...'\n\n"
            "3. Implement this method using the pattern above\n\n"
            "4. Key features:\n"
            "   - Simple API (similar to OpenAI format)\n"
            "   - Base64 response (like Google/Stability)\n"
            "   - Very fast for FLUX.1-schnell (4 steps)\n"
            "   - Most cost-effective FLUX provider\n\n"
            "Recommended models:\n"
            "- black-forest-labs/FLUX.1-schnell (fast, $0.0004/image)\n"
            "- black-forest-labs/FLUX.1-dev (quality, $0.0025/image)\n\n"
            "Documentation:\n"
            "- Provider guide: docs/skills/imagegen/providers/creating.md\n"
            "- Together docs: https://docs.together.ai/docs/image-models\n"
            "- Example: docs/skills/imagegen/providers/together.md"
        )

    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit an image using Together AI (TEMPLATE - NOT IMPLEMENTED).

        Most Together models don't support editing, only generation.
        You could use img2img models if available.

        Args:
            prompt: Text description of the desired edit
            output_path: Where to save the edited image
            input_images: List of input images
            **kwargs: Model-specific parameters

        Raises:
            NotImplementedError: This is a template provider
        """
        raise NotImplementedError(
            "Together AI edit method is a template.\n\n"
            "Most Together models focus on text-to-image generation.\n"
            "Check Together AI docs for img2img model availability:\n"
            "https://docs.together.ai/docs/image-models\n\n"
            "See: docs/skills/imagegen/providers/together.md"
        )
