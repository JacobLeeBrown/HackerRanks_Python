import maze

if __name__ == "__main__":
    m = maze.Maze(30, 10, 0, 0, 29, 9)
    m.generate_maze(True)
    print('~~~~ Grid:')
    m.print_grid()
    print()
    print('~~~~ Maze:')
    m.print_maze()
