import streamlit as st
from openai import OpenAI
from llama_index.llms.gemini import Gemini
import requests
from PIL import Image
from io import BytesIO

# Initialize the OpenAI and Gemini clients
client = OpenAI(api_key="sk-proj-MeAjSiN9dKRNuD8EgCuuT3BlbkFJpD1MFY3PJuOiHc42FQ1B")

model = Gemini(
    model_name="models/gemini-1.5-flash-latest",
    api_key="AIzaSyDej1alzYxFwPNNd0h08pJAlyKOGeg4zs0",
)

# Set the page configuration
st.set_page_config(layout="wide")

# Title of the app
st.title(
    "🤖📝 BlogBuddy: Your writing companion, here to turn ideas into engaging content"
)
st.subheader(
    "Seamlessly assist with writing, editing, and brainstorming—your ultimate blog support partner."
)

# Sidebar for user inputs
with st.sidebar:
    st.title("Input Your Blog Details")
    st.subheader("Enter your blog details")

    blog_title = st.text_input("Blog Title")
    keywords = st.text_area("Keywords (comma-separated)")
    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=100)
    num_images = st.number_input("Number of images", min_value=1, max_value=5, step=1)

    prompt_parts = [
        f"Generate a comprehensive, engaging blog post relevant to the given title '{blog_title}' and keywords '{keywords}'. The blog should be approximately {num_words} words in length, suitable for an online audience, and readable with different subtitles."
    ]

    submit_button = st.button("Generate Blog")

if submit_button:
    # Generate the blog content
    response = model.complete(prompt_parts[0])

    # Generate an image using Craiyon API
    image_prompt = "a cute cat with a hat on"  # Example prompt for image generation
    try:
        image_res = requests.post(
            "https://api.craiyon.com/generate", json={"prompt": image_prompt}
        )

        # Check if the response is JSON
        image_res.raise_for_status()
        image_data = image_res.json()

        # Debug: print raw response for inspection
        st.write("Raw API response:", image_res.text)

        # Display the generated image
        if image_data and image_data.get("images"):
            image_url = image_data["images"][0]
            image_res = requests.get(image_url)
            image = Image.open(BytesIO(image_res.content))

            st.header(blog_title)
            st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.header(blog_title)
            st.write("Image generation failed: No image data received.")

    except requests.RequestException as e:
        st.write("An error occurred while generating the image:", e)
    except ValueError as e:
        st.write("An error occurred while processing the image response:", e)

    # Display the generated blog content
    st.markdown(response)
