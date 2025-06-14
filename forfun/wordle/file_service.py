
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

    print(f'{count} lines of length {n} found')
    return valid_words


def load_words(input_file):
    """ Reads all lines from target input file and returns them as a set.

    Parameters
    ----------
    input_file : str
        Name of input file with newline-delimited lines.

    Returns
    -------
    lines : set of str
        Words from input file.
    """
    with open(input_file) as word_file:
        words = set(word_file.read().split())

    return words


def file_diff(file_a, file_b, output_file):
    """ Assumes both `file_a` and `file_b` are newline-delimited lists and
    writes any entries that are in the former but not the latter to
    `output_file`.

    Parameters
    ----------
    file_a : str
        Name of file for left side of set difference operation.
    file_b : str
        Name of file for right side of set difference operation.
    output_file : str
        Name of file to write result to.
    """
    words_a = load_words(file_a)
    print(f'{file_a} total count = {len(words_a)}')
    words_b = load_words(file_b)
    print(f'{file_b} total count = {len(words_b)}')
    words_diff = sorted(words_a - words_b)
    word_count = 0
    with open(output_file, 'w') as out_file:
        for word in words_diff:
            out_file.write(word + '\n')
            word_count += 1

    print(f'Found {len(words_diff)} lines in {file_a} not in {file_b}.\n'
          f'Successfully wrote {word_count} to {output_file}')


def add_to_file(lines, file, sort=False):
    """ Adds entries of `lines` to the end of `file`, putting each on a newline.
    Will only write entries not already in `file`.

    Parameters
    ----------
    lines : set of str
        Lines to append to the end of the target file.
    file : str
        Name of file to append lines to.
    sort : bool
        True if lines of the file should be sorted alphabetically.
    """
    print(f'Passed lines total count = {len(lines)}')
    file_lines = load_words(file)
    print(f'{file} total line count = {len(file_lines)}')
    new_entries = lines - file_lines
    if len(new_entries) != 0:
        if sort:
            for entry in new_entries:
                file_lines.add(entry)
            with open(file, 'w') as file_:
                file_.writelines('\n'.join(sorted(file_lines)))
        else:
            with open(file, 'a') as file_:
                file_.write('\n' + '\n'.join(new_entries))

    print(f'Wrote {len(new_entries)} lines in passed lines not in {file} to {file}.')


def remove_from_file(lines, file):
    print(f'Passed lines total count = {len(lines)}')
    file_lines = load_words(file)
    print(f'{file} total line count = {len(file_lines)}')
    unique_entries = file_lines - lines
    if len(unique_entries) != 0:
        with open(file, 'w') as file_:
            file_.write('\n'.join(unique_entries))

    print(f'Found {len(file_lines)-len(unique_entries)} words to remove from {file}.')
    print(f'Wrote {len(unique_entries)} lines to {file}.')


def sort_file(file):
    sorted_lines = sorted(load_words(file))
    with open(file, 'w') as file_:
        file_.write('\n'.join(sorted_lines))


if __name__ == '__main__':
    print('Begin file_service')
    # Update ignored words (from scratch) to account for manual removals from simple word list
    # file_diff('scrabble_dict.txt', 'possible_wordle_words_simple.txt', 'ignored_words.txt')

    # Update simple word list to remove ignored words
    # file_diff('possible_wordle_words_simple.txt', 'ignored_words.txt', 'possible_wordle_words_simple.txt')

    # Update ignored words (append to) to account for manual removals from simple word list
    # file_diff('possible_wordle_words.txt', 'possible_wordle_words_simple.txt', 'temp_diff.txt')
    # add_to_file(load_words('temp_diff.txt'), 'ignored_words.txt')
    # sort_file('ignored_words.txt')
    print('End file_service')
