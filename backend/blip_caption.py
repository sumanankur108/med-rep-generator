from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from huggingface_hub import snapshot_download

# Download the model snapshot (only once)
model_path = snapshot_download("Salesforce/blip-image-captioning-base")

# Load processor and model from the downloaded snapshot
processor = BlipProcessor.from_pretrained(model_path)
model = BlipForConditionalGeneration.from_pretrained(model_path)

def generate_caption(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
