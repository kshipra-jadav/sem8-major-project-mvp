# Speech to text
import io
import speech_recognition as sr

from utils import play_audio, performSTT


rec = sr.Recognizer()


def speech_to_text():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise ...")

        rec.adjust_for_ambient_noise(source, duration=1)

        print("Starting To Record ... ")

        play_audio("beep.mp3", bg=False)

        wav_audio = rec.listen(source).get_wav_data()

        text = performSTT(wav_audio)

        return text
