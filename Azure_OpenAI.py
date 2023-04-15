import os
from dotenv import load_dotenv
import streamlit as st  
from compile_scss import compile_scss  
from secrets_and_keys import secrets
  
from PIL import Image

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
    


# # Main content 


# Function to get the list of image files in the specified directory
def get_image_files(directory):
    image_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(filename)
    return image_files

# Function to display the selected image
def display_image(image_path):
    image = Image.open(image_path)
    st.image(image, use_column_width=True)

folder_path = "slides/"
image_files = get_image_files(folder_path)

# Create a dictionary to store the image file paths by their pill names
image_dict = {}
for filename in image_files:
    # Get the pill name from the filename
    pill_name = filename.split("_", 1)[-1].replace("_", " ").rsplit(".", 1)[0]
    image_dict[pill_name] = os.path.join(folder_path, filename)

# Sort the dictionary by the pill names
sorted_image_dict = {k: v for k, v in sorted(image_dict.items(), key=lambda item: item[0])}

# Create the sidebar with the image pills
st.sidebar.title("Slides")
for pill_name, image_path in sorted_image_dict.items():
    if st.sidebar.button(pill_name, use_container_width=True):
        display_image(image_path)

# Create the main page with the selected image
if "selected_image_path" in st.session_state:
    display_image(st.session_state.selected_image_path)


# Function to display the selected image
def display_image(image_path):
    image = Image.open(image_path)
    st.image(image, use_column_width=True)
