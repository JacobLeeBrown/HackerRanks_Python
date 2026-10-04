import types
import unittest
from maze import Maze
from maze_gui import MazeGui


class TestMazeGui(unittest.TestCase):

    def setUp(self):
        # Create a small 5x5 maze for fast testing
        self.maze = Maze(5, 5, 0, 0, 4, 4)
        self.maze.generate_maze()
        self.gui = MazeGui(self.maze)

    def tearDown(self):
        self.gui.root.destroy()

    def test_initial_player_position(self):
        self.assertEqual(self.gui.x_pos, self.maze.start_x)
        self.assertEqual(self.gui.y_pos, self.maze.start_y)
        player_items = self.gui.canvas.find_withtag('player')
        self.assertEqual(len(player_items), 1)

    def test_move_player_free_movement(self):
        # Initial pos is (0, 0)
        # Move right
        moved = self.gui.move_player(1, 0)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # Move down
        moved = self.gui.move_player(0, 1)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 1))

        # Move left
        moved = self.gui.move_player(-1, 0)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 1))

        # Move up
        moved = self.gui.move_player(0, -1)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

    def test_boundary_clamping(self):
        # Try moving up and left from (0, 0) - should stay at (0, 0)
        moved = self.gui.move_player(-1, 0)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        moved = self.gui.move_player(0, -1)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        # Move to bottom right corner (4, 4)
        self.gui.move_player(4, 4)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (4, 4))

        # Moving beyond max bounds should stay clamped
        moved = self.gui.move_player(1, 0)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (4, 4))

        moved = self.gui.move_player(0, 1)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (4, 4))

    def test_key_press_arrow_keys(self):
        # From (0, 0), press Down
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Down'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 1))

        # Press Right
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Right'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 1))

        # Press Up
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Up'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # Press Left
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Left'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

    def test_key_press_asdw_lowercase_and_uppercase(self):
        # 's' = Down
        self.gui._handle_key_press(types.SimpleNamespace(keysym='s'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 1))

        # 'D' = Right (uppercase)
        self.gui._handle_key_press(types.SimpleNamespace(keysym='D'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 1))

        # 'W' = Up (uppercase)
        self.gui._handle_key_press(types.SimpleNamespace(keysym='W'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # 'a' = Left
        self.gui._handle_key_press(types.SimpleNamespace(keysym='a'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

    def test_key_press_unmapped_key(self):
        # Pressing unmapped keys should not change position
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Return'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        self.gui._handle_key_press(types.SimpleNamespace(keysym='space'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

    def test_player_tag_redraw(self):
        # Ensure only 1 player item exists after multiple moves
        self.gui.move_player(1, 0)
        self.gui.move_player(0, 1)
        self.gui.move_player(-1, 0)
        player_items = self.gui.canvas.find_withtag('player')
        self.assertEqual(len(player_items), 1)


if __name__ == '__main__':
    unittest.main()
