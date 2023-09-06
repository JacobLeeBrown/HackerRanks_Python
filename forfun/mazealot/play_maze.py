from maze import Maze
from maze_gui import MazeGui
import time
import tkinter as tk


def basic_maze():
    m = Maze(30, 10, 0, 0, 29, 9)
    m.generate_maze(True)
    print('~~~~ Grid:')
    m.print_grid()
    print()
    print('~~~~ Maze:')
    m.print_maze()


def debug_with_gui():
    m = Maze(20, 20, 0, 0, 19, 19)
    m.randomize()
    mg = MazeGui(m, title_='Post-Randomize')
    mg.play()
    mg.quit()
    m._make_playable()
    mg = MazeGui(m, title_='Post-Playable')
    mg.play()
    mg.quit()
    m._post_process()
    mg = MazeGui(m, title_='Post-Post-Process')
    mg.play()
    mg.quit()


if __name__ == "__main__":
    # basic_maze()
    # mg = MazeGui(20, 20, 0, 0, 19, 19)
    # mg.play()
    debug_with_gui()
