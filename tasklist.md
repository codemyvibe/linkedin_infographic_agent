# Task List: YouTube Thumbnail Agent to LinkedIn Infographic Carousel Agent Refactor

## Phase 1: Preparation & Project Setup

* [ ] **Clone Existing Project:**
    * [ ] In Cursor (or your preferred Git client/terminal), clone your existing `youtube_thumbnail_agent` repository to a new local directory that will house the new project.
    * [ ] Rename the new project directory (e.g., `linkedin_infographic_agent`).
* [ ] **Version Control:**
    * [ ] Navigate into the new project directory.
    * [ ] If your old project had a remote, ensure this new project points to a new remote repository if you want to keep them separate, or work on a new branch if preferred. For a distinct new agent, a new repository is often cleaner.
    * [ ] Make an initial commit for the "as-is" cloned state in the new project.
* [ ] **Virtual Environment:**
    * [ ] Create a new virtual environment or update the existing one within the new project directory (e.g., `python -m venv .venv`).
    * [ ] Activate the virtual environment (e.g., `source .venv/bin/activate` or `.venv\Scripts\activate` on Windows).
* [ ] **Install Dependencies:**
    * [ ] Review `requirements.txt`.
    * [ ] Install base dependencies: `pip install -r requirements.txt`.
    * [ ] Add `Pillow` to `requirements.txt`: `Pillow>=9.0.0` (or latest).
    * [ ] Install `Pillow`: `pip install Pillow`.
* [ ] **API Keys & Environment:**
    * [ ] Create a `.env` file from `.env.example` in the new project.
    * [ ] Ensure `OPENAI_API_KEY` and `GOOGLE_API_KEY` are correctly filled.
    * [ ] Remove `YOUTUBE_API_KEY` from `.env` and `.env.example` as it's no longer needed.

## Phase 2: Core Component Modification (Adapting Existing YouTube Agent Parts)

* [ ] **Update Constants (`linkedin_infographic_agent/constants.py`):**
    * [ ] Change `THUMBNAIL_IMAGE_SIZE` to `INFOGRAPHIC_IMAGE_SIZE = "1080x1080"`.
    * [ ] Rename `GENERATED_THUMBNAILS_DIR` to `GENERATED_SLIDES_DIR = f"{IMAGE_ROOT_DIR}/generated_slides"`.
    * [ ] Rename `THUMBNAIL_ASSETS_DIR` to `INFOGRAPHIC_ASSETS_DIR = f"{IMAGE_ROOT_DIR}/assets"`.
    * [ ] Decide if `REFERENCE_IMAGES_DIR` is needed; if not, comment out or remove. Consider `ARTICLE_CONTENT_DIR = f"{IMAGE_ROOT_DIR}/article_content"` if you plan to save processed article text locally.
* [ ] **Update Shared Libraries (`linkedin_infographic_agent/shared_lib/`):**
    * **`callbacks.py`:**
        * [ ] Rename `ensure_thumbnail_assets_directory_exists` to `ensure_infographic_assets_directory_exists`.
        * [ ] Update the renamed function to use `INFOGRAPHIC_ASSETS_DIR` from `constants.py`.
        * [ ] Ensure all references to the old function name and constant are updated within this file.
    * **`image_utils.py`:**
        * [ ] Review `list_images` and `delete_image`. Update them to use `GENERATED_SLIDES_DIR` and potentially `INFOGRAPHIC_ASSETS_DIR` if they are intended to manage these.
        * [ ] Ensure `ensure_image_directory_exists` (which creates the root `images` folder) is still appropriate.
* [ ] **Modify Image Generation Tool:**
    * [ ] Rename directory `youtube_thumbnail_agent/sub_agents/generate_image_agent/` to `linkedin_infographic_agent/sub_agents/slide_generator_agent/`.
    * [ ] Rename file `tools/create_image.py` to `tools/create_slide.py`.
    * [ ] **Inside `create_slide.py`:**
        * [ ] Rename the main function from `create_image` to `create_slide`.
        * [ ] Update all internal constant imports to use the new names (e.g., `INFOGRAPHIC_IMAGE_SIZE`, `GENERATED_SLIDES_DIR`, `INFOGRAPHIC_ASSETS_DIR`).
        * [ ] Change the `size` parameter in the `client.images.generate` (or `edit`) call to use `INFOGRAPHIC_IMAGE_SIZE`.
        * [ ] Modify or remove the YouTube-specific prompt cleaning logic (e.g., `if "youtube thumbnail" not in clean_prompt.lower():`).
        * [ ] Implement dynamic filename generation for slides (e.g., `slide_01.png`, `slide_02.png`). This might involve passing a `slide_filename` or `slide_index` as an argument or through `tool_context.state`.
        * [ ] Update state keys like `thumbnail_generated`, `thumbnail_path`, `image_filename` to more generic terms like `slide_generated`, `current_slide_path`, `current_slide_filename`.
        * [ ] **(Decision Point) Text-on-Image Strategy:**
            * [ ] **If using Pillow for text overlay (Recommended):**
                * [ ] Add `Pillow` imports (`Image`, `ImageDraw`, `ImageFont`) at the top of `create_slide.py`.
                * [ ] After `image_bytes` are decoded from base64, insert Pillow code to open the image, draw text, and save it back to `image_bytes`.
                * [ ] The text content, positions, fonts, and colors for Pillow will need to be passed to this tool, likely via `tool_context.state` (e.g., `tool_context.state.get("current_slide_texts_for_pillow", [])`).
                * [ ] Ensure font files (e.g., `.ttf`) are accessible if not using default fonts (consider adding a `fonts` directory).
            * [ ] **If attempting text via image model prompt:** Ensure prompts are structured to request this.
* [ ] **Modify Image Generation Agent:**
    * **Inside `linkedin_infographic_agent/sub_agents/slide_generator_agent/agent.py` (formerly `generate_image_agent/agent.py`):**
        * [ ] Rename the agent variable (e.g., `generate_image_agent` to `slide_generator_agent`).
        * [ ] Update `name` and `description` of the `Agent` to reflect slide generation (e.g., "slide_generator_agent", "An agent that generates a single 1080x1080 infographic slide...").
        * [ ] Update the `tools` list to include the renamed `create_slide` tool.
        * [ ] Completely rewrite the `instruction` to focus on taking a detailed prompt for a *single* infographic slide, mentioning 1080x1080, and using `create_slide`.

## Phase 3: Implement New Core Agents

* [ ] **Create Article Processor Agent:**
    * [ ] Create new directory: `linkedin_infographic_agent/sub_agents/article_processor_agent/`.
    * [ ] Create `__init__.py` and `agent.py` inside it.
    * [ ] Create a `tools` subdirectory if custom tools are needed (e.g., `tools/process_text.py`).
    * **`agent.py`:**
        * [ ] Define `article_processor_agent = Agent(...)`.
        * [ ] Set `name`, `description`.
        * [ ] Write the `instruction` focusing on receiving article text, using an LLM to extract key information (summary, key points, structure), and outputting structured data (e.g., JSON) to `tool_context.state['processed_article']`.
        * [ ] Define any tools it needs (e.g., a simple tool to pass text to Gemini).
    * **`tools/process_text.py` (if created):**
        * [ ] Implement the tool function(s) for text processing via LLM.
* [ ] **Create Infographic Content Planner Agent:**
    * [ ] Create new directory: `linkedin_infographic_agent/sub_agents/infographic_content_planner_agent/`.
    * [ ] Create `__init__.py` and `agent.py` inside it.
    * **`agent.py`:**
        * [ ] Define `infographic_content_planner_agent = Agent(...)`.
        * [ ] Set `name`, `description`.
        * [ ] Write the `instruction` focusing on taking `tool_context.state['processed_article']`, planning a sequence of 3-7 slides, defining purpose/text/visual ideas for each, and outputting a list of slide definitions to `tool_context.state['slide_plans']`.
        * [ ] This agent will be heavily LLM-driven.
* [ ] **Modify Prompt Generator Agent:**
    * [ ] Rename directory `youtube_thumbnail_agent/sub_agents/prompt_generator/` to `linkedin_infographic_agent/sub_agents/infographic_prompt_generator_agent/`.
    * **Inside `linkedin_infographic_agent/sub_agents/infographic_prompt_generator_agent/agent.py`:**
        * [ ] Rename agent variable (e.g., `prompt_generator` to `infographic_prompt_generator_agent`).
        * [ ] Update `name`, `description`.
        * [ ] The `save_prompt` tool is likely still useful for the individual slide prompt.
        * [ ] Completely rewrite the `instruction`:
            * It will take structured content for a *single slide* from `tool_context.state['current_slide_plan']` (which the main agent will populate from the `slide_plans` list).
            * It will generate a detailed, verbose prompt for the `slide_generator_agent` for that one slide (layout, text/placeholders, colors, icons, style).
            * Remove references to YouTube `style_guide` and `thumbnail_analysis`.
            * Adapt asset handling if users can upload logos/images per slide.
            * The output prompt should be saved to `tool_context.state['current_slide_generation_prompt']`.

## Phase 4: Remove Obsolete Agents & Update Main Orchestrator

* [ ] **Remove Unused YouTube-Specific Agents:**
    * [ ] Delete the entire `youtube_thumbnail_agent/sub_agents/thumbnail_scraper/` directory.
    * [ ] Delete the entire `youtube_thumbnail_agent/sub_agents/thumbnail_analyzer_agent/` directory.
    * [ ] (Ensure no import errors arise from these deletions in remaining files; update `__init__.py` files if necessary).
* [ ] **Update Main Orchestrating Agent (`linkedin_infographic_agent/agent.py`):**
    * [ ] Rename the main agent variable (e.g., `thumbnail_agent` to `linkedin_infographic_agent_manager` or similar).
    * [ ] Update its `name` and `description`.
    * [ ] Update the `sub_agents` list to include the new and modified agents:
        ```python
        from .sub_agents.article_processor_agent.agent import article_processor_agent
        from .sub_agents.infographic_content_planner_agent.agent import infographic_content_planner_agent
        from .sub_agents.infographic_prompt_generator_agent.agent import infographic_prompt_generator_agent
        from .sub_agents.slide_generator_agent.agent import slide_generator_agent

        # ...
        sub_agents=[
            article_processor_agent,
            infographic_content_planner_agent,
            infographic_prompt_generator_agent, # These two will be called in a loop
            slide_generator_agent,            # managed by the main agent's instruction
        ],
        # ...
        ```
    * [ ] **Completely rewrite the `instruction` for the main agent:**
        * [ ] Define the new multi-step workflow:
            1.  Welcome user, request article text/URL.
            2.  Delegate to `article_processor_agent`.
            3.  Delegate to `infographic_content_planner_agent` (receives processed article data, outputs `slide_plans` to state).
            4.  **Implement Loop Logic:** Iterate through `tool_context.state['slide_plans']`. For each `slide_plan`:
                * Set current `slide_plan` to a state key like `tool_context.state['current_slide_plan']`.
                * If using Pillow for text, also set `tool_context.state['current_slide_texts_for_pillow']` based on the `current_slide_plan`.
                * Set a unique filename for the current slide in state: `tool_context.state['current_slide_filename']`.
                * Delegate to `infographic_prompt_generator_agent` (it reads `current_slide_plan` and outputs prompt to `current_slide_generation_prompt`).
                * Delegate to `slide_generator_agent` (it reads `current_slide_generation_prompt`, `current_slide_filename`, and `current_slide_texts_for_pillow`).
                * Collect/report the path/artifact of the generated slide.
            5.  Present all generated slide details to the user.
        * [ ] This instruction will be complex as it manages the loop and data flow explicitly.

## Phase 5: Testing & Refinement

* [ ] **Unit Testing (Conceptual):**
    * [ ] Test `create_slide.py` tool directly with a sample prompt and expected 1080x1080 output. If using Pillow, test text overlay.
    * [ ] Test `article_processor_agent` with a sample article snippet. Check its structured output.
    * [ ] Test `infographic_content_planner_agent` with sample processed article data. Check its `slide_plans` output.
    * [ ] Test `infographic_prompt_generator_agent` with a sample `slide_plan`. Check the detailed image prompt.
* [ ] **Initial Agent Run (Simple Article):**
    * [ ] Prepare a short, simple news article or scientific abstract.
    * [ ] Run the main `linkedin_infographic_agent`.
    * [ ] Carefully observe the logs and agent transitions.
    * [ ] Check `tool_context.state` at various points if your ADK environment allows, or add print statements for debugging.
    * [ ] Verify that directories for generated slides and assets are created.
    * [ ] Verify that slide images are generated in 1080x1080.
    * [ ] Verify text (if using Pillow) appears correctly.
* [ ] **Debugging File Paths and Imports:**
    * [ ] Address any `ModuleNotFoundError` or `ImportError` issues. Pay attention to relative imports (`from .`, `from ..`).
* [ ] **Prompt Engineering Iteration:**
    * [ ] For `article_processor_agent`: Adjust instructions for better key point extraction.
    * [ ] For `infographic_content_planner_agent`: Adjust instructions for better slide breakdown and content allocation.
    * [ ] For `infographic_prompt_generator_agent`: This is critical. Refine instructions to produce prompts that result in good visual layouts from your chosen image generation model. Specify styles (e.g., "modern flat design," "minimalist," "data-driven look"), color palette ideas, icon descriptions, etc.
    * [ ] For `slide_generator_agent` (specifically its tool `create_slide`): Refine the base instruction/cleaning added to the prompt to better guide the OpenAI model for infographic styles.
* [ ] **Loop Logic in Main Agent:**
    * [ ] Ensure the main agent correctly iterates through all planned slides.
    * [ ] Ensure state variables (`current_slide_plan`, `current_slide_generation_prompt`, etc.) are correctly updated and used in each iteration.
* [ ] **Test with Diverse Articles:**
    * [ ] Test with longer articles.
    * [ ] Test with articles that have different structures (e.g., news vs. scientific paper).
    * [ ] Test with articles that might have lists, data, or quotes to see how they are handled.
* [ ] **Asset Handling Test (If Implemented):**
    * [ ] If you kept the user asset uploading (`before_model_callback` and logic in `create_slide`), test uploading a logo and instructing the agent (via prompt) to include it.

## Phase 6: Final Touches & Documentation

* [ ] **Code Cleanup:**
    * [ ] Remove unused variables, functions, and commented-out code.
    * [ ] Ensure consistent formatting.
    * [ ] Add comments where logic is complex.
* [ ] **Update `README.md`:**
    * [ ] Change title and description to reflect the LinkedIn Infographic Carousel Agent.
    * [ ] Update installation instructions if anything changed (e.g., new dependencies).
    * [ ] Update API Setup (remove YouTube API).
    * [ ] Update Usage instructions to show how to run the new agent and what input it expects (article text/URL).
    * [ ] Update the Architecture section to describe the new agent flow and sub-agents.
* [ ] **Review `.gitignore`:**
    * [ ] Ensure it correctly ignores `.env`, image output directories (`images/` or `linkedin_infographic_agent/images/`), `__pycache__`, and `.venv/`.
* [ ] **Final End-to-End Test:**
    * [ ] Run the agent with a representative article from start to finish.
    * [ ] Check output quality, coherence of slides, and overall user experience.
* [ ] **Consider Error Handling & Edge Cases:**
    * [ ] What happens if an article URL is invalid?
    * [ ] What if the article is very short or very long?
    * [ ] What if the image generation API fails for one slide? (Does it retry? Skip? Halt?)

This checklist should provide a solid framework for your refactoring project. Remember to commit your changes frequently at logical checkpoints!