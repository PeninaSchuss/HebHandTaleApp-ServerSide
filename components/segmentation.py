import os
import cv2
import numpy as np
from PIL import Image

from config import IMAGE_SIZE


def process_image(image_path):
    assert os.path.exists(image_path)
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    connected_components_output = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    chars = process_characters(connected_components_output, img)
    return chars


def process_characters(connected_components_output, original_img):
    num_labels, labels, stats, centroids = connected_components_output
    num_chars = num_labels - 1
    chars_cropped = []
    coords = []

    for i in range(num_chars):
        char_cropped, char_coords = process_char(i, stats[i + 1], labels)
        chars_cropped.append(char_cropped)
        coords.append(char_coords)

    chars_cropped = combine_contained_chars(chars_cropped, coords, original_img)
    return chars_cropped


def process_char(i, char_stats, labels):
    x, y, w, h, _ = char_stats
    char = labels == i + 1
    char = np.stack([char] * 3, axis=-1).astype(np.uint8) * 255
    char = cv2.bitwise_not(char)
    char_cropped = char[y:y + h, x:x + w]

    if char_cropped.shape[0] != char_cropped.shape[1]:
        char_cropped = pad_and_resize(char_cropped)

    char_square = resize_as_square(char_cropped)
    return char_square, char_stats


def pad_and_resize(img):
    max_dim = max(img.shape[0], img.shape[1])
    top = (max_dim - img.shape[0]) // 2
    bottom = max_dim - img.shape[0] - top
    left = (max_dim - img.shape[1]) // 2
    right = max_dim - img.shape[1] - left
    padded_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return padded_img


def combine_contained_chars(chars_cropped, coords, original_img):
    # Sort chars_cropped while maintaining the original order
    sorted_data = sorted(zip(coords, chars_cropped), key=lambda x: x[0][0], reverse=True)
    coords = [coord for coord, _ in sorted_data]
    chars_cropped = [char for _, char in sorted_data]

    chars_to_delete = []

    for i in range(len(chars_cropped)):
        for j in range(len(chars_cropped)):
            if i != j and len(chars_cropped) > j > -1 and is_contained(coords[i], coords[j]):
                char_combined = combine_chars(original_img, coords[i], coords[j])
                chars_cropped[i] = resize_as_square(char_combined)
                chars_to_delete.append(j)

    chars_cropped_copy = [char for idx, char in enumerate(chars_cropped) if idx not in chars_to_delete]
    return chars_cropped_copy


def is_contained(coords1, coords2):
    x1, _, w1, _, _ = coords1
    x2, _, w2, _, _ = coords2
    return x2 <= x1 <= x2 + w2 and x2 <= x1 + w1 <= x2 + w2


def combine_chars(original_img, coords1, coords2):
    min_x = min(coords1[0], coords2[0])
    min_y = min(coords1[1], coords2[1])
    max_x = max(min_x + coords1[2], min_x + coords2[2])
    max_y = max(min_y + coords1[3], min_y + coords2[3])
    char_combined = original_img[min_y:max_y, min_x:max_x]
    return char_combined


def resize_as_square(img_np):
    img_square = Image.fromarray(img_np).resize((IMAGE_SIZE, IMAGE_SIZE))
    if img_square.mode != 'RGB':
        img_square = img_square.convert('RGB')
    return np.array(img_square)
