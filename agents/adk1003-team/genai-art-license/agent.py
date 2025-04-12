import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

# Debug: Print current working directory and script location
# print(f"Current working directory: {os.getcwd()}")
# print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")

script_dir = os.path.dirname(os.path.abspath(__file__))

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
    # read the instruction from script_dir/inst_greeting.md
    with open(os.path.join(script_dir, 'inst_greeting.md'), 'r', encoding='utf-8') as file:
        instruction_root = file.read()
    greeting_agent = Agent(
        # Using a potentially different/cheaper model for a simple task
        model="gemini-2.0-flash",
        name="greeting_agent",
        instruction=instruction_root,
        description="利用 say_hello 工具做簡單的問候", # Crucial for delegation
        tools=[say_hello],
    )
    print(f"✅ Agent '{greeting_agent.name}' created using model 'gemini-2.0-flash'.")
except Exception as e:
    print(f"❌ Could not create Greeting agent. Check API Key (gemini-2.0-flash). Error: {e}")


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

genai_art_license_agent = Agent(
    name="genai_art_license_agent",
    model="gemini-2.0-flash",
    description=(
        "熟悉著作權的法律專家"
    ),
    instruction=(
        prompt_content
    ),
    tools=[get_taichung_pubarts_list]
)

# read the instruction from script_dir/inst_root.md
with open(os.path.join(script_dir, 'inst_root.md'), 'r', encoding='utf-8') as file:
    instruction_root = file.read()
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=(
        "主要的分配協調者，處理台中中央公園生成式公共藝術品的相關請求，同時依據任務目的適當地分配與委託給接待或智財權助理"
    ),
    instruction=(
        instruction_root
    ),
    sub_agents=[greeting_agent, genai_art_license_agent]
)

