import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

# Debug: Print current working directory and script location
# print(f"Current working directory: {os.getcwd()}")
# print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")

script_dir = os.path.dirname(os.path.abspath(__file__))

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

# Try multiple possible locations for prompt.md
prompt_file_paths = [
    './prompt.md',
    os.path.join(script_dir, 'prompt.md'),
    '../prompt.md',
    '../../prompt.md',
]

prompt_content = None
for path in prompt_file_paths:
    print(f"Trying to open: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as file:
            prompt_content = file.read()
            print(f"Successfully loaded prompt from: {path}")
            break
    except FileNotFoundError:
        print(f"File not found: {path}")

if prompt_content is None:
    raise FileNotFoundError(
        "Could not find prompt.md in any of the expected locations")

# Original agent initialization
root_agent = Agent(
    name="genai_art_license_agent",
    model="gemini-2.0-flash",
    description=(
        "熟悉著作權的法律專家以及作家"
    ),
    instruction=(
        prompt_content
    ),
    tools=[get_taichung_pubarts_list],
)
