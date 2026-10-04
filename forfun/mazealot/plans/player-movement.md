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
