"""OpenAI DALL-E 3 provider (TEMPLATE - Not Implemented).

This is a template provider demonstrating how to implement image generation
with the OpenAI DALL-E 3 API. This provider is not fully implemented and
serves as an educational example showing the URL-based image retrieval pattern.

To implement this provider:
1. Install OpenAI SDK: `uv pip install openai`
2. Get API key from https://platform.openai.com/api-keys
3. Set environment: `export OPENAI_API_KEY='sk-...'`
4. Implement the methods below following the GoogleProvider pattern

API Documentation:
    https://platform.openai.com/docs/guides/images/introduction
"""

from pathlib import Path
from typing import Union

from skills.imagegen.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI DALL-E 3 image generation provider (TEMPLATE).

    DALL-E 3 supports high-quality image generation and editing with a
    REST API that returns image URLs (different from base64 response pattern).

    Key Features:
        - High-quality, photorealistic images
        - Natural language understanding
        - Image editing with masks
        - Multiple size options
        - Style and quality controls

    Models:
        - dall-e-3: Latest high-quality model
        - dall-e-2: Previous generation (more affordable)

    API Pattern:
        This provider demonstrates the URL-based retrieval pattern:
        1. POST to /v1/images/generations
        2. Receive response with image URL
        3. Download image from URL
        4. Save to output_path

    Supported Sizes:
        - 1024x1024 (square)
        - 1792x1024 (landscape)
        - 1024x1792 (portrait)

    Pricing (as of 2025):
        - DALL-E 3 Standard: $0.040 per image (1024x1024)
        - DALL-E 3 HD: $0.080 per image (1024x1024)
        - DALL-E 2: $0.020 per image (1024x1024)
    """

    BASE_URL = "https://api.openai.com/v1"

    # Supported sizes for DALL-E 3
    SIZES = ["1024x1024", "1792x1024", "1024x1792"]

    # Quality options
    QUALITIES = ["standard", "hd"]  # HD costs 2x

    # Style options
    STYLES = ["vivid", "natural"]

    @property
    def supports_editing(self) -> bool:
        """DALL-E supports image editing with inpainting."""
        return True

    @property
    def max_resolution(self) -> str:
        """Maximum resolution is 1792x1024."""
        return "2K"

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """Supported aspect ratios."""
        return ["1:1", "16:9", "9:16"]

    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate an image using DALL-E 3 (TEMPLATE - NOT IMPLEMENTED).

        Args:
            prompt: Text description of the image to generate
            output_path: Where to save the generated image
            **kwargs:
                size: Image size ("1024x1024", "1792x1024", "1024x1792")
                quality: "standard" or "hd" (hd costs 2x)
                style: "vivid" or "natural"
                n: Number of images to generate (1-10, default 1)

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation:
            ```python
            import httpx

            size = kwargs.get("size", "1024x1024")
            quality = kwargs.get("quality", "standard")
            style = kwargs.get("style", "vivid")
            n = kwargs.get("n", 1)

            async with httpx.AsyncClient(timeout=120.0) as client:
                # Make API request
                response = await client.post(
                    f"{self.BASE_URL}/images/generations",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "size": size,
                        "quality": quality,
                        "style": style,
                        "n": n,
                        "response_format": "url"  # Get URL, not base64
                    }
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                data = response.json()

                # Download image from URL
                image_url = data["data"][0]["url"]
                img_response = await client.get(image_url)

                # Save image
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(img_response.content)
            ```

        Reference:
            See skills/imagegen/providers/google.py for a complete implementation
            See docs/skills/imagegen/providers/creating.md for step-by-step guide
        """
        raise NotImplementedError(
            "OpenAI DALL-E 3 provider is a template and not yet implemented.\n\n"
            "To implement this provider:\n"
            "1. Install OpenAI SDK:\n"
            "   uv pip install openai\n\n"
            "2. Get your API key:\n"
            "   https://platform.openai.com/api-keys\n\n"
            "3. Set environment variable:\n"
            "   export OPENAI_API_KEY='sk-...'\n\n"
            "4. Implement this method using the pattern above\n\n"
            "5. Key differences from Google provider:\n"
            "   - API returns image URL (not base64)\n"
            "   - Need to download image from URL\n"
            "   - Different parameter names (size vs aspect_ratio)\n\n"
            "Documentation:\n"
            "- Provider guide: docs/skills/imagegen/providers/creating.md\n"
            "- OpenAI docs: https://platform.openai.com/docs/guides/images\n"
            "- Reference impl: skills/imagegen/providers/google.py"
        )

    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit an image using DALL-E (TEMPLATE - NOT IMPLEMENTED).

        DALL-E supports image editing (inpainting) where you can modify
        specific parts of an image using a mask.

        Args:
            prompt: Text description of the desired edit
            output_path: Where to save the edited image
            input_images: List containing [image, mask] (mask is optional)
            **kwargs:
                size: Output image size
                n: Number of variations to generate

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation:
            ```python
            import httpx
            from pathlib import Path

            image_path = Path(input_images[0])
            mask_path = Path(input_images[1]) if len(input_images) > 1 else None

            size = kwargs.get("size", "1024x1024")

            async with httpx.AsyncClient(timeout=120.0) as client:
                # Prepare files for multipart upload
                files = {
                    "image": image_path.read_bytes(),
                }
                if mask_path:
                    files["mask"] = mask_path.read_bytes()

                data = {
                    "prompt": prompt,
                    "size": size,
                    "n": 1,
                }

                response = await client.post(
                    f"{self.BASE_URL}/images/edits",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files=files,
                    data=data
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                result = response.json()

                # Download edited image
                image_url = result["data"][0]["url"]
                img_response = await client.get(image_url)

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(img_response.content)
            ```

        Reference:
            https://platform.openai.com/docs/guides/images/edits
        """
        raise NotImplementedError(
            "OpenAI DALL-E 3 edit method is a template.\n\n"
            "Implementation notes:\n"
            "- DALL-E editing requires multipart/form-data upload\n"
            "- Image must be PNG, square, and <4MB\n"
            "- Mask (optional) indicates where to edit (transparent areas)\n"
            "- Returns URL to download edited image\n\n"
            "See: docs/skills/imagegen/providers/openai.md for detailed guide"
        )
