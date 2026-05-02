import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Fetch Key
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # 2. Configure with a stable transport layer
    genai.configure(api_key=api_key, transport='rest')
    
    # 3. Use the LATEST stable model name
    # We use 'gemini-1.5-flash' but force the API to version v1
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    
    st.title("🧠 GUET Smart Vision")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file and st.button("Identify"):
        img = Image.open(uploaded_file)
        try:
            # Add a small text prompt to help the AI understand its job
            response = model.generate_content(["What is this? Describe it in detail.", img])
            st.success("### AI Result:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
