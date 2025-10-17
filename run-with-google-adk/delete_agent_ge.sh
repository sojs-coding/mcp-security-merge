#!/bin/bash
AGENT_SPACE_PROJECT_ID="AGENT_SPACE_PROJECT_ID"
AGENT_SPACE_APP_NAME="AGENT_SPACE_APP_NAME"
AGENT_SPACE_AGENT_NAME="AGENT_SPACE_AGENT_NAME"

curl -X DELETE \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-H "X-Goog-User-Project: ${AGENT_SPACE_PROJECT_ID}" \
"https://discoveryengine.googleapis.com/v1alpha/projects/${AGENT_SPACE_PROJECT_ID}/locations/global/collections/default_collection/engines/${AGENT_SPACE_APP_NAME}/assistants/default_assistant/agents/${AGENT_SPACE_AGENT_NAME}"