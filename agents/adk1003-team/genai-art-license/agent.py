import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

# Debug: Print current working directory and script location
# print(f"Current working directory: {os.getcwd()}")
# print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")

script_dir = os.path.dirname(os.path.abspath(__file__))


def retrieve_agent_details(markdown_content: str) -> dict:
    """Retrieves the instruction for the agent from the markdown content.

    Args:
        markdown_content (str): The markdown content containing agent instructions.

    Returns:
        dict: A dictionary containing the agent instruction information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes 'name', 'description' and 'instruction' keys.
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

        # Validate and extract agent name from the first line
        first_line = lines[0].strip()
        if not first_line.startswith('# ') or ' 的 AI Agent 任務說明書' not in first_line:
            return {
                "status": "error",
                "message": "First line must follow format: '# [Agent Name] 的 AI Agent 任務說明書'"
            }

        agent_name = first_line.replace(
            '# ', '').replace(' 的 AI Agent 任務說明書', '')

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
            "name": agent_name,
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
    # read the list from script_dir/taichung_pubarts_list.txt
    file_path = os.path.join(script_dir, 'taichung_pubarts_list.txt')
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": f"File not found: {file_path}",
        }
    with open(file_path, 'r', encoding='utf-8') as file:
        pubarts_list = file.read()
    return {
        "status": "success",
        "output": pubarts_list,
    }


def say_hello(name: str = "there") -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str, optional): The name of the person to greet. Defaults to "there".

    Returns:
        str: A friendly greeting message.
    """
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello, {name}!"


# --- Greeting Agent ---
greeting_agent = None
try:
    with open(os.path.join(script_dir, 'agent-greeting.md'), 'r', encoding='utf-8') as file:
        agent_greeting_md = file.read()
    # extract the instruction from the markdown
    agent_greeting_detail = retrieve_agent_details(agent_greeting_md)
    greeting_agent = Agent(
        model="gemini-2.0-flash",
        name=agent_greeting_detail['name'],
        instruction=agent_greeting_detail['instruction'],
        # Crucial for delegation
        description=agent_greeting_detail['description'],
        tools=[say_hello, get_taichung_pubarts_list],
    )
    print(
        f"✅ Agent '{greeting_agent.name}' created using model 'gemini-2.0-flash'.")
except Exception as e:
    print(
        f"❌ Could not create Greeting agent. Check API Key (gemini-2.0-flash). Error: {e}")

with open(os.path.join(script_dir, 'agent-license.md'), 'r', encoding='utf-8') as file:
    agent_license_md = file.read()
# extract the instruction from the markdown
agent_license_details = retrieve_agent_details(agent_license_md)

genai_art_license_agent = Agent(
    name=agent_license_details["name"],
    model="gemini-2.0-flash",
    description=agent_license_details["description"],
    instruction=agent_license_details["instruction"],
    tools=[get_taichung_pubarts_list]
)

# read the instruction from script_dir/agent-root.md
with open(os.path.join(script_dir, 'agent-root.md'), 'r', encoding='utf-8') as file:
    agent_root_md = file.read()
# extract the instruction from the markdown
agent_root_details = retrieve_agent_details(agent_root_md)

# Debug agent_root_details
print(f"Agent Root Details: {agent_root_details}")
if agent_root_details["status"] != "success":
    raise ValueError(
        f"Error retrieving agent details: {agent_root_details['message']}")

root_agent = Agent(
    name=agent_root_details["name"],
    model="gemini-2.0-flash",
    description=agent_root_details["description"],
    instruction=agent_root_details["instruction"],
    sub_agents=[greeting_agent, genai_art_license_agent]
)
