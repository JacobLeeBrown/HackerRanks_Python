import maze
from maze_gui import MazeGui
import tkinter as tk


def basic_maze():
    m = maze.Maze(30, 10, 0, 0, 29, 9)
    m.generate_maze(True)
    print('~~~~ Grid:')
    m.print_grid()
    print()
    print('~~~~ Maze:')
    m.print_maze()


if __name__ == "__main__":
    # basic_maze()
    m = MazeGui()
    m.play()
