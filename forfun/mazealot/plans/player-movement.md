# Implementation Plan: Player Movement

## Objective
Enable interactive player movement in [`MazeGui`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py#L17-L180) using directional keys (Arrow keys or ASDW), updating and redrawing the player's icon position on the Tkinter canvas smoothly without collision restrictions for now.

---

## Technical Details

### 1. Key Binding & Input Handling
- Bind `<Key>` event on the root Tkinter window (`self.root.bind("<Key>", self._handle_key_press)`).
- Map keysyms to directional coordinate deltas $(\Delta x, \Delta y)$:
  - **Left**: `'Left'`, `'a'`, `'A'` $\rightarrow (-1, 0)$
  - **Right**: `'Right'`, `'d'`, `'D'` $\rightarrow (1, 0)$
  - **Up**: `'Up'`, `'w'`, `'W'` $\rightarrow (0, -1)$
  - **Down**: `'Down'`, `'s'`, `'S'` $\rightarrow (0, 1)$

### 2. Player State & Movement Logic
- Movement method `move_player(dx, dy)`:
  - Updates `self.x_pos` and `self.y_pos`.
  - Clamps player coordinates to maze boundaries:
    $$0 \le x < \text{width}, \quad 0 \le y < \text{height}$$
  - No wall collisions enforced at this stage (player can move freely).
  - Triggers redrawing of the player icon if the position changed.

### 3. Rendering Approach (Approach A: Canvas Tagging)
- Add method `_draw_player()`:
  - Deletes any existing player canvas items via tag (`self.canvas.delete("player")`).
  - Computes micro-grid coordinates for `(self.x_pos, self.y_pos)`:
    - `x_idx = self.x_pos * PIECE_SIZE + 1`
    - `y_idx = self.y_pos * PIECE_SIZE + 1`
    - `ref_x = x_idx * GRID_PIXEL_SIZE + (PX_DIFF / 2)`
    - `ref_y = y_idx * GRID_PIXEL_SIZE + (PX_DIFF / 2)`
  - Creates the player oval using `self.accent_color` (default `RED`) with `tags="player"`.
- Invoke `_draw_player()` during `__init__` so the player icon is rendered at the starting position when the GUI opens.

### 4. Testing & Verification Plan
- Create unit tests in [`maze_gui_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui_test.py):
  - Test key mappings for arrow keys and ASDW.
  - Test valid coordinate updates for each direction.
  - Test boundary clamping (moving beyond edges does not cause off-grid coordinates).
  - Test canvas tag management (confirm player tag is created and updated).


---

## Sub-Plan: Wall Collision Detection

### Objective
Prevent the player from moving through walls or out of bounds by evaluating maze piece passage openings and adjacent piece connectivity before updating player coordinates.

### Technical Details

#### 1. Maze Boundary and Passage Validation ([`maze.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py))
- Expose a public query method `can_move(x_idx: int, y_idx: int, direction: int) -> bool` on [`Maze`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L7-L254).
- Leverage the existing [`_can_move_check`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L217-L223) algorithm, which verifies:
  1. Grid boundary limits (`dv[BOUND_FUNC](x_idx, y_idx, self)`).
  2. The current cell's piece has an open passage in the target direction (`cur_piece.is_open(direction)`).
  3. The adjacent cell's piece has an open passage facing back (`next_piece.is_open(opposite_direction)`).

#### 2. Directional Key Resolution & Movement Enforcement ([`maze_gui.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py))
- Map keys to cardinal direction constants (`LEFT`, `UP`, `RIGHT`, `DOWN`) from [`maze_pieces.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_pieces.py#L77-L87).
- In [`MazeGui.move_player`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py#L212-L226):
  - Support both `direction: int` and `(dx, dy)` parameters for backward compatibility.
  - Before updating coordinates, query `self.maze.can_move(self.x_pos, self.y_pos, direction)`.
  - If invalid (blocked by a wall or grid limit), reject the move (return `False`) and preserve current position without redrawing.
  - If valid, advance `(self.x_pos, self.y_pos)` and invoke `self._draw_player()`.

#### 3. Test Coverage & Verification ([`maze_gui_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui_test.py) & [`maze_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_test.py))
- Unit test `Maze.can_move`:
  - Verify blocked directions return `False` when attempting to pass into walls or off-grid boundaries.
  - Verify open passages return `True`.
- Unit test `MazeGui` collision enforcement:
  - Construct a deterministic maze with known walls and openings.
  - Verify movement is allowed along open passages and rejected against walls.
  - Verify arrow key and ASDW inputs obey collision rules.
