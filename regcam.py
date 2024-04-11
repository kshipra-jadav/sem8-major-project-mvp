import cv2
import time
import google.generativeai as genai
from PIL import Image
import PIL.PngImagePlugin

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-pro-vision")

cap = cv2.VideoCapture("/dev/video0")

cv2.namedWindow("Window")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)





while cap.isOpened():
    start = time.perf_counter()
    _, frame = cap.read()
    
    cv2.imshow("Window", cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))
    
    fps = f"{1 / (time.perf_counter() - start):.2f} FPS"
    
    #print(fps)
    
    key = cv2.waitKey(25)
    
    if key == 27:
        cv2.destroyAllWindows()
        break
    elif key == -1:
        continue
    
    elif key == 32:
        print('capturing image and sending to Gemini')
        img = Image.fromarray(frame)
        prompt = "Please tell me about the contents of this image and tell me exactly what is written inside the image"
        
        response = model.generate_content([prompt, img], stream=True)
        response.resolve()
        
        print(response.text)
cap.release()
