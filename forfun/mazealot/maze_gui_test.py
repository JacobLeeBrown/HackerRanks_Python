import types
import unittest
from maze import Maze
from maze_pieces import LEFT, UP, RIGHT, DOWN
from maze_gui import MazeGui


class TestMazeGui(unittest.TestCase):

    def setUp(self):
        # Create a deterministic 3x3 maze
        # Layout:
        # (0,0)[piece 0: open all] <---> (1,0)[piece 0: open all]   (2,0)[piece 15: solid wall]
        #        |                                |
        #        v                                v
        # (0,1)[piece 15: solid wall]    (1,1)[piece 0: open all]   (2,1)[piece 15: solid wall]
        # (0,2)[piece 15: solid wall]    (1,2)[piece 15: solid wall](2,2)[piece 15: solid wall]
        self.maze = Maze(3, 3, 0, 0, 2, 2)
        self.maze.grid = [
            [0, 0, 15],
            [15, 0, 15],
            [15, 15, 15]
        ]
        self.gui = MazeGui(self.maze)

    def tearDown(self):
        self.gui.root.destroy()

    def test_initial_player_position(self):
        self.assertEqual(self.gui.x_pos, self.maze.start_x)
        self.assertEqual(self.gui.y_pos, self.maze.start_y)
        player_items = self.gui.canvas.find_withtag('player')
        self.assertEqual(len(player_items), 1)

    def test_move_player_open_passages(self):
        # Move RIGHT from (0,0) to (1,0) via direction constant
        moved = self.gui.move_player(RIGHT)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # Move DOWN from (1,0) to (1,1) via (dx, dy)
        moved = self.gui.move_player(0, 1)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 1))

        # Move UP from (1,1) back to (1,0) via UP constant
        moved = self.gui.move_player(UP)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # Move LEFT from (1,0) back to (0,0) via (-1, 0)
        moved = self.gui.move_player(-1, 0)
        self.assertTrue(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

    def test_move_player_wall_collision(self):
        # From (0,0), attempting to move DOWN into piece 15 (solid wall) must fail
        moved = self.gui.move_player(DOWN)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        # From (1,0), attempting to move RIGHT into (2,0)[piece 15] must fail
        self.gui.move_player(RIGHT)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))
        moved = self.gui.move_player(RIGHT)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

    def test_move_player_boundary_collision(self):
        # From (0,0), moving LEFT or UP is blocked by grid boundaries
        moved = self.gui.move_player(LEFT)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        moved = self.gui.move_player(UP)
        self.assertFalse(moved)
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

    def test_key_press_arrow_keys_with_collision(self):
        # Blocked DOWN keypress against wall
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Down'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        # Blocked UP and LEFT against grid bounds
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Up'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Left'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        # Allowed RIGHT keypress
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Right'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # Allowed DOWN keypress from (1,0) to (1,1)
        self.gui._handle_key_press(types.SimpleNamespace(keysym='Down'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 1))

    def test_key_press_asdw_with_collision(self):
        # 's' is blocked down against wall from (0,0)
        self.gui._handle_key_press(types.SimpleNamespace(keysym='s'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (0, 0))

        # 'd' (or 'D') moves right
        self.gui._handle_key_press(types.SimpleNamespace(keysym='D'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # 's' moves down from (1,0) to (1,1)
        self.gui._handle_key_press(types.SimpleNamespace(keysym='s'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 1))

        # 'w' (or 'W') moves up back to (1,0)
        self.gui._handle_key_press(types.SimpleNamespace(keysym='W'))
        self.assertEqual((self.gui.x_pos, self.gui.y_pos), (1, 0))

        # 'a' moves left back to (0,0)
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
        self.gui.move_player(RIGHT)
        self.gui.move_player(DOWN)
        self.gui.move_player(UP)
        player_items = self.gui.canvas.find_withtag('player')
        self.assertEqual(len(player_items), 1)

    def test_is_completed(self):
        # Initially at (0, 0), not at end (2, 2)
        self.assertFalse(self.gui.is_completed())

        # Move to end coordinates
        self.gui.x_pos = self.maze.end_x
        self.gui.y_pos = self.maze.end_y
        self.assertTrue(self.gui.is_completed())

    def test_reset_maze_generates_new_maze_and_resets_player(self):
        orig_maze = self.gui.maze
        self.assertEqual(self.gui.completed_count, 0)

        # Move player away from start
        self.gui.x_pos = 1
        self.gui.y_pos = 1

        self.gui.reset_maze()

        self.assertEqual(self.gui.completed_count, 1)
        self.assertEqual(self.gui.x_pos, self.gui.maze.start_x)
        self.assertEqual(self.gui.y_pos, self.gui.maze.start_y)
        self.assertEqual(self.gui.maze.width, orig_maze.width)
        self.assertEqual(self.gui.maze.height, orig_maze.height)
        self.assertIsNot(self.gui.maze, orig_maze)
        player_items = self.gui.canvas.find_withtag('player')
        self.assertEqual(len(player_items), 1)

    def test_reaching_end_cell_triggers_reset(self):
        # Setup maze where end is along the top edge: (0, 0) -> (1, 0) -> (2, 0)
        end_maze = Maze(3, 3, 0, 0, 2, 0)
        end_maze.grid = [
            [0, 0, 0],
            [15, 15, 15],
            [15, 15, 15]
        ]
        gui = MazeGui(end_maze)
        try:
            self.assertEqual(gui.completed_count, 0)
            self.assertEqual((gui.x_pos, gui.y_pos), (0, 0))

            # Move right to (1, 0) - not yet completed
            moved = gui.move_player(RIGHT)
            self.assertTrue(moved)
            self.assertEqual(gui.completed_count, 0)
            self.assertEqual((gui.x_pos, gui.y_pos), (1, 0))

            # Move right to (2, 0) which is end_x, end_y
            moved = gui.move_player(RIGHT)
            self.assertTrue(moved)

            # Reaching end cell should automatically increment completed_count and reset player to start
            self.assertEqual(gui.completed_count, 1)
            self.assertEqual((gui.x_pos, gui.y_pos), (gui.maze.start_x, gui.maze.start_y))
            self.assertEqual(gui.maze.width, 3)
            self.assertEqual(gui.maze.height, 3)
        finally:
            gui.root.destroy()


if __name__ == '__main__':
    unittest.main()
