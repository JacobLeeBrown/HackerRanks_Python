from collections import deque
import unittest

from maze import Maze
from maze_pieces import *


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
        # Check 20 random mazes (from 10x10 to 29x29) 10 times (200 mazes total)
        for j in range(10):
            for i in range(10, 30):
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

    def test_clean_nubs(self):
        fail_count = 0
        # Check 20 random mazes (from 10x10 to 29x29) 10 times (200 mazes total)
        for j in range(10):
            for i in range(10, 30):
                m = Maze(i, i, 0, 0, i-1, i-1)
                m.randomize()
                m._make_playable()
                m._clean_nubs()

                if self._check_for_nubs(m):
                    fail_count += 1

        self.assertEqual(0, fail_count)

    def test_can_move(self):
        m = Maze(3, 3, 0, 0, 2, 2)
        # Setup specific pieces:
        # (0, 0): piece 0 (all sides open)
        # (1, 0): piece 0 (all sides open)
        # (0, 1): piece 15 (all sides closed)
        # (1, 1): piece 10 (1010 in binary: left=closed, up=open, right=closed, down=open)
        #
        #  X . X X . X
        #  . . . . . .
        #  X . X X . X
        #  X X X X . X
        #  X . X X . X
        #  X X X X . X
        #
        m.grid[0][0] = 0
        m.grid[0][1] = 0
        m.grid[1][0] = 15
        m.grid[1][1] = 10

        # Boundary checks from (0, 0)
        self.assertFalse(m.can_move(0, 0, LEFT))
        self.assertFalse(m.can_move(0, 0, UP))

        # Open passage between (0, 0) and (1, 0)
        self.assertTrue(m.can_move(0, 0, RIGHT))
        self.assertTrue(m.can_move(1, 0, LEFT))

        # Wall collision: (0, 0) is open DOWN, but (0, 1) is closed UP (piece 15)
        self.assertFalse(m.can_move(0, 0, DOWN))
        self.assertFalse(m.can_move(0, 1, UP))

        # Out-of-bounds coordinates
        self.assertFalse(m.can_move(-1, 0, RIGHT))
        self.assertFalse(m.can_move(0, 3, DOWN))

        # Invalid direction
        self.assertFalse(m.can_move(0, 0, 99))

    def test_single_path_to_start(self):
        # Generate a few mazes (both 10x10 and 20x20) and validate using BFS
        # that every cell in the maze has exactly 1 path to the start.
        for size in (10, 20):
            for _ in range(5):
                m = Maze(size, size, 0, 0, size - 1, size - 1)
                m.generate_maze()
                self._validate_single_path_bfs(m)

    def _validate_single_path_bfs(self, m: Maze):
        queue = deque([(m.start_x, m.start_y, None)])
        visited = {(m.start_x, m.start_y): None}

        while queue:
            cx, cy, parent = queue.popleft()
            for d in DIRS:
                if m.can_move(cx, cy, d):
                    dv = DIR_VALS[d]
                    nx, ny = cx + dv[X_MOD], cy + dv[Y_MOD]
                    if (nx, ny) == parent:
                        continue
                    # In an undirected graph, reaching an already visited node
                    # indicates a cycle (multiple paths between start and that cell).
                    self.assertNotIn(
                        (nx, ny), visited,
                        f"Multiple paths found to ({nx}, {ny}) from ({cx}, {cy}) and {visited.get((nx, ny))}"
                    )
                    visited[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny, (cx, cy)))

        total_cells = m.width * m.height
        self.assertEqual(
            len(visited), total_cells,
            f"Not all cells are connected to start: visited {len(visited)} / {total_cells}"
        )

    @staticmethod
    def _check_for_nubs(m: Maze) -> bool:
        for y_idx, row in enumerate(m.grid):
            for x_idx, cell in enumerate(row):
                for d in DIRS:
                    dv = DIR_VALS[d]
                    if MazePiece(cell).is_open(d) and \
                            (not dv[BOUND_FUNC](x_idx, y_idx, m) or
                             MazePiece(m.grid[y_idx + dv[Y_MOD]][x_idx + dv[X_MOD]]).is_closed(dv[OPPOSITE])):
                        return True
        return False


if __name__ == '__main__':
    unittest.main()
