import os
import threading
import playsound as playsound
from google.cloud import texttospeech

# Authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Assets/Authentication/Google Cloud.json'

texttospeechClient = texttospeech.TextToSpeechClient()

def textToSpeech(text):
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = texttospeechClient.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("audio.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    
    threading.Thread(target=playsound.playsound, args=("audio.mp3",)).start()
    

textToSpeech('什么鬼')