from functools import lru_cache

from tqdm import tqdm

MIN_EDIT_DISTANCE_LENGTH = 1
WORDS_FILENAME = r"C:\Users\User\Desktop\כללי\שנה ג\פרויקט גמר\HandwritingProject\all_append_fatverb.txt"

def get_word_suggestions(word):
    closest_words = []
    words = open(WORDS_FILENAME, encoding='utf-8').read().splitlines()
    for vocab_word in tqdm(words):
        lev_dist_word = lev_dist(word, vocab_word)
        if lev_dist_word <= MIN_EDIT_DISTANCE_LENGTH:
            closest_words.append(vocab_word)
    return closest_words


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


