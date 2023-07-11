import os
from flask import Flask

from runners.run_e2e import run_e2e


app = Flask(__name__)


@app.route('/recognize_word_by_name/<image_name>')
def recognize_word(image_name):
    print("Image_name:", image_name)
    input_image_dir = "/Users/stav/Projects/CodeSH/HandwritingProject/data"
    input_image_path = os.path.join(input_image_dir, image_name + ".png")
    result = run_e2e(input_image_path)
    return {
        "words": result
    }


@app.route('/recognize_word_by_content/<image_content>')
def recognize_word(image_content):
    decode_image = None
    image_path = decode_image(image_content) #TODO: implement
    result = run_e2e(image_path)
    return {
        "words": result
    }

