import os
from components.segmentation import process_image


IMAGES_DIR      = '/Users/stav/Projects/CodeSH/data'
image_name_call = 'call.png'
image_path_call = os.path.join(IMAGES_DIR, image_name_call)


chars = process_image(image_path_call)
assert len(chars) == 8
