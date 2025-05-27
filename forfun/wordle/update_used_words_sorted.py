import csv

USED_WORDS_CSV_FILE = 'used_words.csv'
USED_WORDS_SORTED_FILE = 'used_words_sorted.txt'


def sort_and_write(lines, output_path):
    with open(output_path, "w") as outfile:
        for line in sorted(lines):
            outfile.write(line)

"""
For updating an alphabetically sorted word file from a chronologically ordered CSV.

Parameters:
USED_WORDS_CSV_FILE (str): File name of chronologically ordered CSV with "word" column. Must be in this script's working 
directory.
USED_WORDS_SORTED_FILE (str): Target file to write the alphabetically sorted words from the CSV.
"""
if __name__ == '__main__':
    in_ = USED_WORDS_CSV_FILE
    out_ = USED_WORDS_SORTED_FILE

    lines_ = []
    with open(in_, mode='r') as f_in:
        csv_reader = csv.DictReader(f_in)
        for row in csv_reader:
            lines_.append(row['word'] + '\n')

    sort_and_write(lines_, out_)
    print(f'Wrote {len(lines_)} words to {out_}')