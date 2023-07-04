import os
from tqdm import tqdm
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import Sequential
from keras.applications.vgg19 import VGG19
from keras.layers import Dense, Flatten
from sklearn.model_selection import train_test_split
from config import DATA_DIR_TRAIN, IMAGE_SIZE, ABC


INPUT_IMAGE_SIZE = (IMAGE_SIZE, IMAGE_SIZE, 3)
SEED           = 42
EPOCHS         = 1


# prepare a list of image files to be loaded
def image_files(input_directory):
    filepaths = []
    labels = []

    digit_folders = os.listdir(input_directory)
    # print(digit_folders)

    for digit in digit_folders:
        path = os.path.join(input_directory, digit)
        flist = os.listdir(path)
        for f in flist:
            fpath = os.path.join(path, f)
            filepaths.append(fpath)
            labels.append(digit)
    return filepaths, labels


def load_images(filepaths):
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
    # load the paths and labels in differnt variables
    filepaths, labels = image_files(DATA_DIR_TRAIN) # 5,099 files
    print(f'Using {len(filepaths):,} files for training.')
    # load the 10K images
    images = load_images(filepaths)
    y = to_categorical(labels, num_classes=28)
    X_train, X_test, y_train, y_test = train_test_split(images, y, random_state=SEED, test_size=0.2)
    print('X_train.shape:', X_train.shape)
    print('X_test.shape:',  X_test.shape)
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=128,
        validation_data=(X_test, y_test)
    )
    return history


model = load_vgg_model()
model.summary()


def predict_letters(X):
    # Get the probability for each possible character
    probabilities = model.predict(X)
    # Get the index of the highest probability character
    max_class_indices = np.argmax(probabilities, axis=1)
    # Get the corresponding Hebrew letter
    predicted_letters = [ABC[i] for i in max_class_indices]
    # Append the predicted letter to the list
    # predicted_letters.append(predicted_letter)
    predicted_letters_word = ''.join(predicted_letters)
    return predicted_letters_word



# history = train_model(model)
