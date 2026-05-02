import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION ---
# This looks for the name "GOOGLE_API_KEY" in your Streamlit Secrets dashboard
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please add it to your Streamlit Secrets tab.")
    st.stop()

# Configure the Google AI library
genai.configure(api_key=api_key)

# --- 2. MODEL SETUP ---
# Using the 'models/' prefix forces the app to the stable API version
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- 3. USER INTERFACE ---
st.set_page_config(page_title="GUET Smart Vision", page_icon="🧠")
st.title("🧠 GUET Smart Vision")
st.write("Upload a photo, and I will describe it with human-level intelligence.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open and display the image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    if st.button("Analyze Image"):
        with st.spinner("The AI is thinking..."):
            try:
                # Send the image to Gemini
                response = model.generate_content(img)
                
                st.success("### AI Analysis Result:")
                st.write(response.text)
                
            except Exception as e:
                # If the 404 persists, this captures the detailed technical reason
                st.error(f"An error occurred: {e}")
                st.info("Technical Tip: Double-check that your API Key is copied correctly from Google AI Studio.")
            
