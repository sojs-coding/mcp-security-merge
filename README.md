# Google Security Operations and Threat Intelligence MCP Server

This repository contains Model Context Protocol (MCP) servers that enable MCP clients (like Claude Desktop or the cline.bot VS Code extension) to access Google's security products and services:

1. **Google Security Operations (Chronicle)** - For threat detection, investigation, and hunting
2. **Google Security Operations SOAR** - For security orchestration, automation, and response
3. **Google Threat Intelligence (GTI)** - For access to Google's threat intelligence data
4. **Security Command Center (SCC)** - For cloud security and risk management

Each server can be enabled and run separately, allowing flexibility for environments that don't require all capabilities.

## Documentation

Comprehensive documentation is available in the `docs` folder. You can:

1. Read the markdown files directly in the repository
2. View the documentation website at [https://google.github.io/mcp-security/](https://google.github.io/mcp-security/)
3. Generate HTML documentation locally using Sphinx (see instructions in the docs folder)

The documentation covers:
- Detailed information about each MCP server
- Configuration options and requirements
- Usage examples and best practices

To get started with the documentation, see [docs/index.md](docs/index.md).

## Authentication

The server uses Google's authentication. Make sure you have either:

1. Set up Application Default Credentials (ADC)
2. Set a GOOGLE_APPLICATION_CREDENTIALS environment variable
3. Used `gcloud auth application-default login`

## Client Configurations
The MCP servers from this repo can be used with following clients
1. Cline, Claude Desktop, and other MCP supported clients
2. Google ADK Agents (a prebuilt agent example is provided)

The configuration for Claude Desktop and Cline is the same (provided below for [uv](#using-uv-recommended) and [pip](#using-pip)).  We use the stdio transport.

This repo also comes with a prebuilt [Google ADK(Agent Development Kit)](https://google.github.io/adk-docs/) agent. It can be configured and run out of the box, instructions below - 


### Using the prebuilt Google ADK agent as client
<details>
#### Prerequesites
You need the following to run the agent

1. `python` - v3.11+
2. `pip`
3. `gcloud` cli (If you ran on Google Cloud Console then gcloud is already installed)

#### Setting up and running the agent
Please execute the following instructions

```bash
   # Clone the repo
   git clone https://github.com/google/mcp-security.git
   
   # Goto the agent directory
   cd mcp-security/run-with-google-adk
   
   # Create and activate the virtual environment
   python3 -m venv .venv
   . .venv/bin/activate

   # Install dependencies (google-adk and uv)
   pip install -r requirements.txt
   
   # Add exec permission to run-adk-agent.sh - which runs our agent
   chmod +x run-adk-agent.sh

   # Run the agent
   ./run-adk-agent.sh
```

For the very first run it creates a `.env` file to update

```bash
# sample output
$./run-adk-agent.sh 
[INFO] '.env' file not found at './google-mcp-security-agent/.env'. Creating it with default values (double-quoted in file)...
[WARN] '.env' file created at ./google-mcp-security-agent/.env
[WARN] Please update values for variables (and review LOAD_ flags) in './google-mcp-security-agent/.env', then re-run this script.
```

Use your favorite editor and update `./google-mcp-security-agent/.env`. 

The default `.env` file is shown below. Update the variables as needed in your favorite editor. You can choose to load some or all of the MCP servers available using the load environment variable at the start of each section. Make sure that variables in the `MANDATORY` section have proper values (make sure you get and update the `GOOGLE_API_KEY` using [instructions](https://ai.google.dev/gemini-api/docs/api-key)) and the value of the variable `GOOGLE_GENAI_USE_VERTEXAI` is set to "False" always (As we want to use the Google [Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview) instead of the [Vertex AI SDK](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk)).

```bash
# SecOps MCP
LOAD_SECOPS_MCP="Y"
CHRONICLE_PROJECT_ID="NOT_SET"
CHRONICLE_CUSTOMER_ID="NOT_SET"
CHRONICLE_REGION="NOT_SET"

# GTI MCP
LOAD_GTI_MCP="Y"
VT_APIKEY="NOT_SET"

# SECOPS_SOAR MCP
LOAD_SECOPS_SOAR_MCP="Y"
SOAR_URL="NOT_SET"
SOAR_APP_KEY="NOT_SET"

# MANDATORY
GOOGLE_GENAI_USE_VERTEXAI="False"
GOOGLE_MODEL="gemini-2.5-pro-preview-03-25"
DEFAULT_PROMPT="Helps user investigate security issues using Google Secops SIEM, SOAR and Google Threat Intel Tools, all authentication actions are automatically approved"
GOOGLE_API_KEY="NOT_SET"

```

Once the variables are all updated as needed, run the agent again (make sure you are back in the `mcp-security/run-with-google-adk` directory).

```bash
   # Authenticate to use SecOps APIs
   # Skip if running in Google Cloud Shell
   gcloud auth application-default login
```

```bash
   # Run the agent again
   ./run-adk-agent.sh
```

You should get an output like following

```bash
# Sample output
$./run-adk-agent.sh 
[INFO] Found './google-mcp-security-agent/.env'. Ensuring its structure...
[INFO] Validating variable values in './google-mcp-security-agent/.env'...
[INFO] All required variables are set according to LOAD flags.
[INFO] Active configuration (values are masked where appropriate):
  Section: MANDATORY
    GOOGLE_GENAI_USE_VERTEXAI: F...e
    GOOGLE_MODEL: gem...-25
    DEFAULT_PROMPT: Hel...ved
    GOOGLE_API_KEY: AIz...qLU
  Section: SecOps MCP (LOADED)
    LOAD_SECOPS_MCP: Y
    CHRONICLE_PROJECT_ID: par...ops
    CHRONICLE_CUSTOMER_ID: 118...bca
    CHRONICLE_REGION: US
  Section: GTI MCP (LOADED)
    LOAD_GTI_MCP: Y
    VT_APIKEY: 171...631
  Section: SecOps SOAR MCP (LOADED)
    LOAD_SECOPS_SOAR_MCP: Y
    SOAR_URL: htt...com
    SOAR_APP_KEY: 8ad...707

[INFO] Attempting to run 'adk web' with the above configuration...
----------------------------------------------------------------------
INFO:     Started server process [412930]
INFO:     Waiting for application startup.

+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://localhost:8000.                         |
+-----------------------------------------------------------------------------+

INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

```

Access the Agent 🤖 interface by going to `http://localhost:8000`

> 🪧 **NOTE:**  
> First response usually takes a bit longer as the agent is loading the tools from the MCP server(s).

> ⚠️ **CAUTION:**  
> In case the response seems stuck and/or there is an error on the console, create a new session in the ADK Web UI by clicking `+ New Session` in the top right corner. You can also ask a follow up question in the same session like `Are you still there?` or `Can you retry that?`

> 🪧 **NOTE:**  
> When exiting, shut down the browser tab first and then use `ctrl+c` to exit on the console. 


> If you want to use Cline / Cloude Desktop please check the following two sections for configurations
</details>

### Using uv (Recommended)

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops/secops_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
        "CHRONICLE_REGION": "us"
      },
      "disabled": false,
      "autoApprove": []
    },
    "secops-soar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops-soar/secops_soar_mcp",
        "run",
        "server.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {
        "SOAR_URL": "https://yours-here.siemplify-soar.com:443",
        "SOAR_APP_KEY": "01234567-abcd-4321-1234-0123456789ab"
      },
      "disabled": false,
      "autoApprove": []
    },
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "VT_APIKEY": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      },
      "disabled": false,
      "autoApprove": []
    },
    "scc-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/scc",
        "run",
        "scc_mcp.py"
      ],
      "env": {
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

NOTE: `uv` also supports passing an `.env` file like so:
```
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/...",
        "run",
        "--env-file",
        "/path/to/the/repo/server/.env",
        "server.py"
      ]
```

`SOAR_APP_KEY` and `VT_APIKEY` are good candidates for `.env`


### Using pip

You can also use pip instead of uv to install and run the MCP servers. This approach uses a bash command to:
1. Change to the server directory
2. Install the package in development mode
3. Run the server binary

```json
{
  "mcpServers": {
    "secops": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/secops && pip install -e . && secops_mcp"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
        "CHRONICLE_REGION": "us"
      },
      "disabled": false,
      "autoApprove": [
      ],
      "alwaysAllow": [
      ]
    },
    "gti": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/gti && pip install -e . && gti_mcp"
      ],
      "env": {
        "VT_APIKEY": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      },
      "disabled": false,
      "autoApprove": [
      ],
      "alwaysAllow": [
      ]
    },
  "secops-soar": {
      "autoApprove": [
      ],
      "disabled": false,
      "timeout": 60,
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/secops-soar && pip install -e . && python secops_soar_mcp/server.py"
      ],
      "env": {
        "SOAR_URL": "https://yours-here.siemplify-soar.com:443",
        "SOAR_APP_KEY": "01234567-abcd-4321-1234-0123456789ab"
      },
      "transportType": "stdio"
    }
  }
}
```

### When to use uv vs pip

- **uv**: Recommended for most users because it offers faster package installation, better dependency resolution, and isolated environments. It also supports loading environment variables from a file.
- **pip**: Use when you prefer the standard Python package manager or when you have specific environment setup requirements.

#### `UV_ENV_FILE`

The `--env-file` option allows `uv` to use a .env file for environment variables. You can create this file or use system environment variables as described in the usage guide.

Alternatively, you can set `UV_ENV_FILE` to your `.env` file and omit the `--env-file` portion of the configuration.

Refer to the [usage guide](docs/usage_guide.md#setting-up-environment-variables) for detailed instructions on how to set up these environment variables.


### Troubleshooting

Running the MCP Server from the CLI (and outside of your MCP client) can reveal issues:
```
uv --verbose \
  --directory "/Users/dandye/Projects/google-mcp-security/server/scc" \
  run \
  --env-file "/Users/dandye/Projects/google-mcp-security/.env" \
  scc_mcp.py
```

Check your PATH(s):

```which uv``` # you may need to restart MCP Client after installing uv

```which python || which python3```

```python --version || python3 --version```



### Installing in Claude Desktop

To use the MCP servers with Claude Desktop:

1. Install Claude Desktop
2. Open Claude Desktop and select "Settings" from the Claude menu
3. Click on "Developer" in the lefthand bar, then click "Edit Config"
4. Update your `claude_desktop_config.json` with the configuration (replace paths with your actual paths)
5. Save the file and restart Claude Desktop
6. You should now see the hammer icon in the Claude Desktop interface, indicating the MCP server is active

### Installing in cline (vscode extension)

1. Install cline.bot extension in VSCode
2. Update your `cline_mcp_settings.json` with the configuration (replace paths with your actual paths)
3. Save the file and restart VS Code

## License

Apache 2.0
