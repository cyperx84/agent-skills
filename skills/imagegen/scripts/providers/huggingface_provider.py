"""Hugging Face provider (TEMPLATE - Not Implemented).

This is a template provider demonstrating how to implement image generation
with the Hugging Face Inference API. This provider showcases integration
with the open-source community and custom model support.

To implement this provider:
1. Get API token from https://huggingface.co/settings/tokens
2. Set environment: `export HUGGINGFACE_API_KEY='hf_...'`
3. Implement the methods below

API Documentation:
    https://huggingface.co/docs/api-inference/index
"""

from pathlib import Path
from typing import Union

from skills.imagegen.providers.base import BaseProvider


class HuggingFaceProvider(BaseProvider):
    """Hugging Face image generation provider (TEMPLATE).

    Hugging Face provides access to thousands of community models through
    their Inference API. This provider demonstrates how to integrate with
    community models and handle variable response formats.

    Key Features:
        - Access to 1000+ image generation models
        - Free tier available (rate limited)
        - Custom model support
        - Community fine-tunes
        - Latest research models
        - Flexible model selection

    Popular Models:
        - stabilityai/stable-diffusion-xl-base-1.0: SDXL base
        - runwayml/stable-diffusion-v1-5: SD 1.5
        - prompthero/openjourney: Midjourney-style
        - wavymulder/Analog-Diffusion: Analog photo style
        - Any community fine-tune on the Hub

    API Pattern:
        POST to model inference endpoint with prompt, receive image bytes
        Response format varies by model (usually raw image bytes or JSON)

    Pricing:
        - Free tier: Rate limited, shared infrastructure
        - Pro: $9/month, higher rate limits
        - Enterprise: Dedicated endpoints

    Note:
        Response format can vary between models. Some return raw bytes,
        others return JSON with base64. Check model card for details.
    """

    BASE_URL = "https://api-inference.huggingface.co/models"

    @property
    def supports_editing(self) -> bool:
        """Depends on model, some support img2img/inpainting."""
        return False  # Default to False, override for specific models

    @property
    def max_resolution(self) -> str:
        """Varies by model."""
        return "1K"

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """Varies by model."""
        return ["1:1"]

    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate an image using Hugging Face (TEMPLATE - NOT IMPLEMENTED).

        Args:
            prompt: Text description of the image to generate
            output_path: Where to save the generated image
            **kwargs:
                negative_prompt: What to avoid (if model supports)
                num_inference_steps: Number of steps (if model supports)
                guidance_scale: CFG scale (if model supports)
                wait_for_model: Wait if model is loading (default True)

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation (Raw Bytes Response):
            ```python
            import httpx

            payload = {
                "inputs": prompt,
            }

            # Add optional parameters if supported by model
            parameters = {}
            if "negative_prompt" in kwargs:
                parameters["negative_prompt"] = kwargs["negative_prompt"]
            if "num_inference_steps" in kwargs:
                parameters["num_inference_steps"] = kwargs["num_inference_steps"]
            if "guidance_scale" in kwargs:
                parameters["guidance_scale"] = kwargs["guidance_scale"]

            if parameters:
                payload["parameters"] = parameters

            wait_for_model = kwargs.get("wait_for_model", True)

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/{self.model}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    params={"wait_for_model": wait_for_model}
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                # Response is raw image bytes for most models
                image_bytes = response.content

                # Save image
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_bytes)
            ```

        Example Implementation (JSON Response):
            ```python
            # Some models return JSON with base64
            import base64

            data = response.json()

            # Handle different response formats
            if isinstance(data, list) and len(data) > 0:
                # Format: [{"image": "base64string"}]
                if "image" in data[0]:
                    image_b64 = data[0]["image"]
                    image_bytes = base64.b64decode(image_b64)
                else:
                    # Fallback: raw bytes
                    image_bytes = response.content
            else:
                image_bytes = response.content

            output_path.write_bytes(image_bytes)
            ```

        Reference:
            - HF Inference API: https://huggingface.co/docs/api-inference
            - Model cards: Check specific model page for parameters
        """
        raise NotImplementedError(
            "Hugging Face provider is a template and not yet implemented.\n\n"
            "To implement this provider:\n"
            "1. Get your API token:\n"
            "   https://huggingface.co/settings/tokens\n\n"
            "2. Set environment variable:\n"
            "   export HUGGINGFACE_API_KEY='hf_...'\n\n"
            "3. Choose a model from Hugging Face Hub:\n"
            "   - stabilityai/stable-diffusion-xl-base-1.0\n"
            "   - runwayml/stable-diffusion-v1-5\n"
            "   - Or any community model\n\n"
            "4. Implement this method using the pattern above\n\n"
            "5. Key considerations:\n"
            "   - Response format varies by model (bytes vs JSON)\n"
            "   - Check model card for supported parameters\n"
            "   - Free tier is rate limited\n"
            "   - Models may need warmup time (use wait_for_model)\n\n"
            "Popular models:\n"
            "- stabilityai/stable-diffusion-xl-base-1.0 (SDXL)\n"
            "- runwayml/stable-diffusion-v1-5 (classic SD)\n"
            "- prompthero/openjourney (Midjourney-style)\n\n"
            "Documentation:\n"
            "- Provider guide: docs/skills/imagegen/providers/creating.md\n"
            "- HF Inference: https://huggingface.co/docs/api-inference\n"
            "- Example: docs/skills/imagegen/providers/huggingface.md\n"
            "- Browse models: https://huggingface.co/models?pipeline_tag=text-to-image"
        )

    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit an image using Hugging Face (TEMPLATE - NOT IMPLEMENTED).

        Some Hugging Face models support img2img or inpainting.
        Check the specific model's documentation.

        Args:
            prompt: Text description of the desired edit
            output_path: Where to save the edited image
            input_images: List of input images
            **kwargs: Model-specific parameters

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation (img2img):
            ```python
            import httpx
            import base64
            from pathlib import Path

            image_path = Path(input_images[0])
            image_bytes = image_path.read_bytes()
            image_b64 = base64.b64encode(image_bytes).decode()

            payload = {
                "inputs": {
                    "prompt": prompt,
                    "image": image_b64
                },
                "parameters": {
                    "strength": kwargs.get("strength", 0.75),
                }
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/{self.model}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                output_path.write_bytes(response.content)
            ```
        """
        raise NotImplementedError(
            "Hugging Face edit method is a template.\n\n"
            "Some HF models support img2img or inpainting:\n"
            "- timbrooks/instruct-pix2pix (instruction-based editing)\n"
            "- runwayml/stable-diffusion-inpainting\n\n"
            "Check model card for specific API usage.\n\n"
            "See: docs/skills/imagegen/providers/huggingface.md"
        )
