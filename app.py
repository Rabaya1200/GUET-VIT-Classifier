import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- STEP 1: CONFIGURATION ---
# In a real project, use st.secrets for the API Key
GOOGLE_API_KEY = "AIzaSyBbWtBZcmePuNHBa8OjBgjroCfR9mAzjbo" 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- STEP 2: UI DESIGN ---
st.set_page_config(page_title="Multimodal AI", page_icon="🧠")
st.title("🧠 Human-Level Image Understanding")
st.write("This app uses a Multimodal LLM to describe images with context.")

uploaded_file = st.file_uploader("Upload any image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Image", use_container_width=True)
    
    # Let the user ask a specific question or use a default prompt
    user_query = st.text_input("What do you want to know about this image?", 
                               "Identify this object and describe its cultural context.")
    
    if st.button("Analyze Image"):
        with st.spinner('Thinking like a human...'):
            # Gemini takes the image and the text together
            response = model.generate_content([user_query, img])
            
            st.subheader("AI Analysis:")
            st.write(response.text)

