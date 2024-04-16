import cv2
import time
import google.generativeai as genai
from PIL import Image
import PIL.PngImagePlugin
from tts import text_to_speech
import RPi.GPIO as GPIO

TOUCH_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN)

genai.configure(api_key="AIzaSyDXCmwp6bBeP1ztyK3EKF5BjnsYIx1Tpsg")

model = genai.GenerativeModel("gemini-pro-vision")

cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

cv2.namedWindow("Window")
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


while True:
    start = time.perf_counter()
    _, frame = cap.read()
    
    cv2.imshow("Window", cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))
    
    fps = f"{1 / (time.perf_counter() - start):.2f} FPS"
    
    #print(fps)
    
    if GPIO.input(TOUCH_PIN):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        prompt = "Please tell me about the contents of this image and tell me exactly what is written inside the image"
        ocr_prompt = "Perform OCR on the given image. Do not summarize the content. Give back to me text as you have detected it."
        response = model.generate_content([prompt, img], stream=True)
        response.resolve()
        
        print(response.text)
        text_to_speech(response.text)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
        
cap.release()
