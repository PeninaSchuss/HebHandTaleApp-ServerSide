import os
from tqdm import tqdm

from evaluation.test_set import TEST_SET
from config import IMAGES_DIR_TEST
from runners.run_e2e import run_e2e

AMOUNT_OF_IMAGES_FOR_EVALUATION = 103


def get_accuracy_at_k(test_set, k=10):
    total_items = len(test_set)
    correct_items = 0
    for filename, label in tqdm(test_set):
        image_path = os.path.join(IMAGES_DIR_TEST, filename)
        print(filename)
        result = run_e2e(image_path, k)
        if label in result:
            correct_items += 1

    score = correct_items / total_items
    return score


test_set = TEST_SET[:AMOUNT_OF_IMAGES_FOR_EVALUATION]
score_at_10 = get_accuracy_at_k(test_set, k=10)
print(score_at_10)
