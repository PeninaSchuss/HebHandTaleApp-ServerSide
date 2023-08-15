import os
from flask import Flask, request, jsonify

from api_utils.word_img_decode import save_image_from_base64
from dbs.db_history import add_history_to_db, get_history
from dbs.db_popular_word import add_word_to_db
from runners.run_e2e import run_e2e
from api_utils.google_translate_api import translate_word
from config import DIR_PATH  # Import the DATABASE_PATH from your config

app = Flask(__name__)


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


@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>/<language_name>/<user>')
def translate_word_route(word_to_translate, target_language, language_name, user):
    translation = translate_word(word_to_translate, target_language)
    add_history_to_db(user, language_name, word_to_translate, translation)
    return translation


@app.route('/add_word_to_popular_words_db/<word_to_add>', methods=['GET'])
def add_word_to_popular_words_db(word_to_add):
    return add_word_to_db(word_to_add)
