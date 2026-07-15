import sys
import argparse
from player import HumanPlayer, AIPlayer
from game import GameEngine

try:
    from gui import launch_gui
except ImportError:
    launch_gui = None

def print_header():
    title = """
=========================================
      🌟 PYTHON TIC-TAC-TOE 🌟
   (Unbeatable Minimax AI Opponent)
=========================================
    """
    print(title)

def get_game_settings():
    # 1. Select Mode
    print("Choose Game Mode:")
    print("1. Single Player (vs AI)")
    print("2. Multiplayer (Human vs Human)")
    while True:
        mode_choice = input("Enter option (1-2): ").strip()
        if mode_choice in ("1", "2"):
            break
        print("Invalid choice. Please select 1 or 2.")

    if mode_choice == "1":
        # AI Mode settings
        # Choice of Symbol
        print("\nChoose your symbol:")
        print("X - Plays First")
        print("O - Plays Second")
        while True:
            symbol_choice = input("Select symbol (X/O): ").strip().upper()
            if symbol_choice in ("X", "O"):
                break
            print("Invalid choice. Please select X or O.")

        # Choice of AI Difficulty
        print("\nChoose AI Difficulty:")
        print("1. Easy (Random Moves)")
        print("2. Medium (Strategic Blocks/Wins)")
        print("3. Hard (Unbeatable Minimax)")
        difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
        while True:
            diff_choice = input("Select difficulty (1-3): ").strip()
            if diff_choice in difficulty_map:
                difficulty = difficulty_map[diff_choice]
                break
            print("Invalid choice. Please select 1, 2, or 3.")

        human_symbol = symbol_choice
        ai_symbol = "O" if human_symbol == "X" else "X"
        
        human = HumanPlayer(human_symbol)
        ai = AIPlayer(ai_symbol, difficulty=difficulty)

        # X always goes first
        if human_symbol == "X":
            return human, ai
        else:
            return ai, human
    else:
        # Multiplayer settings
        print("\nMultiplayer Setup:")
        print("Player 1 is X (goes first)")
        print("Player 2 is O")
        p1 = HumanPlayer("X")
        p2 = HumanPlayer("O")
        return p1, p2

def run_cli_game():
    try:
        # Enable ANSI colors for Windows if applicable
        if sys.platform == "win32":
            import os
            os.system("color")
    except Exception:
        pass

    print_header()
    
    while True:
        player1, player2 = get_game_settings()
        game = GameEngine(player1, player2)
        game.play()

        # Ask for replay
        while True:
            replay = input("Do you want to play again? (y/n): ").strip().lower()
            if replay in ("y", "n", "yes", "no"):
                break
            print("Please enter 'y' or 'n'.")
            
        if replay in ("n", "no"):
            print("\nThanks for playing Python Tic-Tac-Toe! Goodbye! 👋")
            break
        print("\n" + "="*41)

def main():
    parser = argparse.ArgumentParser(description="Python Tic-Tac-Toe with Unbeatable AI")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run the game in terminal CLI mode instead of launching the desktop GUI."
    )
    args = parser.parse_args()

    # Launch GUI by default (unless --cli is specified or GUI load fails)
    if args.cli or launch_gui is None:
        run_cli_game()
    else:
        launch_gui()

if __name__ == "__main__":
    main()
