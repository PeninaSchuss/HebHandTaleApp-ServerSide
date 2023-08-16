import os
from functools import lru_cache
from tqdm import tqdm
import sqlite3
import random
from config import WORDS_FILENAME, DIR_PATH

# Replace these with your actual file names and configurations
MIN_EDIT_DISTANCE_LENGTH = 1


def get_word_suggestions(word, top_k=10, min_edit_dist=MIN_EDIT_DISTANCE_LENGTH):
    closest_words = []
    words = open(WORDS_FILENAME, encoding='utf-8').read().splitlines()
    for vocab_word in tqdm(words):
        lev_dist_word = lev_dist(word, vocab_word)
        if lev_dist_word <= min_edit_dist:
            closest_words.append((lev_dist_word, vocab_word))
    closest_words = sorted(closest_words, key=lambda x: (x[0], x[1]))

    if len(closest_words) >= top_k:
        # Connect to the database
        database_filename = "popular_words.db"  # Replace with your database file
        database_path = os.path.join(DIR_PATH, "dbs", database_filename)
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Fetch popular words from the database
        cursor.execute("SELECT data_string FROM popular_words;")
        popular_words = set(row[0] for row in cursor.fetchall())

        # Get popular suggestions that exist in both closest_words and popular_words.db
        popular_suggestions = [word for _, word in closest_words if word in popular_words]

        # Check if popular_suggestions is more than top_k
        if len(popular_suggestions) > top_k:
            selected_popular_suggestions = [word for _, word in popular_suggestions[:top_k]]

        else:
            # Get remaining random suggestions from closest_words
            remaining_suggestions = [word for _, word in closest_words if word not in popular_words]

            # Calculate how many random suggestions are needed to reach top_k
            remaining_count = top_k - len(popular_suggestions)
            random_count = min(remaining_count, len(remaining_suggestions))

            # Select random suggestions from remaining_suggestions
            random_suggestions = remaining_suggestions[:random_count]

            # Combine popular and random suggestions
            selected_popular_suggestions = popular_suggestions + random_suggestions

        # Close the database connection
        connection.close()

        return selected_popular_suggestions

    return get_word_suggestions(word, top_k=10, min_edit_dist=min_edit_dist + 1)


def lev_dist(a, b):
    '''
    This function will calculate the levenshtein distance between two input
    strings a and b
    example: a = 'stamp', b = 'stomp', lev_dist(a,b) >> 1.0
    '''

    @lru_cache(None)  # for memorization
    def min_dist(s1, s2):

        if s1 == len(a) or s2 == len(b):
            return len(a) - s1 + len(b) - s2

        # no change required
        if a[s1] == b[s2]:
            return min_dist(s1 + 1, s2 + 1)

        return 1 + min(
            min_dist(s1, s2 + 1),  # insert character
            min_dist(s1 + 1, s2),  # delete character
            min_dist(s1 + 1, s2 + 1),  # replace character
        )

    return min_dist(0, 0)
