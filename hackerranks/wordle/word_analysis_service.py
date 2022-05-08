
import my_pprint as pprint
import string


def analyze_most_used_letters(words, should_print=False):
    """ Calculates the count of letters across the given word set, both overall
    and per-index.

    Parameters
    ----------
    words : list of str
        Words to calculate letter counts from.
    should_print : bool, default=False
        True to pretty print results to console.

    Returns
    -------
    letter_count : dict
        Dictionary where each key is a character and its value is the count of
        how much it occurred throughout the given set of words.
    letter_index_count : dict
        Dictionary where each key is a character and its value is a list of
        counts of how much it occurred in each index in the given set of words.
    """
    letter_count = {}
    letter_index_count = _init_char_index_dict()
    for word in words:
        for i, letter in enumerate(word):
            # Overall occurrence count
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

            # Occurrence per index count
            letter_index_count[letter][i] += 1

    letter_count = _fill_dict(letter_count)

    if should_print:
        print('#### Overall Results')
        pprint.pprint_alpha_dict(letter_count)
        print('#### Per Index Results')
        pprint.pprint_2d_alpha_dict(letter_index_count)

    return letter_count, letter_index_count


def _init_char_index_dict(char_set=string.ascii_uppercase, word_len=5):
    res = {}
    for char in char_set:
        res[char] = [0] * word_len
    return res


def _fill_dict(d, key_set=string.ascii_uppercase):
    for key in key_set:
        if key not in d:
            d[key] = 0
    return d


def find_best_words(words, letter_count, letter_index_count, n=10, should_print=False):
    best_words = []
    for word in words:
        word_score = _score_word(word, letter_count, letter_index_count)
        best_words = _update_top_x(best_words, (word, word_score), n)

    if should_print:
        print(f'Best {n} Words: {best_words}')
    return best_words


def _score_word(word, letter_count, letter_index_count):
    score = 0
    for i, letter in enumerate(word):
        score += letter_index_count[letter][i]
    return score


def _update_top_x(items, elem, n):
    items.append(elem)
    items = sorted(items, key=lambda x: x[1], reverse=True)
    if len(items) > n:
        items = items[:-1]
    return items
