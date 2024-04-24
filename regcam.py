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

OS_BASE_PATH = "/home/gsfc-pi/Desktop/final_codes/"


SD_BTN = 18 # purple orange blue
OCR_BTN = 23 # yellow green blue

GPIO.setmode(GPIO.BCM)
GPIO.setup(SD_BTN, GPIO.IN)
GPIO.setup(OCR_BTN, GPIO.IN)


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


def setup_camera():
    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    return cap


TIMES_EXEC = 0
while True:
    if TIMES_EXEC == 0:
        play_file("greeting.mp3")
        TIMES_EXEC += 1
        
    if GPIO.input(SD_BTN):
        cap = setup_camera()
        
        for i in range(10): 
            _, frame = cap.read()
            
        _, frame = cap.read()
        
        text = speech_to_text()
            
        if text == 1:
            text_to_speech("Sorry. Couldn't understand you. Please take an image again and try again")
            cap.release()
            
            continue
    
        print(text)
    
        getLLMResponse(frame, text)
        
        cap.release()
        
    if GPIO.input(OCR_BTN):
        cap = setup_camera()
        
        for i in range(10): 
            _, frame = cap.read()
            
        _, frame = cap.read()
        
        text = image_ocr(frame)
        
        text_to_speech(f"The text reads - {text}")
        
        cap.release()
        

    
        
