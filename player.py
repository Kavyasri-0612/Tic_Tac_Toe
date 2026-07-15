import math
import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        """Should return a 0-indexed position (0-8) where the player wants to move."""
        raise NotImplementedError("Subclasses must implement get_move()")


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, board):
        valid_move = False
        while not valid_move:
            user_input = input(f"Player {self.symbol}'s turn. Enter your move (1-9): ")
            try:
                # User enters 1-9, translate to 0-8 for array indexing
                val = int(user_input) - 1
                if val not in board.get_available_moves():
                    print("Invalid move! That spot is either occupied or out of bounds. Try again.")
                else:
                    valid_move = True
                    return val
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 9.")


class AIPlayer(Player):
    def __init__(self, symbol, difficulty="hard"):
        super().__init__(symbol)
        self.difficulty = difficulty.lower()
        self.opponent_symbol = "O" if symbol == "X" else "X"

    def get_move(self, board):
        # If difficulty is set to "easy", play randomly
        if self.difficulty == "easy":
            return random.choice(board.get_available_moves())
        
        # If difficulty is "medium", make basic checks (win or block), otherwise random
        if self.difficulty == "medium":
            available_moves = board.get_available_moves()
            
            # 1. Check if AI can win in this turn
            for move in available_moves:
                board.make_move(move, self.symbol)
                if board.check_winner() == self.symbol:
                    board.undo_move(move)
                    return move
                board.undo_move(move)
                
            # 2. Check if opponent can win, and block them
            for move in available_moves:
                board.make_move(move, self.opponent_symbol)
                if board.check_winner() == self.opponent_symbol:
                    board.undo_move(move)
                    return move
                board.undo_move(move)
                
            # 3. Take center if available
            if 4 in available_moves:
                return 4
                
            # 4. Otherwise play random
            return random.choice(available_moves)

        # "hard" (unbeatable) using minimax algorithm
        # For the first move when board is completely empty, pick center or a random corner for speed optimization
        available_moves = board.get_available_moves()
        if len(available_moves) == 9:
            # Pick center or a corner randomly
            return random.choice([4, 0, 2, 6, 8])
            
        best_score = -math.inf
        best_move = None
        
        for move in available_moves:
            board.make_move(move, self.symbol)
            score = self.minimax(board, 0, False)
            board.undo_move(move)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def minimax(self, board, depth, is_maximizing):
        """
        Implementation of the Minimax decision-making algorithm.
        Returns the optimal evaluation score for the current board state.
        """
        winner = board.check_winner()
        
        # Base cases: return scores if terminal state reached
        if winner == self.symbol:
            return 10 - depth  # Prefer faster wins
        elif winner == self.opponent_symbol:
            return depth - 10  # Prefer delayed losses
        elif board.is_full():
            return 0           # Tie

        if is_maximizing:
            best_score = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.symbol)
                score = self.minimax(board, depth + 1, False)
                board.undo_move(move)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.opponent_symbol)
                score = self.minimax(board, depth + 1, True)
                board.undo_move(move)
                best_score = min(score, best_score)
            return best_score
