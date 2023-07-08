import os
import cv2
import numpy as np
from PIL import Image
from config import IMAGE_SIZE


def process_image(image_path):
    assert os.path.exists(image_path)
    # 01 - Load the image
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    # img = cv2.imread(image_path)
    # 02 - Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # numpy.ndarray, (257, 522)
    # 03 - Apply thresholding to convert the image to binary
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 04 - Perform connected component analysis to separate the characters
    connected_components_output = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    # 05 - Extract characters
    chars = _process_characters(connected_components_output)
    return chars


def _process_characters(connected_components_output):
    num_labels, labels, stats, centroids = connected_components_output
    # Get the number of characters (excluding the background)
    num_chars = num_labels - 1
    # Define a list to store individual characters
    chars = []
    chars_cropped = []
    # Define a list to store the coordinates of each character
    coords = []
    # Loop through each character
    for i in range(num_chars):
        # Add char
        char = labels == i + 1
        char = np.stack([char] * 3, axis=-1).astype(np.uint8) * 255
        char = cv2.bitwise_not(char)
        chars.append(char)
        x, y, w, h, area = stats[i + 1]
        char_cropped = char[y:y + h, x:x + w]
        if char_cropped.shape[0] != char_cropped.shape[1]:
            max_dim = max(char_cropped.shape[0], char_cropped.shape[1])
            # Calculate the amount of padding required
            top = (max_dim - char_cropped.shape[0]) // 2
            bottom = max_dim - char_cropped.shape[0] - top
            left = (max_dim - char_cropped.shape[1]) // 2
            right = max_dim - char_cropped.shape[1] - left
            # Add padding to the image
            char_cropped = cv2.copyMakeBorder(char_cropped, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                              value=[255, 255, 255])
            char_square = resize_as_square(char_cropped)
        chars_cropped.append(char_square)

        coords.append(stats[i + 1][:2])
    # Sort the characters based on their x-coordinates (from right to left)
    chars_cropped = [char for _, char in sorted(zip(coords, chars_cropped), key=lambda x: x[0][0], reverse=True)]

    return chars_cropped


def resize_as_square(img_np):
    img_square = Image.fromarray(img_np).resize((IMAGE_SIZE, IMAGE_SIZE))
    return np.array(img_square)
