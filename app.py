import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. Setup
api_key = st.secrets.get("GOOGLE_API_KEY")

def analyze_image(image_bytes, api_key):
    # This URL forces the stable v1 version and bypasses the library 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Convert image to base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": "What is in this image? Describe it briefly."},
                {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
            ]
        }]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

st.title("🧠 GUET Smart Vision (Direct Mode)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img)
    
    if st.button("Identify Now"):
        # Convert PIL image to bytes
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        with st.spinner("Talking directly to Google..."):
            result = analyze_image(byte_im, api_key)
            
            if "candidates" in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                st.success(text)
            else:
                st.error(f"Server Response: {result}")
