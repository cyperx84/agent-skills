"""Google Gemini native image generation (Nano Banana / Nano Banana Pro)."""

import base64
from pathlib import Path
from typing import Optional, Union

import httpx

from skills.imagegen.providers.base import BaseProvider


class GoogleProvider(BaseProvider):
    """Google Gemini native image generation and editing.

    Models:
        - gemini-2.5-flash-image: Fast generation (Nano Banana)
        - gemini-3-pro-image-preview: Advanced with thinking, 4K (Nano Banana Pro)
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    # Valid aspect ratios
    ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]

    # Valid resolutions
    RESOLUTIONS = ["1K", "2K", "4K"]

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """List of supported aspect ratios."""
        return self.ASPECT_RATIOS

    @property
    def max_resolution(self) -> str:
        """Maximum supported resolution."""
        # gemini-3-pro-image-preview supports 4K, base model supports 1K
        if "gemini-3-pro" in self.model:
            return "4K"
        return "1K"

    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate image using Gemini native image generation.

        Args:
            prompt: Text description of image to generate
            output_path: Where to save the generated image
            **kwargs:
                aspect_ratio: One of ASPECT_RATIOS (default: "1:1")
                image_size: One of RESOLUTIONS (default: "1K")
                use_search: Enable Google Search grounding
        """
        await self._generate_content(prompt, output_path, input_images=None, **kwargs)

    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit image(s) using Gemini native image generation.

        Args:
            prompt: Text description of the edit to make
            output_path: Where to save the edited image
            input_images: List of input images (paths, bytes, or base64 strings)
            **kwargs:
                aspect_ratio: One of ASPECT_RATIOS (default: "1:1")
                image_size: One of RESOLUTIONS (default: "1K")
        """
        await self._generate_content(prompt, output_path, input_images=input_images, **kwargs)

    async def _generate_content(
        self,
        prompt: str,
        output_path: Path,
        input_images: Optional[list[Union[str, Path, bytes]]] = None,
        **kwargs,
    ) -> None:
        """Internal method for both generation and editing."""
        url = f"{self.BASE_URL}/models/{self.model}:generateContent"

        # Build generation config
        generation_config: dict = {
            "responseModalities": ["TEXT", "IMAGE"],
        }

        # Image config
        image_config: dict = {}

        aspect_ratio = kwargs.get("aspect_ratio", "1:1")
        if aspect_ratio in self.ASPECT_RATIOS:
            image_config["aspectRatio"] = aspect_ratio

        # Resolution (only supported by gemini-3-pro-image-preview)
        if "gemini-3-pro" in self.model:
            image_size = kwargs.get("image_size", "1K")
            if image_size in self.RESOLUTIONS:
                image_config["imageSize"] = image_size

        if image_config:
            generation_config["imageConfig"] = image_config

        # Build content parts
        parts: list[dict] = [{"text": prompt}]

        # Add input images for editing
        if input_images:
            for img in input_images:
                img_data = self._encode_image(img)
                parts.append(
                    {
                        "inlineData": {
                            "mimeType": img_data["mime_type"],
                            "data": img_data["data"],
                        }
                    }
                )

        # Build request payload
        payload: dict = {
            "contents": [{"parts": parts}],
            "generationConfig": generation_config,
        }

        # Google Search grounding
        if kwargs.get("use_search"):
            payload["tools"] = [{"google_search": {}}]

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        # Longer timeout for complex operations
        timeout = 300.0

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                raise RuntimeError(f"Gemini API error ({response.status_code}): {response.text}")

            data = response.json()

            # Extract image from response parts
            image_bytes = self._extract_image(data)
            if not image_bytes:
                raise RuntimeError("No image returned from Gemini API")

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(image_bytes)

    def _encode_image(self, image: Union[str, Path, bytes]) -> dict:
        """Encode image to base64 with mime type detection."""
        if isinstance(image, bytes):
            # Raw bytes
            data = base64.b64encode(image).decode()
            mime_type = self._detect_mime_type(image)
        elif isinstance(image, (str, Path)):
            path = Path(image)
            if not path.exists():
                raise ValueError(f"Image file not found: {path}")

            image_bytes = path.read_bytes()
            data = base64.b64encode(image_bytes).decode()
            mime_type = self._get_mime_from_extension(path.suffix)
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")

        return {"data": data, "mime_type": mime_type}

    @staticmethod
    def _detect_mime_type(data: bytes) -> str:
        """Detect mime type from image magic bytes."""
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return "image/png"
        elif data[:2] == b"\xff\xd8":
            return "image/jpeg"
        elif data[:6] in (b"GIF87a", b"GIF89a"):
            return "image/gif"
        elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            return "image/webp"
        else:
            return "image/png"  # Default fallback

    @staticmethod
    def _get_mime_from_extension(ext: str) -> str:
        """Get mime type from file extension."""
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return mime_map.get(ext.lower(), "image/png")

    def _extract_image(self, data: dict) -> Optional[bytes]:
        """Extract base64 image from Gemini response."""
        try:
            candidates = data.get("candidates", [])
            if not candidates:
                return None

            parts = candidates[0].get("content", {}).get("parts", [])

            for part in parts:
                # Skip thought parts (interim images)
                if part.get("thought"):
                    continue

                inline_data = part.get("inlineData")
                if inline_data and inline_data.get("data"):
                    return base64.b64decode(inline_data["data"])

            return None
        except (KeyError, IndexError):
            return None
