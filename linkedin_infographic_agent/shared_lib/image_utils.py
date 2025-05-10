import os
from typing import List
from ..constants import GENERATED_SLIDES_DIR, INFOGRAPHIC_ASSETS_DIR, IMAGE_ROOT_DIR

def ensure_image_directory_exists() -> None:
    """Ensure the root image directory exists."""
    os.makedirs(IMAGE_ROOT_DIR, exist_ok=True)

def list_images() -> List[str]:
    """List all images in the generated slides directory."""
    if not os.path.exists(GENERATED_SLIDES_DIR):
        return []
    return [f for f in os.listdir(GENERATED_SLIDES_DIR) if os.path.isfile(os.path.join(GENERATED_SLIDES_DIR, f))]

def delete_image(filename: str) -> bool:
    """Delete an image from the generated slides directory by filename."""
    filepath = os.path.join(GENERATED_SLIDES_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def list_assets() -> List[str]:
    """List all asset files in the assets directory."""
    if not os.path.exists(INFOGRAPHIC_ASSETS_DIR):
        return []
    return [f for f in os.listdir(INFOGRAPHIC_ASSETS_DIR) if os.path.isfile(os.path.join(INFOGRAPHIC_ASSETS_DIR, f))] 