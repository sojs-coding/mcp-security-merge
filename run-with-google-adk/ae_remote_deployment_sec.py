
import dotenv
import os
import sys


dotenv.load_dotenv("./google_mcp_security_agent/.env")

import vertexai
import sys

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = os.environ.get("AE_STAGING_BUCKET")

if not STAGING_BUCKET.startswith("gs://"):
    STAGING_BUCKET="gs://"+STAGING_BUCKET

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET
)

# TODO add check for number of params.
env_vars = sys.argv[1]
env_vars_list=env_vars.split(",")

env_vars_to_send = {}

for key in env_vars_list:
    if key not in ["GOOGLE_CLOUD_PROJECT","GOOGLE_CLOUD_LOCATION"]: # These are not allowed as env variables on the AE, filtering them.
        env_vars_to_send[key] = os.environ.get(key)
   
# override
env_vars_to_send['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

# important for pickling
os.environ["AE_RUN"] = "Y"

env_vars_to_send['REMOTE_RUN'] = 'Y'
env_vars_to_send['AE_RUN'] = 'Y'


# # remote deplyment and first run
# # remote run
from vertexai import agent_engines
from google_mcp_security_agent import agent

print(f"env_vars_to_send => {env_vars_to_send}")

remote_app = agent_engines.create(
# Mostly for agent engine Console.
display_name="google_security_agent",description="Allows security actions on various google security products", 
agent_engine=agent.root_agent,
requirements="requirements.txt",
extra_packages=[
    "./google_mcp_security_agent", # a directory
    "./utils_extensions_cbs_tools", # a directory
    "./server", # a directory
    "./temp",
    "./object-viewer-sa.json", # a file
],
env_vars=env_vars_to_send # send all required variables to agent engine.
)

# This is just for testing after the deployment.
remote_session = remote_app.create_session(user_id="test_user")
remote_session

for event in remote_app.stream_query(
    user_id="test_user",
    session_id=remote_session["id"],
    message="what can you do?",
):
    print(event)

