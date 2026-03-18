"""Stability AI provider (TEMPLATE - Not Implemented).

This is a template provider demonstrating how to implement image generation
with the Stability AI API. This provider showcases advanced generation
parameters like CFG scale, steps, and negative prompts.

To implement this provider:
1. Install stability SDK: `uv pip install stability-sdk`
2. Get API key from https://platform.stability.ai/account/keys
3. Set environment: `export STABILITY_API_KEY='sk-...'`
4. Implement the methods below

API Documentation:
    https://platform.stability.ai/docs/api-reference
"""

from pathlib import Path
from typing import Union

from skills.imagegen.providers.base import BaseProvider


class StabilityProvider(BaseProvider):
    """Stability AI image generation provider (TEMPLATE).

    Stability AI provides access to Stable Diffusion models including
    SD3, SDXL, and various fine-tuned versions. This provider demonstrates
    advanced generation parameters and control options.

    Key Features:
        - Stable Diffusion 3 (latest)
        - Stable Diffusion XL 1.0
        - Control over generation parameters
        - Negative prompts
        - Multiple samplers
        - Seed control for reproducibility
        - Image-to-image and inpainting

    Models:
        - stable-diffusion-3-medium: Latest SD3 model
        - stable-diffusion-xl-1024-v1-0: SDXL base
        - stable-diffusion-xl-1024-v0-9: SDXL beta

    Advanced Parameters:
        - cfg_scale: Classifier-free guidance (how closely to follow prompt)
        - steps: Number of diffusion steps (quality vs speed)
        - sampler: Sampling algorithm
        - negative_prompt: What to avoid in generation
        - seed: For reproducible results

    Pricing (as of 2025):
        - SD3: ~$0.065 per image
        - SDXL: ~$0.035 per image
    """

    BASE_URL = "https://api.stability.ai/v1"

    # Available samplers
    SAMPLERS = [
        "DDIM",
        "DDPM",
        "K_DPMPP_2M",
        "K_DPMPP_2S_ANCESTRAL",
        "K_DPM_2",
        "K_DPM_2_ANCESTRAL",
        "K_EULER",
        "K_EULER_ANCESTRAL",
        "K_HEUN",
        "K_LMS",
    ]

    @property
    def supports_editing(self) -> bool:
        """Stability AI supports image-to-image and inpainting."""
        return True

    @property
    def max_resolution(self) -> str:
        """SDXL supports up to 1024x1024, SD3 similar."""
        return "1K"

    @property
    def supported_aspect_ratios(self) -> list[str]:
        """Supports various aspect ratios."""
        return ["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16"]

    async def generate(self, prompt: str, output_path: Path, **kwargs) -> None:
        """Generate an image using Stability AI (TEMPLATE - NOT IMPLEMENTED).

        Args:
            prompt: Text description of the image to generate
            output_path: Where to save the generated image
            **kwargs:
                height: Image height (default 1024)
                width: Image width (default 1024)
                cfg_scale: Guidance scale 0-35 (default 7)
                steps: Number of steps 10-50 (default 30)
                samples: Number of images to generate (default 1)
                sampler: Sampling algorithm (default K_DPM_2_ANCESTRAL)
                negative_prompt: What to avoid in the image
                seed: Random seed for reproducibility

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation:
            ```python
            import httpx
            import base64

            # Prepare parameters
            height = kwargs.get("height", 1024)
            width = kwargs.get("width", 1024)
            cfg_scale = kwargs.get("cfg_scale", 7.0)
            steps = kwargs.get("steps", 30)
            samples = kwargs.get("samples", 1)
            sampler = kwargs.get("sampler", "K_DPM_2_ANCESTRAL")
            seed = kwargs.get("seed", 0)

            # Build request payload
            payload = {
                "text_prompts": [
                    {"text": prompt, "weight": 1.0}
                ],
                "cfg_scale": cfg_scale,
                "height": height,
                "width": width,
                "samples": samples,
                "steps": steps,
                "sampler": sampler,
                "seed": seed,
            }

            # Add negative prompt if provided
            negative_prompt = kwargs.get("negative_prompt")
            if negative_prompt:
                payload["text_prompts"].append({
                    "text": negative_prompt,
                    "weight": -1.0  # Negative weight
                })

            async with httpx.AsyncClient(timeout=120.0) as client:
                # Make API request
                response = await client.post(
                    f"{self.BASE_URL}/generation/{self.model}/text-to-image",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    json=payload
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                data = response.json()

                # Decode base64 image
                image_data = data["artifacts"][0]["base64"]
                image_bytes = base64.b64decode(image_data)

                # Save image
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_bytes)
            ```

        Reference:
            - Stability API: https://platform.stability.ai/docs/api-reference
            - Provider guide: docs/skills/imagegen/providers/creating.md
        """
        raise NotImplementedError(
            "Stability AI provider is a template and not yet implemented.\n\n"
            "To implement this provider:\n"
            "1. Install stability SDK:\n"
            "   uv pip install stability-sdk\n\n"
            "2. Get your API key:\n"
            "   https://platform.stability.ai/account/keys\n\n"
            "3. Set environment variable:\n"
            "   export STABILITY_API_KEY='sk-...'\n\n"
            "4. Implement this method using the pattern above\n\n"
            "5. Key features to implement:\n"
            "   - Base64 response (like Google)\n"
            "   - Advanced parameters (cfg_scale, steps, sampler)\n"
            "   - Negative prompts\n"
            "   - Multiple samples\n"
            "   - Seed control\n\n"
            "Documentation:\n"
            "- Provider guide: docs/skills/imagegen/providers/creating.md\n"
            "- Stability docs: https://platform.stability.ai/docs\n"
            "- Example: docs/skills/imagegen/providers/stability.md"
        )

    async def edit(
        self,
        prompt: str,
        output_path: Path,
        input_images: list[Union[str, Path, bytes]],
        **kwargs,
    ) -> None:
        """Edit an image using Stability AI (TEMPLATE - NOT IMPLEMENTED).

        Stability AI supports image-to-image and inpainting operations.

        Args:
            prompt: Text description of the desired edit
            output_path: Where to save the edited image
            input_images: List containing [image] or [image, mask]
            **kwargs:
                image_strength: How much to transform (0.0-1.0, default 0.35)
                cfg_scale: Guidance scale
                steps: Number of steps
                negative_prompt: What to avoid

        Raises:
            NotImplementedError: This is a template provider

        Example Implementation:
            ```python
            import httpx
            import base64
            from pathlib import Path

            image_path = Path(input_images[0])
            image_strength = kwargs.get("image_strength", 0.35)

            # Read and encode image
            image_bytes = image_path.read_bytes()
            image_b64 = base64.b64encode(image_bytes).decode()

            payload = {
                "text_prompts": [{"text": prompt, "weight": 1.0}],
                "init_image": image_b64,
                "init_image_mode": "IMAGE_STRENGTH",
                "image_strength": image_strength,
                "cfg_scale": kwargs.get("cfg_scale", 7.0),
                "steps": kwargs.get("steps", 30),
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/generation/{self.model}/image-to-image",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

                if response.status_code != 200:
                    raise RuntimeError(f"API error: {response.text}")

                data = response.json()
                image_data = data["artifacts"][0]["base64"]
                image_bytes = base64.b64decode(image_data)

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_bytes)
            ```

        Reference:
            https://platform.stability.ai/docs/api-reference#tag/v1generation/operation/imageToImage
        """
        raise NotImplementedError(
            "Stability AI edit method is a template.\n\n"
            "Stability supports:\n"
            "- Image-to-image: Transform existing image\n"
            "- Inpainting: Edit specific masked regions\n\n"
            "See: docs/skills/imagegen/providers/stability.md"
        )
