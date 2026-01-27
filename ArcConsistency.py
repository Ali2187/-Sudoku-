from Board import SudokuBoard


class ArcConsistencySolver:
    def __init__(self, board_obj: SudokuBoard):
        # Reference to the Sudoku board
        self.board_obj = board_obj

        # Domain of possible values for each cell
        self.domains = {}

        for r in range(9):
            for c in range(9):
                val = board_obj.board[r][c]

                # Fixed domain for assigned cells
                if val != 0:
                    self.domains[(r, c)] = {val}
                # Full domain for empty cells
                else:
                    self.domains[(r, c)] = set(range(1, 10))

    def get_neighbors(self, row, col):
        # Cells that share a row, column, or 3x3 box
        neighbors = set()

        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def revise(self, xi, xj):
        # Remove inconsistent values from xi's domain
        revised = False

        if len(self.domains[xj]) == 1:
            val_to_remove = list(self.domains[xj])[0]
            if val_to_remove in self.domains[xi]:
                self.domains[xi].remove(val_to_remove)
                revised = True

        return revised

    def apply_ac3(self):
        # Initialize queue with all constraint arcs
        queue = []

        for r in range(9):
            for c in range(9):
                for neighbor in self.get_neighbors(r, c):
                    queue.append(((r, c), neighbor))

        # Enforce arc consistency
        while queue:
            (xi, xj) = queue.pop(0)

            if self.revise(xi, xj):
                # Failure if no values remain
                if len(self.domains[xi]) == 0:
                    return False

                # Propagate changes to related arcs
                for xk in self.get_neighbors(*xi):
                    if xk != xj:
                        queue.append((xk, xi))

        # Assign cells with single remaining values
        for (r, c), values in self.domains.items():
            if len(values) == 1:
                self.board_obj.board[r][c] = list(values)[0]

        return True
