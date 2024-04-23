import io

from google.cloud import vision
import cv2

client = vision.ImageAnnotatorClient()

def image_ocr(frame):
    image_bytes = cv2.imencode(".jpg", frame)[1].tobytes()
    
    image = vision.Image(content=image_bytes)
    
    response = client.text_detection(image=image)
    
    texts = response.text_annotations
    
    print(texts)