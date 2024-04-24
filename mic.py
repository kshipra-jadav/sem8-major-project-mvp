import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io

rec = sr.Recognizer()

def capture_audio():
    with sr.Microphone() as source:
        print("adjusting for ambient noise ...")
        
        rec.adjust_for_ambient_noise(source, duration=1)
        
        print("starting recording ... ")
        audio_data = rec.listen(source)
        
        return audio_data

def speech_to_text():
    audio = capture_audio()
    
    print("recognizing text ...")
    
    try:
    
        text = rec.recognize_google(audio)
    
        return text
    
    except sr.UnknownValueError:
        return 1
    
    except sr.RequestError:
        return 1

if __name__ == "__main__":
    speech_to_text()
    
    
    
    
