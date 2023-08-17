import requests
from gtts import gTTS
import os

# Replace with your API keys
translation_api_key = "AIzaSyCWyf75O4tu-99gTJb-q3QYKWs6Qqa8Vfo"
tts_api_key = "AIzaSyC8HYAXg_-HC3kyhqpy-rflZFiNf3CH3pg"


def translate_text(text, target_language):
    base_url = "https://translation.googleapis.com/language/translate/v2"

    params = {
        "q": text,
        "target": target_language,
        "format": "text",
        "key": translation_api_key,
    }

    response = requests.get(base_url, params=params, verify=False)
    data = response.json()

    translated_text = data["data"]["translations"][0]["translatedText"]
    return translated_text


def play_audio(translated_text, target_language):
    tts = gTTS(translated_text, lang=target_language)
    tts.save("translated_audio.mp3")

    os.system("start translated_audio.mp3")


def get_tts_audio(text, tts_api_key, target_language):
    base_url = "https://texttospeech.googleapis.com/v1/text:synthesize"

    data = {
        "input": {"text": text},
        "voice": {"languageCode": target_language, "ssmlGender": "FEMALE"},
        "audioConfig": {"audioEncoding": "MP3"},
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tts_api_key}",
    }

    response = requests.post(base_url, json=data, headers=headers, verify=False)
    audio_data = response.content

    with open("translated_audio.mp3", "wb") as audio_file:
        audio_file.write(audio_data)


# Example usage
word = "hello"
target_language = "fr"  # Target language code (e.g., "fr" for French)

translated_text = translate_text(word, target_language)
print("Translation:", translated_text)

get_tts_audio(translated_text, tts_api_key, target_language)
play_audio(translated_text, target_language)
