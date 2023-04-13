import os
from dotenv import load_dotenv

# Secrets and keys
SECRETS = ['AZURE_OPENAI_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_VERSION']

# Load environment variables
def load_environment_variables():
    if not os.getenv("ON_AZURE"):
        load_dotenv()

    env_vars = {}
    for var_name in SECRETS:
        env_vars[var_name] = os.getenv(var_name)

    return env_vars

secrets = load_environment_variables()