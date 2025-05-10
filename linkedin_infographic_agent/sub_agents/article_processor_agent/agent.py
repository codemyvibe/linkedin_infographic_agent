from google.adk.agents import Agent
from .tools.process_text import process_text

article_processor_agent = Agent(
    name="article_processor_agent",
    description="An agent that extracts structured information (summary, key points, structure, citation) from article text and outputs a consistent JSON object.",
    tools=[process_text],
    instruction="""
    You are the Article Processor Agent. Your job is to:
    1. Receive article text from the user or another agent.
    2. Use the process_text tool to extract:
        - A concise summary
        - Key points
        - The article's structure (sections, headings, etc.)
        - Citation (source, author, date, or URL if available)
    3. Ensure your output is always a JSON object with these fields: summary, key_points, structure, citation.
    4. Save the result to tool_context.state['processed_article'].
    5. If any field is missing, use null or an empty value, but always include the citation field.
    """,
)
