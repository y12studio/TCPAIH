import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

script_dir = Path(__file__).resolve().parent

def read_file_content(file_path: Path) -> str:
    """Reads the content of a file and returns it as a string."""
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise


def retrieve_agent_details(markdown_content: str) -> dict:
    """Retrieves the instruction for the agent from the markdown content.

    Args:
        markdown_content (str): The markdown content containing agent instructions.

    Returns:
        dict: A dictionary containing the agent instruction information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes 'description' and 'instruction' keys.
              If 'error', includes a 'message' key.
    """
    try:
        # Extract description and instruction from markdown
        lines = markdown_content.strip().split('\n')

        # Make sure the content contains the expected key words
        required_keywords = ['任務描述', '任務指令']
        markdown_text = ' '.join(lines)
        for keyword in required_keywords:
            if keyword not in markdown_text:
                return {
                    "status": "error",
                    "message": f"Missing required section: '{keyword}'"
                }

        # Find description section
        description_start = lines.index("# 任務描述") + 1
        description_end = lines.index("# 任務指令")
        description = "\n".join(
            lines[description_start:description_end]).strip()

        # Get instruction (everything after "# 任務指令")
        instruction_start = description_end + 1
        instruction = "\n".join(lines[instruction_start:]).strip()

        return {
            "status": "success",
            "description": description,
            "instruction": instruction
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error parsing markdown content: {str(e)}"
        }


def get_taichung_pubarts_list() -> dict:
    """Retrieves the current list of public artworks in Taichung.

    Returns:
        dict: A dictionary containing the taichung public arts list information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'output' key with Taichung public arts list details.
              If 'error', includes an 'message' key.
    """
    file_path = script_dir / 'taichung_pubarts_list.txt'
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return {
            "status": "error",
            "message": f"File not found: {file_path}",
        }
    try:
        pubarts_list = read_file_content(file_path)
        return {
            "status": "success",
            "output": pubarts_list,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading file: {e}",
        }


def load_agent_from_markdown(agent_id: str, model: str = "gemini-2.0-flash-001", tools: list = None):
    """Loads an agent from a markdown file and creates an Agent object.
    
    Args:
        agent_id (str): The identifier for the agent, used for both the filename and agent name.
        model (str, optional): The model to use for the agent. Defaults to "gemini-2.0-flash-001".
        tools (list, optional): List of tools available to the agent. Defaults to None.
    
    Returns:
        Agent or None: The created Agent object, or None if an error occurred.
        
    Raises:
        ValueError: If agent creation fails.
    """
    try:
        md_file_path = script_dir / f"{agent_id}.md"
        agent_md_content = read_file_content(md_file_path)
        agent_details = retrieve_agent_details(agent_md_content)
        if agent_details["status"] != "success":
            raise ValueError(f"Error retrieving agent details: {agent_details['message']}")
        agent = LlmAgent(
            name=agent_id,
            model=model,
            description=agent_details["description"],
            instruction=agent_details["instruction"],
            tools=tools or []
        )
        logger.info(f"✅ Agent '{agent.name}' created using model '{model}'.")
        return agent
    except Exception as e:
        error_msg = f"❌ Could not create {agent_id} agent. Error: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg)

# --- Greeting Agent ---
greeting_agent = load_agent_from_markdown(
    agent_id="agent_greeting",
    tools=[]
)

# --- License Agent ---
genai_art_license_agent = load_agent_from_markdown(
    agent_id="agent_license",
    tools=[get_taichung_pubarts_list]
)

# --- Root Agent ---
root_agent = load_agent_from_markdown(
    agent_id="agent_root"
)

root_agent.sub_agents = [greeting_agent, genai_art_license_agent]