import streamlit as st
from google import genai # Note the new import
from PIL import Image

# 1. Access Secret
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # 2. Use the new Client protocol (bypasses v1beta automatically)
    client = genai.Client(api_key=api_key)
    
    st.title("🧠 GUET Smart Vision")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file and st.button("Identify"):
        img = Image.open(uploaded_file)
        try:
            # New direct call method
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=img
            )
            st.success("### Analysis:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check if your VPN is set to 'Singapore' or 'USA'.")
else:
    st.error("API Key missing in Streamlit Secrets!")
