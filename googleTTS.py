import os
import threading
import playsound as playsound
from google.cloud import texttospeech
from gtts import gTTS

# Authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Assets/Authentication/Google Cloud.json'

texttospeechClient = texttospeech.TextToSpeechClient()

def cloudTextToSpeech(text, lang, name, speed):
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang,
        name=name,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed
    )

    response = texttospeechClient.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    if os.path.exists("Assets/audio.mp3"):
        os.remove("Assets/audio.mp3")
    # The response's audio_content is binary.
    with open("Assets/audio.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def textToSpeech(text, lang):
    if os.path.exists("Assets/audio.mp3"):
        os.remove("Assets/audio.mp3")
    gTTS(text=text, lang=lang, slow=False).save("Assets/audio.mp3")

def playSpeech():
    threading.Thread(target=playsound.playsound, args=("Assets/audio.mp3",)).start()

if __name__ == "__main__":
    cloudTextToSpeech('你好，你加什么名字？', "yue-HK", "yue-HK-Standard-B", 0.75)
    playSpeech()