## About Model:        bytedance/ sdxl-lightning-4step : # SDXL-Lightning by ByteDance: a fast text-to-image model that makes high-quality images in 4 steps 
## Replicate.com URL:  https://replicate.com/bytedance/sdxl-lightning-4step?prediction=nr53bjbbeq2sohbzopy7o66apu

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import replicate

# Function to send text to REST API and receive image
def call_replicate_fuction(text):
    prompt = text
    replicate_url = "bytedance/sdxl-lightning-4step:727e49a643e999d602a896c774a0658ffefea21465756a6ce24b7ea4165eba6a"
    try:
        # Send request to the REST API
        response = replicate.run(
        replicate_url,
        input={
            "width": 1024,
            "height": 1024,
            "prompt": prompt,
            "scheduler": "K_EULER",
            "num_outputs": 1,
            "guidance_scale": 0,
            "negative_prompt": "worst quality, low quality",
            "num_inference_steps": 4
        })
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing API: {e}")
        return None


# Function to display image from URL
def display_image_from_url(image_url):
    try:
        # Send GET request to fetch image
        response = requests.get(image_url)
        response.raise_for_status()  # Raise exception for any HTTP error

        # Read image from response content
        img = Image.open(BytesIO(response.content))
        st.image(img, caption='Generated Image', use_column_width=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing image from URL: {e}")


# Streamlit UI
st.title("Image Generator")

# Input text field
input_text = st.text_area("Enter text:")
if st.button("Generate Image"):
    if input_text:
        # Call function to get image from API
        #"self-portrait of a man on a ship, huge waves, lightning in the background "
        response = call_replicate_fuction(input_text)
        #st.write(response)
        # Extract image URL from JSON output
        image_url = response[0]
        # st.write(image_url)
        # Display image
        if image_url:
            display_image_from_url(image_url)
        else:
            st.warning("No image URL found in JSON data.")
    else:
        st.warning("Please enter some text.")

