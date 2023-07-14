import os
import base64
import uuid
from flask import Flask, request
from runners.run_e2e import run_e2e

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
    return {
        "words": result
    }


def save_image_from_base64(image_content):
    image_data = base64.b64decode(image_content)
    filename = str(uuid.uuid4()) + '.png'
    image_path = os.path.join(data_directory, filename)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    return image_path
