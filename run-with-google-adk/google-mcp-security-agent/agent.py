from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import os
import logging

logging.basicConfig(
    level=logging.INFO)

async def get_all_tools():
  """Get Tools from All MCP servers"""
  logging.info("Attempting to connect to MCP servers...")
  secops_tools = []
  gti_tools = []
  secops_soar_tools = []
  exit_stack = None

  if os.environ.get("LOAD_SECOPS_MCP") == "Y":
    secops_tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uv',
                args=["--directory",
                        "../server/secops/secops_mcp",
                        "run",
                        "--env-file",
                        "../../../run-with-google-adk/google-mcp-security-agent/.env",
                        "server.py"
                    ],
                ),async_exit_stack=exit_stack
    )

  if os.environ.get("LOAD_GTI_MCP") == "Y":
    gti_tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        "../server/gti/gti_mcp",
                        "run",
                        "--env-file",
                        "../../../run-with-google-adk/google-mcp-security-agent/.env",
                        "server.py"
                    ],
                ),async_exit_stack=exit_stack
    )  

  if os.environ.get("LOAD_SECOPS_SOAR_MCP") == "Y":
    secops_soar_tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uv',
                args=["--directory",
                        "../server/secops-soar/secops_soar_mcp",
                        "run",
                        "--env-file",
                        "../../../run-with-google-adk/google-mcp-security-agent/.env",
                        "server.py",
                        "--integrations",
                        "CSV,OKTA"
                    ],
                ),async_exit_stack=exit_stack
    )  

  logging.info("MCP Toolsets created successfully.")
  return secops_tools+gti_tools+secops_soar_tools, exit_stack

async def create_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_all_tools()

  agent = LlmAgent(
      model=os.environ.get("GOOGLE_MODEL"), 
      name='google_security_assistant',
      instruction=os.environ.get("DEFAULT_PROMPT"),
      tools=tools 
  )
  return agent, exit_stack


root_agent = create_agent()
