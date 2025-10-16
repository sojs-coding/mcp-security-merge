# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents.llm_agent import LlmAgent
from  google.adk.tools.mcp_tool.mcp_toolset  import StdioServerParameters, StdioConnectionParams
import os
import logging

from utils_extensions_cbs_tools.extensions import MCPToolSetWithSchemaAccess
from utils_extensions_cbs_tools.callbacks import bmc_trim_llm_request
from typing import TextIO
import sys

# TODO improve logging
logging.basicConfig(
    level=logging.INFO,)

if os.environ.get("MINIMAL_LOGGING","N") == "Y":
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.ERROR)

is_any_variable_unset = any(
    os.getenv(var, "NOT_SET") == "NOT_SET"
    for var in ["FALCON_CLIENT_ID","FALCON_CLIENT_SECRET","FALCON_BASE_URL"]
)
if is_any_variable_unset:
  print(f"Please set all required environment variables, check .env file")
  exit(1)

def get_all_tools():
  """Get Tools from IDP MCP"""
  logging.info("Attempting to connect to MCP servers for Falcon...")
  falcon_tools = None # Initialize falcon_tools
  
  uv_dir_prefix="../server"
  env_file_path = "../../run-with-google-adk/google_mcp_security_agent/.env"

  if os.environ.get("REMOTE_RUN","N") == "Y":
    uv_dir_prefix="./server"

  if os.environ.get("AE_RUN","N") == "Y":
    uv_dir_prefix="./server"    

  # required temporarily for https://github.com/google/adk-python/issues/1024
  errlog_ae : TextIO = sys.stderr
  if os.environ.get("AE_RUN","N") == "Y":
    errlog_ae = None

  timeout = float(os.environ.get("STDIO_PARAM_TIMEOUT","60.0"))

  if os.environ.get("LOAD_FALCON_MCP") == "Y":

    falcon_tools = MCPToolSetWithSchemaAccess(
                  connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                      command='uv',
                      args=[ "--directory",
                              uv_dir_prefix + "/falcon_mcp",
                              "run",
                              "--env-file",
                              env_file_path,
                              "server.py",
                            ]
                    ),
                  timeout=timeout),
                tool_set_name="falcon_mcp",
                errlog=errlog_ae
                )

  logging.info("MCP Toolsets for Falcon created successfully.")
  return [falcon_tools]

tools:any = [item for item in get_all_tools() if item is not None]

falcon_agent = LlmAgent(
    model=os.environ.get("GOOGLE_MODEL"), 
    name="falcon_agent",
    instruction=
    """**1. Persona & Mission**

You are a Falcon SOC Analyst Agent, an AI security assistant designed to investigate threats within the CrowdStrike Falcon platform. Your mission is to act as a partner to human analysts by efficiently executing investigation tasks and providing clear, actionable insights.

**2. Operational Workflow**

For every request, you must follow this four-step process:

1.  **Understand:** Determine the user's investigative goal.
2.  **Act:** Silently select and use the necessary tools to find the answer.
3.  **Summarize:** Analyze the tool's output and present a concise summary of the key findings. Never show raw data.
4.  **Suggest:** Proactively recommend the next logical step to continue the investigation.""",
    tools=tools,
    before_model_callback=bmc_trim_llm_request,
    description="""This agent acts as a virtual Security Operations Center (SOC) analyst for the CrowdStrike Falcon ecosystem. It uses a dedicated toolset to perform security investigations.

Capabilities:

Investigates: Searches for and retrieves details on security detections and incidents.

Analyzes: Queries for information on hosts, assets, and user identities.

Enriches: Gathers threat intelligence on indicators (IPs, hashes, domains) and actors.

Responds: Can perform endpoint actions like network containment.

Delegation Rule: This agent's expertise is strictly limited to the CrowdStrike Falcon platform. For any requests that fall outside this scope—such as general security queries, web searches, questions about other security products, or non-security tasks—you must delegate the work to the google_mcp_security_agent"""
)
