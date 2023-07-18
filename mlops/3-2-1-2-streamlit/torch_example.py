import requests
import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import transforms

# 모델 정의
model = torch.hub.load(
    "pytorch/vision",
    "resnet18",
    weights="ResNet18_Weights.DEFAULT"
).eval()
# ImageNet 레이블 다운로드
response = requests.get("https://git.io/JJkYN")
labels = response.text.split("\n")

def predict(image: Image.Image) -> dict[str, float]:
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(model(image)[0], dim=0)
        confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
    return confidences

st.title("Image Classification with ResNet-18")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")

    if st.button("Predict"):
        results = predict(image)
        top_results = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]

        for label, confidence in top_results:
            st.write(f"{label}: {confidence * 100:.2f}%")
