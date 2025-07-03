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