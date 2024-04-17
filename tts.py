from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
import io

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="en-IN", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3)

def text_to_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)


    raw_audio = response.audio_content

    audio = AudioSegment.from_file(io.BytesIO(raw_audio), format="mp3")
    play(audio)
    
if __name__ == '__main__':
    text_to_speech("hello guys this is testing lmao")
