import os
import base64
import sqlite3
import uuid
from flask import Flask, request, jsonify
from runners.run_e2e import run_e2e
from translate_api.google_translate_api import translate_word
from config import DATABASE_PATH  # Import the DATABASE_PATH from your config

app = Flask(__name__)

# Get the path to the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the data directory
data_directory = os.path.join(current_directory, '../data')


@app.route('/recognize_word_by_name/<image_name>')
def recognize_word_by_name(image_name):
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


@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>')
def translate_word_route(word_to_translate, target_language):
    translation = translate_word(word_to_translate, target_language)

    # Return the translation or an error message
    return translation


# Connect to the database
def connect_to_db():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


@app.route('/add_word_to_popular_words_db/<word_to_add>', methods=['GET'])
def add_word_to_popular_words_db(word_to_add):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Insert the word into the table
        insert_query = '''
        INSERT INTO popular_words (data_string)
        VALUES (?);
        '''
        cursor.execute(insert_query, (word_to_add,))
        connection.commit()

        return jsonify({"message": f"Word '{word_to_add}' added to popular_words.db"}), 201  # Created

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

    finally:
        connection.close()


def save_image_from_base64(image_content):
    image_data = base64.b64decode(image_content)
    filename = str(uuid.uuid4()) + '.png'
    image_path = os.path.join(data_directory, filename)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    return image_path
