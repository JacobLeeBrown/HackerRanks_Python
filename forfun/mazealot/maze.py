from typing import Tuple

from maze_pieces import *
import random


class Maze(object):

    def __init__(self, width_=10, height_=10,
                 start_x_=0, start_y_=0,
                 end_x_=9, end_y_=9):
        """
        Parameters
        ----------
        width_ : int
            Width of the playable area of the maze (not including outer bounds).
        height_ : int
            Height of the maze.
        start_x_ : int
            X-coordinate of starting spot of maze. Zero being left most playable
            column.
        start_y_ : int
            Y-coordinate of starting spot of maze. Zero being top most playable
            row.
        end_x_ : int
            X-coordinate of ending spot of maze. Zero being left most playable
            column.
        end_y_ : int
            Y-coordinate of ending spot of maze. Zero being top most playable
            row.
        """
        self.width = width_
        self.height = height_
        self.start_x = start_x_
        self.start_y = start_y_
        self.end_x = end_x_
        self.end_y = end_y_

        self._verify()

        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _verify(self):
        # Verify map bounds are valid
        assert (self.width >= 3), f'Width ({self.width}) is too small!'
        assert (self.height >= 3), f'Height ({self.height}) is too small!'

        # Verify starting position is along the edge of the maze
        if (self.start_x not in (0, self.width-1) and
                self.start_y not in (0, self.height-1)):
            assert False, f'Starting position ({self.start_x}, {self.start_y}) not on edge!'

        # Verify ending position is along the edge of the maze
        if (self.end_x not in (0, self.width-1) and
                self.end_y not in (0, self.height-1)):
            assert False, f'Ending position ({self.end_x}, {self.end_y}) not on edge!'

        # Verify ending position is not too close to starting position
        if (self.start_x in range(self.end_x - 1, self.end_x + 2) and
                self.start_y in range(self.end_y - 1, self.end_y + 2)):
            assert False, f'Starting position ({self.start_x}, {self.start_y}) too close to ending position ' \
                          f'({self.end_x}, {self.end_y})! ' \
                          f'They need to be at least 2 spaces apart.'

    def generate_maze(self, should_print=False):
        self.randomize()
        if should_print:
            print('Before making playable:')
            print('~~~~ Grid:')
            self.print_grid()
            print('~~~~ Maze:')
            self.print_maze()
        self._make_playable()
        self._post_process()

    def randomize(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = get_random_piece(DEFAULT_PROBABILITIES)

    def convert_grid(self):
        printable_grid = []
        for row in self.grid:
            for i in range(PIECE_SIZE):
                printable_row = []
                for cell in row:
                    piece = MazePiece(cell)
                    printable_row += piece.get_grid()[i]
                printable_grid.append(printable_row)
        return printable_grid

    def print_grid(self):
        for row in self.grid:
            print(row)

    def print_maze(self, open_char=' ', wall_char='#'):
        printable_grid = self.convert_grid()
        width = len(printable_grid[0])
        print(''.join('#' for _ in range(width + 2)))
        for row in printable_grid:
            print('#', end='')
            for elem in row:
                print(open_char if elem == OPEN else wall_char, end='')
            print('#')
        print(''.join('#' for _ in range(width + 2)))

    def _make_playable(self):
        path_to_start = self._init_path_to_start()

        # To improve general maze generation, rather than iterate through all
        # cells in a start-to-end fashion, randomly pick cells to connect to
        # the start
        coords = []
        for y_ in range(self.height):
            for x_ in range(self.width):
                coords.append((x_, y_))

        while len(coords) > 0:
            rand_idx = random.randint(0, len(coords)-1)
            x_pos, y_pos = coords.pop(rand_idx)
            if not path_to_start[y_pos][x_pos]:
                traversed = [[False for _ in range(self.width)] for _ in range(self.height)]
                self._connect_to_start(x_pos, y_pos, path_to_start, traversed)

    def _connect_to_start(self, x_idx: int, y_idx: int,
                          path_to_start, traversed):
        cur_val = MazePiece(self.grid[y_idx][x_idx])
        # No matter what, this piece will connect to start after code executes
        path_to_start[y_idx][x_idx] = True

        # First check if any nearby piece connects to start
        for d in DIRS:
            dv = DIR_VALS[d]
            if self._connect_to_start_check(x_idx, y_idx, d, path_to_start, traversed):
                next_val = MazePiece(self.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]])
                self.grid[y_idx][x_idx] = cur_val.open_path(d)
                self.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]] = next_val.open_path(dv[OPPOSITE])
                return

        # If no connecting space connects to start, then work towards start
        traversed[y_idx][x_idx] = True
        d1, d2 = self._direction_towards_start_rand(x_idx, y_idx)
        dir_to_start = d1 if DIR_VALS[d1][BOUND_FUNC](x_idx, y_idx, self) else d2

        dv = DIR_VALS[dir_to_start]
        next_val = MazePiece(self.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]])
        self.grid[y_idx][x_idx] = cur_val.open_path(dir_to_start)
        self.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]] = next_val.open_path(dv[OPPOSITE])
        self._connect_to_start(x_idx + dv[X_MOD], y_idx + dv[Y_MOD], path_to_start, traversed)

    def _connect_to_start_check(self, x_idx: int, y_idx: int,
                                direction: int, path_to_start,
                                traversed):
        dv = DIR_VALS[direction]
        return dv[BOUND_FUNC](x_idx, y_idx, self) and \
            path_to_start[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]] and \
            not traversed[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]]

    def _direction_towards_start_rand(self, x_idx: int, y_idx: int, weight=0.5) -> Tuple[int, int]:
        dir1, dir2 = self._direction_towards_start(x_idx, y_idx)
        # Add a little randomness
        if random.random() <= weight:
            return dir1, dir2
        else:
            return dir2, dir1

    def _direction_towards_start(self, x_idx: int, y_idx: int) -> Tuple[int, int]:
        x_diff = x_idx - self.start_x
        y_diff = y_idx - self.start_y

        if abs(x_diff) >= abs(y_diff):
            # Primary direction is RIGHT or LEFT
            if x_diff < 0:
                dir1 = RIGHT
            else:
                dir1 = LEFT
            # Secondary direction is DOWN or UP
            if y_diff < 0:
                dir2 = DOWN
            else:
                dir2 = UP
        else:
            # Primary direction is DOWN or UP
            if y_diff < 0:
                dir1 = DOWN
            else:
                dir1 = UP
            # Secondary direction is RIGHT or LEFT
            if x_diff < 0:
                dir2 = RIGHT
            else:
                dir2 = LEFT

        return dir1, dir2

    def _init_path_to_start(self):
        path_to_start = [[False for _ in range(self.width)] for _ in range(self.height)]
        # DFS from start
        self._init_path_to_start_r(self.start_x, self.start_y, path_to_start)
        return path_to_start

    def _init_path_to_start_r(self, x_idx, y_idx, path_to_start):
        if path_to_start[y_idx][x_idx]:
            return

        path_to_start[y_idx][x_idx] = True

        for d in DIRS:
            dv = DIR_VALS[d]
            if self._can_move_check(x_idx, y_idx, d):
                self._init_path_to_start_r(
                    x_idx + dv[X_MOD],
                    y_idx + dv[Y_MOD],
                    path_to_start
                )

    def _can_move_check(self, x_idx: int, y_idx: int, direction: int) -> bool:
        cur_piece = MazePiece(self.grid[y_idx][x_idx])
        dv = DIR_VALS[direction]
        return dv[BOUND_FUNC](x_idx, y_idx, self) and \
            cur_piece.is_open(direction) and \
            MazePiece(self.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]]).is_open(dv[OPPOSITE])

    def _post_process(self):
        # Cleans up "nubs"; the paths from pieces that run into the walls of adjacent pieces
        self._clean_nubs()

        # Open start and end spots to the edge
        self._open_to_edge(self.start_x, self.start_y)
        self._open_to_edge(self.end_x, self.end_y)

    def _clean_nubs(self):
        for y_idx, row in enumerate(self.grid):
            for x_idx, cell in enumerate(row):
                cur_piece = MazePiece(cell)
                for d in DIRS:
                    dv = DIR_VALS[d]
                    if cur_piece.is_open(d) and \
                            (not dv[BOUND_FUNC](x_idx, y_idx, self) or
                             MazePiece(self.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]]).is_closed(dv[OPPOSITE])):
                        cur_piece = MazePiece(cur_piece.close_path(d))
                self.grid[y_idx][x_idx] = cur_piece.piece_id

    def _open_to_edge(self, x_idx, y_idx):
        cur_piece = MazePiece(self.grid[y_idx][x_idx])
        if y_idx == 0:
            self.grid[y_idx][x_idx] = cur_piece.open_path(UP)
        elif y_idx == self.height - 1:
            self.grid[y_idx][x_idx] = cur_piece.open_path(DOWN)
        elif x_idx == 0:
            self.grid[y_idx][x_idx] = cur_piece.open_path(LEFT)
        elif x_idx == self.width - 1:
            self.grid[y_idx][x_idx] = cur_piece.open_path(RIGHT)
