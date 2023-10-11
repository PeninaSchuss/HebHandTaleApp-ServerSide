import os
from flask import Flask, request, jsonify
from api_utils.edenAi_api import generate_and_play_audio
from api_utils.word_img_decode import save_image_from_base64
from dbs.db_history import add_history_to_db, get_history
from dbs.db_popular_word import add_word_to_db
from runners.run_e2e import run_e2e
from api_utils.google_translate_api import translate_word

app = Flask(__name__)


@app.route('/recognize_word_by_content', methods=['POST'])
def recognize_word_by_content():
    """
    This function receives an image in base64 format and returns the predicted word and the word suggestions for it
    :return: a json with the predicted word and the word suggestions for it
    """
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
    """
    This function receives a user token and returns the history of the user
    :param user_token: the user token
    :return: a json with the history of the user
    """
    history_list = get_history(user_token)
    return jsonify({"history": history_list})


@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>/<language_name>',
           defaults={'user': None})
@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>/<language_name>/<user>')
def translate_word_route(word_to_translate, target_language, language_name, user=None):
    """
    This function receives a word to translate, a target language and a language name and returns the translation
    :param word_to_translate: the word to translate
    :param target_language: the target language code for google api
    :param language_name: the language name
    :param user: the user token (optional)
    :return: a json with the translation
    """
    translation = translate_word(word_to_translate, target_language)
    audio_url = ""

    if translation:
        audio_url = generate_and_play_audio(translation, target_language)

    if user is not None:
        add_history_to_db(user, language_name, word_to_translate, translation)

    response_data = {
        "translation": translation,
        "audio_url": audio_url
    }

    return jsonify(response_data)


@app.route('/add_word_to_popular_words_db/<word_to_add>', methods=['GET'])
def add_word_to_popular_words_db(word_to_add):
    """
    This function receives a word to add to the popular words db
    :param word_to_add: the word to add
    :return: a json with the result of the addition to the db (True/False)
    """
    return add_word_to_db(word_to_add)
