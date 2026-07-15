from board import Board

class GameEngine:
    def __init__(self, player1, player2):
        """
        player1 and player2 are instances of Player subclasses.
        Normally, player1 has symbol 'X' (goes first) and player2 has symbol 'O'.
        """
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def play(self):
        """Orchestrates the main game loop."""
        print("\n=== STARTING NEW GAME ===")
        self.board.print_board()

        while not self.board.is_game_over():
            # Get current player's move
            move = self.current_player.get_move(self.board)
            self.board.make_move(move, self.current_player.symbol)
            
            # Print updated board
            self.board.print_board()
            
            # Check for win or draw
            winner = self.board.check_winner()
            if winner:
                print(f"🎉 Game Over! Player {winner} wins! 🎉\n")
                return winner

            if self.board.is_full():
                print("🤝 Game Over! It's a draw! 🤝\n")
                return "Draw"

            # Alternate turn
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
