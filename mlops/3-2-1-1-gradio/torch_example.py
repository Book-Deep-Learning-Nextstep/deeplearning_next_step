import gradio as gr
import numpy as np
import requests
import torch
import torchvision.transforms as transforms
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

def predict(image: np.ndarray) -> dict[str, float]:
    image = transforms.ToTensor()(image).unsqueeze(0)
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(model(image)[0], dim=0)
        confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
    return confidences

# 입력 & 결과 형식 정의
input_type = gr.components.Image()
output_type = gr.components.Label()

# 인터페이스 정의 및 실행
interface = gr.Interface(fn=predict, inputs=input_type, outputs=output_type)
interface.launch()
