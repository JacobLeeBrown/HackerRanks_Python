import maze_pieces as mp
from maze_pieces import LEFT, UP, DOWN, RIGHT


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
            assert False, f'Starting position ({self.start_x}, {self.start_y}) too close to ending position ({self.end_x}, {self.end_y})! ' \
                          f'They need to be at least 2 spaces apart.'

    def generate_maze(self):
        # Algorithm:
        #   Randomly assign maze_pieces to grid
        #   Traverse entire grid, making sure each spot connects to start
        #       Can recursively track spots that do connect, then spots that
        #       don't connect just need to connect to ones that do.
        pass

    def randomize(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = mp.get_random_piece(mp.DEFAULT_PROBABILITIES)

    def _convert_grid(self):
        printable_grid = []
        for row in self.grid:
            for i in range(mp.PIECE_SIZE):
                printable_row = []
                for cell in row:
                    piece = mp.MazePiece(cell)
                    printable_row += piece.get_grid()[i]
                printable_grid.append(printable_row)
        return printable_grid

    def print_grid(self):
        for row in self.grid:
            print(row)

    def print_maze(self, open_char=' ', wall_char='#'):
        printable_grid = self._convert_grid()
        width = len(printable_grid[0])
        print(''.join('#' for _ in range(width + 2)))
        for row in printable_grid:
            print('#', end='')
            for elem in row:
                print(open_char if elem == 0 else wall_char, end='')
            print('#')
        print(''.join('#' for _ in range(width + 2)))

    def _make_playable(self):
        path_to_start = [[False for _ in range(self.width)] for _ in range(self.height)]
        path_to_start[self.start_y][self.start_x] = True

        for i in range(self.height):
            for j in range(self.width):
                if not path_to_start[i][j]:
                    pass

    def _connect_to_start(self, x_idx: int, y_idx: int,
                          path_to_start):
        cur_val = mp.MazePiece(self.grid[y_idx][x_idx])
        # First check if any nearby piece connects to start
        # To the right
        if (x_idx + 1) < self.width and path_to_start[y_idx][x_idx + 1]:
            right_val = mp.MazePiece(self.grid[y_idx][x_idx + 1])
            self.grid[y_idx][x_idx] = cur_val.open_path(RIGHT)
            self.grid[y_idx][x_idx + 1] = right_val.open_path(LEFT)
        # Downward
        if (y_idx + 1) < self.height and path_to_start[y_idx + 1][x_idx]:
            down_val = mp.MazePiece(self.grid[y_idx + 1][x_idx])
            self.grid[y_idx][x_idx] = cur_val.open_path(DOWN)
            self.grid[y_idx + 1][x_idx] = down_val.open_path(UP)
        # To the left
        if (x_idx - 1) >= 0 and path_to_start[y_idx][x_idx - 1]:
            left_val = mp.MazePiece(self.grid[y_idx][x_idx - 1])
            self.grid[y_idx][x_idx] = cur_val.open_path(LEFT)
            self.grid[y_idx][x_idx - 1] = left_val.open_path(RIGHT)
        # Upward
        if (y_idx - 1) >= 0 and path_to_start[y_idx - 1][x_idx]:
            up_val = mp.MazePiece(self.grid[y_idx - 1][x_idx])
            self.grid[y_idx][x_idx] = cur_val.open_path(UP)
            self.grid[y_idx - 1][x_idx] = up_val.open_path(DOWN)

        # If no connecting space connects to start, then work towards start

