import unittest
from maze_pieces import MazePiece
from maze_pieces import LEFT, UP, RIGHT, DOWN


class TestMaze(unittest.TestCase):

    def test_maze_piece_open_sides(self):
        target = MazePiece(0)
        self.assertEqual(target.open_sides, [0, 0, 0, 0])
        target = MazePiece(1)
        self.assertEqual(target.open_sides, [0, 0, 0, 1])
        target = MazePiece(4)
        self.assertEqual(target.open_sides, [0, 1, 0, 0])
        target = MazePiece(7)
        self.assertEqual(target.open_sides, [0, 1, 1, 1])
        target = MazePiece(10)
        self.assertEqual(target.open_sides, [1, 0, 1, 0])
        target = MazePiece(15)
        self.assertEqual(target.open_sides, [1, 1, 1, 1])

    def test_maze_piece_open_path(self):
        target = MazePiece(0)
        self.assertEqual(target.open_path(LEFT), 0)
        self.assertEqual(target.open_path(UP), 0)
        self.assertEqual(target.open_path(RIGHT), 0)
        self.assertEqual(target.open_path(DOWN), 0)
        target = MazePiece(15)
        self.assertEqual(target.open_path(LEFT), 7)
        self.assertEqual(target.open_path(UP), 11)
        self.assertEqual(target.open_path(RIGHT), 13)
        self.assertEqual(target.open_path(DOWN), 14)

    def test_maze_piece_get_grid(self):
        target = MazePiece(0)
        self.assertEqual(target.get_grid(), [[1, 0, 1],
                                             [0, 0, 0],
                                             [1, 0, 1]])
        target = MazePiece(15)
        self.assertEqual(target.get_grid(), [[1, 1, 1],
                                             [1, 0, 1],
                                             [1, 1, 1]])
        target = MazePiece(6)
        self.assertEqual(target.get_grid(), [[1, 1, 1],
                                             [0, 0, 1],
                                             [1, 0, 1]])
        target = MazePiece(10)
        self.assertEqual(target.get_grid(), [[1, 0, 1],
                                             [1, 0, 1],
                                             [1, 0, 1]])


if __name__ == '__main__':
    unittest.main()
