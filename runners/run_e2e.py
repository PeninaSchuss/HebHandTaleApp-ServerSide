import os
import numpy as np

from config import IMAGES_DIR
from components.segmentation import process_image
from components.letter_classification import predict_letters
from components.word_correction import get_word_suggestions


IMAGE_NAME_WORD_CALL  = 'call.png'
IMAGE_NAME_WORD_HELLO = 'hello.png'


def run_e2e(image_path):
    characters = process_image(image_path)
    predicted_word = predict_letters(np.array(characters))
    print(predicted_word)
    word_suggestions = get_word_suggestions(predicted_word)
    print(word_suggestions)


input_image_name = IMAGE_NAME_WORD_HELLO  # Choose here
input_image_fullpath = os.path.join(IMAGES_DIR, input_image_name)
print(f'Predict word... {input_image_fullpath}')
run_e2e(input_image_fullpath)
