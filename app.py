import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SET UP THE BRAIN ---
# This looks for the secret key you saved in the Streamlit dashboard
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key or "AIza" not in api_key:
    st.error("🚨 API Key is missing or invalid!")
    st.info("Go to your Streamlit App Settings -> Secrets and paste your key there.")
    st.stop()

# Initialize the Google AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"request_options": {"api_version": "v1"}}
)

# --- 2. USER INTERFACE ---
st.set_page_config(page_title="GUET Smart Vision", page_icon="🤖")
st.title("🛡️ GUET Smart Vision AI")
st.write("This AI understands images like a human. Upload your photo to see.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the image you uploaded
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    # Analyze button
    if st.button("Analyze Image"):
        with st.spinner("Thinking..."):
            try:
                # We send the image + a specific prompt to the AI
                prompt = "Identify everything in this image. If it is food, describe what it is and its cultural context."
                response = model.generate_content([prompt, img])
                
                st.success("### AI Analysis:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Check if your API key is active at aistudio.google.com")
