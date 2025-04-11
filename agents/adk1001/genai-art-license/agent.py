import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

# Debug: Print current working directory and script location
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")

# Try multiple possible locations for prompt.md
prompt_file_paths = [
    './prompt.md',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompt.md'),
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
    raise FileNotFoundError("Could not find prompt.md in any of the expected locations")

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
    tools=[],
)