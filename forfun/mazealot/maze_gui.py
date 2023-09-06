from maze import Maze, OPEN, WALL
from maze_pieces import PIECE_SIZE
import tkinter as tk


GRID_PIXEL_SIZE = 10
MARKER_PIXEL_SIZE = 6
PX_DIFF = GRID_PIXEL_SIZE - MARKER_PIXEL_SIZE
WHITE = 'white'
BLACK = 'black'
RED = 'red'
BLUE = 'blue'
GREEN = 'green'


class MazeGui(object):

    TITLE = 'Maze 4 Dayz'

    def __init__(self, width_=10, height_=10,
                 start_x_=0, start_y_=0,
                 end_x_=9, end_y_=9,
                 background_color_=WHITE,
                 wall_color_=BLACK,
                 accent_color_=RED,
                 title_=TITLE):
        """
        Parameters
        ----------
        @see maze.py
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
        background_color_: String
            The color of open spaces.
        wall_color_: String
            The color of wall spaces.
        accent_color_: String
            The color of accent elements.
        title_: String
            The title of the canvas window.
        """

        m = Maze(width_, height_, start_x_, start_y_, end_x_, end_y_)
        m.generate_maze()
        self.maze = m

        self.width = width_ * PIECE_SIZE * GRID_PIXEL_SIZE
        self.height = height_ * PIECE_SIZE * GRID_PIXEL_SIZE

        self.background_color = background_color_
        self.wall_color = wall_color_
        self.accent_color = accent_color_

        self.root = tk.Tk()
        self.title = title_
        self.root.title(self.title)
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.background_color)
        self.canvas.pack()
        self._draw_maze()

    def __init__(self, maze_: Maze,
                 background_color_=WHITE,
                 wall_color_=BLACK,
                 accent_color_=RED,
                 title_=TITLE):
        """
        Parameters
        ----------
        maze_ : Maze
            An existing Maze object to instantiate this GUI to.
        background_color_: String
            The color of open spaces.
        wall_color_: String
            The color of wall spaces.
        accent_color_: String
            The color of accent elements.
        title_: String
            The title of the canvas window.
        """

        self.maze = maze_

        self.width = maze_.width * PIECE_SIZE * GRID_PIXEL_SIZE
        self.height = maze_.height * PIECE_SIZE * GRID_PIXEL_SIZE

        self.background_color = background_color_
        self.wall_color = wall_color_
        self.accent_color = accent_color_

        self.root = tk.Tk()
        self.title = title_
        self.root.title(self.title)
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.background_color)
        self.canvas.pack()
        self._draw_maze()

    def play(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()

    def _draw_maze(self):
        c = self.canvas
        m = self.maze.convert_grid()

        for j, row in enumerate(m):
            for i, cell in enumerate(row):
                if cell is WALL:
                    c.create_rectangle(i * GRID_PIXEL_SIZE, j * GRID_PIXEL_SIZE,
                                       (i + 1) * GRID_PIXEL_SIZE, (j + 1) * GRID_PIXEL_SIZE,
                                       fill=self.wall_color)

        self._draw_marker(self.maze.start_x * PIECE_SIZE + 1, self.maze.start_y * PIECE_SIZE + 1, BLUE)
        self._draw_marker(self.maze.end_x * PIECE_SIZE + 1, self.maze.end_y * PIECE_SIZE + 1, GREEN)

    def _draw_marker(self, x_idx, y_idx, color):
        ref_x = x_idx * GRID_PIXEL_SIZE + (PX_DIFF / 2)
        ref_y = y_idx * GRID_PIXEL_SIZE + (PX_DIFF / 2)
        self.canvas.create_oval(ref_x, ref_y,
                                ref_x + MARKER_PIXEL_SIZE,
                                ref_y + MARKER_PIXEL_SIZE,
                                fill=color)


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

# import tkinter as tk
# from tkinter import Canvas
# from PIL import Image, ImageDraw
#
# # Create the main window
# root = tk.Tk()
# root.title("Export Canvas as PNG")
#
# # Create a canvas
# canvas = Canvas(root, width=400, height=400, bg="white")
# canvas.pack()
#
# # Draw something on the canvas (for demonstration)
# canvas.create_rectangle(50, 50, 350, 350, fill="blue")
#
# # Function to export the canvas as PNG
# def export_as_png():
#     # Capture the canvas content as PostScript data
#     ps_data = canvas.postscript(colormode="color")
#
#     # Convert PostScript data to an Image object
#     img = Image.open(io.BytesIO(ps_data.encode("utf-8")))
#
#     # Save the Image object as a PNG file
#     img.save("canvas.png")
#
# # Create a button to trigger export
# export_button = tk.Button(root, text="Export as PNG", command=export_as_png)
# export_button.pack()
#
# # Run the Tkinter main loop
# root.mainloop()