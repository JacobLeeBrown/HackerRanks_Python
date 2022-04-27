
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


def analyze_most_used_letters(words):
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

    print('#### Overall Results')
    pprint_alpha_dict(letter_count)
    print('#### Per Index Results')
    pprint_2d_alpha_dict(letter_index_count)


def pprint_alpha_dict(d):
    # Fill dict
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letter not in d:
            d[letter] = 0

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


def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


if __name__ == '__main__':
    print('Begin wordle_service')
    wordle_words = get_all_used_words()
    analyze_most_used_letters(wordle_words)
    print('End wordle_service')
