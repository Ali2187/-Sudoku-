import tkinter as tk
from tkinter import messagebox
import random
from Board import SudokuBoard
from Backtracking import BacktrackingSolver
from ArcConsistency import ArcConsistencySolver


class SudokuSimplified:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku AI Agent - Omar Hany - Aly Ameen")
        self.board_obj = SudokuBoard([[0] * 9 for _ in range(9)])
        self.cells = {}

        # 🎨 Colors for each 3x3 block
        self.block_colors = [
            "#ffffff", "#e6f2ff", "#fff0f5",
            "#f0fff0", "#fffacd", "#f5f5dc",
            "#e0ffff", "#ffe4e1", "#f8f8ff"
        ]

        # Create grid frame
        grid_frame = tk.Frame(root, bg="black", bd=2)
        grid_frame.pack(padx=10, pady=10)

        # Create 9x9 grid
        for r in range(9):
            for c in range(9):
                block_index = (r // 3) * 3 + (c // 3)
                bg_color = self.block_colors[block_index]

                e = tk.Entry(
                    grid_frame,
                    width=2,
                    font=("Arial", 22),
                    justify="center",
                    bg=bg_color,
                    relief="solid",
                    bd=1
                )

                # Thicker borders between 3x3 blocks
                e.grid(
                    row=r,
                    column=c,
                    padx=(3 if c % 3 == 0 else 1),
                    pady=(3 if r % 3 == 0 else 1)
                )

                e.bind("<KeyRelease>", lambda ev, row=r, col=c: self.validate(row, col))
                self.cells[(r, c)] = e

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame,
            text="Generate Puzzle",
            command=self.generate,
            bg="blue",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Solve (AI Agent)",
            command=self.solve,
            bg="green",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Clear", command=self.clear).pack(
            side=tk.LEFT, padx=5
        )

    # ================= VALIDATION =================
    def validate(self, r, c):
        val = self.cells[(r, c)].get()

        if val.isdigit() and 1 <= int(val) <= 9:
            num = int(val)
            self.board_obj.board[r][c] = 0

            if self.board_obj.is_valid(r, c, num):
                self.board_obj.board[r][c] = num
                self.cells[(r, c)].config(fg="green")
            else:
                self.cells[(r, c)].config(fg="red")
        else:
            self.board_obj.board[r][c] = 0
            self.cells[(r, c)].config(fg="black")

    # ================= SOLVER =================
    def solve(self):
        ac3 = ArcConsistencySolver(self.board_obj)
        ac3.apply_ac3()

        bt = BacktrackingSolver()
        if bt.solve(self.board_obj):
            self.sync_gui()
            messagebox.showinfo("Success", "Solved by AI Agent!")
        else:
            messagebox.showerror("Error", "No solution exists!")

    # ================= GENERATOR =================
    def generate(self):
        self.clear()

        # Add a few random valid numbers
        for _ in range(5):
            r, c, n = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            if self.board_obj.is_valid(r, c, n):
                self.board_obj.board[r][c] = n

        # Solve full board
        BacktrackingSolver().solve(self.board_obj)

        # Remove cells to create puzzle
        for _ in range(50):
            self.board_obj.board[random.randint(0, 8)][random.randint(0, 8)] = 0

        self.sync_gui()

    # ================= GUI SYNC =================
    def sync_gui(self):
        for r in range(9):
            for c in range(9):
                val = self.board_obj.board[r][c]
                cell = self.cells[(r, c)]
                cell.delete(0, tk.END)

                if val != 0:
                    cell.insert(0, str(val))
                    cell.config(fg="black")
                else:
                    cell.config(fg="black")

    # ================= CLEAR =================
    def clear(self):
        self.board_obj.board = [[0] * 9 for _ in range(9)]
        for e in self.cells.values():
            e.delete(0, tk.END)
            e.config(fg="black")


# ================= RUN APP =================
if __name__ == "__main__":
    root = tk.Tk()
    SudokuSimplified(root)
    root.mainloop()
