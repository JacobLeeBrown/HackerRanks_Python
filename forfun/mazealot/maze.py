class Maze(object):

    def __init__(self, width_=10, height_=10,
                 start_x_=0, start_y_=0,
                 end_x_=10, end_y_=10):
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
        assert (self.width > 0), f'Width ({self.width}) is not positive!'
        assert (self.height > 0), f'Height ({self.height}) is not positive!'

        # Verify starting position is along the edge of the maze
        if (self.start_x not in (0, self.width) and
                self.start_y not in (0, self.height)):
            assert False, f'Starting position ({self.start_x}, {self.start_y}) not on edge!'

        # Verify ending position is along the edge of the maze
        if (self.end_x not in (0, self.width) and
                self.end_y not in (0, self.height)):
            assert False, f'Ending position ({self.end_x}, {self.end_y}) not on edge!'

        # Verify ending position is not too close to starting position
        if (self.start_x in range(self.end_x - 1, self.end_x + 2) and
                self.start_y in range(self.end_y - 1, self.end_y + 2)):
            assert False, f'Starting position ({self.start_x}, {self.start_y}) too close to ending position ({self.end_x}, {self.end_y})! ' \
                          f'They need to be at least 2 spaces apart.'

    def generate_maze(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        traversed = [[False for _ in range(self.width)] for _ in range(self.height)]
        # Will need another 2d array to track "turns" -> Will only want at most 3 exits per turn position
        # Will need to direct original path from start to end,
        #   then make branching paths off of that path that terminate
        # Need to determine how best to "fill in" total space of maze



