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

This repo also comes with a prebuilt [Google ADK(Agent Development Kit)](https://google.github.io/adk-docs/) agent. It can be configured and run out of the box using the instructions provided [below](#using-the-prebuilt-google-adk-agent-as-client) - 

> 💡 **Agent for more than one user / tester:**  
> The ADK based agent can also be deployed on [Cloud Run](https://cloud.google.com/run). Please refer to the **Cloud Run Deployment Instructions** in the next section.

### Using the prebuilt Google ADK agent as client
<details>

<summary>Local Deployment Instructions.</summary>

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

For the very first run it creates a default .env file in `./google-mcp-security-agent/.env`

```bash
# sample output
$./run-adk-agent.sh 
Copying ./google-mcp-security-agent/sample.env to ./google-mcp-security-agent/.env...
Please update the environment variables in ./google-mcp-security-agent/.env
```

Use your favorite editor and update `./google-mcp-security-agent/.env`. 

The default `.env` file is shown below. 

1. Update the variables as needed in your favorite editor. You can choose to load some or all of the MCP servers available using the load environment variable at the start of each section. Don't use quotes for values except for `DEFAULT_PROMPT`. 
2. Make sure that variables in the `MANDATORY` section have proper values (make sure you get and update the `GOOGLE_API_KEY` using these [instructions](https://ai.google.dev/gemini-api/docs/api-key)) 
3. The value of the variable `GOOGLE_GENAI_USE_VERTEXAI` is set to "False" always (As we want to use the Google [Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview) instead of the [Vertex AI SDK](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk) due to some compatibility issues).
4. You can experiment with the prompt `DEFAULT_PROMPT`. Use single quotes for the prompt. If you plan to later deploy to a Cloud Run Service - avoid commas (or if you use them they will be converted to semicommas during deployment).

```bash
# Please do not use quotes / double quotes for values except for DEFAULT_PROMPT (use single quotes there)

# SecOps MCP
LOAD_SECOPS_MCP=Y
CHRONICLE_PROJECT_ID=NOT_SET
CHRONICLE_CUSTOMER_ID=NOT_SET
CHRONICLE_REGION=NOT_SET

# GTI MCP
LOAD_GTI_MCP=Y
VT_APIKEY=NOT_SET

# SECOPS_SOAR MCP
LOAD_SECOPS_SOAR_MCP=Y
SOAR_URL=NOT_SET
SOAR_APP_KEY=NOT_SET

# SCC MCP
LOAD_SCC_MCP=Y

# MANDATORY
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY=NOT_SET
GOOGLE_MODEL=gemini-2.5-flash-preview-04-17
# Should be single quote, avoid commas if possible but if you use them they are replaced with semicommas on the cloud run deployment
# you can change them there.
DEFAULT_PROMPT='Helps user investigate security issues using Google Secops SIEM, SOAR, Security Command Center(SCC) and Google Threat Intel Tools All authentication actions are automatically approved. If the query is about a SOAR case try to provide a backlink to the user. A backlink is formed by adding /cases/<case id> to this URL present in field ui_base_link. If the user asks with only ? or are you there? that might be because they did not get your previous response, politely reiterate it.'

```

Once the variables are updated, run the agent again (make sure you are back in the `mcp-security/run-with-google-adk` directory).

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
Contents of .env (with masked values):
# Please do not use quotes / double quotes for values except for DEFAULT_PROMPT (use single quotes there)
# SecOps MCP
LOAD_SECOPS_MCP=Y
.
(output cropped)
.

Running adk web command...
INFO:     Started server process [1203693]
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
> In case the response seems stuck and/or there is an error on the console, create a new session in the ADK Web UI by clicking `+ New Session` in the top right corner. You can also ask a follow up question in the same session like `Are you still there?` or `Can you retry that?`. You can also try switching `Token Streaming` on.

> 🪧 **NOTE:**  
> When exiting, shut down the browser tab first and then use `ctrl+c` to exit on the console. 


> If you want to use Cline / Cloude Desktop please check the following two sections for configurations
</details>

<details>

<summary>Cloud Run Deployment Instructions.</summary>

The agent with MCP servers can be deployed as a Cloud Run Service, right from within the source code directory.

#### Prerequesites

1. Must have locally run the ADK based agent successfully at least once.
2. Must have required APIs enabled and proper IAM access ([details](https://cloud.google.com/run/docs/deploying-source-code#before_you_begin))

#### Costs
In addition to Gemini API costs, running agent will incur cloud costs. Please check [Cloud Run Pricing](https://cloud.google.com/run/pricing).

> ⚠️ **WARNING:**  
> It is not recommended to run the a Cloud Run service with unauthenticated invocations enabled (we do that initially for verification). Please follow steps to enable [IAM authentication](https://cloud.google.com/run/docs/authenticating/developers) on your service. You ccould also deploy it behind the [Identity Aware Proxy (IAP)](https://cloud.google.com/iap/docs/enabling-cloud-run) - but that is out of scope for this documentation.

#### Deployment Steps

```bash
# Please run these commands from the mcp-security directory
chmod +x cloudrun_deploy_run.sh

export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=your-region

./cloudrun_deploy_run.sh deploy
```
Sample output is provided below

```bash
# Sample output
$ ./cloudrun_deploy_run.sh deploy
Starting deployment process...
Adding environment variable: LOAD_SECOPS_MCP
Adding environment variable: CHRONICLE_PROJECT_ID
Adding environment variable: CHRONICLE_CUSTOMER_ID
Adding environment variable: CHRONICLE_REGION
Adding environment variable: LOAD_GTI_MCP
Adding environment variable: VT_APIKEY
Adding environment variable: LOAD_SECOPS_SOAR_MCP
Adding environment variable: SOAR_URL
Adding environment variable: SOAR_APP_KEY
Adding environment variable: LOAD_SCC_MCP
Skipping environment variable: GOOGLE_GENAI_USE_VERTEXAI
Adding environment variable: GOOGLE_API_KEY
Adding environment variable: GOOGLE_MODEL
Adding environment variable: DEFAULT_PROMPT
Using environment variables: 
[REDACTED]
Building using Dockerfile and deploying container to Cloud Run service [mcp-security-agent-service] in project [YOUR-PROJECT] region [us-central1]
⠛ Building and deploying... Uploading sources.                                                                                                                                               
⠏ Building and deploying... Uploading sources.                                                                                                                                               
  ⠏ Uploading sources...                                                                                                                                                                     
  . Creating Revision...                                                                                                                                                                     
  . Routing traffic...                                                                                                                                                                       
  . Setting IAM Policy...                                                                                                                                                                    
Creating temporary archive of 576 file(s) totalling 11.2 MiB before compression.
Some files were not included in the source upload.
✓ Building and deploying... Done.                                                                                                                                                            
  ✓ Uploading sources...                                                                                                                                                                     
  ✓ Building Container... Logs are available at [[REDACTED]].          
  ✓ Creating Revision...                                                                                                                                                                     
  ✓ Routing traffic...                                                                                                                                                                       
  ✓ Setting IAM Policy...                                                                                                                                                                    
Done.                                                                                                                                                                                        
Service [mcp-security-agent-service] revision [mcp-security-agent-service-[REDACTED]] has been deployed and is serving 100 percent of traffic.
Service URL: [REDACTED]
Successfully deployed the service.

```
Now, you can verify the service by browsing to the service endpoint.

#### IAM access to use Chronicle and SCC

Please remember that cloud run uses default service account of compute engine service. Go to IAM and provide the service account access to "Chronicle API Viewer" (in the project associated with your SecOps instance) and appropriate role for SCC (roles starting with Security Center in IAM)


#### Restrict Service To Known Developers / Testers

Summarizing the steps from [IAM authentication](https://cloud.google.com/run/docs/authenticating/developers)

1. Goto Cloud Run - Services - click `mcp-security-agent-service`
2. Click `Security`
3. In `Authentication`, `Use Cloud IAM to authenticate incoming requests` should be already selected.
4. Select the radio button `Require authentication`
5. Click `Save`
6. Cloud Run - Services - select `mcp-security-agent-service`
7. At the top click `permissions`, a pane `Permissions for mcp-security-agent-service` should open on the right hand side.
8. Click `Add principal`
9. Add the users you want to provide access to and provide them `Cloud Run Invoker` role.
10. Wait for some time.

##### Accessing the restricted service

1. Ask your users to run the following command (replace project id and region with the project id & region in which you have deployed the service)

```bash
gcloud run services proxy mcp-security-agent-service --project PROJECT-ID --region YOUR-REGION

```
2. Now they can access this agent on `http://localhost:8080`


#### Vertically scaling your container(s)
In case the cloud run logs show errors like below, you can consider increasing the resources for the individual containers

`Memory limit of 512 MiB exceeded with 543 MiB used. Consider increasing the memory limit, see https://cloud.google.com/run/docs/configuring/memory-limits`

##### Steps

1. Goto Cloud Run - Services - click `mcp-security-agent-service`
2. Click `Edit & deploy new revision`
3. In `Container(s)` - `Edit Container(s)` - `Settings`
4. Add resources by updating either Memory/ CPU or both.

#### Reducing Cloud logging
Since the entire context and response from the LLM is printed as logs. You might end up logging some sensitive information. Setting the environment vairable `MINIMAL_LOGGING` to `Y` should fix this issue. This should also reduce cloud logging costs. Mostly applies when the agent is deployed as a cloud run service.

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
    "scc-mcp": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/scc && pip install -e . && scc_mcp"
      ],
      "env": {
      },
      "disabled": false,
      "autoApprove": [],
      "alwaysAllow": []
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
