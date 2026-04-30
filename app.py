import streamlit as st
import torch
import timm
from PIL import Image
import requests
from torchvision import transforms


# --- STEP 1: LOAD THE BRAIN ---
@st.cache_resource
def load_vit_model():
    model = timm.create_model('vit_tiny_patch16_224', pretrained=True)
    model.eval()
    config = timm.data.resolve_model_data_config(model)
    transform = timm.data.create_transform(**config, is_training=False)
    labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    labels = requests.get(labels_url).text.splitlines()
    return model, transform, labels


model, transform, labels = load_vit_model()

# --- STEP 2: UI DESIGN ---
st.set_page_config(page_title="GUET AI Lens", layout="centered")
st.title("🛡️ Vision Transformer (ViT) Smart Lens")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption="Input Image", use_container_width=True)

    if st.button("Run AI Inference"):
        with st.spinner('Transformer is analyzing patches...'):
            input_tensor = transform(img).unsqueeze(0)
            with torch.no_grad():
                output = model(input_tensor)

            # Get Top 3 Predictions
            probs = torch.nn.functional.softmax(output[0], dim=0)
            top_probs, top_idxs = torch.topk(probs, 3)

            # --- DISPLAY SECTION ---
            st.success(f"### Primary Result: {labels[top_idxs[0]].title()}")

            st.write("---")
            st.subheader("📊 Prediction Details")
            for i in range(3):
                label = labels[top_idxs[i]].replace('_', ' ').title()
                score = top_probs[i].item()
                st.write(f"**{label}**")
                st.progress(score)
                st.caption(f"Confidence: {score * 100:.2f}%")

            st.write("---")
            st.subheader("💡 AI Description")
            main_label = labels[top_idxs[0]].lower()
            st.write(f"The Vision Transformer (ViT) identified this object as a **{main_label}**.")
            st.info(
                "Technical Explanation: Unlike a standard camera, this AI breaks your photo into 196 small patches. It uses 'Self-Attention' to understand how the textures in one part of the image relate to the shapes in another.")




