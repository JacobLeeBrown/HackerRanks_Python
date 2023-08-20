import unittest
from maze_pieces import MazePiece


class TestMaze(unittest.TestCase):

    def test_maze_piece_open_side(self):
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


if __name__ == '__main__':
    unittest.main()
