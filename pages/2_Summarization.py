import streamlit as st
import json
import httpx
import pandas as pd
import pydeck as pdk
import requests
from bs4 import BeautifulSoup 
import re


# Set streamlit page config

# This must be called before any other Streamlit commands.
st.set_page_config(
    page_title="Azure OpenAI | Summarization Demo",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)  

def remove_irrelevant_elements(soup):
    for elem in soup(['script', 'style', 'aside', 'nav', 'footer']):
        elem.decompose()

    for a in soup.find_all('a'):
        
        a.attrs.pop('href', None)    

    return soup

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def sanitize_text(text):
    return re.sub(r'[\'"]', '', text)

def extract_text_from_url(url):
    # Add User-Agent header to mimic web browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # Get the HTML content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove irrelevant elements
    soup = remove_irrelevant_elements(soup)

    # Extract the text within the relevant tags
    text = '\n'.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])

    # Clean the text by removing extra whitespaces and special characters
    text = clean_text(text)
    text = sanitize_text(text)

    return text


# Setup page variables 
#url = "http://127.0.0.1:8000/chat"
url = "http://20.85.173.27/chat"

default_messages = [
  {
    "role": "system",
    "content": "You are a website summarizer. You produce comprehensive summaries in Markdown format from all content you are given. Your users only know English so regardless of the language the page is written in, your summaries are English."
  },
  {
    "role": "user",
    "content": f"Summarize:\n\nContent:\n\n{{page_content}}"
  }
]
prompt = json.dumps(default_messages)

# Prepopulated list of URLs
url_options = [
    "https://www.state.gov/overseas-buildings-operations/",
    "https://www.irs.gov/es/refunds/get-your-refund-faster-tell-irs-to-direct-deposit-your-refund-to-one-two-or-three-accounts"
]


# Setup Sidebar options
st.sidebar.title("Model Options")

# Model
model_options = ['gpt-35-turbo', 'gpt-4', 'gpt-4-32k']
default_model = 'gpt-4-32k'
model_choice = st.sidebar.selectbox('Model', model_options, index=model_options.index(default_model))

# Temperature slider
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.75, step=0.25)


# Page heading
st.title("Azure OpenAI - Summarization Demo")

with st.expander("Prompt"):
    messages_str = st.text_area("", json.dumps(default_messages, indent=2), height=305)

url_for_summary = st.selectbox("Select a URL:", url_options)

# Create two columns in the layout
col1, col2 = st.columns([0.2, 0.8])

# Place the "Submit" button in the first column
if col1.button("Submit"):
    # Step 1: Get the text from the website.
    web_text = extract_text_from_url(url_for_summary)

    # Step 2: JSON encode the extracted text.
    encoded_web_text = json.dumps(web_text)

    # Step 3: Load the messages from messages_str.
    messages = json.loads(messages_str)

    # Step 4: Replace the {page_content} placeholder with the encoded web_text in the messages list.
    user_message = messages[1]
    user_message["content"] = user_message["content"].replace("{page_content}", encoded_web_text)

    payload = {
        "model": model_choice,
        "messages": messages,
        "temperature": temperature
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
            response_box.markdown(response, unsafe_allow_html=True)

    st.markdown("----")

# Place the "Go to Page" link in the second column
col2.markdown(f'<a href="{url_for_summary}" target="_blank">Go to Page</a>', unsafe_allow_html=True)

