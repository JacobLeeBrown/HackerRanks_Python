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

PIECE_SIZE = 3
PIECE_COUNT = 16
# Relative Probability to Randomly Generate a Particular Piece
DEFAULT_PROBABILITIES = [0.2, 0.8, 0.8, 1, 0.8, 1, 1, 0.5, 0.8, 1, 1, 0.5, 1, 0.5, 0.5, 0]


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


LEFT, UP, RIGHT, DOWN = (0, 1, 2, 3)
SIDE_COUNT = 4


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

