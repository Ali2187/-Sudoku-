# Sudoku AI Agent

A Python-based Sudoku solver with both graphical (GUI) and command-line interfaces, implementing two solving algorithms: **Arc Consistency (AC-3)** and **Backtracking**.

---

## Features

- **Dual Solving Strategy**: Combines Arc Consistency (AC-3) for constraint propagation with Backtracking for complete search
- **Graphical Interface**: Built with `tkinter` — interactive 9×9 grid with color-coded 3×3 blocks
- **Command-Line Mode**: Run the solver directly on predefined or custom puzzles
- **Puzzle Generator**: Create new Sudoku puzzles with a single click
- **Real-Time Validation**: Visual feedback (green/red) as you enter numbers
- **Clean Architecture**: Modular design with separate classes for board representation, solvers, and UI

---

## Project Structure

```
.
├── main.py              # Command-line entry point (sample puzzle demo)
├── gui.py               # Graphical interface entry point
├── Board.py             # SudokuBoard class — board representation & validation
├── Backtracking.py      # BacktrackingSolver class — recursive depth-first search
├── ArcConsistency.py    # ArcConsistencySolver class — AC-3 constraint propagation
└── README.md            # This file
```

---

## Quick Start

### Prerequisites
- Python 3.8+

No external dependencies — only standard library modules (`tkinter`, `random`).

---

### Run the GUI

```bash
python gui.py
```

**GUI Controls:**
| Button | Action |
|--------|--------|
| **Generate Puzzle** | Creates a new valid Sudoku puzzle |
| **Solve (AI Agent)** | Runs AC-3 + Backtracking to solve the current board |
| **Clear** | Resets the board to empty |

**Usage:**
1. Click **Generate Puzzle** for a new puzzle, or enter numbers manually
2. Invalid entries appear in **red**, valid in **green**
3. Click **Solve (AI Agent)** to let the AI solve it

---

### Run the Command-Line Demo

```bash
python main.py
```

This runs the solver on a built-in sample puzzle, showing each step:
1. Original board
2. After AC-3 domain reduction
3. Final solution (or "no solution" message)

---

## Algorithms

### Arc Consistency (AC-3)
- **Purpose**: Reduce variable domains by enforcing local consistency
- **How it works**: Maintains a queue of arcs (cell pairs with constraints). For each arc `(Xi, Xj)`, removes values from `Xi`'s domain that have no valid counterpart in `Xj`'s domain. Propagates changes until queue is empty or a domain becomes empty (failure).
- **Complexity**: O(n³) worst-case, very fast for Sudoku in practice
- **Result**: Often solves easy/medium puzzles completely; reduces search space for harder ones

### Backtracking
- **Purpose**: Complete search when AC-3 alone doesn't finish
- **How it works**: Recursive depth-first search. Finds an empty cell, tries values 1–9 that satisfy constraints, recurses. Backtracks on dead ends.
- **Guarantee**: Finds a solution if one exists; proves unsolvability otherwise
- **Optimization**: Runs *after* AC-3, so search space is dramatically smaller

### Combined Strategy
```
AC-3 → (if incomplete) → Backtracking
```
This hybrid approach is significantly faster than pure backtracking on most puzzles.

---

## Board Representation

- **Internal**: 9×9 list of lists (`board[row][col]`), `0` = empty
- **Validation**: Row, column, and 3×3 subgrid constraints checked in `SudokuBoard.is_valid()`
- **Display**: CLI shows `.` for empty cells; GUI uses colored `Entry` widgets

---

## Extending the Project

### Add a New Puzzle (CLI)
Edit `main.py` and replace `sample_grid` with your own 9×9 grid (use `0` for blanks).

### Customize GUI Colors
Modify `block_colors` list in `gui.py` (9 hex colors, one per 3×3 block).

### Swap Solvers
Both solvers implement a simple interface:
```python
solver = BacktrackingSolver()  # or ArcConsistencySolver(board)
solver.solve(board)  # returns True/False, mutates board in place
```

---

## License

MIT License — free to use, modify, and distribute.

---

## Authors

- **Omar Hany**
- **Aly Ameen**

---

## Acknowledgments

- AC-3 algorithm from *Artificial Intelligence: A Modern Approach* (Russell & Norvig)
- Sudoku constraint modeling inspired by standard CSP formulations