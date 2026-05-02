import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SET UP THE BRAIN ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Key is missing! Go to Streamlit Settings -> Secrets.")
    st.stop()

# Initialize the model simply
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. USER INTERFACE ---
st.set_page_config(page_title="GUET Smart Vision", page_icon="🧠")
st.title("🧠 GUET Smart Vision")
st.write("Upload an image and the AI will describe it perfectly.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    if st.button("Analyze Image"):
        with st.spinner("Thinking..."):
            try:
                # We send the prompt and image directly
                response = model.generate_content(["Tell me exactly what is in this photo.", img])
                st.success("### AI Analysis:")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
