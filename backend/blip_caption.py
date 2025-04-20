import os
import requests
import base64
from PIL import Image

def generate_caption(image_path: str) -> str:
    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        raise EnvironmentError("Missing Hugging Face token")

    # Read and encode image
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        b64_image = base64.b64encode(img_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": b64_image
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get caption: {response.text}")

    result = response.json()
    return result[0]["generated_text"]
