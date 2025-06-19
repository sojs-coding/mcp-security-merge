import os
from dotenv import load_dotenv
load_dotenv('./google_mcp_security_agent/.env')
#print(os.environ.get("DEFAULT_PROMPT"))
text=os.environ.get("DEFAULT_PROMPT")
prepared_text = text.replace('\\', '\\\\')
prepared_text = prepared_text.replace('"', '\\"')
prepared_text = prepared_text.replace('\n', '\\n')
print(prepared_text)
