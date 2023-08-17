import os
from flask import Flask, request, jsonify
from playsound import playsound
from api_utils.word_img_decode import save_image_from_base64
from dbs.db_history import add_history_to_db, get_history
from dbs.db_popular_word import add_word_to_db
from runners.run_e2e import run_e2e
from api_utils.google_translate_api import translate_word
from config import DIR_PATH  # Import the DATABASE_PATH from your config
import requests

app = Flask(__name__)
# Define the API URL
edenai_url = "https://api.edenai.run/v2/audio/text_to_speech"

# Define the request headers including the authorization token
edenai_headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTM0ZGNhZDQtYmU4NS00YWQ4LTkzY2ItZmUyYTgwYzY2ZDY2IiwidHlwZSI6ImFwaV90b2tlbiJ9.QdMoXDg6S_a7YqwrrL21R7QqyrpVAZEt2iNxO1m7rbU",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@app.route('/recognize_word_by_name/<image_name>')
def recognize_word_by_name(image_name):
    # Get the path to the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the data directory
    data_directory = os.path.join(current_directory, '../data')
    print("Image_name:", image_name)
    input_image_path = os.path.join(data_directory, image_name + ".png")
    result = run_e2e(input_image_path)
    return {
        "words": result
    }


@app.route('/recognize_word_by_content', methods=['POST'])
def recognize_word_by_content():
    image_content = request.data
    image_path = save_image_from_base64(image_content)
    result = run_e2e(image_path)
    if os.path.exists(image_path):
        os.remove(image_path)
    return {
        "words": result
    }


@app.route('/get_history_by_user/<user_token>')
def get_history_by_user(user_token):
    history_list = get_history(user_token)
    return jsonify({"history": history_list})


@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>/<language_name>',
           defaults={'user': None})
@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>/<language_name>/<user>')
def translate_word_route(word_to_translate, target_language, language_name, user=None):
    translation = translate_word(word_to_translate, target_language)

    if translation:
        # EdenAI API request for audio generation
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
            "text": translation,
            "option": "FEMALE"
        }

        edenai_response = requests.post(edenai_url, headers=edenai_headers, json=edenai_payload, verify=False)

        if edenai_response.status_code == 200:
            audio_data = edenai_response.json()
            audio_url = audio_data.get("audio_resource_url")

            if audio_url:
                playsound(audio_url)

    if user is not None:
        add_history_to_db(user, language_name, word_to_translate, translation)

    response_data = {
        "translation": translation,
        "audio_url": audio_url if audio_url else ""
    }

    return jsonify(response_data)


@app.route('/add_word_to_popular_words_db/<word_to_add>', methods=['GET'])
def add_word_to_popular_words_db(word_to_add):
    return add_word_to_db(word_to_add)
