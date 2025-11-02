import csv
from datetime import datetime, timedelta
import re

import file_service as fs

USED_WORDS_CSV_FILE = 'used_words.csv'
USED_WORDS_SORTED_FILE = 'used_words_sorted.txt'
IGNORED_WORDS_FILE = 'ignored_words.txt'

def update_files_with_new_word(word_):
    word_ = word_.upper()
    fs.add_to_file({word_}, USED_WORDS_SORTED_FILE, True)
    fs.add_to_file({word_}, IGNORED_WORDS_FILE, True)

    with open(USED_WORDS_CSV_FILE, newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        last_row = rows[-1] if rows else None

    if last_row is None:
        raise ValueError("CSV is empty?!")

    last_date = datetime.strptime(last_row[0], "%Y-%m-%d").date()
    num_match = re.search('\d+', last_row[1])
    if not num_match:
        raise ValueError("Last row is missing day? " + str(last_row))
    last_day = int(num_match.group())

    new_date = last_date + timedelta(days=1)
    csv_line = f'{new_date},Day {last_day+1},{word_}'
    fs.add_to_file({csv_line}, USED_WORDS_CSV_FILE)

"""
For adding a missed Wordle word to the tracking files.

Parameters:
USED_WORDS_CSV_FILE (str): File name of chronologically ordered CSV. Expected columns are:
    "date" (2025-06-01),
    "number" (Day 1443),
    "word" (ROUGH)
USED_WORDS_SORTED_FILE (str): Simplified version of the CSV, just with the "word" column as a sorted list.
IGNORED_WORDS_FILE (str): Like the used words file, but with additional, unlikely Wordle words.
"""
if __name__ == '__main__':

    while True:
        user_input = input('What word would you like to add? ')
        if user_input == 'q':
            break
        if len(user_input) != 5:
            print('Word must be 5 letters, please try again.')
        else:
            update_files_with_new_word(user_input)
