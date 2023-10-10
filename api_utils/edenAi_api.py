import requests
edenai_url = "https://api.edenai.run/v2/audio/text_to_speech"

# Define the request headers including the authorization token
edenai_headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTM0ZGNhZDQtYmU4NS00YWQ4LTkzY2ItZmUyYTgwYzY2ZDY2IiwidHlwZSI6ImFwaV90b2tlbiJ9.QdMoXDg6S_a7YqwrrL21R7QqyrpVAZEt2iNxO1m7rbU",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def generate_and_play_audio(text, target_language):
    edenai_payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "rate": 0,
        "pitch": 0,
        "volume": 10,
        "sampling_rate": 0,
        "providers": "microsoft,lovoai,google,ibm,amazon",
        "language": target_language,
        "text": text,
        "option": "MALE"
    }

    edenai_response = requests.post(edenai_url, headers=edenai_headers, json=edenai_payload, verify=False)

    if edenai_response.status_code == 200:
        audio_data = edenai_response.json()
        microsoft_data = audio_data.get("microsoft")
        if microsoft_data:
            audio_url = microsoft_data.get("audio_resource_url")
            print("audio_url: ", audio_url)
    else:
        audio_url = None

    return audio_url if audio_url else ""



