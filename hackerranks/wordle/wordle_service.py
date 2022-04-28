
import csv
from datetime import datetime, date


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
                if row_date >= today:
                    break
                else:
                    word = row['word'].strip()
                    if len(word) != 5:
                        pass  # Skip removed words
                    else:
                        used_words.append(word)
                        word_count += 1
        print(f'Processed {word_count-1} words.')
    return used_words


def analyze_most_used_letters(words, should_print=False):
    letter_count = {}
    letter_index_count = {}
    for word in words:
        for i, letter in enumerate(word):
            # Overall occurrence count
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

            # Occurrence per index count
            if i in letter_index_count:
                index_dict = letter_index_count[i]
                if letter in index_dict:
                    index_dict[letter] += 1
                else:
                    index_dict[letter] = 1
                letter_index_count[i] = index_dict
            else:
                new_dict = {letter: 1}
                letter_index_count[i] = new_dict

    letter_count = fill_alpha_dict(letter_count)
    for i in letter_index_count.keys():
        letter_index_count[i] = fill_alpha_dict(letter_index_count[i])

    if should_print:
        print('#### Overall Results')
        pprint_alpha_dict(letter_count)
        print('#### Per Index Results')
        pprint_2d_alpha_dict(letter_index_count)

    return letter_count, letter_index_count


def fill_alpha_dict(d):
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letter not in d:
            d[letter] = 0
    return d


def pprint_alpha_dict(d):
    d_sorted_key = sorted(d.items(), key=lambda x: x[0])
    d_sorted_val = sorted(d.items(), key=lambda x: x[1], reverse=True)
    for i, key_item in enumerate(d_sorted_key):
        val_item = d_sorted_val[i]
        print("{} = {} {}: {} = {}".format(
            key_item[0], str(key_item[1]).ljust(6), str(i).rjust(3), val_item[0], val_item[1]))


def pprint_2d_alpha_dict(dd):
    for i in dd.keys():
        print(f'  ## Index {i} Results')
        pprint_alpha_dict(dd[i])


def get_words_of_length(n, save=False, output_file=''):
    valid_words = {}
    count = 0
    with open('words_alpha.txt') as word_file:
        if save:
            out = open(output_file, 'w')

        for word in word_file:
            word = word.strip().upper()
            if len(word) == n:
                valid_words[word] = 1
                count += 1
                if save:
                    out.write(word + '\n')
        if save:
            out.close()

    print(f'{count} words of length {n} found')
    return valid_words


def load_words(input_file):
    with open(input_file) as word_file:
        words = set(word_file.read().split())

    return words


def score_word(word, letter_count, letter_index_count):
    score = 0
    for i, letter in enumerate(word):
        score += letter_index_count[i][letter]
    return score


def update_top_x(items, elem, n):
    items.append(elem)
    items = sorted(items, key=lambda x: x[1], reverse=True)
    if len(items) > n:
        items = items[:-1]
    return items


def find_best_words(words, letter_count, letter_index_count, n=10, should_print=False):
    best_words = []
    for word in words:
        word_score = score_word(word, letter_count, letter_index_count)
        best_words = update_top_x(best_words, (word, word_score), n)

    if should_print:
        print(f'Best {n} Words: {best_words}')
    return best_words


if __name__ == '__main__':
    print('Begin wordle_service')
    # wordle_words = get_all_used_words()
    # analyze_most_used_letters(wordle_words)
    # get_words_of_length(5, save=True, output_file='possible_wordle_words.txt')

    possible_wordle_words = load_words('possible_wordle_words.txt')
    analysis = analyze_most_used_letters(get_all_used_words(), should_print=True)
    find_best_words(possible_wordle_words, analysis[0], analysis[1], should_print=True)

    print('End wordle_service')
