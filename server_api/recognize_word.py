import os
import base64
import sqlite3
import uuid
from flask import Flask, request, jsonify
from runners.run_e2e import run_e2e
from translate_api.google_translate_api import translate_word
from config import dir_path  # Import the DATABASE_PATH from your config

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


@app.route('/get_history_by_user/<user_token>')
def get_history_by_user(user_token):
    database_filename = "history.db"
    database_path = os.path.join(dir_path, "dbs", database_filename)

    connection = connect_to_db(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM translations WHERE user = ?
    ''', (user_token,))

    rows = cursor.fetchall()
    connection.close()

    history_list = []
    for row in rows:
        history_list.append({
            "id": row[0],
            "user": row[1],
            "language": row[2],
            "word": row[3],
            "translation": row[4]
        })

    return jsonify({"history": history_list})


@app.route('/translate_word_with_google_api/<word_to_translate>/<target_language>/<language_name>/<user>')
def translate_word_route(word_to_translate, target_language, language_name, user):
    database_filename = "history.db"
    database_path = os.path.join(dir_path, "dbs", database_filename)

    translation = translate_word(word_to_translate, target_language)

    connection = connect_to_db(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO translations (user, language, word, translation)
        VALUES (?, ?, ?, ?)
    ''', (user, language_name, word_to_translate, translation))

    connection.commit()
    connection.close()

    return translation


# Connect to the database
def connect_to_db(database_path):
    connection = sqlite3.connect(database_path)
    return connection


@app.route('/add_word_to_popular_words_db/<word_to_add>', methods=['GET'])
def add_word_to_popular_words_db(word_to_add):
    database_filename = "popular_words.db"  # Replace with your database file
    database_path = os.path.join(dir_path, "dbs", database_filename)

    try:
        connection = connect_to_db(database_path)
        cursor = connection.cursor()

        # Check if the word already exists in the table
        select_query = '''
        SELECT data_string FROM popular_words WHERE data_string = ?;
        '''
        cursor.execute(select_query, (word_to_add,))
        existing_word = cursor.fetchone()

        if existing_word:
            return jsonify({"message": f"Word '{word_to_add}' already exists in popular_words.db"}), 200  # OK

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
