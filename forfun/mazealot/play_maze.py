import maze

if __name__ == "__main__":
    m = maze.Maze(30, 5, 0, 0, 29, 4)
    m.randomize()
    print('~~~~ Grid:')
    m.print_grid()
    print()
    print('~~~~ Maze:')
    m.print_maze()
