from Board import SudokuBoard
class BacktrackingSolver:
    def solve(self, board: SudokuBoard):

        empty = board.find_empty()
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if board.is_valid(row, col, num):
                board.board[row][col] = num

                if self.solve(board):
                    return True

                # Undo assignment (backtrack)
                board.board[row][col] = 0

        return False

