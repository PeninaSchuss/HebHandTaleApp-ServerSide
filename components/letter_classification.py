import numpy as np
from config import ABC
from keras.models import model_from_json, load_model
from config import MODEL_PATH_ARCHITECTURE, MODEL_PATH_WEIGHTS


def load_model():
    """
    This function loads the saved_model from the disk
    :return: model - the saved_model loaded from the disk
    """
    # Load saved_model architecture from JSON
    with open(MODEL_PATH_ARCHITECTURE, 'r') as json_file:
        loaded_model_json = json_file.read()

    model = model_from_json(loaded_model_json)

    # Load saved_model weights
    model.load_weights(MODEL_PATH_WEIGHTS)

    print("Model loaded successfully.")
    return model


def predict_letters(X):
    """
    This function predicts the letters from images
    :param X: the images to predict
    :return: predicted_letters_word - the predicted letters
    """
    model = load_model()
    probabilities = model.predict(X)
    # Get the index of the highest probability character
    max_class_indices = np.argmax(probabilities, axis=1)
    print(max_class_indices)
    # Get the corresponding Hebrew letter
    predicted_letters = [ABC[i] for i in max_class_indices]
    # Append the predicted letter to the list
    predicted_letters_word = ''.join(predicted_letters)
    return predicted_letters_word
