import argparse
import httpx
import json
from typing import Any, Dict, Optional, List
import logging
import os
# change this to WARN when running in inspector
logging.basicConfig(level=os.environ.get("LOGGING_LEVEL",logging.ERROR))
# Try importing the actual FastMCP library
try:
    # Attempt to import the real FastMCP class
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # If the import fails, print a warning. The script will likely exit
    # later when 'mcp = FastMCP(...)' is called if the import truly failed.
    logging.warning("Warning: 'mcp.server.fastmcp' not found. Ensure the MCP SDK is installed.")
    # You might want to raise the ImportError or exit here in a real app
    # raise
# --- Configuration Variables (populated by argparse) ---
API_BASE_URL: Optional[str] = None
CLIENT_ID: Optional[str] = None
CLIENT_SECRET: Optional[str] = None
# Store the token globally for simplicity in this example
ACCESS_TOKEN: Optional[str] = None
# --- Initialize FastMCP server ---
# This line will now raise a NameError if the import above failed
mcp = FastMCP("api_tools")
# --- Helper Functions ---
async def _make_request(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    send_as_json: bool = True # Relevant for POST/PUT etc.
) -> Optional[Dict[str, Any]]:
    """
    Internal helper to make asynchronous HTTP requests (GET, POST).
    Automatically adds Authorization header if ACCESS_TOKEN is available.
    Args:
        method: HTTP method ('GET', 'POST').
        url: The URL for the request.
        params: Dictionary of query parameters for GET requests.
        payload: Dictionary for the request body (JSON or form-encoded).
        headers: Optional dictionary of custom headers.
        send_as_json: For POST, determines if payload is sent as JSON or form-data.
    Returns:
        The JSON response as a dictionary, or a dictionary containing error details.
    """
    if headers is None:
        headers = {}
    # Add Authorization header if token exists
    if ACCESS_TOKEN:
        headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
    else:
        # For endpoints requiring auth, we should ideally check before calling _make_request
        # This check is now primarily done within the tool functions themselves.
        logging.warning("Warning: ACCESS_TOKEN is not set. Request may fail if auth is required.")
    # Set Content-Type for POST/PUT etc. based on send_as_json flag
    if method.upper() == 'POST': # Add other methods like PUT if needed
        if send_as_json:
            headers['Content-Type'] = 'application/json'
        # else: httpx handles form-encoding Content-Type automatically
    # Always accept JSON response unless specified otherwise
    if 'Accept' not in headers:
        headers['Accept'] = 'application/json'
    if 'User-Agent' not in headers:
        headers['User-Agent'] = 'mcp-tool-client/1.0'
    async with httpx.AsyncClient() as client:
        try:
            logging.warning(f"Making {method} request to: {url}")
            request_kwargs = {"headers": headers, "timeout":120.0} #, "timeout": 30.0
            if method.upper() == 'GET':
                if params:
                    # httpx handles encoding of query parameters
                    request_kwargs["params"] = params
                response = await client.get(url, **request_kwargs)
            elif method.upper() == 'POST':
                if send_as_json:
                    request_kwargs["json"] = payload
                else:
                    request_kwargs["data"] = payload
                # Add params to POST request URL if needed (like include_hidden)
                if params:
                     # Build URL with params for POST request
                     post_url = httpx.URL(url, params=params)
                     response = await client.post(post_url, **request_kwargs)
                else:
                     response = await client.post(url, **request_kwargs)
            else:
                return {"error": "UnsupportedMethod", "detail": f"HTTP method '{method}' not supported by helper."}
            response.raise_for_status() # Check for 4xx/5xx errors
            logging.warning(f"Request successful, status code: {response.status_code}")
            # Handle potential empty response body for success codes like 204
            if response.status_code == 204:
                 return {"status": "success", "detail": "Request successful, no content returned."}
            logging.warning(type(response))
            # Assume response is JSON, handle decode error
            return response.json()
        except httpx.RequestError as exc:
            logging.warning(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            return {"error": "RequestError", "detail": str(exc)}
        except httpx.HTTPStatusError as exc:
            logging.warning(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc.response.text}")
            # Check specifically for auth errors
            if exc.response.status_code in [401, 403]:
                 # Reset token if it caused an auth error? Maybe.
                 # global ACCESS_TOKEN
                 # ACCESS_TOKEN = None
                 return {"error": "AuthenticationError", "status_code": exc.response.status_code, "detail": "Invalid or expired token, or insufficient permissions. Please re-authenticate."}
            try:
                # Try to parse error response as JSON
                return exc.response.json()
            except json.JSONDecodeError:
                 # Return structured error if response is not JSON
                 return {"error": "HTTPStatusError", "status_code": exc.response.status_code, "detail": exc.response.text}
        except json.JSONDecodeError as exc:
            logging.warning(f"Failed to decode JSON response from {url}: {exc}")
            response_text = getattr(exc, 'response_text', 'N/A')
            return {"error": "JSONDecodeError", "detail": f"Invalid JSON received. Response text: {response_text[:200]}..."}
        except Exception as exc:
            logging.warning(f"An unexpected error occurred: {exc}")
            return {"error": "UnexpectedError", "detail": str(exc)}
async def make_get_request(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    """Makes an asynchronous GET request, automatically adding auth."""
    return await _make_request("GET", url, params=params, headers=headers)
async def make_post_request(
    url: str,
    payload: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None, # Added params for POST
    headers: Optional[Dict[str, str]] = None,
    send_as_json: bool = True
) -> Optional[Dict[str, Any]]:
    """Makes an asynchronous POST request, automatically adding auth."""
    # Pass params to _make_request for POST
    return await _make_request("POST", url, params=params, payload=payload, headers=headers, send_as_json=send_as_json)
def format_message(tool_name: str, is_error: bool, response_data: Any) -> str:
    """
    Formats the response from a tool into a user-friendly string.
    Args:
        tool_name: The name of the tool that was called.
        is_error: Boolean indicating if the response represents an error.
        response_data: The data returned by the tool's core logic (or error details).
    Returns:
        A formatted string representation of the response.
    """
    output = {
        "error" : "y",
        "message": "There was some error, that's all we know",
        "data":{}
    }
    logging.warning(f"Formatting message for tool '{tool_name}'. Is error: {is_error}. Data: {response_data}")
    status = "Failed" if is_error else "Succeeded"
    # --- Authentication Formatting ---
    if tool_name == "auth":
        if is_error:
            if isinstance(response_data, dict):
                message = response_data.get("error_description") or \
                          response_data.get("detail") or \
                          response_data.get("message") or \
                          response_data.get("error", "Unknown error")
            elif isinstance(response_data, str):
                message = response_data
            else:
                message = "An unexpected error occurred during authentication."
            output["message"] = f"Authentication {status}: {message}"
        else:
            # Updated success message for authentication as per request (but not returning raw token)
            output["error"] = "n"
            output["message"] = "Authentication Succeeded. Token received and stored for use by other tools."
    # --- Fetch Alert IDs Formatting ---
    elif tool_name == "fetch_alert_ids":
        if is_error:
             error_detail = response_data.get("detail", str(response_data)) if isinstance(response_data, dict) else str(response_data)
             output["message"] = f"Fetching Alert IDs {status}: {error_detail}"
        else:
            # Assuming response_data contains the list of IDs, potentially under a key like 'resources'
            ids = response_data.get("resources", []) if isinstance(response_data, dict) else response_data
            if isinstance(ids, list):
                 count = len(ids)
                 output["error"] = "n"
                 output["message"] = f"Fetching Alert IDs {status}: Found {count} new alert IDs matching the criteria." # Returning only count for brevity
                 output["data"] = ids
            else:
                 output["message"] = f"Fetching Alert IDs {status}: Unexpected response format: {response_data}"
    # --- Fetch Alert Details Formatting ---
    elif tool_name == "fetch_alert_details":
         logging.warning("in fetch_alert_details processing - 1")
         logging.warning(response_data)
         if is_error:
             logging.warning("in fetch_alert_details processing - 2")
             error_detail = response_data.get("detail", str(response_data)) if isinstance(response_data, dict) else str(response_data)
             output["message"] = f"Fetching Alert Details {status}: {error_detail}"
             # Keep output["data"] as the raw error dict if available
         else:
            logging.warning(f"in fetch_alert_details processing - 3")
            # Fetch alert details success
            alerts = response_data.get("resources", []) if isinstance(response_data, dict) else None # Expect resources key
            logging.warning(f"in fetch_alert_details processing - 4 {len(alerts)}")
            if isinstance(alerts, list):
                 count = len(alerts)
                 extracted_data = []
                 # Iterate through each alert and extract specified fields
                 for alert in alerts:
                     if not isinstance(alert, dict): continue # Skip if an item is not a dict
                     device_info = alert.get('device', {}) # Safely get device sub-dict
                     if not isinstance(device_info, dict): device_info = {} # Ensure device_info is a dict
                     formatted_alert = {
                         "description": alert.get('description'),
                         "status": alert.get('status'),
                         "tactic": alert.get('tactic'),
                         "tactic_id": alert.get('tactic_id'),
                         "technique": alert.get('technique'),
                         "technique_id": alert.get('technique_id'),
                         "user_name": alert.get('user_name'),
                         "severity_name": alert.get('severity_name'),
                         # Use requested keys, extracting from nested device_info
                         "device_hostname": device_info.get('hostname'),
                         "device_os_version": device_info.get('os_version')
                     }
                     extracted_data.append(formatted_alert)
                 output["message"] =  f"Fetching Alert Details {status}: Extracted details for {count} alerts."
                 output["data"] = extracted_data # Assign the list of extracted dictionaries
                 output["error"] = "n"
            else:
                 # Handle unexpected success response format
                 output["error"] = "y" # Treat unexpected format as an error
                 output["message"] = f"Fetching Alert Details {status}: Unexpected response format received."
                 output["data"] = response_data # Include the unexpected data
    # --- Generic Fallback ---
    else:
        logging.warning("in fetch_alert_details processing - 4")
        if is_error:
             output["message"] = f"Tool '{tool_name}' {status}. Error: {response_data}"
        else:
             output["message"] = f"Tool '{tool_name}' {status}. Response: {response_data}"
             output["error"] = "n"
    
    return output
# --- MCP Tools ---
@mcp.tool()
async def crowdstrike_authenticate() -> str:
    """Authenticate using client id and client secret
    Args:
        None, uses arguments
    Returns:
        A JSON with following keys - 
        error - y when error else n
        message - error or success message
        data - data when applicable
    """
    global ACCESS_TOKEN
    if not all([API_BASE_URL, CLIENT_ID, CLIENT_SECRET]):
        error_msg = "Server configuration (API Base URL, Client ID, Client Secret) is not set."
        logging.warning(f"Error in authenticate: {error_msg}")
        return format_message("auth", True, error_msg)
    auth_url = f"{API_BASE_URL.rstrip('/')}/oauth2/token"
    auth_payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    logging.warning("Attempting authentication (form-urlencoded)...")
    # Use the specific make_post_request for auth, sending as form data
    response_data = await make_post_request(auth_url, payload=auth_payload, send_as_json=False)
    if isinstance(response_data, dict) and "access_token" in response_data:
        ACCESS_TOKEN = response_data["access_token"]
        logging.warning("Successfully obtained access token.")
        # Pass success indicator to format_message
        return format_message("auth", False, {"status": "success"}) # Pass simple success data
    else:
        logging.warning("Authentication failed.")
        ACCESS_TOKEN = None
        error_msg = response_data if response_data else \
                    {"error": "Unknown Authentication Failure", "detail": "Failed to process the authentication request."}
        return format_message("auth", True, error_msg)
@mcp.tool()
async def crowdstrike_fetch_alert_ids(hostname: str) -> str:
    """Fetches the latest new Endpoint Detection alert/detection composite IDs for a specific hostname
    Args:
        hostname: The hostname to filter alerts for.
    Returns:
        A JSON with following keys - 
        error - y when error else n
        message - error or success message
        data - data (generally an array/list)
    """
    tool_name = "fetch_alert_ids"
    if not ACCESS_TOKEN:
        return format_message(tool_name, True, "Authentication required. Please run 'authenticate' first.")
    if not API_BASE_URL:
         return format_message(tool_name, True, "API Base URL not configured.")
    if not hostname or not isinstance(hostname, str):
        return format_message(tool_name, True, "A valid hostname string must be provided.")
    # Construct the dynamic filter string including hostname (case-insensitive wildcard)
    hostname_upper = hostname.upper()
    hostname_lower = hostname.lower()
    # FQL filter string construction
    filter_string = f'status:"new"+product:"epp"+(device.hostname:*"*{hostname_upper}*",device.hostname:*"*{hostname_lower}*")'
    # Construct URL and parameters
    alerts_url = f"{API_BASE_URL.rstrip('/')}/alerts/queries/alerts/v2"
    query_params = {
        "include_hidden": "true",
        "filter": filter_string
    }
    logging.warning(f"Fetching alert IDs from {alerts_url} with filter: {filter_string}")
    response_data = await make_get_request(alerts_url, params=query_params)
    # Check for errors returned by the helper
    if isinstance(response_data, dict) and "error" in response_data:
        logging.warning(f"{tool_name} failed.")
        return format_message(tool_name, True, response_data)
    else:
        logging.warning(f"{tool_name} succeeded.")
        # Assuming the API returns IDs in a 'resources' list
        return format_message(tool_name, False, response_data)
@mcp.tool()
async def crowdstrike_fetch_alert_details(composite_ids: List[str]) -> str:
    """Fetches the information about alerts using a list of composite IDs.
       Very useful to find whether there are any alerts for the host and how many there are.
    Args:
        composite-ids - generally from the previous fetch_alert_ids call.
    Returns:
        A JSON with following keys - 
        error - y when error else n
        message - error or success message
        data - array of JSONs one for each alert. Having important details about the alerts
    """
    tool_name = "fetch_alert_details"
    if not ACCESS_TOKEN:
        return format_message(tool_name, True, "Authentication required. Please run 'authenticate' first.")
    if not API_BASE_URL:
         return format_message(tool_name, True, "API Base URL not configured.")
    if not isinstance(composite_ids, list) or not composite_ids:
         return format_message(tool_name, True, "Input 'composite_ids' must be a non-empty list of strings.")
    # Construct URL and payload
    details_url = f"{API_BASE_URL.rstrip('/')}/alerts/entities/alerts/v2"
    # Pass query params to make_post_request helper
    query_params = {"include_hidden": "true"}
    payload = {"composite_ids": composite_ids} # As JSON body
    logging.warning(f"Fetching alert details for {len(composite_ids)} IDs from {details_url}")
    # Use make_post_request, sending payload as JSON (default)
    # Pass query_params to the helper function
    
    response_data = await make_post_request(details_url, payload=payload, params=query_params, send_as_json=True)
    logging.warning("Done - Executing fetch_alert_details")
    # Check for errors returned by the helper
    if isinstance(response_data, dict) and "error" in response_data:
        logging.warning(f"{tool_name} failed.")
        logging.warning(f"{tool_name} failed.")
        return format_message(tool_name, True, response_data)
    else:
        #logging.warning(f"{tool_name} succeeded.")
        #logging.warning(response_data)
        # Assuming the API returns alert details in a 'resources' list
        return format_message(tool_name, False, response_data)
# --- Main Execution Block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server (`server.py`) with API Tools")
    parser.add_argument("--crwd-api-base", required=True, help="Base URL for the API")
    parser.add_argument("--client-id", required=True, help="Client ID for API authentication")
    parser.add_argument("--client-secret", required=True, help="Client Secret for API authentication")
    #parser.add_argument("--transport", default="stdio", help="MCP transport mechanism (e.g., stdio, http)")
    args = parser.parse_args()
    # Store parsed arguments in global variables
    API_BASE_URL = args.crwd_api_base
    CLIENT_ID = args.client_id
    CLIENT_SECRET = args.client_secret
    logging.warning("Configuration loaded:")
    logging.warning(f"  API Base URL: {API_BASE_URL}")
    logging.warning(f"  Client ID: {CLIENT_ID}")
    logging.warning(f"  Client Secret: {'*' * len(CLIENT_SECRET) if CLIENT_SECRET else 'Not Set'}")
    # Initialize and run the server
    mcp.run(transport='stdio')