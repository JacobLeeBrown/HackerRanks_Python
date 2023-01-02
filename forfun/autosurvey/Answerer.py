import csv
from typing import List

CSV_SEPARATOR = ','
VAL_SEPARATOR = '|'
DB_FILE = 'question_db.txt'


class Answerer:

    question_db = {}

    def __init__(self, input_file=DB_FILE):
        with open(input_file, mode='r') as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                questions = str(row['questions']).split(VAL_SEPARATOR)
                answers = str(row['answers']).split(VAL_SEPARATOR)
                for q in questions:
                    self.question_db[q] = answers

    def get_answers(self, q: str):
        if q in self.question_db:
            return self.question_db[q]
        return []

    def add_new_question(self, q: str, a: List[str], output_file=DB_FILE):
        self.question_db[q] = a
        output_row = q + ',' + VAL_SEPARATOR.join(a)
        with open(output_file, mode='a') as f:
            f.write(output_row)

    def add_similar_question(self, q_orig: str, q_new: str, target_file=DB_FILE):
        a = self.question_db[q_orig]
        self.question_db[q_new] = a
        lines = []
        with open(target_file, mode='r') as f:
            for line in f:
                if q_orig in line:
                    vals = line.split(CSV_SEPARATOR)
                    new_line = vals[0] + VAL_SEPARATOR + q_new + CSV_SEPARATOR + vals[1]
                    lines.append(new_line)
                else:
                    lines.append(line)
        with open(target_file, mode='w') as f:
            f.writelines(lines)

    def add_answers(self, q: str, a_new: List[str], target_file=DB_FILE):
        answers = self.question_db[q]
        for a in a_new:
            answers.append(a)
        lines = []
        with open(target_file, mode='r') as f:
            for line in f:
                if q in line:
                    vals = line.split(CSV_SEPARATOR)
                    new_line = vals[0] + CSV_SEPARATOR + VAL_SEPARATOR.join(a)
                    for _q in vals[0].split(VAL_SEPARATOR):
                        self.question_db[_q] = answers
                    lines.append(new_line)
                else:
                    lines.append(line)
        with open(target_file, mode='w') as f:
            f.writelines(lines)

    def add_new_question_cli(self, q: str):
        print('No answers for question: ' + q)
        user_input = input('Is this similar to an existing question? Y or N? ')
        if user_input.lower() in ('y', 'yes'):
            while (user_input not in self.question_db) and (user_input.lower() not in ('q', 'quit')):
                user_input = input('What question is similar?\n')
            if user_input.lower() not in ('q', 'quit'):
                print('Let\' try again...')
                self.add_new_question_cli(q)
                return
            self.add_similar_question(user_input, q)
        else:
            print('Please enter answers in descending priority, pipe (|) delimited:')
            a_str = input()
            self.add_new_question(q, a_str.split(VAL_SEPARATOR))

