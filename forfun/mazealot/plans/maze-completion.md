# Implementation Plan: Maze Completion & Reset

## Objective
Detect when the player reaches the maze's end cell, automatically generate a new maze of the same dimensions, and reset the player to the starting position.

---

## Technical Details

### 1. Completion Detection
- End cell coordinates: `(self.maze.end_x, self.maze.end_y)`.
- Add helper method `is_completed(self) -> bool` on [`MazeGui`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py#L17-L250):
  ```python
  def is_completed(self) -> bool:
      return self.x_pos == self.maze.end_x and self.y_pos == self.maze.end_y
  ```
- Track completion statistics: initialize `self.completed_count = 0` in `MazeGui.__init__`.

### 2. Maze Regeneration & State Reset
- Add method `reset_maze(self, new_maze: Optional[Maze] = None)`:
  1. Increment `self.completed_count += 1`.
  2. If `new_maze` is provided, assign it to `self.maze`. Otherwise, instantiate a new [`Maze`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze.py#L7-L254) with the same dimensions (`width`, `height`) and perimeter anchors (`start_x`, `start_y`, `end_x`, `end_y`), and generate its layout (`new_maze.generate_maze()`).
  3. Reset player coordinates:
     - `self.x_pos = self.maze.start_x`
     - `self.y_pos = self.maze.start_y`
  4. Clear the canvas: `self.canvas.delete("all")`.
  5. Redraw the new maze layout via `self._draw_maze()` and place the player token at the start position via `self._draw_player()`.

### 3. Integration with Player Movement
- In [`MazeGui.move_player`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui.py#L219-L235):
  - After validating the move and updating coordinates, check if `self.is_completed()` is `True`.
  - If completed, invoke `self.reset_maze()`.
  - Return `True` to confirm the move was executed.

### 4. Testing & Verification Plan
- Unit tests in [`maze_gui_test.py`](file:///C:/dev/github/HackerRanks_Python/forfun/mazealot/maze_gui_test.py):
  - Test `is_completed` evaluation: returns `False` when player is not at the end cell, and `True` when player arrives at `(end_x, end_y)`.
  - Test `reset_maze` behavior:
    - Verifies `completed_count` increments.
    - Verifies player coordinates reset to `(start_x, start_y)`.
    - Verifies canvas items are cleared and redrawn with the new maze and player token.
  - Test automated completion trigger upon navigating to the exit:
    - Setup a deterministic path to `(end_x, end_y)`.
    - Make the final move into the end cell.
    - Assert that completion was detected, player was reset to `start`, and `completed_count` incremented.
