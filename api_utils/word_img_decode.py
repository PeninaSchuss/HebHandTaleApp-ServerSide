import base64
import os
import uuid

from config import DIR_PATH


def save_image_from_base64(image_content):
    image_data = base64.b64decode(image_content)
    filename = str(uuid.uuid4()) + '.png'
    image_path = os.path.join(DIR_PATH, "base64_imgs", filename)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    return image_path
