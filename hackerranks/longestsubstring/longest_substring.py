
def longest_substring(s):
    """Determine the length of the longest substring of `s` with no repeating
    characters.

    Parameters
    ----------
    s : str
        Target string to search

    Returns
    -------
    int
        Length of longest substring of `s` with no repeating characters
    """

    # Track the current longest substring
    max_substr_len = 0
    # Track the last index of each character traversed
    char_to_last_idx = {}
    # Index after farthest repeated character's last occurrence
    start_idx = 0

    for i, char in enumerate(s):
        # char seen before -> shift start_idx if it was before last_idx
        if char in char_to_last_idx:
            last_idx = char_to_last_idx[char]
            if (last_idx + 1) > start_idx:
                start_idx = (last_idx + 1)

        # Update max_substr_len if current segment is longer
        if (i - start_idx + 1) > max_substr_len:
            max_substr_len = i - start_idx + 1

        # Update last_idx for current char
        char_to_last_idx[char] = i

    return max_substr_len
