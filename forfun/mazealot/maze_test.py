import unittest
from typing import List

from maze import Maze
from maze_pieces import MazePiece, LEFT, UP, RIGHT, DOWN


class TestMaze(unittest.TestCase):

    def test_maze_piece_open_sides(self):
        target = MazePiece(0)
        self.assertEqual([0, 0, 0, 0], target.open_sides)
        target = MazePiece(1)
        self.assertEqual([0, 0, 0, 1], target.open_sides)
        target = MazePiece(4)
        self.assertEqual([0, 1, 0, 0], target.open_sides)
        target = MazePiece(7)
        self.assertEqual([0, 1, 1, 1], target.open_sides)
        target = MazePiece(10)
        self.assertEqual([1, 0, 1, 0], target.open_sides)
        target = MazePiece(15)
        self.assertEqual([1, 1, 1, 1], target.open_sides)

    def test_maze_piece_open_path(self):
        target = MazePiece(0)
        self.assertEqual(0, target.open_path(LEFT))
        self.assertEqual(0, target.open_path(UP))
        self.assertEqual(0, target.open_path(RIGHT))
        self.assertEqual(0, target.open_path(DOWN))
        target = MazePiece(15)
        self.assertEqual(7, target.open_path(LEFT))
        self.assertEqual(11, target.open_path(UP))
        self.assertEqual(13, target.open_path(RIGHT))
        self.assertEqual(14, target.open_path(DOWN))

    def test_maze_piece_close_path(self):
        target = MazePiece(0)
        self.assertEqual(8, target.close_path(LEFT))
        self.assertEqual(4, target.close_path(UP))
        self.assertEqual(2, target.close_path(RIGHT))
        self.assertEqual(1, target.close_path(DOWN))
        target = MazePiece(15)
        self.assertEqual(15, target.close_path(LEFT))
        self.assertEqual(15, target.close_path(UP))
        self.assertEqual(15, target.close_path(RIGHT))
        self.assertEqual(15, target.close_path(DOWN))

    def test_maze_piece_get_grid(self):
        target = MazePiece(0)
        self.assertEqual([[1, 0, 1],
                          [0, 0, 0],
                          [1, 0, 1]], target.get_grid())
        target = MazePiece(15)
        self.assertEqual([[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]], target.get_grid())
        target = MazePiece(6)
        self.assertEqual([[1, 1, 1],
                          [0, 0, 1],
                          [1, 0, 1]], target.get_grid())
        target = MazePiece(10)
        self.assertEqual([[1, 0, 1],
                          [1, 0, 1],
                          [1, 0, 1]], target.get_grid())

    def test_direction_towards_start(self):
        target = Maze()
        self.assertEqual((LEFT, UP), target._direction_towards_start(5, 5))
        self.assertEqual((LEFT, UP), target._direction_towards_start(9, 2))
        self.assertEqual((UP, LEFT), target._direction_towards_start(2, 9))
        self.assertEqual((LEFT, UP), target._direction_towards_start(0, 0))

        target = Maze(start_x_=3, start_y_=9)
        self.assertEqual((DOWN, LEFT), target._direction_towards_start(5, 5))
        self.assertEqual((DOWN, RIGHT), target._direction_towards_start(1, 2))
        self.assertEqual((RIGHT, DOWN), target._direction_towards_start(2, 8))
        self.assertEqual((LEFT, UP), target._direction_towards_start(5, 9))

    def test_make_playable(self):
        fail_count = 0
        for i in range(10, 50):
            m = Maze(i, i, 0, 0, i-1, i-1)
            m.randomize()
            m._make_playable()

            grid = m.grid
            traversed = [[False for _ in range(m.width)] for _ in range(m.height)]
            self._traverse_maze_grid(0, 0, i, i, grid, traversed)

            for row in traversed:
                should_break = False
                for b in row:
                    if not b:
                        should_break = True
                        fail_count += 1
                        break
                if should_break:
                    break

        self.assertEqual(0, fail_count)

    def _traverse_maze_grid(self, x_idx, y_idx, width, height, grid: List[List[int]], traversed):
        if traversed[y_idx][x_idx]:
            return

        traversed[y_idx][x_idx] = True
        cur_val = MazePiece(grid[y_idx][x_idx])

        # To the right
        if x_idx + 1 < width and cur_val.is_open(RIGHT) and MazePiece(grid[y_idx][x_idx + 1]).is_open(LEFT):
            self._traverse_maze_grid(x_idx + 1, y_idx, width, height, grid, traversed)
        # Downward
        if y_idx + 1 < height and cur_val.is_open(DOWN) and MazePiece(grid[y_idx + 1][x_idx]).is_open(UP):
            self._traverse_maze_grid(x_idx, y_idx + 1, width, height, grid, traversed)
        # To the left
        if x_idx - 1 >= 0 and cur_val.is_open(LEFT) and MazePiece(grid[y_idx][x_idx - 1]).is_open(RIGHT):
            self._traverse_maze_grid(x_idx - 1, y_idx, width, height, grid, traversed)
        # Upward
        if y_idx - 1 >= 0 and cur_val.is_open(UP) and MazePiece(grid[y_idx - 1][x_idx]).is_open(DOWN):
            self._traverse_maze_grid(x_idx, y_idx - 1, width, height, grid, traversed)


if __name__ == '__main__':
    unittest.main()
