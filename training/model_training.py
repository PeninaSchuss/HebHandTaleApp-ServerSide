import os

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import Sequential
from keras.applications.vgg19 import VGG19
from keras.layers import Dense, Flatten
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm
from config import DATA_DIR_TRAIN

INPUT_IMAGE_SIZE = (32, 32, 3)
SEED = 42
EPOCHS = 5


def image_files(input_directory):
    """
    This function returns the filepaths and labels of the images in the input directory
    :param input_directory: the directory to search for images
    :return: filepaths, labels - lists of the filepaths and labels of the images
    """
    filepaths = []
    labels = []

    digit_folders = os.listdir(input_directory)

    for digit in digit_folders:
        path = os.path.join(input_directory, digit)
        flist = os.listdir(path)
        for f in flist:
            fpath = os.path.join(path, f)
            filepaths.append(fpath)
            labels.append(digit)
    return filepaths, labels


def load_images(filepaths):
    """
    This function loads the images from the filepaths and returns them as a numpy array
    :param filepaths: the filepaths of the images
    :return: images - a numpy array of the images
    """
    images = []
    for i in tqdm(range(len(filepaths))):
        img = load_img(filepaths[i], target_size=INPUT_IMAGE_SIZE, grayscale=False)
        img = img_to_array(img)
        img.astype('float32')
        img = img / 255
        images.append(img)

    images = np.array(images)
    return images


def load_vgg_model():
    """
    This function loads the VGG19 model and adds a dense layer on top of it
    :return: model - the model with the dense layer on top of it
    """
    vgg19 = VGG19(
        weights='imagenet',
        include_top=False,
        input_shape=INPUT_IMAGE_SIZE
    )
    model = Sequential()
    model.add(vgg19)
    model.add(Flatten())
    model.add(Dense(28, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])
    return model


def train_model(model):
    """
    This function trains the model and returns the history of the training
    :param model: the model to train
    :return: history - the history of the training
    """
    # load the paths and labels in different variables
    filepaths, labels = image_files(DATA_DIR_TRAIN)  # 5,099 files
    print(f'Using {len(filepaths):,} files for training.')
    images = load_images(filepaths)
    y = to_categorical(labels, num_classes=28)
    X_train, X_test, y_train, y_test = train_test_split(images, y, random_state=SEED, test_size=0.2)
    print('X_train.shape:', X_train.shape)
    print('X_test.shape:', X_test.shape)
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=128,
        validation_data=(X_test, y_test)
    )
    score = model.evaluate(X_test, y_test)
    print('score: ', score)
    # evaluate the saved_model on your test data
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print('Test loss: ', test_loss)
    print('Test accuracy: ', test_accuracy)
    return history


def save_model(model, weights_path, architecture_path):
    """
    This function saves the model weights and architecture
    :param model: the model to save
    :param weights_path: the path to save the weights to
    :param architecture_path: the path to save the architecture to
    :return: None
    """
    # Save saved_model weights
    model.save_weights(weights_path)

    # Save saved_model architecture as JSON
    model_json = model.to_json()
    with open(architecture_path, 'w') as json_file:
        json_file.write(model_json)

    print("Model saved successfully.")
