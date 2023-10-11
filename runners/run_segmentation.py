import os
from components.segmentation import process_image
from config import DATA_DIR
import matplotlib.pyplot as plt

IMAGE_PATH_TO_TEST = os.path.join(DATA_DIR, "חמאה.png")

chars = process_image(IMAGE_PATH_TO_TEST)
for i in range(len(chars)):
    plt.imshow(chars[i])
    plt.show()
