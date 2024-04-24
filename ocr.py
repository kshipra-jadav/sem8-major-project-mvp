import io

from google.cloud import vision
import cv2

client = vision.ImageAnnotatorClient()

def image_ocr(frame):
    image_bytes = cv2.imencode(".jpg", frame)[1].tobytes()
    
    image = vision.Image(content=image_bytes)
    
    response = client.text_detection(image=image)
    
    texts = response.text_annotations
    
    final_str = ""
    
    for text in texts:
        print(f"text {text}")
        final_str += text.description + " "
            
    print(final_str)
    
    return final_str

if __name__ == '__main__':
    img = cv2.imread('img.jpg')
    image_ocr(img)