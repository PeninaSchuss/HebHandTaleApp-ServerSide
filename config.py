import os

dir_path = os.path.dirname(os.path.realpath(__file__))  # Current file's directory

# ========= Paths ============
# Data for training VGG
DATA_DIR_TRAIN = os.path.join(dir_path, "data", "letters")
# Vocabulary
WORDS_FILENAME = os.path.join(dir_path, "data/vocab/he-vocab.txt")
# Examples directory
DATA_DIR = os.path.join(dir_path, "data")
IMAGES_DIR_TEST = os.path.join(DATA_DIR, "for_evaluation")

# Update the path to the correct location of the saved_model architecture file
MODEL_PATH_ARCHITECTURE = os.path.join(DATA_DIR, "saved_model", "model_architecture.json")
MODEL_PATH_WEIGHTS = os.path.join(DATA_DIR, "saved_model", "model_weights.h5")
DATABASE_FILENAME = "popular_words.db"  # Replace with your database file
DATABASE_PATH = os.path.join(dir_path, "dbs", DATABASE_FILENAME)

# ========= Settings ============
IMAGE_SIZE = 32

# Define a dictionary to map the classification index to Hebrew letters
ABC = "אבגדהוזחטיכךלמםנןסעפףצץקרשת,"
