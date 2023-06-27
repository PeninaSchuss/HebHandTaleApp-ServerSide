import os
from components.segmentation import process_image
from components.letter_classification import predict_letters

IMAGES_DIR      = '/Users/stav/Projects/CodeSH/data'
image_name_call = 'call.png'
image_path_call = os.path.join(IMAGES_DIR, image_name_call)


chars = process_image(image_path_call)
assert len(chars) == 8

output = predict_letters(chars[3])
print(output)