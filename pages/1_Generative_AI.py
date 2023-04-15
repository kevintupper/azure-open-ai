import streamlit as st
import json
import httpx
import pandas as pd
import pydeck as pdk

# Set streamlit page config

# This must be called before any other Streamlit commands.
st.set_page_config(
    page_title="Azure OpenAI | Generative AI Demo",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)  

# Setup page variables 
url = "http://20.85.173.27/chat"
#url = "http://127.0.0.1:8000/chat"

default_messages = [
  {
    "role": "system",
    "content": "You are a historian capable of writing comprehensive, informative reports in any language."
  },
  {
    "role": "user",
    "content": "Return a nice looking report in markdown titled, 'Fifty-five from five'.  The report contains the first 55 words from five famous speeches.  Include information about each speech: e.g. What were the conditions like?  Why was the speech made?  Include things like where, when, why, and who.  Then include a summary of whether or not the speech was impactful and why.  Make it presentation ready."
  }
]
prompt = json.dumps(default_messages)


# Setup Sidebar options
st.sidebar.title("Model Options")

# Model
model_options = ['gpt-35-turbo', 'gpt-4', 'gpt-4-32k']
default_model = 'gpt-4-32k'
model_choice = st.sidebar.selectbox('Model', model_options, index=model_options.index(default_model))

# Temperature slider
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.75, step=0.25)


# Page heading
st.title("Azure OpenAI - Generative AI Demo")

with st.expander("Prompt"):
    messages_str = st.text_area("", json.dumps(default_messages, indent=2), height=305)

if st.button("Submit"):
    messages = json.loads(messages_str)

    payload = {
        "model": model_choice,
        "messages": messages,
        "temperature": temperature
    }

    st.markdown("----")
    response_box = st.empty()
    print(model_choice)

    # Set the read timeout to 10 seconds
    timeout = (2, 30)

    headers = {"Content-Type": "application/json"}

    with httpx.stream('POST', url, json=payload, timeout=timeout ) as r:
        response=""
        for chunk in r.iter_raw():  

            response += chunk.decode("utf-8")
            response_box.markdown(response, unsafe_allow_html=True)

    st.markdown("----")

