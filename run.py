import tkinter as tk
from tkinter import messagebox
import random

class BaghChal:
    BOARD_SIZE = 5
    EMPTY, TIGER, GOAT = 0, 1, 2
    TIGER_PLAYER, GOAT_PLAYER = 0, 1
    PLACEMENT_PHASE, MOVEMENT_PHASE = 0, 1

    def __init__(self):
        self.bot_tiger = False
        self.bot_goat = False
        self.ask_bot_mode()
        self.root = tk.Tk()
        self.root.title("Bagh-Chal")
        self.canvas_size = 500
        self.cell_size = self.canvas_size // (self.BOARD_SIZE + 1)
        self.offset = self.cell_size

        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.status = tk.Label(self.root)
        self.status.pack()

        self.setup_connections()
        self.reset_game()
        self.root.after(300, self.bot_move_if_needed)

    def setup_connections(self):
        self.connections = {}
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.connections[(i, j)] = [(i + di, j + dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]
                                            if (di or dj) and 0 <= i + di < self.BOARD_SIZE and 0 <= j + dj < self.BOARD_SIZE]

    def reset_game(self):
        self.phase = self.PLACEMENT_PHASE
        self.turn = self.GOAT_PLAYER
        self.board = [[self.EMPTY]*self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.goats_placed = 0
        self.goats_captured = 0
        self.selected = None
        self.game_over = False

        for r, c in [(0, 0), (0, 4), (4, 0), (4, 4)]:
            self.board[r][c] = self.TIGER

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x, y = self.offset + j * self.cell_size, self.offset + i * self.cell_size
                for ni, nj in self.connections[(i, j)]:
                    nx, ny = self.offset + nj * self.cell_size, self.offset + ni * self.cell_size
                    self.canvas.create_line(x, y, nx, ny)
                if self.board[i][j] == self.TIGER:
                    self.canvas.create_text(x, y, text="🐅", font=("Arial", 16))
                elif self.board[i][j] == self.GOAT:
                    self.canvas.create_text(x, y, text="🐐", font=("Arial", 14))
        self.status.config(text=f"Turn: {'Tiger' if self.turn == self.TIGER_PLAYER else 'Goat'}")

    def get_coords(self, x, y):
        col = round((x - self.offset) / self.cell_size)
        row = round((y - self.offset) / self.cell_size)
        return (row, col) if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE else (None, None)

    def on_click(self, event):
        if self.game_over or (self.turn == self.TIGER_PLAYER and self.bot_tiger) or (self.turn == self.GOAT_PLAYER and self.bot_goat):
            return

        row, col = self.get_coords(event.x, event.y)
        if row is None:
            return

        if self.phase == self.PLACEMENT_PHASE and self.turn == self.GOAT_PLAYER and self.board[row][col] == self.EMPTY:
            self.board[row][col] = self.GOAT
            self.goats_placed += 1
            if self.goats_placed == 20:
                self.phase = self.MOVEMENT_PHASE
            self.turn = self.TIGER_PLAYER
        elif self.selected:
            sr, sc = self.selected
            if self.is_valid_move(sr, sc, row, col):
                self.make_move(sr, sc, row, col)
                self.turn = 1 - self.turn
            self.selected = None
        elif self.board[row][col] in (self.TIGER, self.GOAT) and ((self.turn == self.TIGER_PLAYER and self.board[row][col] == self.TIGER) or (self.turn == self.GOAT_PLAYER and self.board[row][col] == self.GOAT)):
            self.selected = (row, col)

        self.draw()
        self.check_win()
        self.root.after(300, self.bot_move_if_needed)

    def is_valid_move(self, fr, fc, tr, tc):
        if self.board[tr][tc] != self.EMPTY:
            return False
        if (tr, tc) in self.connections[(fr, fc)]:
            return True
        if self.board[fr][fc] == self.TIGER:
            mr, mc = (fr + tr) // 2, (fc + tc) // 2
            if abs(fr - tr) == 2 or abs(fc - tc) == 2:
                return self.board[mr][mc] == self.GOAT
        return False

    def make_move(self, fr, fc, tr, tc):
        if self.board[fr][fc] == self.TIGER and abs(fr - tr) == 2 or abs(fc - tc) == 2:
            mr, mc = (fr + tr) // 2, (fc + tc) // 2
            if self.board[mr][mc] == self.GOAT:
                self.board[mr][mc] = self.EMPTY
                self.goats_captured += 1
        self.board[tr][tc] = self.board[fr][fc]
        self.board[fr][fc] = self.EMPTY

    def bot_move_if_needed(self):
        if self.game_over:
            return
        if self.phase == self.PLACEMENT_PHASE and self.turn == self.GOAT_PLAYER and self.bot_goat and self.goats_placed < 20:
            choices = [(i, j) for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE) if self.board[i][j] == self.EMPTY]
            if choices:
                r, c = random.choice(choices)
                self.board[r][c] = self.GOAT
                self.goats_placed += 1
                if self.goats_placed == 20:
                    self.phase = self.MOVEMENT_PHASE
                self.turn = self.TIGER_PLAYER
        elif self.phase == self.MOVEMENT_PHASE and ((self.turn == self.TIGER_PLAYER and self.bot_tiger) or (self.turn == self.GOAT_PLAYER and self.bot_goat)):
            moves = []
            for i in range(self.BOARD_SIZE):
                for j in range(self.BOARD_SIZE):
                    if self.board[i][j] == (self.TIGER if self.turn == self.TIGER_PLAYER else self.GOAT):
                        for ni, nj in self.connections[(i, j)]:
                            if self.is_valid_move(i, j, ni, nj):
                                moves.append((i, j, ni, nj))
                        if self.board[i][j] == self.TIGER:
                            for di in [-2, 0, 2]:
                                for dj in [-2, 0, 2]:
                                    ni, nj = i + di, j + dj
                                    if 0 <= ni < self.BOARD_SIZE and 0 <= nj < self.BOARD_SIZE and self.is_valid_move(i, j, ni, nj):
                                        moves.append((i, j, ni, nj))
            if moves:
                fr, fc, tr, tc = random.choice(moves)
                self.make_move(fr, fc, tr, tc)
                self.turn = 1 - self.turn
        self.draw()
        self.check_win()
        self.root.after(300, self.bot_move_if_needed)

    def check_win(self):
        if self.goats_captured >= 5:
            self.game_over = True
            messagebox.showinfo("Game Over", "Tigers Win!")
        elif self.phase == self.MOVEMENT_PHASE and not self.can_tigers_move():
            self.game_over = True
            messagebox.showinfo("Game Over", "Goats Win!")

    def can_tigers_move(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.TIGER:
                    for ni, nj in self.connections[(i, j)]:
                        if self.is_valid_move(i, j, ni, nj):
                            return True
        return False

    def ask_bot_mode(self):
        import tkinter.simpledialog as sd
        root = tk.Tk()
        root.withdraw()
        mode = sd.askstring("Choose Mode", "1: Human vs Human\n2: Human vs Bot (Bot=Tigers)\n3: Human vs Bot (Bot=Goats)")
        if mode == '2':
            self.bot_tiger = True
        elif mode == '3':
            self.bot_goat = True
        root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    BaghChal().run()
