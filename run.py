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