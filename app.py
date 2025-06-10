# Import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key
# from google.generativeai.types import Part
import base64
from PIL import Image
import io

# Configure Gemini API
genai.configure(api_key=api_key)

# Set the page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")
st.image("medical_logo.jpg", width=120)
st.title("Vital Image Analytics")
st.subheader("An application that helps users identify visual medical conditions")

# Upload file
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
submit_button = st.button("Generate the Analysis")

# Prompt template
prompt_template = """
You are a medical assistant AI. A patient has uploaded a photo showing a visible health condition (like a skin issue, rash, pimple, or other visible disease).

Please provide a professional medical analysis in the following structure:

1. **Detailed Description**: Describe the visible condition observed in the image.
2. **Reason of Causes**: List common or possible causes behind such a condition.
3. **Solution**: Suggest general remedies, treatments, or medications (OTC or natural, if applicable).
4. **Preventive Measures**: How can one avoid or reduce the risk of this condition.
5. **Disclaimer / Caution**: Clearly mention this is not a substitute for professional medical advice, and visiting a doctor is recommended for accurate diagnosis.
"""

# Function to convert image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()

# Analysis section
if submit_button and uploaded_file:
    try:
        # Load image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Convert to base64 for Gemini
        image_base64 = image_to_base64(image)

        # Create content for Gemini API
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(
            [
                prompt_template,
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64decode(image_base64)
                }
            ],
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                top_p=1,
                top_k=10,
                max_output_tokens=1024,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
            ]
        )

        # Display the output
        st.markdown("### Analysis Report")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
