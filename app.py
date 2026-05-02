import streamlit as st
from google import genai  # Ensure this matches your requirements.txt
from PIL import Image

# 1. Fetch Key
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # 2. FORCE THE STABLE v1 VERSION
    # This is the critical change to stop the v1beta 404 error
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    
    st.title("🧠 GUET Smart Vision")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file and st.button("Identify"):
        img = Image.open(uploaded_file)
        try:
            # 3. Use the most stable model alias
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=img
            )
            st.success("### Analysis Result:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check if your VPN is set to 'Singapore' or 'USA'.")
else:
    st.error("API Key missing in Streamlit Secrets!")
