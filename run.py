import tkinter as tk
from tkinter import messagebox
import math

class BaghChalTkinter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bagh-Chal: Tiger and Goats")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        self.BOARD_SIZE = 5
        self.CANVAS_SIZE = 500
        self.CELL_SIZE = self.CANVAS_SIZE // (self.BOARD_SIZE + 1)
        self.OFFSET = self.CELL_SIZE
        self.PLACEMENT_PHASE = 0
        self.MOVEMENT_PHASE = 1
        self.EMPTY = 0
        self.TIGER = 1
        self.GOAT = 2
        self.TIGER_PLAYER = 0
        self.GOAT_PLAYER = 1
        self.setup_ui()
        self.setup_connections()
        self.reset_game()

    def setup_ui(self):
        """Setup the user interface"""
        title_label = tk.Label(self.root, text="🐅 Bagh-Chal: Tiger and Goats 🐐",
                               font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)

        self.status_frame = tk.Frame(self.root, bg='#2c3e50')
        self.status_frame.pack(pady=5)

        self.status_label = tk.Label(self.status_frame, text="", font=('Arial', 12),
                                     bg='#2c3e50', fg='#ecf0f1')
        self.status_label.pack()

        self.canvas = tk.Canvas(self.root, width=self.CANVAS_SIZE, height=self.CANVAS_SIZE,
                                bg='#34495e', highlightthickness=2, highlightbackground='#ecf0f1')
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)

        restart_btn = tk.Button(button_frame, text="🔄 Restart Game", command=self.reset_game,
                                font=('Arial', 12), bg='#3498db', fg='white', padx=20)
        restart_btn.pack(side=tk.LEFT, padx=10)

        rules_btn = tk.Button(button_frame, text="📖 Rules", command=self.show_rules,
                              font=('Arial', 12), bg='#2ecc71', fg='white', padx=20)
        rules_btn.pack(side=tk.LEFT, padx=10)

        quit_btn = tk.Button(button_frame, text="❌ Quit", command=self.root.quit,
                             font=('Arial', 12), bg='#e74c3c', fg='white', padx=20)
        quit_btn.pack(side=tk.LEFT, padx=10)

        self.instruction_label = tk.Label(self.root, text="", font=('Arial', 10),
                                          bg='#2c3e50', fg='#f39c12', wraplength=600)
        self.instruction_label.pack(pady=5)

    def reset_game(self):
        """Reset the game to initial state"""
        self.current_phase = self.PLACEMENT_PHASE
        self.current_player = self.GOAT_PLAYER
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.goats_placed = 0
        self.goats_captured = 0
        self.selected_row = -1
        self.selected_col = -1
        self.piece_selected = False
        self.game_over = False
        self.winner = None

        self.board[0][0] = self.TIGER
        self.board[0][4] = self.TIGER
        self.board[4][0] = self.TIGER
        self.board[4][4] = self.TIGER

        self.draw_board()
        self.update_status()

    def setup_connections(self):
        """Setup valid connections between board positions"""
        self.connections = {}
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                neighbors = []

                # All 8 directions (horizontal, vertical, diagonal)
                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.BOARD_SIZE and 0 <= nj < self.BOARD_SIZE:
                        neighbors.append((ni, nj))

                self.connections[(i, j)] = neighbors

    def get_canvas_coords(self, row, col):
        """Convert board coordinates to canvas coordinates"""
        x = self.OFFSET + col * self.CELL_SIZE
        y = self.OFFSET + row * self.CELL_SIZE
        return x, y

    def get_board_coords(self, canvas_x, canvas_y):
        """Convert canvas coordinates to board coordinates"""
        col = round((canvas_x - self.OFFSET) / self.CELL_SIZE)
        row = round((canvas_y - self.OFFSET) / self.CELL_SIZE)

        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            return row, col
        return None, None

    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("all")

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x, y = self.get_canvas_coords(i, j)

                # Draw lines to connected positions
                for ni, nj in self.connections[(i, j)]:
                    if ni > i or (ni == i and nj > j):  # Avoid drawing duplicate lines
                        nx, ny = self.get_canvas_coords(ni, nj)
                        self.canvas.create_line(x, y, nx, ny, fill='#ecf0f1', width=2)

        # Draw intersection points
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x, y = self.get_canvas_coords(i, j)
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill='#ecf0f1', outline='#bdc3c7')

        self.draw_pieces()

    def draw_pieces(self):
        """Draw tigers and goats on the board"""
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x, y = self.get_canvas_coords(i, j)

                if self.board[i][j] == self.TIGER:
                    # Draw tiger (orange circle with T)
                    self.canvas.create_oval(x-20, y-20, x+20, y+20, fill='#ff6b35', outline='#d35400', width=3)
                    self.canvas.create_text(x, y, text='🐅', font=('Arial', 16))

                elif self.board[i][j] == self.GOAT:
                    # Draw goat (white circle with G)
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill='#ecf0f1', outline='#95a5a6', width=2)
                    self.canvas.create_text(x, y, text='🐐', font=('Arial', 12))

        if self.piece_selected:
            x, y = self.get_canvas_coords(self.selected_row, self.selected_col)
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill='', outline='#2ecc71', width=4)

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid"""
        if self.board[to_row][to_col] != self.EMPTY:
            return False

        if (to_row, to_col) in self.connections[(from_row, from_col)]:
            return True

        if self.board[from_row][from_col] == self.TIGER:
            # Calculate middle position for jump
            if abs(to_row - from_row) == 2 and abs(to_col - from_col) <= 2:
                mid_row = (from_row + to_row) // 2
                mid_col = (from_col + to_col) // 2
                if self.board[mid_row][mid_col] == self.GOAT:
                    return True
            elif abs(to_col - from_col) == 2 and abs(to_row - from_row) <= 2:
                mid_row = (from_row + to_row) // 2
                mid_col = (from_col + to_col) // 2
                if self.board[mid_row][mid_col] == self.GOAT:
                    return True

        return False

    def make_move(self, from_row, from_col, to_row, to_col):
        """Execute a move"""
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = self.EMPTY
        self.board[to_row][to_col] = piece

        if piece == self.TIGER and (abs(to_row - from_row) == 2 or abs(to_col - from_col) == 2):
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            if self.board[mid_row][mid_col] == self.GOAT:
                self.board[mid_row][mid_col] = self.EMPTY
                self.goats_captured += 1

    def can_tigers_move(self):
        """Check if any tiger can move"""
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.TIGER:
                    # Check all possible moves
                    for ni, nj in self.connections[(i, j)]:
                        if self.is_valid_move(i, j, ni, nj):
                            return True
                    # Check jump moves
                    for di in [-2, -1, 0, 1, 2]:
                        for dj in [-2, -1, 0, 1, 2]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.BOARD_SIZE and 0 <= nj < self.BOARD_SIZE:
                                if self.is_valid_move(i, j, ni, nj):
                                    return True
        return False

    def check_win_condition(self):
        """Check if game is over"""
        if self.goats_captured >= 5:
            self.game_over = True
            self.winner = "Tigers"
            messagebox.showinfo("Game Over", "🐅 Tigers Win! They captured 5 goats!")
        elif self.current_phase == self.MOVEMENT_PHASE and not self.can_tigers_move():
            self.game_over = True
            self.winner = "Goats"
            messagebox.showinfo("Game Over", "🐐 Goats Win! All tigers are blocked!")

    def on_canvas_click(self, event):
        """Handle canvas clicks"""
        if self.game_over:
            return

        row, col = self.get_board_coords(event.x, event.y)
        if row is None or col is None:
            return

        if self.current_phase == self.PLACEMENT_PHASE and self.current_player == self.GOAT_PLAYER:
            if self.board[row][col] == self.EMPTY and self.goats_placed < 20:
                self.board[row][col] = self.GOAT
                self.goats_placed += 1

                if self.goats_placed == 20:
                    self.current_phase = self.MOVEMENT_PHASE

                self.current_player = self.TIGER_PLAYER
        else:
            if not self.piece_selected:
                if ((self.current_player == self.TIGER_PLAYER and self.board[row][col] == self.TIGER) or
                        (self.current_player == self.GOAT_PLAYER and self.board[row][col] == self.GOAT)):
                    self.selected_row = row
                    self.selected_col = col
                    self.piece_selected = True
            else:
                if row == self.selected_row and col == self.selected_col:
                    self.piece_selected = False
                    self.selected_row = -1
                    self.selected_col = -1
                elif self.is_valid_move(self.selected_row, self.selected_col, row, col):
                    self.make_move(self.selected_row, self.selected_col, row, col)
                    self.piece_selected = False
                    self.selected_row = -1
                    self.selected_col = -1

                    self.current_player = 1 - self.current_player
                else:
                    if ((self.current_player == self.TIGER_PLAYER and self.board[row][col] == self.TIGER) or
                            (self.current_player == self.GOAT_PLAYER and self.board[row][col] == self.GOAT)):
                        self.selected_row = row
                        self.selected_col = col
                        self.piece_selected = True
                    else:
                        self.piece_selected = False
                        self.selected_row = -1
                        self.selected_col = -1

        self.draw_board()
        self.update_status()
        self.check_win_condition()

    def update_status(self):
        """Update status labels"""
        if self.game_over:
            status_text = f"Game Over! Winner: {self.winner}"
        else:
            phase_text = "Placement Phase" if self.current_phase == self.PLACEMENT_PHASE else "Movement Phase"
            player_text = "Tigers" if self.current_player == self.TIGER_PLAYER else "Goats"
            status_text = f"{phase_text} - Current Player: {player_text}"

        self.status_label.config(text=status_text)

        if self.game_over:
            instruction_text = f"🎉 {self.winner} have won the game! Click 'Restart Game' to play again."
        elif self.current_phase == self.PLACEMENT_PHASE:
            instruction_text = f"🐐 Place goats on empty intersections. Goats placed: {self.goats_placed}/20"
        elif self.current_player == self.TIGER_PLAYER:
            if self.piece_selected:
                instruction_text = "🐅 Tiger selected! Click on an empty adjacent position or jump over a goat to capture it."
            else:
                instruction_text = "🐅 Tigers' turn! Click on a tiger to select it."
        else:
            if self.piece_selected:
                instruction_text = "🐐 Goat selected! Click on an empty adjacent position to move."
            else:
                instruction_text = "🐐 Goats' turn! Click on a goat to select it."

        additional_info = f"Goats captured: {self.goats_captured}/5"
        self.instruction_label.config(text=f"{instruction_text}\n{additional_info}")

    def show_rules(self):
        """Display game rules"""
        rules_text = """
🐅 BAGH-CHAL RULES 🐐

OBJECTIVE:
• Tigers: Capture 5 goats to win
• Goats: Block all tigers so they cannot move

SETUP:
• 4 tigers start at the corners
• 20 goats to be placed during the game

GAMEPLAY:
1. PLACEMENT PHASE:
   • Goats are placed one by one on empty intersections
   • After each goat placement, tigers can move

2. MOVEMENT PHASE (after all 20 goats are placed):
   • Both tigers and goats can move to adjacent empty positions
   • Tigers can also jump over goats to capture them
   • Only one piece can be moved per turn

MOVEMENT RULES:
• All pieces move along the lines to adjacent intersections
• Tigers can jump over adjacent goats to capture them
• Captured goats are removed from the board
• Goats cannot jump or capture

WIN CONDITIONS:
• Tigers win by capturing 5 goats
• Goats win by blocking all tigers from moving
        """
        messagebox.showinfo("Bagh-Chal Rules", rules_text)

    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = BaghChalTkinter()
    game.run()