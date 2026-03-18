"""Replicate provider (TEMPLATE - Not Implemented).

This is a template provider demonstrating how to implement image generation
with the Replicate API. This provider showcases the async polling pattern
for services that don't provide immediate results.

To implement this provider:
1. Install replicate: `uv pip install replicate`
2. Get API token from https://replicate.com/account/api-tokens
3. Set environment: `export REPLICATE_API_TOKEN='r8_...'`
4. Implement the methods below following the patterns

API Documentation:
    https://replicate.com/docs/reference/http
"""

from pathlib import Path
from typing import Union

from skills.imagegen.providers.base import BaseProvider


class ReplicateProvider(BaseProvider):
    """Replicate image generation provider (TEMPLATE).

    Replicate provides access to FLUX, Stable Diffusion, and many other
    open-source models. It uses an async polling pattern where you submit
    a prediction and poll for results.

    Key Features:
        - Access to FLUX.1-schnell, FLUX.1-dev models
        - Stable Diffusion XL and variants
        - Custom model hosting
        - Very affordable pricing
        - Community models

    Popular Models:
        - black-forest-labs/flux-schnell: Fast FLUX model (~1s generation)
        - black-forest-labs/flux-dev: High-quality FLUX model
        - stability-ai/sdxl: Stable Diffusion XL
        - bytedance/sdxl-lightning-4step: 4-step SDXL

    API Pattern (Async Polling):
        1. POST to /v1/predictions (create prediction)
        2. Receive prediction ID
        3. Poll GET /v1/predictions/{id} until status is "succeeded"
        4. Download image from output URL
        5. Save to output_path

    Alternative (Webhooks):
        For production, you can use webhooks instead of polling.
        The API will POST results to your webhook URL when ready.

    Pricing (pay-per-use, as of 2025):
        - FLUX Schnell: ~$0.003 per image
        - FLUX Dev: ~$0.01 per image
        - SDXL: ~$0.0055 per image
    """

    BASE_URL = "https://api.replicate.com/v1"

    # Polling configuration
    POLL_INTERVAL = 0.5  # seconds between polls
    MAX_POLL_TIME = 60  # maximum time to wait

    @property
    def supports_editing(self) -> bool:
        """Most Replicate models don't support editing, only generation."""
        return False

    @property
    def max_resolution(self) -> str:
        """Maximum resolution varies by model, typically 1024x1024."""
        return "1K"

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """Aspect ratios vary by model."""
        return ["1:1", "16:9", "9:16", "3:2", "2:3"]

    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate an image using Replicate (TEMPLATE - NOT IMPLEMENTED).

        Args:
            prompt: Text description of the image to generate
            output_path: Where to save the generated image
            **kwargs:
                width: Image width (default varies by model)
                height: Image height (default varies by model)
                num_inference_steps: Number of denoising steps
                guidance_scale: How closely to follow prompt
                seed: Random seed for reproducibility

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation (Async Polling):
            ```python
            import httpx
            import asyncio

            # Prepare input for model
            input_data = {
                "prompt": prompt,
                "width": kwargs.get("width", 1024),
                "height": kwargs.get("height", 1024),
                "num_inference_steps": kwargs.get("num_inference_steps", 4),
                "guidance_scale": kwargs.get("guidance_scale", 0),  # FLUX schnell uses 0
            }

            # Add seed if provided
            seed = kwargs.get("seed")
            if seed is not None:
                input_data["seed"] = seed

            async with httpx.AsyncClient(timeout=120.0) as client:
                # Step 1: Create prediction
                response = await client.post(
                    f"{self.BASE_URL}/predictions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": self.model,  # Model version ID
                        "input": input_data
                    }
                )

                if response.status_code != 201:
                    raise RuntimeError(f"API error: {response.text}")

                prediction = response.json()
                prediction_id = prediction["id"]

                # Step 2: Poll for completion
                start_time = asyncio.get_event_loop().time()

                while True:
                    # Check prediction status
                    response = await client.get(
                        f"{self.BASE_URL}/predictions/{prediction_id}",
                        headers={"Authorization": f"Bearer {self.api_key}"}
                    )

                    prediction = response.json()
                    status = prediction["status"]

                    if status == "succeeded":
                        # Step 3: Download image
                        output_url = prediction["output"][0]  # First output
                        img_response = await client.get(output_url)

                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_bytes(img_response.content)
                        break

                    elif status == "failed":
                        error = prediction.get("error", "Unknown error")
                        raise RuntimeError(f"Prediction failed: {error}")

                    elif status in ["starting", "processing"]:
                        # Check timeout
                        if asyncio.get_event_loop().time() - start_time > self.MAX_POLL_TIME:
                            raise TimeoutError("Prediction timed out")

                        # Wait before next poll
                        await asyncio.sleep(self.POLL_INTERVAL)

                    else:
                        raise RuntimeError(f"Unknown status: {status}")
            ```

        Example Implementation (With Webhooks):
            ```python
            # For production, use webhooks instead of polling:
            response = await client.post(
                f"{self.BASE_URL}/predictions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "version": self.model,
                    "input": input_data,
                    "webhook": "https://your-app.com/webhook",
                    "webhook_events_filter": ["completed"]
                }
            )
            # Replicate will POST to your webhook when done
            ```

        Reference:
            - Replicate docs: https://replicate.com/docs/reference/http
            - FLUX schnell: https://replicate.com/black-forest-labs/flux-schnell
            - Provider guide: docs/skills/imagegen/providers/creating.md
        """
        raise NotImplementedError(
            "Replicate provider is a template and not yet implemented.\n\n"
            "To implement this provider:\n"
            "1. Install replicate SDK:\n"
            "   uv pip install replicate\n\n"
            "2. Get your API token:\n"
            "   https://replicate.com/account/api-tokens\n\n"
            "3. Set environment variable:\n"
            "   export REPLICATE_API_TOKEN='r8_...'\n\n"
            "4. Implement async polling pattern:\n"
            "   a) POST /predictions to create job\n"
            "   b) Poll GET /predictions/{id} until succeeded\n"
            "   c) Download image from output URL\n\n"
            "5. Key differences from other providers:\n"
            "   - Async polling required (not immediate response)\n"
            "   - Output is URL (like OpenAI)\n"
            "   - Need to handle 'starting', 'processing', 'succeeded', 'failed' states\n"
            "   - For production, use webhooks instead of polling\n\n"
            "Popular models:\n"
            "- black-forest-labs/flux-schnell (fast, ~1s, $0.003/image)\n"
            "- black-forest-labs/flux-dev (quality, ~10s, $0.01/image)\n"
            "- stability-ai/sdxl (stable diffusion, $0.0055/image)\n\n"
            "Documentation:\n"
            "- Provider guide: docs/skills/imagegen/providers/creating.md\n"
            "- Replicate HTTP API: https://replicate.com/docs/reference/http\n"
            "- Example: docs/skills/imagegen/providers/replicate.md"
        )

    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit an image using Replicate (TEMPLATE - NOT IMPLEMENTED).

        Most Replicate models don't support editing, only generation.
        However, some models like img2img or inpainting models could be used.

        Args:
            prompt: Text description of the desired edit
            output_path: Where to save the edited image
            input_images: List of input images
            **kwargs: Model-specific parameters

        Raises:
            NotImplementedError: This is a template provider
        """
        raise NotImplementedError(
            "Replicate edit method is a template.\n\n"
            "Most Replicate models focus on generation, not editing.\n"
            "However, you could use img2img or inpainting models:\n"
            "- stability-ai/stable-diffusion-img2img\n"
            "- stability-ai/stable-diffusion-inpainting\n\n"
            "Implementation would follow the same polling pattern as generate(),\n"
            "but include the input image in the request.\n\n"
            "See: docs/skills/imagegen/providers/replicate.md"
        )
