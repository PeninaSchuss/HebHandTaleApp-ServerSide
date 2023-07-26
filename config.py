import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # Current file's directory


# ========= Paths ============
# Data for training VGG
DATA_DIR_TRAIN = r'/Users/stav/Projects/CodeSH/vgg_for_final_project/TRAIN'
# Vocabulary
WORDS_FILENAME = os.path.join(dir_path, "data/vocab/he-vocab.txt")
# Examples directory
IMAGES_DIR      = os.path.join(dir_path, "data")
IMAGES_DIR_TEST = os.path.join(IMAGES_DIR, "for_evaluation")

MODEL_PATH_ARCHITECTURE = os.path.join(dir_path, "model", "model_architecture.json")
MODEL_PATH_WEIGHTS      = os.path.join(dir_path, "model", "model_weights.h5")


# ========= Settings ============
IMAGE_SIZE = 32

# Define a dictionary to map the classification index to Hebrew letters
ABC = "אבגדהוזחטיכךלמםנןסעפףצץקרשת,"





