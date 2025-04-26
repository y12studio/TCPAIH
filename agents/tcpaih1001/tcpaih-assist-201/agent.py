import datetime
import os
import sys
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.transfer_to_agent_tool import transfer_to_agent
from pathlib import Path
import logging
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters

MODEL="gemini-2.5-flash-preview-04-17"
#MODEL="gemini-2.0-flash"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

script_dir = Path(__file__).resolve().parent
docs_dir = script_dir / "docs"
resolved_docs_path = docs_dir.absolute().as_posix()

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

def get_taichung_pubarts_list() -> dict:
    """Retrieves the current list of public artworks in Taichung.

    Returns:
        dict: A dictionary containing the taichung public arts list information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'output' key with Taichung public arts list details.
              If 'error', includes an 'message' key.
    """
    file_path = docs_dir / 'taichung_central_park_public_art_list.txt'
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


agent_genai_art_license = load_agent_from_markdown(
    agent_id="agent_license",
    tools=[get_taichung_pubarts_list]
)


agent_time = LlmAgent(
    name="agent_time",
    model=MODEL,
    description=(
        "回答城市時間問題的代理程式。"
    ),
    instruction=(
        "我可以回答您有關城市時間的問題。"
    ),
    tools=[get_current_time],
)

agent_security = load_agent_from_markdown(
    agent_id="agent_security",
    tools=[]
)

agent_resumes = load_agent_from_markdown(
    agent_id="agent_resumes",
    tools=[]
)

async def get_mcp_filesystem_async():
    """Gets tools from the File System MCP Server."""
    print("Attempting to connect to MCP Filesystem server...")
    tools, exit_stack = await MCPToolset.from_server(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command='npx', 
            args=["-y",
                  "@modelcontextprotocol/server-filesystem",
                  resolved_docs_path],
        )
        # For remote servers, you would use SseServerParams instead:
        # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
    )
    print("MCP Toolset created successfully.")
    # MCP requires maintaining a connection to the local MCP Server.
    # exit_stack manages the cleanup of this connection.
    return tools, exit_stack


async def create_agent():
  """Gets tools from MCP Server."""
  mcp_tools, exit_stack = await get_mcp_filesystem_async()

  agent_filesystem = LlmAgent(
      model='gemini-2.0-flash',
      name='agent_filesystem',
      instruction=f"""利用可用的工具來協助使用者與檔案系統互動。
      - 預設利用 '{resolved_docs_path}' 目錄來查詢檔案資料。
      - 你將列出目錄下所有的英文檔案名稱來判斷其中那一個檔案是使用者想要找的檔案，讀取檔案提供給使用者。
      """,
      tools=mcp_tools,
  )

  root_agent = LlmAgent(
    name="info_coordinator",
    model=MODEL,
    instruction="""負責確認使用者資格，將符合資格的使用者請求導引到適合的人工智慧代理程式。
    1. 利用提出問題來確認使用者是否具備利用代理程式的資格，使用者必須答對全部的問題，禁止提供任何可能讓使用者聯想到答案的提示。
    - 問題 1 「什麼動物早晨用四條腿走路，中午用兩條腿走路，晚上用三條腿走路？腿最多的時候，也正是他走路最慢，體力最弱的時候。」，答案是「人」。
    - 問題 2 「使用者參與的專案名稱？」，回答的專案名稱如果沒有同時出現'臺中'與'TCPAIH'，則不符合資格。
    
    禁止將無法答對問題的使用者的請求導引到任何代理程式。
    
    2. 確認完專案名稱符合之後，主動提示有哪些可用的代理程式，並詢問使用者他們想要使用哪一個。
    - 使用 agent_resumes 回答專案面試的履歷問題。
    - 使用 agent_security 回答專案測試時資訊安全（資安）問題。
    - 使用 agent_filesystem 回答檔案文件問題。
    - 使用 agent_genai_art_license 回答公共藝術品人工智慧生成改作授權問題。
    - 使用 agent_time 回答時間問題。
    - 對於其他任何請求，請適當回應或聲明您無法處理。

    """,
    description="專案資訊的服務台。",
    sub_agents=[agent_time, agent_security, agent_resumes, agent_filesystem, agent_genai_art_license]
  )

  return root_agent, exit_stack

root_agent = create_agent()

