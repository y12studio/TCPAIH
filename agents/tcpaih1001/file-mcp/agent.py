import asyncio
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService  # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
from pathlib import Path

script_dir = Path(__file__).resolve().parent
docs_dir = script_dir / "docs"
resolved_docs_path = docs_dir.absolute().as_posix()

# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
    """Gets tools from the File System MCP Server."""
    print("Attempting to connect to MCP Filesystem server...")
    tools, exit_stack = await MCPToolset.from_server(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command='npx',  # Command to run the server
            args=["-y",    # Arguments for the command
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
  tools, exit_stack = await get_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash', # Adjust model name if needed based on availability
      name='filesystem_assistant',
      instruction=f"""利用可用的工具來協助使用者與檔案系統互動。
      - 預設利用 '{resolved_docs_path}' 目錄來查詢檔案資料。
      - 你將列出目錄下所有的英文檔案名稱來判斷其中那一個檔案是使用者想要找的檔案，讀取檔案提供給使用者。
      """,
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return agent, exit_stack

root_agent = create_agent()


