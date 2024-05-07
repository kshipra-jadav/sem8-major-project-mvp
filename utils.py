import os
import io
import base64
import threading

import cv2
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OS_BASE_PATH = r"D:\SEM 8\to_pi\openai stuff\audio"  # CHANGE THIS

client = OpenAI()


def setup_camera():
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    return cap


def play_audio(filename=None, bytes=None, bg=True):
    if filename:
        print(f"Loading {filename}")

        audio = AudioSegment.from_file(os.path.join(OS_BASE_PATH, filename))

        print(f"Playing {filename}")

        if not bg:
            play(audio)
        else:
            t = threading.Thread(target=play, args=(audio, ))
            t.start()

    if bytes:
        print(f"Loading audio from bytes ...")

        audio = AudioSegment.from_file(io.BytesIO(bytes), type="mp3")

        print(f"Playing audio ...")

        t = threading.Thread(target=play, args=(audio, ))
        t.start()


def performSTT(wav_audio):
    audio_bytes = io.BytesIO(wav_audio)
    audio_bytes.name = "myfile.wav"

    text = client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        response_format="text",
        file=audio_bytes
    )

    return text


def performVision(img_b64, prompt):
    messages = [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_b64}"
                }
            }
        ]
    }]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=300,
        n=1

    )

    return response.choices[0].message.content


def performTTS(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
        response_format="mp3",
    )

    return response


def sceneDetection(frame, text):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".jpg", frame)
    img_b64 = base64.b64encode(buffer).decode('utf-8')

    model_response = performVision(img_b64, text)

    return model_response
