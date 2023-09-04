from maze import Maze, OPEN, WALL
from maze_pieces import PIECE_SIZE
import tkinter as tk


GRID_PIXEL_SIZE = 10
WHITE = 'white'
BLACK = 'black'
RED = 'red'


class MazeGui(object):

    def __init__(self, width_=10, height_=10,
                 start_x_=0, start_y_=0,
                 end_x_=9, end_y_=9,
                 background_color_=WHITE,
                 wall_color_=BLACK,
                 accent_color_=RED):
        """
        Parameters
        ----------
        @see maze.py
        """

        m = Maze(width_, height_, start_x_, start_y_, end_x_, end_y_)
        m.generate_maze()
        self.maze = m

        self.width = width_ * PIECE_SIZE * GRID_PIXEL_SIZE
        self.height = width_ * PIECE_SIZE * GRID_PIXEL_SIZE

        self.background_color = background_color_
        self.wall_color = wall_color_
        self.accent_color = accent_color_

        self.root = tk.Tk()
        self.root.title("Maze 4 Dayz")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.background_color)
        self.canvas.pack()
        self._draw_maze()

    def play(self):
        self.root.mainloop()

    def _draw_maze(self):
        c = self.canvas
        m = self.maze.convert_grid()

        for j, row in enumerate(m):
            for i, cell in enumerate(row):
                if cell is WALL:
                    c.create_rectangle(i * GRID_PIXEL_SIZE, j * GRID_PIXEL_SIZE,
                                       (i + 1) * GRID_PIXEL_SIZE, (j + 1) * GRID_PIXEL_SIZE,
                                       fill=self.wall_color)


# Example Tkinter code:
#
# Constants
# CANVAS_WIDTH = 400
# CANVAS_HEIGHT = 400
# PIXEL_SIZE = 10
# ROWS = CANVAS_HEIGHT // PIXEL_SIZE
# COLS = CANVAS_WIDTH // PIXEL_SIZE

# Function to handle a pixel click event
# def handle_click(event):
#     x, y = event.x, event.y
#     row = y // PIXEL_SIZE
#     col = x // PIXEL_SIZE
#     canvas.create_rectangle(col * PIXEL_SIZE, row * PIXEL_SIZE,
#                             (col + 1) * PIXEL_SIZE, (row + 1) * PIXEL_SIZE,
#                             fill="black")
#
# # Create the main window
# root = tk.Tk()
# root.title("Programmable Pixel Canvas")
#
# # Create a canvas
# canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
# canvas.pack()
#
# # Bind mouse click events to the canvas
# canvas.bind("<Button-1>", handle_click)
#
# # Run the Tkinter main loop
# root.mainloop()

# def run_gui():
#     # Create the main window
#     root = tk.Tk()
#     root.title("Simple GUI")
#
#     # Create widgets (GUI components)
#     label = tk.Label(root, text="Enter your name:")
#     entry = tk.Entry(root)
#
#     def on_button_click():
#         label.config(text="Hello, " + entry.get())
#
#     button = tk.Button(root, text="Submit", command=on_button_click)
#
#     # Layout widgets using the grid geometry manager
#     label.grid(row=0, column=0, padx=10, pady=10)
#     entry.grid(row=0, column=1, padx=10, pady=10)
#     button.grid(row=1, columnspan=2, padx=10, pady=10)
#
#     # Start the GUI event loop
#     root.mainloop()
