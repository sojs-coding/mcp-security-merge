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

#!/bin/bash

ENV_FILE="./run-with-google-adk/google-mcp-security-agent/.env"

# Check if required environment variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ] || [ -z "$GOOGLE_CLOUD_LOCATION" ]; then
  echo "Error: GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables must be set."
  echo "Please set them before running this script, e.g.:"
  echo "export GOOGLE_CLOUD_PROJECT=your-project-id"
  echo "export GOOGLE_CLOUD_LOCATION=your-region"
  exit 1
fi

# Function to create .env file
create_env_file() {
  local env_file="$1"
  shift # Remove the first argument ($env_file)
  
  # Check if the .env file already exists
  if [ -f "$env_file" ]; then
    echo "Warning: $env_file already exists. Overwriting."
  fi

  # Create the .env file
  touch "$env_file"

  # Add variables to the .env file
  for var in "$@"; do
    key=$(echo "$var" | cut -d'=' -f1)
    value=$(eval "echo \$$key") # Expand the variable
    echo "$key=$value" >> "$env_file"
  done
  echo "Successfully created $env_file with specified variables."
}

# Check the command
if [ "$1" = "deploy" ]; then
  echo "Starting deployment process..."
  # Initialize the env_vars string with the given values
  env_vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=False,REMOTE_RUN=Y"

  # Check if the .env file exists
  if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found. Please create it with your environment variables."
    exit 1
  fi

  # Read the .env file, line by line
  while IFS='=' read -r key value; do
    # Skip empty lines and comments
    if [[ -n "$key" && "$key" != "#"* ]]; then
      # Skip GOOGLE_GENAI_USE_VERTEXAI
      if [ "$key" != "GOOGLE_GENAI_USE_VERTEXAI" ]; then
        # Replace commas with semi commas for DEFAULT_PROMPT
        if [ "$key" = "DEFAULT_PROMPT" ]; then
          value=$(echo "$value" | sed 's/,/;/g')
        fi
        # Append to the env_vars string
        if [ -z "$env_vars" ]; then
          env_vars="$key=$value"
        else
          env_vars="$env_vars,$key=$value"
        fi
        echo "Adding environment variable: $key"
      else
        echo "Skipping environment variable: GOOGLE_GENAI_USE_VERTEXAI"
      fi
    fi
  done < "$ENV_FILE"

  # Check if any environment variables were found
  if [ -z "$env_vars" ]; then
    echo "Warning: No environment variables found in $ENV_FILE or all were skipped."
    echo "The 'gcloud run deploy' command may fail if required variables are missing."
  fi

  # Print the constructed environment variables string
  echo "Using environment variables: $env_vars"

  # Deploy the service with the dynamically constructed environment variables
  gcloud run deploy mcp-security-agent-service \
    --source . \
    --region "$GOOGLE_CLOUD_LOCATION" \
    --project "$GOOGLE_CLOUD_PROJECT" \
    --allow-unauthenticated \
    --set-env-vars="$env_vars" \
    --memory 2Gi
  
  deploy_status=$? #get the status

  # Check the status of the deployment
  if [ "$deploy_status" -eq 0 ]; then
    echo "Successfully deployed the service."
  else
    echo "Failed to deploy the service."
    exit 1
  fi

elif [ "$1" = "run" ]; then
  echo "Creating .env file with specified variables..."
  # Create the .env file with the specified variables
  create_env_file "/tmp/.env" \
    "LOAD_SECOPS_MCP=$LOAD_SECOPS_MCP" \
    "CHRONICLE_PROJECT_ID=$CHRONICLE_PROJECT_ID" \
    "CHRONICLE_CUSTOMER_ID=$CHRONICLE_CUSTOMER_ID" \
    "CHRONICLE_REGION=$CHRONICLE_REGION" \
    "LOAD_GTI_MCP=$LOAD_GTI_MCP" \
    "VT_APIKEY=$VT_APIKEY" \
    "LOAD_SECOPS_SOAR_MCP=$LOAD_SECOPS_SOAR_MCP" \
    "SOAR_URL=$SOAR_URL" \
    "SOAR_APP_KEY=$SOAR_APP_KEY" \
    "GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI" \
    "GOOGLE_API_KEY=$GOOGLE_API_KEY" \
    "GOOGLE_MODEL=$GOOGLE_MODEL" \
    "DEFAULT_PROMPT=$DEFAULT_PROMPT"

    echo "Starting uvicorn server ..."
    uvicorn cloudrun_deploy:app --host 0.0.0.0 --port $PORT
else
  echo "Error: Invalid command. Use 'deploy' or 'run'."
  exit 1
fi
