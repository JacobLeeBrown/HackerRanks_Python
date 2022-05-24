
import csv
from datetime import datetime, timedelta
import file_service as fs
import word_analysis_service as was


def get_all_used_words():
    used_words_ = []
    today = datetime.today()
    with open('all_wordle_words.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        word_count = 0
        for row in csv_reader:
            if word_count == 0:  # Header row
                word_count += 1
            else:
                row_date = datetime.strptime(row['date'], '%b %d %Y')
                if row_date >= (today + timedelta(days=7)):  # Offset for removed words
                    break
                else:
                    word = row['word'].strip()
                    if len(word) != 5:
                        pass  # Skip removed words
                    else:
                        used_words_.append(word)
                        word_count += 1
        print(f'Processed {word_count-1} used Wordle words.')
    return used_words_


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


def analysis_with_user_input(correct_, close_, wrong_):
    # Data Prep
    used_words = get_all_used_words()
    fs.add_to_file({used_words[-1]}, 'used_wordle_words.txt')  # Add newest word to used list
    fs.add_to_file({used_words[-1]}, 'ignored_words.txt')  # Add newest word to ignored list
    ignored_words = fs.load_words('ignored_words.txt')
    possible_wordle_words = fs.load_words('possible_wordle_words_simple.txt')
    analysis = was.analyze_most_used_letters(used_words, should_print=True)

    # Solving
    while True:
        potential_solutions = solver(possible_wordle_words, ignored_words, correct_, close_, wrong_)
        best_solutions = was.find_best_words(potential_solutions, analysis[0], analysis[1], n=20, should_print=False)

        print(f'Last 10 Wordle Words: {used_words[-10:]}')
        print('#### Ignored Potential Solutions')
        ignored_solutions = solver(ignored_words, set(), correct_, close_, wrong_)
        was.find_best_words(ignored_solutions, analysis[0], analysis[1], n=10, should_print=True)
        print('####')

        print('#### Best Potential Solutions')
        for i, item in enumerate(best_solutions):
            print(f'{str(i).rjust(3)} = {item}')
        print('####')

        print('Select words to remove by denoting their indices. Ex: "1,3-4,7". "q" or "quit" to stop.')
        user_input = input()
        if user_input.lower() in {'q', 'quit'}:
            break

        words_to_remove = my_splice([x[0] for x in best_solutions], user_input)
        print(f'Removed words = {words_to_remove}')
        fs.add_to_file(words_to_remove, 'ignored_words.txt')
        ignored_words = ignored_words.union(words_to_remove)
    fs.sort_file('ignored_words.txt')


def simple_analysis(correct_, close_, wrong_):
    # Data Prep
    used_words = get_all_used_words()
    fs.add_to_file({used_words[-1]}, 'used_wordle_words.txt')  # Add newest word to used list
    fs.add_to_file({used_words[-1]}, 'ignored_words.txt')  # Add newest word to ignored list
    ignored_words = fs.load_words('ignored_words.txt')
    possible_wordle_words = fs.load_words('possible_wordle_words_simple.txt')
    analysis = was.analyze_most_used_letters(used_words, should_print=False)

    print(f'Last 10 Wordle Words: {used_words[-10:]}')
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

    simple_analysis(correct, close, wrong)
    # analysis_with_user_input(correct, close, wrong)
    print('End wordle_service')
