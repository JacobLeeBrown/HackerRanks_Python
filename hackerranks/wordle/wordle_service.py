
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


if __name__ == '__main__':
    print('Begin wordle_service')
    # wordle_words = get_all_used_words()
    # was.analyze_most_used_letters(wordle_words)
    # fs.get_words_of_length(input_file='scrabble_dict.txt', n=5, alpha_only=True, save=True, output_file='possible_wordle_words.txt')

    possible_wordle_words = fs.load_words('possible_wordle_words.txt')
    analysis = was.analyze_most_used_letters(get_all_used_words(), should_print=True)
    was.find_best_words(possible_wordle_words, analysis[0], analysis[1], should_print=True)

    print('End wordle_service')
