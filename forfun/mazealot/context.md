# Mazealot Context & Architecture

## 1. Project Goal

The primary goal of **Mazealot** is to randomly generate 2D mazes and provide an interactive graphical user interface (GUI) where a user can "play" the maze by navigating a player avatar from an assigned starting position on the perimeter to an exit on the perimeter.

---

## 2. File Structure & Responsibilities

| File | Primary Responsibility |
| :--- | :--- |
| [`maze_pieces.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_pieces.py) | Defines the mathematical foundation of the maze pieces: 4-bit binary piece encoding (16 piece types), direction vectors, boundary checks, and the [`MazePiece`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_pieces.py#L93-L130) model. |
| [`maze.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py) | Contains the [`Maze`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L7-L254) class which handles grid instantiation, perimeter start/end validation, generation logic (randomize, path-to-start connectivity, nub cleanup, perimeter openings), and terminal printing. |
| [`maze_gui.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py) | Contains [`MazeGui`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py#L17-L180), built on `tkinter.Canvas`, responsible for rendering the maze tiles, markers, and managing the window event loop. |
| [`tk_helper.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/tk_helper.py) | Helper utility containing [`rect`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/tk_helper.py#L4-L5) for drawing filled and outlined rectangles without coordinate offset mismatches on `tkinter.Canvas`. |
| [`play_maze.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/play_maze.py) | Main launcher script with test/debug functions ([`basic_maze`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/play_maze.py#L5-L13), [`debug_with_gui`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/play_maze.py#L15-L29), [`test_canvas`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/play_maze.py#L31-L79)). |
| [`maze_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_test.py) | Comprehensive `unittest` suite covering [`MazePiece`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_pieces.py#L93-L130) operations, directional resolution towards start, playability/reachability across 200 random mazes, and nub cleanup. |
| [`maze_gui_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui_test.py) | `unittest` suite covering GUI player initialization, keyboard bindings (Arrow keys + ASDW), boundary clamping, and tag-based canvas redraws. |

---

## 3. Core Mechanics & Data Encoding

### Piece Representation (Binary Bitmask)
The maze is modeled as an $H \times W$ grid of cells. Each cell contains one piece represented by an integer in $[0, 15]$.
Each piece has 4 entry/exit boundaries corresponding to directional bits:
- **Left**: Bit 3 ($2^3 = 8$)
- **Up**: Bit 2 ($2^2 = 4$)
- **Right**: Bit 1 ($2^1 = 2$)
- **Down**: Bit 0 ($2^0 = 1$)

Value conventions:
- `0` = **Open passage**
- `1` = **Closed wall**

For instance:
- `0` (`0000`): Open in all four directions (4-way intersection).
- `6` (`0110`): Up and Right are closed; Left and Down are open (corner piece).
- `15` (`1111`): All sides closed (solid wall piece).

### 3x3 Micro-Grid Expansion
Each piece expands into a $3 \times 3$ matrix of open paths and walls:
- The 4 corners are always walls (`1`).
- The center $(1, 1)$ is always open (`0`).
- The orthogonal edges $(0, 1), (1, 0), (1, 2), (2, 1)$ reflect the open/closed status of `LEFT`, `UP`, `RIGHT`, and `DOWN`.

---

## 4. Maze Generation Pipeline

The generation sequence in [`Maze.generate_maze()`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L65-L75) proceeds in three distinct phases:

```
[ Randomize Grid ] -> [ Make Playable (DFS / Pathfinding) ] -> [ Post-Processing (Nubs & Exits) ]
```

1. **`randomize()`**:
   - Every cell in the grid is assigned a random piece using weighted probabilities ([`DEFAULT_PROBABILITIES`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_pieces.py#L38)).
   - Fully open (`0`) and fully closed (`15`) pieces have low or zero initial probability; bends and corridors have higher weights.

2. **`_make_playable()`**:
   - Guarantees that every cell in the maze is reachable from the starting cell (no isolated regions or disconnected loops).
   - Runs a DFS from `(start_x, start_y)` using [`_can_move_check()`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L217-L223) to mark reachable cells in `path_to_start`.
   - Iterates through unreached cells in randomized order.
   - For each unreached cell, [`_connect_to_start()`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L125-L150) checks if any adjacent cell is already connected to start. If found, it opens both facing walls to join them. If not, it carves a path towards the start coordinates ([`_direction_towards_start_rand()`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L159-L166)) recursively until connection with the main network is achieved.

3. **`_post_process()`**:
   - **Nub Cleanup ([`_clean_nubs()`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L232-L243))**: Eliminates dead-end passages that lead directly into the solid outer wall or a closed side of an adjacent cell by turning those open openings back into walls.
   - **Perimeter Openings ([`_open_to_edge()`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L244-L254))**: Opens the outer boundary walls at `(start_x, start_y)` and `(end_x, end_y)`.

---

## 5. Current State of the GUI & Rendering

- Built with **Tkinter Canvas** inside [`MazeGui`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py#L17-L180).
- Start marker (Blue) and End marker (Green) are rendered.
- **Rendering Evolution**:
  - `_draw_maze_orig()`: Working baseline that converts the entire maze to an expanded $(H \times 3) \times (W \times 3)$ binary matrix and draws every wall square directly with `create_rectangle`.
  - `_draw_maze()` & `_draw_maze_piece()`: An incomplete rewrite attempting to draw pieces with customizable path thickness (`path_weight`) to make walls look cleaner. In the current file, opening of side corridors was commented out, and a coordinate multiplication typo (`ref_y * center_offset`) was left unresolved.
- Canvas boundary testing in [`play_maze.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/play_maze.py#L31-L79) investigated 1-pixel border clipping behavior on Tkinter canvas rectangles.

---

## 6. Current State of Gameplay (Gap Analysis)

The maze generation and player navigation are functional:
- **Player Representation**: Rendered as a distinct accent-colored token (default red) on top of the maze using Tkinter canvas tags (`tag="player"`).
- **Input Handling**: Keyboard events for Arrow keys (`Left`, `Right`, `Up`, `Down`) and ASDW keys (`a`/`A`, `s`/`S`, `d`/`D`, `w`/`W`) are bound to move the player and redraw the avatar instantly.
- **Boundary Clamping**: The player is constrained within the $H \times W$ maze dimensions.
- **Remaining Work (Collision & Win State)**:
  - Movement is currently unconstrained by internal walls (free movement). Collision validation against open/closed piece boundaries is pending.
  - Game state and win condition handling (detecting reaching `(end_x, end_y)`, victory UI, reset) is pending.

---

## 7. Verification & Testing

- **[`maze_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_test.py)**: 7/7 tests passing. Verifies piece bitmasks, path modifications, binary micro-grid conversions, directional heuristics, reachability of 200 random mazes, and nub cleanup.
- **[`maze_gui_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui_test.py)**: 7/7 tests passing. Verifies initial avatar placement, free movement via arrow keys and ASDW, boundary clamping at maze edges, and single-item canvas tag updates.
