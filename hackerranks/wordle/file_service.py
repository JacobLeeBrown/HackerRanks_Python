
def get_words_of_length(input_file='words_alpha.txt', n=5, alpha_only=True, output_file=''):
    """ Finds all words of length 'n' in 'input_file', returning them as a set.
    Will also save the target words to 'output_file` if value is non-empty.

    Parameters
    ----------
    input_file : str, default='words_alpha.txt'
        Name of file with universal set of newline-delimited words to search
        through.
    n : int, default=5
        Length of target words.
    alpha_only : bool, default=True
        Flag for characteristic of target words. True to search only words with
        no symbols or numbers.
    output_file : str, default=''
        Name of file to write target words to. Will only be written if value is
        non-empty. Each word will be written on its own line and all uppercase.

    Returns
    -------
    valid_words : set of str
        Words from input file matching criteria defined by parameters.
    """
    valid_words = {}
    count = 0
    save = (output_file is not None) and (len(output_file) > 0)
    with open(input_file) as word_file:
        if save:
            out = open(output_file, 'w')

        for word in word_file:
            word = word.strip().upper()
            if len(word) == n and (not alpha_only or word.isalpha()):
                valid_words[word] = 1
                count += 1
                if save:
                    out.write(word + '\n')
        if save:
            out.close()

    print(f'{count} words of length {n} found')
    return valid_words


def load_words(input_file):
    """ Reads all words from target input file and returns them as a set.

    Parameters
    ----------
    input_file : str
        Name of input file with newline-delimited words.

    Returns
    -------
    words : set of str
        Words from input file.
    """
    with open(input_file) as word_file:
        words = set(word_file.read().split())

    return words
