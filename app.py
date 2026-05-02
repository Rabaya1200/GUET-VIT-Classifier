import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API Key from Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Key is missing in Streamlit Secrets!")
    st.stop()

# 2. Configure Gemini
genai.configure(api_key=api_key)

# 3. Simple UI
st.title("🧠 GUET Smart Vision")
st.write("I will describe your image with human-level detail.")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    if st.button("Analyze Now"):
        with st.spinner("Analyzing..."):
            try:
                # We use the most basic call possible
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(img)
                
                st.success("### Analysis:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Try checking if your API Key is active at aistudio.google.com")
