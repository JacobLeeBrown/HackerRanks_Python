import random
from typing import List

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

# Reference List
#             1 0 1              1 0 1              1 0 1              1 0 1
#  0 = 0000 = 0 0 0   1 = 0001 = 0 0 0   2 = 0010 = 0 0 1   3 = 0011 = 0 0 1
#             1 0 1              1 1 1              1 0 1              1 1 1
#
#             1 1 1              1 1 1              1 1 1              1 1 1
#  4 = 0100 = 0 0 0   5 = 0101 = 0 0 0   6 = 0110 = 0 0 1   7 = 0111 = 0 0 1
#             1 0 1              1 1 1              1 0 1              1 1 1
#
#             1 0 1              1 0 1              1 0 1              1 0 1
#  8 = 1000 = 1 0 0   9 = 1001 = 1 0 0  10 = 1010 = 1 0 1  11 = 1011 = 1 0 1
#             1 0 1              1 1 1              1 0 1              1 1 1
#
#             1 1 1              1 1 1              1 1 1              1 1 1
# 12 = 1100 = 1 0 0  13 = 1101 = 1 0 0  14 = 1110 = 1 0 1  15 = 1111 = 1 0 1
#             1 0 1              1 1 1              1 0 1              1 1 1


PIECE_SIZE = 3
PIECE_COUNT = 16
# Relative Probability to Randomly Generate a Particular Piece
#                          0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15
DEFAULT_PROBABILITIES = [0.1, 0.4, 0.4, 1.0, 0.4, 1.0, 1.0, 0.8, 0.4, 1.0, 1.0, 0.8, 1.0, 0.8, 0.8, 0.0]


def get_random_piece(p) -> int:
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


# Bound Functions: Given an x-coord, y-coord, and Maze, returns if you can move
# in the respective direction.

# noinspection PyUnusedLocal
def left_bound_func(x: int, y: int, m) -> bool:
    return x - 1 >= 0


# noinspection PyUnusedLocal
def up_bound_func(x: int, y: int, m) -> bool:
    return y - 1 >= 0


# noinspection PyUnusedLocal
def right_bound_func(x: int, y: int, m) -> bool:
    return x + 1 < m.width


# noinspection PyUnusedLocal
def down_bound_func(x: int, y: int, m) -> bool:
    return y + 1 < m.height


LEFT, UP, RIGHT, DOWN = (0, 1, 2, 3)
# For a given direction, what is the x-modifier, y-modifier, opposite direction,
# and applicable bound function?
X_MOD, Y_MOD, OPPOSITE, BOUND_FUNC = (0, 1, 2, 3)
DIR_VALS = {
    LEFT: [-1, 0, RIGHT, left_bound_func],
    UP: [0, -1, DOWN, up_bound_func],
    RIGHT: [1, 0, LEFT, right_bound_func],
    DOWN: [0, 1, UP, down_bound_func]
}
DIRS = DIR_VALS.keys()
SIDE_COUNT = len(DIRS)

OPEN, WALL = (0, 1)


class MazePiece(object):

    def __init__(self, piece_id: int):
        self.piece_id = piece_id
        self.open_sides = self._get_open_sides()

    def _get_open_sides(self) -> List[int]:
        # Basically converting to binary
        res = [0, 0, 0, 0]
        rem = self.piece_id
        for i in range(SIDE_COUNT-1, -1, -1):
            if rem % 2 == 1:
                res[i] = 1
                rem -= 1
            rem /= 2
        return res

    def open_path(self, direction: int) -> int:
        if self.open_sides[direction] == 0:
            return self.piece_id
        return self.piece_id - (2 ** (SIDE_COUNT - 1 - direction))

    def close_path(self, direction: int) -> int:
        if self.open_sides[direction] == 1:
            return self.piece_id
        return self.piece_id + (2 ** (SIDE_COUNT - 1 - direction))

    def get_grid(self) -> List[List[int]]:
        return [[1, self.open_sides[UP], 1],
                [self.open_sides[LEFT], 0, self.open_sides[RIGHT]],
                [1, self.open_sides[DOWN], 1]]

    def is_open(self, direction: int) -> bool:
        return self.open_sides[direction] == 0

    def is_closed(self, direction: int) -> bool:
        return self.open_sides[direction] == 1
