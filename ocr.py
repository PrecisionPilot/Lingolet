import os
from PIL import Image, ImageGrab
from internetConnection import isConnected
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
    try:
        response = client.text_detection(image=image)
        texts = response.text_annotations
        texts = texts[0].description
        
        return texts
    except:
        # check if it's connected to the internet
        if not isConnected():
            print("Error: Not connected to the internet")
        else:
            print("Something with the image recognition went wrong")
            print("Make sure selected image contains text")
        
        return None