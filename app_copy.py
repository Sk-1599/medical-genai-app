# Import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# configure genai with api key
genai.configure(api_key=api_key)

# set the page configuration
st.set_page_config(page_title="VitalImage Analytics",page_icon=":robot:")

# set the logo
st.image("medical_logo.jpg",width=120)

# set the title
st.title("Vital Image Analytics")

#set the subtitle
st.subheader("An application that can help users to identify medical images")

uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg","jpeg"])
submit_button = st.button("Generate the Analysis")

if submit_button:
    pass

