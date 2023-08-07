from functools import lru_cache
from tqdm import tqdm

from config import WORDS_FILENAME

MIN_EDIT_DISTANCE_LENGTH = 1


def get_word_suggestions(word, top_k=10, min_edit_dist=MIN_EDIT_DISTANCE_LENGTH):
    closest_words = []
    words = open(WORDS_FILENAME, encoding='utf-8').read().splitlines()
    for vocab_word in tqdm(words):
        lev_dist_word = lev_dist(word, vocab_word)
        if lev_dist_word <= min_edit_dist:
            closest_words.append((lev_dist_word, vocab_word))
    closest_words = sorted(closest_words, key=lambda x: (x[0], x[1]))
    if len(closest_words) >= 5:
        return [word for _, word in closest_words[:top_k]]
    return get_word_suggestions(word, top_k=10, min_edit_dist=min_edit_dist+1)


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
