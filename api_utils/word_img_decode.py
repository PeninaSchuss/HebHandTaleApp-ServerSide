import base64
import os
import uuid

from config import DIR_PATH



def save_image_from_base64(image_content):
    """
    This function saves an image from base64 to a file
    :param image_content: image content in base64
    :return: image_path - image path in the server
    """
    image_data = base64.b64decode(image_content)
    filename = str(uuid.uuid4()) + '.png'

    # Create the directory if it doesn't exist
    save_directory = os.path.join(DIR_PATH, "base64_imgs")
    os.makedirs(save_directory, exist_ok=True)

    image_path = os.path.join(save_directory, filename)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    return image_path
