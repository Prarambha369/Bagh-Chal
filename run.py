import tkinter as tk
from tkinter import messagebox
import math

class BaghChalTkinter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bagh-Chal: Tiger and Goats")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')

        # Game constants
        self.BOARD_SIZE = 5
        self.CANVAS_SIZE = 500
        self.CELL_SIZE = self.CANVAS_SIZE // (self.BOARD_SIZE + 1)
        self.OFFSET = self.CELL_SIZE

        # Game states
        self.PLACEMENT_PHASE = 0
        self.MOVEMENT_PHASE = 1

        # Piece types
        self.EMPTY = 0
        self.TIGER = 1
        self.GOAT = 2

        # Players
        self.TIGER_PLAYER = 0
        self.GOAT_PLAYER = 1

        # Initialize game
        self.setup_ui()
        self.setup_connections()
        self.reset_game()

        def setup_ui(self):
    """Setup the user interface"""
    # Title
    title_label = tk.Label(self.root, text="🐅 Bagh-Chal: Tiger and Goats 🐐",
                           font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
    title_label.pack(pady=10)

    # Status frame
    self.status_frame = tk.Frame(self.root, bg='#2c3e50')
    self.status_frame.pack(pady=5)

    self.status_label = tk.Label(self.status_frame, text="", font=('Arial', 12),
                                 bg='#2c3e50', fg='#ecf0f1')
    self.status_label.pack()

    # Canvas for game board
    self.canvas = tk.Canvas(self.root, width=self.CANVAS_SIZE, height=self.CANVAS_SIZE,
                            bg='#34495e', highlightthickness=2, highlightbackground='#ecf0f1')
    self.canvas.pack(pady=10)
    self.canvas.bind("<Button-1>", self.on_canvas_click)

    # Control buttons
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

    # Instructions
    self.instruction_label = tk.Label(self.root, text="", font=('Arial', 10),
                                      bg='#2c3e50', fg='#f39c12', wraplength=600)
    self.instruction_label.pack(pady=5

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

        # Place initial tigers at corners
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

    # Draw grid lines
    for i in range(self.BOARD_SIZE):
        for j in range(self.BOARD_SIZE):
            x, y = self.get_canvas_coords(i, j)

            # Draw lines to connected positions
            for ni, nj in self.connections[(i, j)]:
                if ni > i or (ni == i and nj > j):  # Avoid drawing duplicate lines
                    nx, ny = self.get_canvas_coords(ni, nj)
                    self.canvas.create_line(x, y, nx, ny, fill='#ecf0f1', width=2)