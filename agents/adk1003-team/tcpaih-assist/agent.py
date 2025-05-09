import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from pathlib import Path
import logging

# MODEL="gemini-2.5-flash-preview-04-17"
MODEL="gemini-2.0-flash"


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


def load_agent_from_markdown(agent_id: str, model: str = MODEL, tools: list = None):
    """Loads an agent from a markdown file and creates an Agent object.
    
    Args:
        agent_id (str): The identifier for the agent, used for both the filename and agent name.
        model (str, optional): The model to use for the agent. Defaults to "gemini-2.5-flash-preview-04-17".
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

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "taichung":
        tz_identifier = "Asia/Taipei"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


agent_time = LlmAgent(
    name="time_agent",
    model=MODEL,
    description=(
        "回答城市時間問題的代理程式。"
    ),
    instruction=(
        "我可以回答您有關城市時間的問題。"
    ),
    tools=[get_current_time],
)

# --- License Agent ---
agent_genai_art_license = load_agent_from_markdown(
    agent_id="agent_license",
    tools=[get_taichung_pubarts_list]
)

# --- Agent Reviewer ---
agent_reviewer = load_agent_from_markdown(
    agent_id="agent_reviewer",
    tools=[]
)

agent_security = load_agent_from_markdown(
    agent_id="agent_security",
    tools=[]
)


root_agent = LlmAgent(
    name="human_resource_info_coordinator",
    model=MODEL,
    instruction="""將使用者請求導引到適合的人工智慧代理程式：
- 使用 agent_time 回答時間問題
- 使用 agent_genai_art_license 回答公共藝術品生成式藝術的著作權相關問題
- 使用 agent_reviewer 回答專案測試時工具與學經歷審核問題
- 使用 agent_security 回答專案測試時資訊安全（資安）問題

主動告知你所有的人工智慧代理程式，並詢問使用者的需求。加入引導提示語氣，讓互動更加自然，例如在開始時加上：
「您好！我是您的台中中央公園人工智慧園藝師 (Taichung Central Park AI Horticulturist, TCPAIH)開放原始碼專案資訊小幫手」
對於其他任何請求，請適當回應或聲明您無法處理。
    """,
    description="台中中央公園人工智慧園藝師 (Taichung Central Park AI Horticulturist, TCPAIH)開放原始碼專案資訊的服務台。",
    sub_agents=[agent_time, agent_genai_art_license, agent_reviewer, agent_security]
)