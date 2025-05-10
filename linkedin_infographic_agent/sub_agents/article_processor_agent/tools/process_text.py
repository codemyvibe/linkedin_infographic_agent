from typing import Dict, Optional
from google.adk.tools.tool_context import ToolContext
import os
import google.generativeai as genai

def process_text(article_text: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Process article text to extract summary, key points, structure, and citation.
    Returns a JSON object with these fields. Falls back to a placeholder if LLM call fails.
    """
    # Try to use Gemini flash-2.0 for real extraction
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        system_prompt = (
            "You are an expert assistant. Given an article, extract the following as JSON: "
            "summary (string), key_points (list of strings), structure (list of sections with heading and content), "
            "and citation (object with source, author, date, url). Always include all fields, use null or empty if missing."
        )
        user_prompt = f"""\nArticle:\n{article_text}\n\nReturn only a JSON object with the fields: summary, key_points, structure, citation."""
        response = model.generate_content([
            {"role": "system", "parts": [system_prompt]},
            {"role": "user", "parts": [user_prompt]},
        ])
        import json
        content = response.text.strip()
        return json.loads(content)
    except Exception as e:
        # Fallback to placeholder if LLM call fails
        print(f"[process_text] Gemini call failed, using placeholder. Error: {e}")
        return {
            "summary": "<summary of the article>",
            "key_points": ["<key point 1>", "<key point 2>", "<key point 3>"],
            "structure": [
                {"heading": "Introduction", "content": "..."},
                {"heading": "Main Section", "content": "..."},
                {"heading": "Conclusion", "content": "..."}
            ],
            "citation": {
                "source": "<source or publication>",
                "author": "<author>",
                "date": "<date>",
                "url": "<url>"
            }
        }
