from maze_gui import *
import time


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


def test_canvas():
    root = tk.Tk()
    title = 'Canvas Test'
    root.title(title)
    c = tk.Canvas(root, width=1000, height=1000, bg='black')
    c.pack()

    # Can see clear black "border" on bottom and right edges
    # c.create_rectangle(0, 0, 1000, 1000, fill='red', width=0)
    # Can see thin black "border" on bottom and right edges
    # c.create_rectangle(0, 0, 1001, 1001, fill='red', width=0)
    # No borders at all
    # c.create_rectangle(0, 0, 1002, 1002, fill='red', width=0)
    # Does not expand canvas, just fills visible space
    # c.create_rectangle(0, 0, 2000, 2000, fill='red', width=0)
    # Can see thin black "border" on bottom and right edges
    # c.create_rectangle(0, 0, 1000, 1000, fill='red', outline='red')
    # Can see thin black "border" on bottom and right edges
    # c.create_rectangle(0, 0, 1000, 1000, fill='red', outline='red', width=1)
    # Still thin black border on problem edges
    # c.create_rectangle(0, 0, 1000, 1000, fill='red', outline='red', width=2)
    # No borders at all
    # c.create_rectangle(0, 0, 1001, 1001, fill='red', outline='red')

    # No borders at all
    # c.create_rectangle(1, 1, 1001, 1001, fill='red', outline='red')
    # No borders at all
    # c.create_rectangle(2, 2, 1001, 1001, fill='red', outline='red')
    # Can see thin black "border" on left and top edges
    # c.create_rectangle(3, 3, 1001, 1001, fill='red', outline='red')
    root.mainloop()


if __name__ == "__main__":
    # basic_maze()

    mg = MazeGui(None, 30, 30, 0, 0, 29, 29)
    mg.play()

    # mg = MazeGui(None)
    # mg.play()

    # debug_with_gui()

    # test_canvas()
