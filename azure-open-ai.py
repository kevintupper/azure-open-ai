import os
from dotenv import load_dotenv
import streamlit as st  
from compile_scss import compile_scss  
from secrets_and_keys import secrets
  






#====================================================================================================




#====================================================================================================
# Main code
#====================================================================================================

# Set streamlit page config
# This must be called before any other Streamlit commands.
st.set_page_config(
    page_title="Azure OpenAI",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)  

# Compile SCSS to CSS  
compile_scss()  
  
# Custom styling  
with open("style.css") as f:  
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)  
    
# Main content 
st.write("# Welcome to Streamlit! 👋")


st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!

    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

# Sidebar  
st.sidebar.success("Select a demo above.")
