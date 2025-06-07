
# imports for overriding `get_tools`
from typing_extensions import override
from google.adk.tools.mcp_tool.mcp_session_manager import retry_on_closed_resource
from typing import List
from typing import Optional, Union, TextIO
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.mcp_tool.mcp_tool import MCPTool, BaseTool
from google.adk.tools.mcp_tool.mcp_session_manager import MCPSessionManager, StdioServerParameters, SseServerParams, StreamableHTTPServerParams, StdioConnectionParams, SseConnectionParams,StreamableHTTPConnectionParams
from mcp.types import ListToolsResult
from .cache import tools_cache
from  google.adk.tools.mcp_tool.mcp_toolset  import MCPToolset, ToolPredicate
import sys

# Imports for session manager
from contextlib import AsyncExitStack
from datetime import timedelta
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
import os

import logging


logging.basicConfig(
    level=logging.INFO)


# # to Fix timeout issue
# class SessionManagerWithConfigurableTimeOut(MCPSessionManager):
#   """
#   We had to fix the timeout
#   The uv tools take few seconds to download dependencies and then later as well
#   the timeout needs to be > 5 seconds which is default
#   """
#   async def create_session(self) -> ClientSession:
#     """Creates and initializes an MCP client session.

#     Returns:
#         ClientSession: The initialized MCP client session.
#     """
#     if self._session is not None:
#       return self._session

#     # Create a new exit stack for this session
#     self._exit_stack = AsyncExitStack()

#     try:
#       if isinstance(self._connection_params, StdioServerParameters):
#         # So far timeout is not configurable. Given MCP is still evolving, we
#         # would expect stdio_client to evolve to accept timeout parameter like
#         # other client.
#         client = stdio_client(
#             server=self._connection_params, errlog=self._errlog
#         )
#       elif isinstance(self._connection_params, SseServerParams):
#         client = sse_client(
#             url=self._connection_params.url,
#             headers=self._connection_params.headers,
#             timeout=self._connection_params.timeout,
#             sse_read_timeout=self._connection_params.sse_read_timeout,
#         )
#       elif isinstance(self._connection_params, StreamableHTTPServerParams):
#         client = streamablehttp_client(
#             url=self._connection_params.url,
#             headers=self._connection_params.headers,
#             timeout=timedelta(seconds=self._connection_params.timeout),
#             sse_read_timeout=timedelta(
#                 seconds=self._connection_params.sse_read_timeout
#             ),
#             terminate_on_close=self._connection_params.terminate_on_close,
#         )
#       else:
#         raise ValueError(
#             'Unable to initialize connection. Connection should be'
#             ' StdioServerParameters or SseServerParams, but got'
#             f' {self._connection_params}'
#         )

#       transports = await self._exit_stack.enter_async_context(client)
#       # The streamable http client returns a GetSessionCallback in addition to the read/write MemoryObjectStreams
#       # needed to build the ClientSession, we limit then to the two first values to be compatible with all clients.
#       # The StdioServerParameters does not provide a timeout parameter for the
#       # session, so we need to set a default timeout for it. Other clients
#       # (SseServerParams and StreamableHTTPServerParams) already provide a
#       # timeout parameter in their configuration.
#       if isinstance(self._connection_params, StdioServerParameters):
#         # Default timeout for MCP session is 5 seconds, same as SseServerParams
#         # and StreamableHTTPServerParams.
#         # TODO :
#         #   1. make timeout configurable
#         #   2. Add StdioConnectionParams to include StdioServerParameters as a
#         #      field and rename other two params to XXXXConnetionParams. Ohter
#         #      two params are actually connection params, while stdio is
#         #      special, stdio_client takes the resposibility of starting the
#         #      server and working as a client.
#         session = await self._exit_stack.enter_async_context(
#             ClientSession(
#                 *transports[:2],
#                 read_timeout_seconds=timedelta(seconds=float(os.environ.get("SESSION_TIMEOUT_SECONDS","60"))),
#             )
#         )
#       else:
#         session = await self._exit_stack.enter_async_context(
#             ClientSession(*transports[:2])
#         )
#       await session.initialize()

#       self._session = session
#       return session

#     except Exception:
#       # If session creation fails, clean up the exit stack
#       if self._exit_stack:
#         await self._exit_stack.aclose()
#         self._exit_stack = None
#       raise


class MCPToolSetWithSchemaAccess(MCPToolset):
  """
  TODO - double check

  Required for - name for caching (any other way?)
  Required for - tool caching (is it alrady implemented?) (in get_tools)
  """

  def __init__(
      self,
      *,
      tool_set_name: str, # <-- new parameter
      connection_params: Union[
          StdioServerParameters,
          StdioConnectionParams,
          SseConnectionParams,
          StreamableHTTPConnectionParams,
      ],
      tool_filter: Optional[Union[ToolPredicate, List[str]]] = None,
      errlog: TextIO = sys.stderr,
  ):
    super().__init__(
        connection_params=connection_params,
        tool_filter=tool_filter,
        errlog=errlog
    )
    self.tool_set_name = tool_set_name
    logging.info(f"MCPToolSetWithSchemaAccess initialized with tool_set_name: '{self.tool_set_name}'")  
    self._session = None

  # def __init__(
  #     self,
  #     *,
  #     tool_set_name: str, # <-- new parameter
  #     connection_params: ( # Inherited from MCPToolset
  #         StdioServerParameters | SseServerParams | StreamableHTTPServerParams
  #     ),
  #     tool_filter: Optional[Union[ToolPredicate, List[str]]] = None, # Inherited from BaseToolset/MCPToolset
  #     errlog: TextIO = sys.stderr, # Inherited from MCPToolset
  # ):
  #     """
  #     Initializes the MCPToolSetWithSchemaAccess.

  #     Args:
  #         tool_set_name (str): The name of the tool set (required, keyword-only).
  #         connection_params: Parameters for server connection, passed to MCPToolset (required, keyword-only).
  #         tool_filter: An optional filter for tools, passed to MCPToolset (keyword-only).
  #         errlog: The error log stream, passed to MCPToolset (keyword-only).
  #     """
  #     # Call the parent (MCPToolset) constructor, passing its specific arguments
  #     super().__init__(
  #         connection_params=connection_params,
  #         tool_filter=tool_filter,
  #         errlog=errlog
  #     )
  #     self._mcp_session_manager = SessionManagerWithConfigurableTimeOut(
  #         connection_params=self._connection_params,
  #         errlog=self._errlog,
  #     )      
  #     self.tool_set_name = tool_set_name
  #     logging.info(f"MCPToolSetWithSchemaAccess initialized with tool_set_name: '{self.tool_set_name}'")  

  @retry_on_closed_resource("_reinitialize_session")
  @override
  async def get_tools(
      self,
      readonly_context: Optional[ReadonlyContext] = None,
  ) -> List[BaseTool]:
    """Return all tools in the toolset based on the provided context.

    Args:
        readonly_context: Context used to filter tools available to the agent.
            If None, all tools in the toolset are returned.

    Returns:
        List[BaseTool]: A list of tools available under the specified context.
    """
    # Get session from session manager
    if not self._session:
      self._session = await self._mcp_session_manager.create_session()

    if self.tool_set_name in tools_cache.keys():
      logging.info(f"Tools found in cache for toolset {self.tool_set_name}, returning them")  
      return tools_cache[self.tool_set_name]
    else:
      logging.info(f"No tools found in cache for toolset {self.tool_set_name}, loading")

    tools_response: ListToolsResult = await self._session.list_tools()

    # Apply filtering based on context and tool_filter
    tools = []
    for tool in tools_response.tools:
      mcp_tool = MCPTool(
          mcp_tool=tool,
          mcp_session_manager=self._mcp_session_manager,
      )

      if self._is_tool_selected(mcp_tool, readonly_context):
        tools.append(mcp_tool)

    tools_cache[self.tool_set_name] = tools
    return tools