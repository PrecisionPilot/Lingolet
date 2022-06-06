import io
import os
from google.cloud import vision

# Authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'auth.json'

# Instantiates the client
client = vision.ImageAnnotatorClient()


# Load image into memory
imageDir = "Sample Text.png"
with open(imageDir, "rb") as img:
    content = img.read()
image = vision.Image(content=content)

# OCR detection
response = client.text_detection(image=image)
texts = response.text_annotations

print(texts)