import tkinter as tk
from tkinter import messagebox
import os
from board import Board
from player import AIPlayer

# Modern Flat Color Palette (Dark Theme)
BG_COLOR = "#121214"         # Very dark slate
PANEL_BG = "#1A1A1E"         # Secondary dark container
CARD_BG = "#222228"          # Active/Inactive button base
ACCENT_COLOR = "#5865F2"     # Vibrant purple/blue (Discord blue)
TEXT_COLOR = "#FFFFFF"       # White
MUTED_TEXT = "#72767D"       # Medium gray
HOVER_COLOR = "#2D2F3F"      # Grid hover highlight
ACTIVE_GREEN = "#57F287"     # Vibrant success green

COLOR_X = "#ED4245"          # Red
COLOR_O = "#3498DB"          # Light Blue
GRID_LINE_COLOR = "#2A2A30"  # Divider line gray

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (Unbeatable AI)")
        self.root.configure(bg=BG_COLOR)
        # Allow the window to auto-size based on widgets to prevent clipping on High-DPI displays
        self.root.resizable(True, True)
        self.root.minsize(460, 660)

        # Game State Variables
        self.board = Board()
        self.ai_player = None
        self.game_mode = "vs_ai"      # "vs_ai" or "vs_human"
        self.human_symbol = "X"       # "X" or "O"
        self.ai_symbol = "O"
        self.difficulty = "hard"      # "easy", "medium", "hard"
        self.current_turn = "X"
        self.game_active = True

        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # 1. Main Container
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 2. Header Title Banner (Modern Flat Design)
        title_label = tk.Label(
            main_frame, 
            text="TIC-TAC-TOE", 
            font=("Segoe UI", 26, "bold"), 
            bg=BG_COLOR, 
            fg=ACCENT_COLOR
        )
        title_label.pack(pady=(5, 2))

        subtitle_label = tk.Label(
            main_frame, 
            text="Decoupled MVC Engine • Unbeatable Minimax AI", 
            font=("Segoe UI", 9, "bold"), 
            bg=BG_COLOR, 
            fg=MUTED_TEXT
        )
        subtitle_label.pack(pady=(0, 15))

        # 3. Settings Container (Instead of legacy LabelFrame)
        self.settings_container = tk.Frame(main_frame, bg=PANEL_BG, bd=0)
        self.settings_container.pack(fill="x", pady=(0, 15))
        self.settings_container.config(padx=15, pady=15)

        # Helper to create horizontal segmented selector buttons
        # --- MODE SELECTOR ---
        mode_label = tk.Label(self.settings_container, text="GAME MODE", font=("Segoe UI", 8, "bold"), bg=PANEL_BG, fg=MUTED_TEXT)
        mode_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        mode_btn_frame = tk.Frame(self.settings_container, bg=PANEL_BG)
        mode_btn_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=(0, 12))

        self.btn_vs_ai = tk.Button(
            mode_btn_frame, text="Single Player (vs AI)", font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
            bd=0, relief="flat", padx=15, pady=6, cursor="hand2",
            command=lambda: self.select_game_mode("vs_ai")
        )
        self.btn_vs_ai.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_vs_human = tk.Button(
            mode_btn_frame, text="Local PvP (2 Player)", font=("Segoe UI", 9, "bold"),
            bg=CARD_BG, fg=MUTED_TEXT, activebackground=CARD_BG, activeforeground=MUTED_TEXT,
            bd=0, relief="flat", padx=15, pady=6, cursor="hand2",
            command=lambda: self.select_game_mode("vs_human")
        )
        self.btn_vs_human.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # --- PLAY AS / SYMBOL SELECTOR ---
        self.lbl_play_as = tk.Label(self.settings_container, text="PLAY AS", font=("Segoe UI", 8, "bold"), bg=PANEL_BG, fg=MUTED_TEXT)
        self.lbl_play_as.grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.sym_btn_frame = tk.Frame(self.settings_container, bg=PANEL_BG)
        self.sym_btn_frame.grid(row=3, column=0, columnspan=3, sticky="we", pady=(0, 12))

        self.btn_sym_x = tk.Button(
            self.sym_btn_frame, text="X (Plays First)", font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
            bd=0, relief="flat", padx=15, pady=6, cursor="hand2",
            command=lambda: self.select_symbol("X")
        )
        self.btn_sym_x.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_sym_o = tk.Button(
            self.sym_btn_frame, text="O (Plays Second)", font=("Segoe UI", 9, "bold"),
            bg=CARD_BG, fg=MUTED_TEXT, activebackground=CARD_BG, activeforeground=MUTED_TEXT,
            bd=0, relief="flat", padx=15, pady=6, cursor="hand2",
            command=lambda: self.select_symbol("O")
        )
        self.btn_sym_o.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # --- DIFFICULTY SELECTOR ---
        self.lbl_diff = tk.Label(self.settings_container, text="AI DIFFICULTY", font=("Segoe UI", 8, "bold"), bg=PANEL_BG, fg=MUTED_TEXT)
        self.lbl_diff.grid(row=4, column=0, sticky="w", pady=(0, 5))

        self.diff_btn_frame = tk.Frame(self.settings_container, bg=PANEL_BG)
        self.diff_btn_frame.grid(row=5, column=0, columnspan=3, sticky="we")

        self.btn_diff_easy = tk.Button(
            self.diff_btn_frame, text="Easy", font=("Segoe UI", 9, "bold"),
            bg=CARD_BG, fg=MUTED_TEXT, activebackground=CARD_BG, activeforeground=MUTED_TEXT,
            bd=0, relief="flat", padx=10, pady=6, cursor="hand2",
            command=lambda: self.select_difficulty("easy")
        )
        self.btn_diff_easy.pack(side="left", fill="x", expand=True, padx=(0, 3))

        self.btn_diff_med = tk.Button(
            self.diff_btn_frame, text="Medium", font=("Segoe UI", 9, "bold"),
            bg=CARD_BG, fg=MUTED_TEXT, activebackground=CARD_BG, activeforeground=MUTED_TEXT,
            bd=0, relief="flat", padx=10, pady=6, cursor="hand2",
            command=lambda: self.select_difficulty("medium")
        )
        self.btn_diff_med.pack(side="left", fill="x", expand=True, padx=(3, 3))

        self.btn_diff_hard = tk.Button(
            self.diff_btn_frame, text="Hard (Minimax)", font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
            bd=0, relief="flat", padx=10, pady=6, cursor="hand2",
            command=lambda: self.select_difficulty("hard")
        )
        self.btn_diff_hard.pack(side="left", fill="x", expand=True, padx=(3, 0))

        # Configure weights for the grids in settings panel
        self.settings_container.grid_columnconfigure(0, weight=1)

        # 4. Dynamic Status Bar
        self.status_label = tk.Label(
            main_frame, 
            text="Your Turn (X)", 
            font=("Segoe UI", 13, "bold"), 
            bg=BG_COLOR, 
            fg=TEXT_COLOR
        )
        self.status_label.pack(pady=(5, 10))

        # 5. Grid Board Frame (Responsive)
        board_frame = tk.Frame(main_frame, bg=GRID_LINE_COLOR, bd=0)
        board_frame.pack(fill="both", expand=True, pady=5)
        
        # Configure grid row and column weights for responsiveness
        for r in range(3):
            board_frame.rowconfigure(r, weight=1)
            board_frame.columnconfigure(r, weight=1)

        # Buttons (3x3 grid)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_frame, 
                text="", 
                bg=BG_COLOR, 
                fg=TEXT_COLOR, 
                activebackground=PANEL_BG, 
                activeforeground=TEXT_COLOR, 
                bd=0, 
                relief="flat",
                cursor="hand2",
                width=1,
                height=1
            )
            # Layout placement
            row = i // 3
            col = i % 3
            # We create a 1px border gap around the buttons to let the frame background show as the grid line
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            
            # Setup button commands & hover bindings
            btn.config(command=lambda idx=i: self.handle_click(idx))
            btn.bind("<Enter>", lambda e, idx=i: self.on_hover_enter(idx))
            btn.bind("<Leave>", lambda e, idx=i: self.on_hover_leave(idx))
            
            self.buttons.append(btn)

        # Bind configure event for dynamic font scaling
        board_frame.bind("<Configure>", self.resize_board)

        # 6. Reset Control Footer
        self.reset_btn = tk.Button(
            main_frame, 
            text="RESTART MATCH", 
            font=("Segoe UI", 11, "bold"), 
            bg=ACTIVE_GREEN, 
            fg=BG_COLOR, 
            activebackground="#43B581", 
            activeforeground=BG_COLOR, 
            bd=0, 
            relief="flat",
            padx=25, 
            pady=8, 
            cursor="hand2",
            command=self.reset_game
        )
        self.reset_btn.pack(pady=(20, 0))

    def resize_board(self, event):
        """Dynamically adjusts button font size to match the grid container's size."""
        w = event.width
        h = event.height
        # Cell size will be approximately 1/3 of the board dimensions
        cell_size = min(w, h) // 3
        # Pick a font size relative to the cell size (e.g. 40% of the cell size)
        font_size = max(12, int(cell_size * 0.40))
        
        new_font = ("Segoe UI", font_size, "bold")
        for btn in self.buttons:
            btn.config(font=new_font)

    # --- UI INTERACTION LOGIC (CONTROLLER INTERFACE) ---
    
    def select_game_mode(self, mode):
        if self.game_mode == mode:
            return
        self.game_mode = mode
        
        # Update Segmented Buttons Visually
        if mode == "vs_ai":
            self.btn_vs_ai.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
            self.btn_vs_human.config(bg=CARD_BG, fg=MUTED_TEXT)
            # Re-enable sub-settings
            self.toggle_settings_interaction(enable_ai_settings=True)
        else:
            self.btn_vs_ai.config(bg=CARD_BG, fg=MUTED_TEXT)
            self.btn_vs_human.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
            # Hide/Disable sub-settings
            self.toggle_settings_interaction(enable_ai_settings=False)
            
        self.reset_game()

    def select_symbol(self, symbol):
        if self.human_symbol == symbol or self.game_mode == "vs_human":
            return
        self.human_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        
        # Update Segmented Buttons Visually
        if symbol == "X":
            self.btn_sym_x.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
            self.btn_sym_o.config(bg=CARD_BG, fg=MUTED_TEXT)
        else:
            self.btn_sym_x.config(bg=CARD_BG, fg=MUTED_TEXT)
            self.btn_sym_o.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
            
        self.reset_game()

    def select_difficulty(self, diff):
        if self.difficulty == diff or self.game_mode == "vs_human":
            return
        self.difficulty = diff
        
        # Reset visual backgrounds for difficulty panel
        self.btn_diff_easy.config(bg=CARD_BG, fg=MUTED_TEXT)
        self.btn_diff_med.config(bg=CARD_BG, fg=MUTED_TEXT)
        self.btn_diff_hard.config(bg=CARD_BG, fg=MUTED_TEXT)

        # Highlight selection
        if diff == "easy":
            self.btn_diff_easy.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
        elif diff == "medium":
            self.btn_diff_med.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
        elif diff == "hard":
            self.btn_diff_hard.config(bg=ACCENT_COLOR, fg=TEXT_COLOR)
            
        self.reset_game()

    def toggle_settings_interaction(self, enable_ai_settings):
        """Disables/Enables symbols and difficulty toggles based on the active mode."""
        if enable_ai_settings:
            # Re-highlight active state configurations
            self.select_symbol(self.human_symbol)
            self.select_difficulty(self.difficulty)
            
            self.btn_sym_x.config(state="normal", cursor="hand2")
            self.btn_sym_o.config(state="normal", cursor="hand2")
            self.btn_diff_easy.config(state="normal", cursor="hand2")
            self.btn_diff_med.config(state="normal", cursor="hand2")
            self.btn_diff_hard.config(state="normal", cursor="hand2")
            self.lbl_play_as.config(fg=MUTED_TEXT)
            self.lbl_diff.config(fg=MUTED_TEXT)
        else:
            # Visual disable
            self.btn_sym_x.config(bg=CARD_BG, fg=MUTED_TEXT, state="disabled", cursor="arrow")
            self.btn_sym_o.config(bg=CARD_BG, fg=MUTED_TEXT, state="disabled", cursor="arrow")
            self.btn_diff_easy.config(bg=CARD_BG, fg=MUTED_TEXT, state="disabled", cursor="arrow")
            self.btn_diff_med.config(bg=CARD_BG, fg=MUTED_TEXT, state="disabled", cursor="arrow")
            self.btn_diff_hard.config(bg=CARD_BG, fg=MUTED_TEXT, state="disabled", cursor="arrow")
            self.lbl_play_as.config(fg="#4A4A52")
            self.lbl_diff.config(fg="#4A4A52")

    # --- BUTTON EVENT BINDINGS (HOVER ANIMATION EFFECTS) ---

    def on_hover_enter(self, idx):
        if self.game_active and self.board.grid[idx] == " ":
            self.buttons[idx].config(bg=HOVER_COLOR)
            # Show a faint indicator of who plays next
            faint_color = "#3E4151"
            self.buttons[idx].config(text=self.current_turn, fg=faint_color)

    def on_hover_leave(self, idx):
        if self.game_active and self.board.grid[idx] == " ":
            self.buttons[idx].config(bg=BG_COLOR, text="")

    # --- GAMEPLAY CORE STATE CONTROLS ---

    def reset_game(self):
        """Resets the board state, wipes button graphics, and sets active turn."""
        self.board = Board()
        self.current_turn = "X"
        self.game_active = True
        
        # Reset visual board
        for btn in self.buttons:
            btn.config(text="", state="normal", bg=BG_COLOR)

        # AI Turn instantiation setup
        if self.game_mode == "vs_ai":
            self.ai_player = AIPlayer(self.ai_symbol, difficulty=self.difficulty)
            
            # If AI plays first (Human plays O)
            if self.human_symbol == "O":
                self.update_status("AI is thinking...", color=MUTED_TEXT)
                self.disable_all_buttons()
                self.root.after(400, self.make_ai_move)
            else:
                self.update_status(f"Your Turn (X)", color=TEXT_COLOR)
        else:
            self.ai_player = None
            self.update_status("Player X's Turn", color=TEXT_COLOR)

    def handle_click(self, idx):
        """Executes player selection moves."""
        if not self.game_active or self.board.grid[idx] != " ":
            return

        # Play move
        self.board.make_move(idx, self.current_turn)
        self.update_button(idx, self.current_turn)

        if self.check_game_end():
            return

        # Turn transition
        if self.game_mode == "vs_ai":
            self.current_turn = self.ai_symbol
            self.update_status("AI is thinking...", color=MUTED_TEXT)
            self.disable_all_buttons()
            self.root.after(450, self.make_ai_move)
        else:
            self.current_turn = "O" if self.current_turn == "X" else "X"
            self.update_status(f"Player {self.current_turn}'s Turn", color=TEXT_COLOR)

    def make_ai_move(self):
        """Fires AI search computation, updates board, and restores interaction."""
        if not self.game_active:
            return

        move = self.ai_player.get_move(self.board)
        if move is not None:
            self.board.make_move(move, self.ai_symbol)
            self.update_button(move, self.ai_symbol)

        self.enable_empty_buttons()

        if self.check_game_end():
            return

        self.current_turn = self.human_symbol
        self.update_status(f"Your Turn ({self.human_symbol})", color=TEXT_COLOR)

    def update_button(self, idx, symbol):
        """Sets active cells to represent X/O using curated color properties."""
        color = COLOR_X if symbol == "X" else COLOR_O
        # Disable cell so it cannot be double-clicked
        self.buttons[idx].config(text=symbol, fg=color, bg=BG_COLOR, state="disabled", disabledforeground=color)

    def disable_all_buttons(self):
        """Locks board grid click responses."""
        for btn in self.buttons:
            btn.config(state="disabled")

    def enable_empty_buttons(self):
        """Restores click capabilities only for empty grid nodes."""
        for i, val in enumerate(self.board.grid):
            if val == " ":
                self.buttons[i].config(state="normal", bg=BG_COLOR)

    def check_game_end(self):
        """Analyzes board states to declare victory triggers."""
        winner = self.board.check_winner()
        if winner:
            self.game_active = False
            self.disable_all_buttons()
            
            # Announce winner
            if self.game_mode == "vs_ai":
                if winner == self.human_symbol:
                    self.update_status("🎉 YOU DEFEATED THE AI! 🎉", color=ACTIVE_GREEN)
                    messagebox.showinfo("Match Outcome", "Victory! You defeated the AI!")
                else:
                    self.update_status("💀 THE AI DEFEATED YOU 💀", color=COLOR_X)
                    messagebox.showinfo("Match Outcome", "Defeat! The AI has won.")
            else:
                self.update_status(f"🎉 PLAYER {winner} HAS WON! 🎉", color=ACTIVE_GREEN)
                messagebox.showinfo("Match Outcome", f"Congratulations, Player {winner} has won!")
            return True

        if self.board.is_full():
            self.game_active = False
            self.disable_all_buttons()
            self.update_status("🤝 TIE MATCH - DRAW 🤝", color="#FAA61A")
            messagebox.showinfo("Match Outcome", "Tie match! The board is full.")
            return True

        return False

    def update_status(self, text, color=TEXT_COLOR):
        """Changes the UI status message."""
        self.status_label.config(text=text, fg=color)

def launch_gui():
    # Support high-DPI scaling on Windows systems for clean, crisp typography
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
