import streamlit as st
import json
import httpx
import pandas as pd
import pydeck as pdk
import requests
from bs4 import BeautifulSoup 
import re
import pytesseract
import os
import streamlit.components.v1 as components
import base64
from streamlit.components.v1 import html
import webbrowser

# Set streamlit page config

# This must be called before any other Streamlit commands.
st.set_page_config(
    page_title="Azure OpenAI | Exctraction and QnA Demo",
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
#url = "http://127.0.0.1:8000/chat"
url = "http://20.85.173.27/chat"

default_messages = [
  {
    "role": "system",
    "content": "You are an AI assistant that responsds to a User Prompt asking questions or giving instructions about Provided Content. If you are not able to follow the instructions or answer the questions based on the Provided Content, respond \"I am not able to answer or do that based on the content provided.\""
  },
  {
    "role": "user",
    "content": f"User Prmopt:\n\n{{user_question}}\n\nProvided Content:\n\n{{user_content}}"
  }
]
prompt = json.dumps(default_messages)

# Prepopulated list of URLs
user_prompt_options = [
    "Extract the names of the Articles from the lease into a JSON Array.",
    "Using the lease below, return a JSON object containing:  Lessor, Lessee, Property Address, Property Description, Net Size of Property, Net Size of Property Units, Gross Size of Property, Gross Size of Property Units, Contract Start Date, Lease Start Date, Lease End Date, Lease Term (include the units), Monthly Lease Amount (include currency), Payment Frequency, Payment Address. Format dates as YYYY-MM-DD.",
    "When the lease is finally satisfied, how much will the total lease costs be.  Reason it out step by step and show me.",
    "What are the color of the kitchen walls?",
    "How many bedrooms does the propery have?",
    "I have a dispute about the lease.  What is the process for resolving it?",
    "Adhoc"
]


# Setup Sidebar options
st.sidebar.title("Model Options")

# Model
model_options = ['gpt-35-turbo', 'gpt-4', 'gpt-4-32k']
default_model = 'gpt-4-32k'
model_choice = st.sidebar.selectbox('Model', model_options, index=model_options.index(default_model))

# Page heading
st.title("Azure OpenAI - Extraction and QnA Demo")

# Setup column for prompt and for lease

# Create two columns in the layout
col_prompt, col_lease = st.columns([0.5, 0.5])

# Place the "Prompt" in the first column
with col_prompt:

    # Display prompt as h4
    st.markdown("#### Question")

    user_prompt = st.selectbox("", user_prompt_options, label_visibility="collapsed")

    if user_prompt == "Adhoc":
        question = st.text_input("Enter a question:")
        user_prompt = question if question else user_prompt

    with st.expander("Prompt"):
        messages_str = st.text_area("", json.dumps(default_messages, indent=2), height=305)

    # Place the "Submit" button in the first column
    if st.button("Submit"):

        # Step 1: Get the text from the lease.
        with open("./pages/lease-images/lease.txt", "r") as f:
            lease_text = f.read() 

        # Step 2: JSON encode the extracted text.
        encoded_web_text = json.dumps(lease_text)

        # Step 3: Load the messages from messages_str.
        messages = json.loads(messages_str)

        # Step 4: Replace the {user_content} and {user_question} placeholder with the encoded web_text in the messages list.
        user_message = messages[1]
        user_message["content"] = user_message["content"].replace("{user_question}", user_prompt)
        user_message["content"] = user_message["content"].replace("{user_content}", lease_text)

        payload = {
            "model": model_choice,
            "messages": messages,
            "temperature": 0.0,
            "top_p": 0.0
        }

        st.markdown("----")
        response_box = st.empty()

        # Set the read timeout to 10 seconds
        timeout = (2, 30)

        headers = {"Content-Type": "application/json"}

        with httpx.stream('POST', url, json=payload, timeout=timeout ) as r:
            response=""
            for chunk in r.iter_raw():  
                response += chunk.decode("utf-8")
                if "JSON" in user_prompt:
                    response_box.code(response,language="json")
                else:
                    response_box.write(response)

        st.markdown("----")

with col_lease:
    # Set path to directory containing images
    IMAGE_DIR = "./pages/lease-images/"

    # Get list of image files
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]

    # Set default image to display
    default_image = image_files[0]

    # Display prompt as h4
    st.markdown("#### Lease page")

    # Display dropdown list of images
    selected_option = st.selectbox(" ", options=image_files, index=0, label_visibility="collapsed")

    # Display selected image
    selected_image = st.empty()
    if selected_option != default_image:
        default_image = selected_option
        selected_image.image(os.path.join(IMAGE_DIR, default_image))
    else:
        selected_image.image(os.path.join(IMAGE_DIR, default_image))
