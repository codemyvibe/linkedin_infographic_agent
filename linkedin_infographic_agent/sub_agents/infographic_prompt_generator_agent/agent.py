"""
Sub-agent responsible for generating YouTube thumbnail image prompts that emulate analyzed channel styles.
"""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from linkedin_infographic_agent.constants import GEMINI_MODEL
from ...shared_lib.callbacks import before_model_callback


def save_prompt(prompt: str, tool_context: ToolContext) -> dict:
    """Save the final prompt to state."""
    tool_context.state["prompt"] = prompt
    return {"status": "success", "message": "Prompt saved successfully to state."}


# Create the YouTube Thumbnail Prompt Generator Agent
infographic_prompt_generator_agent = Agent(
    name="infographic_prompt_generator_agent",
    description="An agent that generates a detailed, verbose prompt for a single LinkedIn infographic slide based on structured slide content.",
    instruction="""
    You are the Infographic Prompt Generator Agent. Your job is to:
    1. Take structured content for a single slide from tool_context.state['current_slide_plan'] (provided by the main agent from the slide_plans list).
    2. Generate a detailed, verbose prompt for the slide_generator_agent to create a 1080x1080 infographic slide. The prompt should specify:
        - Layout (where text and visuals should go)
        - All text to appear on the slide (headings, bullets, etc.)
        - Colors, icons, and style (e.g., modern, minimalist, data-driven, etc.)
        - Any user-uploaded assets (logos, images) to be included, if present
    3. Do NOT reference YouTube, style guides, or thumbnail analysis. Focus on LinkedIn infographic/carousel context.
    4. Save the generated prompt to tool_context.state['current_slide_generation_prompt'].
    """,
)
