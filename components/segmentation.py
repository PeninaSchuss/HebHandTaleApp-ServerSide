import os
import cv2
import numpy as np
from PIL import Image
from config import IMAGE_SIZE

def process_image(image_path):
    assert os.path.exists(image_path)
    # 01 - Load the image
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    # 02 - Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 03 - Apply thresholding to convert the image to binary
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 04 - Perform connected component analysis to separate the characters
    connected_components_output = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    # 05 - Extract characters
    chars = _process_characters(connected_components_output, img)
    return chars


def _process_characters(connected_components_output, original_img):
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
        # Resize the character to a square shape
        char_square = resize_as_square(char_cropped)
        chars_cropped.append(char_square)

        coords.append(stats[i + 1])
    chars_cropped = [char for _, char in sorted(zip(coords, chars_cropped), key=lambda x: x[0][0], reverse=True)]

    chars_to_delete = []
    for i in range(num_chars):
        for j in range(i - 1, i + 2):
            if i != j and num_chars > j > -1 and is_contained(coords[i], coords[j]):
                # If ק is found, find the bounding box that contains both parts of ק
                min_x = min(coords[i][0], coords[j][0])
                min_y = min(coords[i][1], coords[j][1])
                max_x = max(min_x + coords[i][2], min_x + coords[j][2])
                max_y = max(min_y + coords[i][3], min_y + coords[j][3])
                char_combined = original_img[min_y:max_y, min_x:max_x]
                char_square_combined = resize_as_square(char_combined)
                chars_cropped[i] = char_square_combined
                chars_to_delete.append(j)

    # Remove the marked characters from chars_cropped list
    chars_cropped_copy = chars_cropped.copy()  # Create a copy to iterate without modifying the original
    for idx in chars_to_delete:
        del chars_cropped_copy[idx]

    # for im in chars_cropped_copy:
    #     # Display the image
    #     cv2.imshow('Char Combined Image', im)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    return chars_cropped_copy


def is_contained(coords1, coords2):
    x1, _, w1, _, _ = coords1
    x2, _, w2, _, _ = coords2

    # Check if coords1 is completely inside coords2 (x-axis overlap)
    if x2 <= x1 <= x2 + w2 and x2 <= x1 + w1 <= x2 + w2:
        return True

    return False


def resize_as_square(img_np):
    img_square = Image.fromarray(img_np).resize((IMAGE_SIZE, IMAGE_SIZE))
    if img_square.mode != 'RGB':
        img_square = img_square.convert('RGB')  # Convert to RGB if not already
    return np.array(img_square)
