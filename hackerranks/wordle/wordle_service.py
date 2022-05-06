
import csv
from datetime import datetime, timedelta
import file_service as fs
import word_analysis_service as was


def get_all_used_words():
    used_words = []
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
                        used_words.append(word)
                        word_count += 1
        print(f'Processed {word_count-1} used Wordle words.')
    return used_words


def solver(words, correct, close, wrong):
    possible_words = []
    for word in words:
        word_matches = True
        close_dict = init_close_dict(close)
        for i, letter in enumerate(word):
            # Conditions for word not being a match
            if letter in wrong:
                word_matches = False
                break
            if letter in close[i]:
                word_matches = False
                break
            elif letter in close_dict:  # Found a close letter not in the known wrong position
                close_dict[letter] = True
            if len(correct[i]) != 0 and letter not in correct[i]:
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
            possible_words.append(word)

    return possible_words


def init_close_dict(close):
    d = {}
    for list in close:
        for letter in list:
            d[letter] = False
    return d


if __name__ == '__main__':
    print('Begin wordle_service')
    # wordle_words = get_all_used_words()
    # was.analyze_most_used_letters(wordle_words)
    # fs.get_words_of_length(input_file='scrabble_dict.txt', n=5, alpha_only=True, save=True, output_file='possible_wordle_words.txt')

    possible_wordle_words = fs.load_words('possible_wordle_words_simple.txt')
    analysis = was.analyze_most_used_letters(get_all_used_words(), should_print=True)

    # Example usage
    # correct = [['H'], ['O'], [], ['E'], ['R']]
    # close = [[], [], [], [], []]
    # wrong = ['S', 'A', 'V']

    correct_ = [[], [], [], [], []]
    close_ = [[], [], [], [], []]
    wrong_ = []

    potential_solutions = solver(possible_wordle_words, correct_, close_, wrong_)
    was.find_best_words(potential_solutions, analysis[0], analysis[1], n=20, should_print=True)

    print('End wordle_service')
