import base64
import glob
import os
from typing import Dict, Optional

import google.genai.types as types
from google.adk.tools.tool_context import ToolContext
from openai import OpenAI

from ....constants import (
    GENERATED_SLIDES_DIR,
    IMAGE_ROOT_DIR,
    INFOGRAPHIC_ASSETS_DIR,
    INFOGRAPHIC_IMAGE_SIZE,
)

def create_slide(
    prompt: str,
    tool_context: Optional[ToolContext] = None,
) -> Dict:
    """
    Create an image using OpenAI's image generation API with gpt-image-1 model,
    automatically incorporating any assets from the assets directory.
    """
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {
                "status": "error",
                "message": "OPENAI_API_KEY not found in environment variables",
            }
        client = OpenAI(api_key=api_key)
        clean_prompt = prompt.strip()
        response = None
        asset_paths = []
        os.makedirs(IMAGE_ROOT_DIR, exist_ok=True)
        assets_dir = INFOGRAPHIC_ASSETS_DIR
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir, exist_ok=True)
        asset_files_paths = glob.glob(os.path.join(assets_dir, "*"))
        for asset_path in asset_files_paths:
            asset_paths.append(asset_path)
        # Use slide-specific state keys
        if tool_context and tool_context.state.get("slide_generated") is True:
            previous_slide_path = tool_context.state.get("current_slide_path")
            if previous_slide_path and os.path.exists(previous_slide_path):
                if previous_slide_path not in asset_paths:
                    asset_paths.append(previous_slide_path)
                try:
                    if asset_files_paths:
                        try:
                            asset_file_objects = [open(path, "rb") for path in asset_files_paths]
                            all_files = [open(previous_slide_path, "rb")] + asset_file_objects
                            try:
                                response = client.images.edit(
                                    model="gpt-image-1",
                                    image=[open(previous_slide_path, "rb"), *[open(path, "rb") for path in asset_files_paths]],
                                    prompt=clean_prompt,
                                    n=1,
                                    size=INFOGRAPHIC_IMAGE_SIZE,
                                )
                            finally:
                                for file in all_files:
                                    file.close()
                        except Exception as e:
                            return {
                                "status": "error",
                                "message": f"Error generating image with previous slide and assets: {str(e)}",
                            }
                    else:
                        with open(previous_slide_path, "rb") as previous_slide:
                            response = client.images.edit(
                                model="gpt-image-1",
                                image=previous_slide,
                                prompt=clean_prompt,
                                n=1,
                                size=INFOGRAPHIC_IMAGE_SIZE,
                            )
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Error generating image with previous slide: {str(e)}",
                    }
        # If we don't have a response yet (no previous slide or error), try with assets
        if response is None:
            if asset_files_paths:
                try:
                    asset_file_objects = [open(path, "rb") for path in asset_files_paths]
                    try:
                        response = client.images.edit(
                            model="gpt-image-1",
                            image=[open(path, "rb") for path in asset_files_paths],
                            prompt=clean_prompt,
                            n=1,
                            size=INFOGRAPHIC_IMAGE_SIZE,
                        )
                    finally:
                        for file in asset_file_objects:
                            file.close()
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Error generating image with assets: {str(e)}",
                    }
            else:
                response = client.images.generate(
                    model="gpt-image-1",
                    prompt=clean_prompt,
                    n=1,
                    size=INFOGRAPHIC_IMAGE_SIZE,
                )
        if response and response.data and len(response.data) > 0:
            image_base64 = response.data[0].b64_json
            if image_base64:
                image_bytes = base64.b64decode(image_base64)
            else:
                return {
                    "status": "error",
                    "message": "No image data returned from the API",
                }
        else:
            return {
                "status": "error",
                "message": "No data returned from the API",
            }
        # Dynamic filename generation
        filename = "slide.png"
        if tool_context and tool_context.state.get("slide_filename"):
            filename = tool_context.state["slide_filename"]
        artifact_version = None
        if tool_context:
            image_artifact = types.Part(
                inline_data=types.Blob(data=image_bytes, mime_type="image/png")
            )
            try:
                artifact_version = tool_context.save_artifact(
                    filename=filename, artifact=image_artifact
                )
                tool_context.state["slide_generated"] = True
                tool_context.state["current_slide_filename"] = filename
                tool_context.state["current_slide_version"] = artifact_version
            except ValueError as e:
                return {
                    "status": "warning",
                    "message": f"Image generated but could not be saved as an artifact: {str(e)}. Is ArtifactService configured?",
                }
            except Exception as e:
                return {
                    "status": "warning",
                    "message": f"Image generated but encountered an error saving as artifact: {str(e)}",
                }
        os.makedirs(GENERATED_SLIDES_DIR, exist_ok=True)
        filepath = os.path.join(GENERATED_SLIDES_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        if tool_context:
            tool_context.state["current_slide_path"] = filepath
            tool_context.state["slide_generated"] = True
        if artifact_version is not None:
            return {
                "status": "success",
                "message": f"Image created successfully and saved as artifact '{filename}' (version {artifact_version}) and local file '{filepath}'",
                "filepath": filepath,
                "artifact_filename": filename,
                "artifact_version": artifact_version,
                "assets_used": (
                    [os.path.basename(path) for path in asset_paths]
                    if asset_paths
                    else []
                ),
                "slide_generated": True,
                "is_first_generation": not (
                    tool_context
                    and tool_context.state.get("slide_generated", False)
                ),
            }
        else:
            return {
                "status": "success",
                "message": f"Image created successfully and saved as local file '{filepath}'",
                "filepath": filepath,
                "assets_used": (
                    [os.path.basename(path) for path in asset_paths]
                    if asset_paths
                    else []
                ),
                "slide_generated": True,
                "is_first_generation": not (
                    tool_context
                    and tool_context.state.get("slide_generated", False)
                ),
            }
    except Exception as e:
        return {"status": "error", "message": f"Error creating image: {str(e)}"} 