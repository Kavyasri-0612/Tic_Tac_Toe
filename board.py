import os
import sys

# ANSI Colors for beautiful terminal output
COLOR_RESET = "\033[0m"
COLOR_X = "\033[91m"  # Bright Red
COLOR_O = "\033[94m"  # Bright Blue
COLOR_GRID = "\033[90m"  # Dark Gray
COLOR_NUM = "\033[37m"  # Light White / Gray for coordinates
COLOR_SUCCESS = "\033[92m"  # Green

class Board:
    def __init__(self):
        # 3x3 grid represented as a list of length 9, initialized with spaces
        self.grid = [" " for _ in range(9)]

    def print_board(self):
        """Prints the board with index numbers for coordinates and colorized X and O."""
        # Check if terminal supports ANSI color codes (simplified check)
        use_color = sys.platform != "win32" or "ANSICON" in os.environ or sys.stdout.isatty()
        
        def format_cell(idx):
            val = self.grid[idx]
            if val == "X":
                return f"{COLOR_X}X{COLOR_RESET}" if use_color else "X"
            elif val == "O":
                return f"{COLOR_O}O{COLOR_RESET}" if use_color else "O"
            else:
                # Print coordinate index (1-9) in light color to help human players choose
                return f"{COLOR_GRID}{idx + 1}{COLOR_RESET}" if use_color else str(idx + 1)

        border = f"{COLOR_GRID}---+---+---{COLOR_RESET}" if use_color else "---+---+---"
        pipe = f"{COLOR_GRID}|{COLOR_RESET}" if use_color else "|"

        print()
        print(f" {format_cell(0)} {pipe} {format_cell(1)} {pipe} {format_cell(2)} ")
        print(border)
        print(f" {format_cell(3)} {pipe} {format_cell(4)} {pipe} {format_cell(5)} ")
        print(border)
        print(f" {format_cell(6)} {pipe} {format_cell(7)} {pipe} {format_cell(8)} ")
        print()

    def get_available_moves(self):
        """Returns list of 0-indexed available positions."""
        return [i for i, val in enumerate(self.grid) if val == " "]

    def make_move(self, index, symbol):
        """Places a symbol at the specified index. Returns True if successful, False otherwise."""
        if 0 <= index < 9 and self.grid[index] == " ":
            self.grid[index] = symbol
            return True
        return False

    def undo_move(self, index):
        """Clears the cell at the specified index."""
        if 0 <= index < 9:
            self.grid[index] = " "

    def is_full(self):
        """Checks if the board is completely full."""
        return " " not in self.grid

    def check_winner(self):
        """
        Checks if there's a winner. 
        Returns the winning symbol ('X' or 'O') if there is one, otherwise None.
        """
        # Winning combinations
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        
        for pos1, pos2, pos3 in win_conditions:
            if self.grid[pos1] == self.grid[pos2] == self.grid[pos3] != " ":
                return self.grid[pos1]
                
        return None

    def is_game_over(self):
        """Returns True if someone has won or the board is full."""
        return self.check_winner() is not None or self.is_full()
