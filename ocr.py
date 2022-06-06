import io
import os
from PIL import Image, ImageGrab
from google.cloud import vision

# Authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'auth.json'

# Instantiates the client
client = vision.ImageAnnotatorClient()


def parseImage(dir):
    # Load image into memory
    with open(dir, "rb") as img:
        content = img.read()
    image = vision.Image(content=content)

    # OCR detection
    response = client.text_detection(image=image)
    texts = response.text_annotations
    texts = texts[0].description

    # Do stuff with the text
    return texts