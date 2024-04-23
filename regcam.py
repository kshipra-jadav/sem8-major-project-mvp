import os
import time

from tts import text_to_speech
from mic import speech_to_text
from ocr import image_ocr

import google.generativeai as genai
from PIL import Image
import PIL.PngImagePlugin
import RPi.GPIO as GPIO
from pydub import AudioSegment
from pydub.playback import play
import cv2


SCENE_DETECTION = True


OS_BASE_PATH = "/home/gsfc-pi/Desktop/final_codes/"


TOUCH_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN)


genai.configure(api_key="AIzaSyDXCmwp6bBeP1ztyK3EKF5BjnsYIx1Tpsg")

model = genai.GenerativeModel("gemini-pro-vision")



def play_file(filename):
    print(f"Loading {filename}")
    audio = AudioSegment.from_file(os.path.join(OS_BASE_PATH, filename), "mp3")
    
    print(f"Playing {filename}")
    play(audio)


def getLLMResponse(frame, prompt):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
         
    play_file("processing.mp3")
    
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    
    print(response.text)
    
    text_to_speech(response.text)


TIMES_EXEC = 0
while True:
    if TIMES_EXEC == 0:
        play_file("greeting.mp3")
        TIMES_EXEC += 1
        
    if GPIO.input(TOUCH_PIN):
        cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)


        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        for i in range(10): 
            _, frame = cap.read()
            
        _, frame = cap.read()
        
        if SCENE_DETECTION:                         
            text = speech_to_text()
        
            print(text)
        
            getLLMResponse(frame, text)
            
        else:
            image_ocr(frame)
        
        cap.release()
        

    
        
