import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Secure Setup
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # --- THE CRITICAL "MAP" FIX ---
    # This forces the library to use 'v1' instead of 'v1beta'
    os.environ["GOOGLE_API_VERSION"] = "v1" 
    
    genai.configure(api_key=api_key, transport='rest')
    
    # 2. Use the stable model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🧠 GUET Smart Vision")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file and st.button("Identify"):
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        with st.spinner("Talking to Google v1 Servers..."):
            try:
                # Direct call to the model
                response = model.generate_content(img)
                st.success("### AI Analysis:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Deployment Error: {e}")
                st.info("If 404 persists, try switching VPN to Singapore or USA-GPT nodes.")
else:
    st.error("API Key not found! Go to Settings -> Secrets.")
