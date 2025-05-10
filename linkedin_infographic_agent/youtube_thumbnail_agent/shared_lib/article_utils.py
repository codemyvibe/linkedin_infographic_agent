import os
import json
from typing import Any, Dict
from linkedin_infographic_agent.constants import ARTICLE_CONTENT_DIR

def save_processed_article(article_data: Dict[str, Any], identifier: str) -> str:
    """
    Save processed article data as a JSON file in ARTICLE_CONTENT_DIR.

    Args:
        article_data (dict): The processed article data to save.
        identifier (str): A unique identifier for the article (e.g., title, hash, or timestamp).

    Returns:
        str: The path to the saved file.
    """
    os.makedirs(ARTICLE_CONTENT_DIR, exist_ok=True)
    # Sanitize identifier for filename
    safe_identifier = "".join(c for c in identifier if c.isalnum() or c in ("-", "_"))
    filename = f"article_{safe_identifier}.json"
    filepath = os.path.join(ARTICLE_CONTENT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)
    return filepath 