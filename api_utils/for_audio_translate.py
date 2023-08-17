import requests
import pygame

# Define the API URL
url = "https://api.edenai.run/v2/audio/text_to_speech"

# Define the request headers including the authorization token
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTM0ZGNhZDQtYmU4NS00YWQ4LTkzY2ItZmUyYTgwYzY2ZDY2IiwidHlwZSI6ImFwaV90b2tlbiJ9.QdMoXDg6S_a7YqwrrL21R7QqyrpVAZEt2iNxO1m7rbU",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Define the request payload (body)
payload = {
    "response_as_dict": True,
    "attributes_as_list": False,
    "show_original_response": False,
    "rate": 0,
    "pitch": 0,
    "volume": 10,
    "sampling_rate": 0,
    "providers": "microsoft,lovoai,google,ibm,amazon",
    "language": "fr",
    "text": "Bonjour Je m'appelle Jane",
    "option": "FEMALE"
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Extract and use the audio URL for playback, assuming it's present in the response
if response.status_code == 200:
    audio_data = response.json()  # Assuming the response is in JSON format
    audio_url = audio_data.get("url")
    if audio_url:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_url)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
else:
    print("API request failed:", response.status_code, response.text)