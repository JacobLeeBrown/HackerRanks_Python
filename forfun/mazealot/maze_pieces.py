import random

# There are 16 possible "pieces" to make a maze grid. The reason for this is
# there are 4 possible entry points to each piece: left, up, right, down.
# Each possible entry is either closed or open, giving us 2^4 options.
# I've chosen to map 0-15 to pieces based on their binary representation, giving
# each bit a corresponding opening in the order of left, up, right down.
# 0 = open, 1 = closed
# So 6 = 0110 corresponds to a 3x3 grid of:
#   1  1  1
#   0  0  1
#   1  0  1
# where the user can enter/exit from the left and bottom.

PIECE_SIZE = 3
PIECE_COUNT = 16

all_pieces = [i for i in range(16)]

open_left = [i for i in range(8)]
open_up = [i for i in range(4)] + [i for i in range(8, 15)]
open_right = [0, 1, 4, 5, 8, 9, 12, 13]
open_down = [i for i in range(0, 15, 2)]

open_left_up = [x for x in all_pieces if x in open_left and x in open_up]
open_up_right = [x for x in all_pieces if x in open_up and x in open_right]
open_right_down = [x for x in all_pieces if x in open_right and x in open_down]
open_down_left = [x for x in all_pieces if x in open_down and x in open_left]

closed_left = [x for x in all_pieces if x not in open_left]
closed_up = [x for x in all_pieces if x not in open_up]
closed_right = [x for x in all_pieces if x not in open_right]
closed_down = [x for x in all_pieces if x not in open_down]

closed_left_up = [x for x in all_pieces if x not in open_left and x not in open_up]
closed_up_right = [x for x in all_pieces if x not in open_up and x not in open_right]
closed_right_down = [x for x in all_pieces if x not in open_right and x not in open_down]
closed_down_left = [x for x in all_pieces if x not in open_down and x not in open_left]

printable_pieces = [
    # 0 = 0000
    [[1, 0, 1],
     [0, 0, 0],
     [1, 0, 1]]
    ,  # 1 = 0001
    [[1, 0, 1],
     [0, 0, 0],
     [1, 1, 1]]
    ,  # 2 = 0010
    [[1, 0, 1],
     [0, 0, 1],
     [1, 0, 1]]
    ,  # 3 = 0011
    [[1, 0, 1],
     [0, 0, 1],
     [1, 1, 1]]
    ,  # 4 = 0100
    [[1, 1, 1],
     [0, 0, 0],
     [1, 0, 1]]
    ,  # 5 = 0101
    [[1, 1, 1],
     [0, 0, 0],
     [1, 1, 1]]
    ,  # 6 = 0110
    [[1, 1, 1],
     [0, 0, 1],
     [1, 0, 1]]
    ,  # 7 = 0111
    [[1, 1, 1],
     [0, 0, 1],
     [1, 1, 1]]
    ,  # 8 = 1000
    [[1, 0, 1],
     [1, 0, 0],
     [1, 0, 1]]
    ,  # 9 = 1001
    [[1, 0, 1],
     [1, 0, 0],
     [1, 1, 1]]
    ,  # 10 = 1010
    [[1, 0, 1],
     [1, 0, 1],
     [1, 0, 1]]
    ,  # 11 = 1011
    [[1, 0, 1],
     [1, 0, 1],
     [1, 1, 1]]
    ,  # 12 = 1100
    [[1, 1, 1],
     [1, 0, 0],
     [1, 0, 1]]
    ,  # 13 = 1101
    [[1, 1, 1],
     [1, 0, 0],
     [1, 1, 1]]
    ,  # 14 = 1110
    [[1, 1, 1],
     [1, 0, 1],
     [1, 0, 1]]
    ,  # 15 = 1111
    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]]
]
# Relative Probability to Randomly Generate a Particular Piece
DEFAULT_PROBABILITIES = [0.2, 0.8, 0.8, 1, 0.8, 1, 1, 0.5, 0.8, 1, 1, 0.5, 1, 0.5, 0.5, 0]


def get_random_piece(p):
    assert len(p) == PIECE_COUNT, f'Probability list is not expected length ({PIECE_COUNT})'
    p_sum = sum(p)
    rand = random.random() * p_sum
    running_sum = 0
    for i, p_ in enumerate(p):
        if (running_sum + p_) > rand:
            return i
        running_sum += p_
    # Should always return by now, but, just in case:
    return random.randint(0, PIECE_COUNT - 1)


