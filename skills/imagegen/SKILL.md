---
name: imagegen
description: >
  Generate and edit images from text prompts using Google Gemini (Nano Banana).
  Triggers: "generate image", "create image", "edit image", "draw".
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [productivity, creative]
---

# Image Generation & Editing Skill

Generate and edit images via Google Gemini (Nano Banana), embed results in markdown notes.

## Tools

### generate_image
Generate an image from a text prompt.

**Parameters:**
- `prompt` (required): Text description of the image to generate
- `provider`: Provider to use (google, google-pro). Default: google
- `output_path`: Where to save the image. Default: ./attachments/
- `aspect_ratio`: Image aspect ratio (1:1, 16:9, 9:16, etc.). Default: 1:1
- `resolution`: Image resolution (1K, 2K, 4K). 4K only with google-pro. Default: 1K

### edit_image
Edit an existing image with a text prompt.

**Parameters:**
- `prompt` (required): Text description of the edit to make
- `input_images` (required): List of input image paths to edit
- `provider`: Provider to use (google, google-pro). Default: google-pro
- `output_path`: Where to save the edited image. Default: ./attachments/
- `aspect_ratio`: Output aspect ratio. Default: 1:1

### list_providers
List available image generation providers.

## Providers

| Provider | Model | Features |
|----------|-------|----------|
| `google` | gemini-2.5-flash-image | Fast generation, editing (Nano Banana) |
| `google-pro` | gemini-3-pro-image-preview | 4K, thinking mode, up to 14 ref images (Nano Banana Pro) |

## Environment Variables

- `GEMINI_API_KEY`: Google AI Studio API key (required)

## Examples

```python
# Generate image
await skill.invoke_tool("generate_image", {
    "prompt": "a sunset over mountains",
    "aspect_ratio": "16:9"
})

# Edit image
await skill.invoke_tool("edit_image", {
    "prompt": "add a rainbow to the sky",
    "input_images": ["./photo.png"]
})
```
