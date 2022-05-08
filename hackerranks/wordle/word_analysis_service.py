
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


def _init_char_index_dict(key_set=string.ascii_uppercase, val_len=5):
    """ Initializes a dictionary with keys listed in `key_set`, and the values
    are int lists of length `val_len`, with each entry being 0.

    Parameters
    ----------
    key_set : iterable, default=string.ascii_uppercase
        Set of key values for new dictionary.
    val_len : int, default=5
        The length of the dictionary's values.

    Returns
    -------
    res : dict
        New dictionary initialized with the given parameters.
    """
    res = {}
    for char in key_set:
        res[char] = [0] * val_len
    return res


def _fill_dict(d, key_set=string.ascii_uppercase):
    """ Fills the given dictionary with missing keys defined by `key_set`.

    Parameters
    ----------
    d : dict
        Target dictionary to fill.
    key_set : iterable, default=string.ascii_uppercase
        Set of key values `d` should have.

    Returns
    -------
    d : dict
        Passed dictionary with missing keys defaulted to 0.
    """
    for key in key_set:
        if key not in d:
            d[key] = 0
    return d


def find_best_words(words, letter_count, letter_index_count, n=10, should_print=False):
    """ Determines best entries from `words` based on scoring system, using
    statistics from `letter_count` and `letter_index_count`.

    Parameters
    ----------
    words : set of str
        Set of words to score.
    letter_count : dict
        Dictionary with key-value pairs of character-int, representing the
        overall count of the character.
    letter_index_count : dict
        Dictionary with key-value pairs of character-list of int, representing
        the per-index count of the character.
    n : int, default=10
        The number of top scoring words to return.
    should_print : bool, default=False
        True to print top words to console.

    Returns
    -------
    best_words : set of str
        The best scoring words.
    """
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
