import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from huggingface_hub import snapshot_download

# Load token securely from environment variable
hf_token = os.getenv("HF_TOKEN")

# Download the model snapshot using token
model_path = snapshot_download("Salesforce/blip-image-captioning-base", token=hf_token)

# Load processor and model from the downloaded snapshot
processor = BlipProcessor.from_pretrained(model_path)
model = BlipForConditionalGeneration.from_pretrained(model_path)

def generate_caption(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
