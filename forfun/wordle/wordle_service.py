
import csv
from datetime import datetime, timedelta, date
import file_service as fs
import word_analysis_service as was
import math


WORDLE_LEN = 5
FIRST_WORDLE_DATE = date(2021, 6, 20)
DATE_IN_FORMAT = '%b %d %Y'
DATE_OUT_FORMAT = '%Y-%m-%d'
ALL_WORDLE_WORDS_FILE = 'all_wordle_words.csv'
USED_WORDS_CSV_FILE = 'used_words.csv'
USED_WORDS_SORTED_FILE = 'used_words_sorted.txt'
IGNORED_WORDS_FILE = 'ignored_words.txt'
POSSIBLE_WORD_FILE = 'possible_wordle_words.txt'


def get_all_used_words():
    used_words_ = []
    today = datetime.today()
    with open(ALL_WORDLE_WORDS_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        word_count = 0
        for row in csv_reader:
            if word_count == 0:  # Header row
                word_count += 1
            else:
                row_date = datetime.strptime(row['date'], DATE_IN_FORMAT)
                if row_date >= (today + timedelta(days=7)):  # Offset for removed words
                    break
                else:
                    word = row['word'].strip()
                    if len(word) != WORDLE_LEN:
                        pass  # Skip removed words
                    else:
                        used_words_.append(word)
                        word_count += 1
        print(f'Processed {word_count-1} used Wordle words.')
    return used_words_


def write_actual_used_words(out_file=USED_WORDS_CSV_FILE):
    today = datetime.today()
    with open(ALL_WORDLE_WORDS_FILE, mode='r') as f_in:
        with open(out_file, mode='w', newline='') as f_out:
            csv_reader = csv.DictReader(f_in)
            csv_writer = csv.writer(f_out)
            row_idx = 0
            true_date = today
            skipped_offset = 0
            for row in csv_reader:
                word = row['word'].strip()
                row_date = datetime.strptime(row['date'], DATE_IN_FORMAT)

                if row_idx == 0:  # Header row
                    csv_writer.writerow(row.keys())
                    true_date = (row_date - timedelta(days=3))  # More must've been skipped then list details

                if len(word) != WORDLE_LEN:
                    print(f'Skipping word: {row_date} - {word}')
                    skipped_offset += 1
                elif row_date >= (today + timedelta(days=skipped_offset)):
                    print(f'Caught up on Wordle Words. Count = {row_idx}, Skipped = {skipped_offset}')
                    break
                else:
                    row_idx += 1
                    id_str = f'Day {row_idx}'
                    csv_writer.writerow([true_date.strftime(DATE_OUT_FORMAT), id_str, word])
                    true_date = true_date + timedelta(days=1)
    return


def get_last_n_used_words(file_name=USED_WORDS_CSV_FILE, n=10):
    today = datetime.today()
    start_date = today - timedelta(days=n)
    words_ = []
    with open(file_name, mode='r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            row_date = datetime.strptime(row['date'], DATE_OUT_FORMAT)
            if row_date >= start_date:
                words_.append(row['word'])
    return words_


def solver(words, ignored_words_, correct_, close_, wrong_):
    """ Determines potential Wordle solutions from universal set `words` not in
    subset `ignored_words_`, further narrowing down options using information
    such as correct letters, close letters, and wrong letters outputted by
    Wordle.

    Parameters
    ----------
    words : set of str
        All potential Wordle words.
    ignored_words_ : set of str
        Words deemed unlikely or impossible to be Wordle solutions (such as
        prior solutions), thus ignored by solver algorithm.
    correct_ : list of list of str
        Letters guessed to be in the correct spot. The position in outer list
        corresponds to the position within the solution.
    close_ : list of list of str
        Letters guessed to be in the solution, but not the right position. The
        position in the outer list corresponds to the position within the
        solution.
    wrong_ : str
        Letters guessed to not be in the solution, concatenated into a single
        string.

    Returns
    -------
    possible_words : set of str
        Potential solutions based on the given parameters.
    """
    words_ = words - ignored_words_
    if _solver_check_empty(correct_, close_, wrong_):
        return words_
    possible_words = set()
    for word in words_:
        word_matches = True
        close_dict = _init_close_dict(close_)
        for i, letter in enumerate(word):
            # Conditions for word not being a match
            if letter in wrong_:
                word_matches = False
                break
            if letter in close_[i]:
                word_matches = False
                break
            elif letter in close_dict:  # Found a close letter not in the known wrong position
                close_dict[letter] = True
            if len(correct_[i]) != 0 and letter not in correct_[i]:
                word_matches = False
                break

        # Once all letters are processed, check we covered all close letters
        if word_matches:
            for val in close_dict.values():
                if not val:
                    word_matches = False
                    break

        # If word still matches, then it's a candidate
        if word_matches:
            possible_words.add(word)

    return possible_words


def _solver_check_empty(correct_, close_, wrong_):
    if (correct_ is not None) and (len(correct_) != 0) and (correct_ != [[]]*len(correct_)):
        return False
    if (close_ is not None) and (len(close_) != 0) and (close_ != [[]]*len(close_)):
        return False
    if (wrong_ is not None) and (len(wrong_) != 0):
        return False
    return True


def _init_close_dict(close_):
    d = {}
    for letters in close_:
        for letter in letters:
            d[letter] = False
    return d


def my_splice(list_, indices_str):
    """ Returns elements of `list_` based on the comma-delimited index
    expressions in `indices_str`.

    Parameters
    ----------
    list_ : list
        List of items to select from.
    indices_str : str
        Comma-delimited index expressions, representing which elements to pull
        out from the passed list. Ex: '0,2,4-6,10'

    Returns
    -------
    res : set
        Set of items denoted by `indices_str` from `list_`.
    """
    res = set()
    indices = indices_str.split(',')
    for ind_exp in indices:
        if '-' in ind_exp:
            bounds = ind_exp.split('-')
            for i in range(int(bounds[0]), int(bounds[1])+1):
                res.add(list_[i])
        elif ind_exp.isdigit():
            res.add(list_[int(ind_exp)])
        else:
            print('Cannot parse index expression: ' + ind_exp)
    return res


def analysis_with_user_input(correct_=None, close_=None, wrong_=''):
    if close_ is None:
        close_ = []
    if correct_ is None:
        correct_ = []
    # Data Prep
    used_words = list(fs.load_words(USED_WORDS_SORTED_FILE))
    ignored_words = fs.load_words(IGNORED_WORDS_FILE)
    possible_wordle_words = fs.load_words(POSSIBLE_WORD_FILE)
    analysis = was.analyze_most_used_letters(used_words, should_print=True)

    last_n_words = get_last_n_used_words(n=10)
    # Solving
    while True:
        print(f'Last 10 Wordle Words: {last_n_words}')

        print('#### Ignored Potential Solutions')
        ignored_solutions = solver(ignored_words, set(), correct_, close_, wrong_)
        print_list_with_cols(was.find_best_words(ignored_solutions, analysis[0], analysis[1], n=10), 3)
        print('####')

        potential_solutions = solver(possible_wordle_words, ignored_words, correct_, close_, wrong_)

        print('#### Best Potential Solutions - No dupes')
        best_solutions_no_dupes = was.find_best_words(potential_solutions, analysis[0], analysis[1], n=20, allow_duplicate_letters=False)
        print_list_with_cols(best_solutions_no_dupes, 3)
        print('####')

        print('#### Best Potential Solutions')
        best_solutions = was.find_best_words(potential_solutions, analysis[0], analysis[1], n=20)
        print_list_with_cols(best_solutions, 3)
        print('####')

        quit_, ignored_words, correct_, close_, wrong_ = user_actions(best_solutions, ignored_words, correct_, close_, wrong_)

        if quit_:
            _action_new_wordle_word()
            break
        else:
            print(f'Correct = {correct_}\nClose   = {close_}\nWrong   = {wrong_}')

    fs.sort_file(USED_WORDS_SORTED_FILE)
    fs.sort_file(IGNORED_WORDS_FILE)


def print_list_with_cols(items, cols=2):
    items_len = len(items)
    rows = math.ceil(items_len / cols)
    items_list = list(items)
    for i in range(rows):
        for j in range(cols):
            if (i + (rows * j)) < items_len:
                print(f'{str(i + (rows * j)).rjust(3)} = {items_list[i + (rows * j)]}     ', end='')
        print()


def user_actions(words, ignored, correct_, close_, wrong_):
    while True:
        user_input = input('What would you like to do? R = remove words, U = update hints, N = next cycle, Q = quit : ')
        if user_input.lower() in {'r', 'remove'}:
            ignored = ignored.union(_action_remove_words(words))
        elif user_input.lower() in {'u', 'update'}:
            correct_, close_, wrong_ = _action_update_hints()
        elif user_input.lower() in {'n', 'next'}:
            return False, ignored, correct_, close_, wrong_
        elif user_input.lower() in {'q', 'quit'}:
            return True, {}, [], [], ''
        else:  # Unrecognized input
            print('Command not recognized. Valid options are: R, U, N, and Q.')


def _action_remove_words(words):
    print('Select words to remove by denoting their indices. Ex = "1,3-4,7". "q" or "quit" to stop. This will add to '
          'prior removals:')
    user_input = input()
    if user_input.lower() in {'q', 'quit'}:
        return {}
    words_to_remove = my_splice([x[0] for x in words], user_input)
    print(f'Removed words = {words_to_remove}')
    fs.add_to_file(words_to_remove, IGNORED_WORDS_FILE, True)
    return words_to_remove


def _action_update_hints():
    print('First update correct, then close, then wrong. Enter "q" or "quit" at any time to abort. This will override '
          'any prior updates.')
    user_input = input('Enter correct hints. Ex = "S,,,R," : ')
    if user_input.lower() in {'q', 'quit'}:
        return
    correct_ = user_input.upper().split(',')
    user_input = input('Enter close hints. Ex = ",,TI,,H" : ')
    if user_input.lower() in {'q', 'quit'}:
        return
    close_ = user_input.upper().split(',')
    user_input = input('Finally, enter wrong letters. Ex = "LOUGD" : ')
    if user_input.lower() in {'q', 'quit'}:
        return
    wrong_ = user_input.upper()
    return correct_, close_, wrong_


def _action_new_wordle_word():
    quit_ = False
    print('Please enter the newest Wordle word:')
    user_input = input()
    while len(user_input) != WORDLE_LEN:
        if user_input.lower() in {'q', 'quit'}:
            print('Fine, be that way :P')
            quit_ = True
            break
        print(f'Entered string \'{user_input}\' is not {WORDLE_LEN} characters. Please re-enter:')
        user_input = input()
    if quit_:
        return
    update_files_with_new_word(user_input)
    print('Thank you! Don\'t have a nice day, have a great day!')


def update_files_with_new_word(word):
    word = word.upper()
    fs.add_to_file({word}, USED_WORDS_SORTED_FILE, True)
    fs.add_to_file({word}, IGNORED_WORDS_FILE, True)

    today = date.today()
    today_id = (today - FIRST_WORDLE_DATE).days + 1
    today_str = today.strftime(DATE_OUT_FORMAT)
    csv_line = f'{today_str},Day {today_id},{word}'
    fs.add_to_file({csv_line}, USED_WORDS_CSV_FILE)


def simple_analysis(correct_, close_, wrong_):
    # Data Prep
    used_words = list(fs.load_words(USED_WORDS_SORTED_FILE))
    ignored_words = fs.load_words(IGNORED_WORDS_FILE)
    possible_wordle_words = fs.load_words(POSSIBLE_WORD_FILE)
    analysis = was.analyze_most_used_letters(used_words, should_print=False)

    print(f'Last 10 Wordle Words: {get_last_n_used_words(n=10)}')
    # Solving
    potential_solutions = solver(possible_wordle_words, ignored_words, correct_, close_, wrong_)
    print('#### Potential Solutions')
    was.find_best_words(potential_solutions, analysis[0], analysis[1], n=20, should_print=True)
    print('####')

    print('#### Ignored Potential Solutions')
    ignored_solutions = solver(ignored_words, set(), correct_, close_, wrong_)
    was.find_best_words(ignored_solutions, analysis[0], analysis[1], n=10, should_print=True)
    print('####')


if __name__ == '__main__':
    print('Begin wordle_service')
    # Example usage
    # correct = [['S'], [], [], [], []]
    # close = [[], [], ['A'], ['R'], []]
    # wrong = 'LTEGOUD'

    # No Hints
    correct = [[], [], [], [], []]
    close = [[], [], [], [], []]
    wrong = ''

    # simple_analysis(correct, close, wrong)
    analysis_with_user_input(correct, close, wrong)
    print('End wordle_service')
