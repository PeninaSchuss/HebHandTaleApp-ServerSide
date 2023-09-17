import os
import numpy as np

from config import DATA_DIR
from components.segmentation import process_image
from components.letter_classification import predict_letters
from components.word_correction import get_word_suggestions

IMAGE_NAME_WORD = 'חמאה.png'


def run_e2e(image_path, top_k=10):
    characters = process_image(image_path)
    predicted_word = predict_letters(np.array(characters))
    print(predicted_word)
    word_suggestions = get_word_suggestions(predicted_word, top_k)
    print(word_suggestions)
    return [predicted_word] + word_suggestions


if __name__ == "__main__":
    input_image_name = IMAGE_NAME_WORD  # Choose here
    input_image_fullpath = os.path.join(DATA_DIR, input_image_name)
    print(f'Predict word... {input_image_fullpath}')
    run_e2e(input_image_fullpath)
