#!/bin/bash
AGENT_SPACE_PROJECT_ID="AGENT_SPACE_PROJECT_ID"
AGENT_SPACE_APP_NAME="AGENT_SPACE_APP_NAME"
AGENT_ENGINE_PROJECT_NUMBER="AGENT_ENGINE_PROJECT_NUMBER"
AGENT_LOCATION="AGENT_LOCATION"
REASONING_ENGINE_NUMBER="REASONING_ENGINE_NUMBER"

# Corrected variable expansion (no '!')
TARGET_URL="https://discoveryengine.googleapis.com/v1alpha/projects/${AGENT_SPACE_PROJECT_ID}/locations/global/collections/default_collection/engines/${AGENT_SPACE_APP_NAME}/assistants/default_assistant/agents"

JSON_DATA=$(cat <<EOF
{
    "displayName": "Google Security Agent",
    "description": "Allows security operations on Google Security Products",
    "adk_agent_definition":
    {
        "tool_settings": {
            "tool_description": "Various Tools from SIEM, SOAR and SCC"
        },
        "provisioned_reasoning_engine": {
            # Corrected variable expansion (no '!')
            "reasoning_engine":"projects/${AGENT_ENGINE_PROJECT_NUMBER}/locations/${AGENT_LOCATION}/reasoningEngines/${REASONING_ENGINE_NUMBER}"
        }
    }
}
EOF
)

echo "Sending POST request to: $TARGET_URL"
echo "Request Body:"
echo "$JSON_DATA"
echo ""

# Perform the POST request using curl
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     # Corrected variable expansion (no '!')
     -H "X-Goog-User-Project: ${AGENT_SPACE_PROJECT_ID}" \
     -d "$JSON_DATA" \
     "$TARGET_URL"

echo "" # Add a newline after curl output for better readability
echo "cURL command finished."