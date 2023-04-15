from secrets_and_keys import secrets
import openai

#====================================================================================================
# Utility and helper functions
#====================================================================================================

def config_azure_openai():
    openai.api_type = "azure"
    openai.api_base = secrets["AZURE_OPENAI_ENDPOINT"]
    openai.api_version = secrets["AZURE_OPENAI_VERSION"]
    openai.api_key = secrets["AZURE_OPENAI_KEY"]
    return openai



# https://extras.streamlit.app/Streamlit%20Faker