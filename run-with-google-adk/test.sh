#!/bin/bash

PYTHON_SCRIPT_PATH="/tmp/default_prompt.py"
ENV_FILE_PATH="./google_mcp_security_agent/.env"

cat << EOF > "$PYTHON_SCRIPT_PATH"
import os
import dotenv
from dotenv import load_dotenv

load_dotenv('$ENV_FILE_PATH')

text = os.environ.get("DEFAULT_PROMPT")

if text is None:
    print("")
else:
    prepared_text = text.replace('"', '\\\"')
    prepared_text = prepared_text.replace('\\n', '\\\n')
    print(prepared_text)
EOF

default_prompt=$(python $PYTHON_SCRIPT_PATH)

echo "$default_prompt"

#rm "$PYTHON_SCRIPT_PATH"