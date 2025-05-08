import tkinter as tk
import tkinter.messagebox
import tkinter.font as font
import re

def create_board():
    return [["" for _ in range(3)] for _ in range(3)]

def check_winner(board, player):
    for row in range(3):
        if all([cell == player for cell in board[row]]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def check_draw(board):
    return all(all(row) for row in board)

def minmax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = 'O'
                    score = minmax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = 'X'
                    score = minmax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def computer_move(board):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = 'O'
                score = minmax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

class TicTacToeApp:
    def __init__(self, master):
        self.flip = 0
        self.master = master
        self.master.title("Tic Tac Toe")
        self.player_starts = True  # New attribute to decide who starts
        self.board = create_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.initialize_gui()
        self.game_mode = tk.StringVar()
        self.init_mode_selection()
        self.master.resizable(width=False, height=False)

        center_window(self.master)
    def initialize_gui(self):

        myFont = font.Font(size=40, weight="bold")
        self.turn_label = tk.Label(self.master, text="Player 1's Turn")
        self.turn_label.grid(row=4, columnspan=3)
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.master, text="", height=2, width=5, padx=3, pady=3, bg='#FF9800',
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button['font'] = myFont
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def radio_changed(self, *args):
        self.flip = 1

    def init_mode_selection(self):

        self.game_mode.trace("w", self.radio_changed)
        tk.Radiobutton(self.master, text="1 Player", variable=self.game_mode, value="1P", command=self.reset_board


        ).grid(row=3, column=0)
        tk.Radiobutton(self.master, text="2 Players", variable=self.game_mode, value="2P", command=self.reset_board

        ).grid(row=3, column=1)

        self.game_mode.set("1P")
        self.reset_board()

    def reset_board(self):
        self.board = create_board()

        if self.flip == 0:
            self.player_starts = not self.player_starts  # Toggle for the next game
        self.player_turn = self.player_starts  # Start with player or computer based on player_starts
        self.flip = 0
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state=tk.NORMAL)

        if not self.player_turn and self.game_mode.get() == "1P":
            self.master.after(180, self.play_computer_turn)

        if  self.game_mode.get() == "1P":
            if self.player_turn:
                self.turn_label.config(text="Player 1's Turn")
            else:
                self.turn_label.config(text="PC's Turn" if self.game_mode.get() == "1P" else "Player 2's Turn")

        if  self.game_mode.get() == "2P":
            if self.player_starts:
                self.turn_label.config(text="Player X's Turn")
            else:
                self.turn_label.config(text="Player O's Turn")

    def on_button_click(self,
                        row,
                        col):
        if self.board[row][col] == "" and (self.player_turn or self.game_mode.get() == "2P"):
            current_player = 'X' if self.player_turn else 'O'
            self.board[row][col] = current_player
            self.buttons[row][col].config(text=current_player, fg='#5F8670' if current_player == 'X' else '#B80000')

            if check_winner(self.board, current_player):
                tkinter.messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
                self.reset_board()
                return
            if check_draw(self.board):
                tkinter.messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
                return

            if self.game_mode.get() == "1P":
                self.player_turn = not self.player_turn
                if not self.player_turn:
                    self.master.after(180, self.play_computer_turn)
                    self.turn_label.config(text="PC's Turn")
            else:
                self.player_turn = not self.player_turn
                next_player = 'X' if current_player == 'O' else 'O'
                self.turn_label.config(text=f"Player {next_player}'s Turn")

    def play_computer_turn(self):
        move = computer_move(self.board)
        if move:
            self.board[move[0]][move[1]] = 'O'
            self.buttons[move[0]][move[1]].config(text='O')
            self.buttons[move[0]][move[1]].config(fg='#B80000')
            if check_winner(self.board, 'O'):
                tkinter.messagebox.showinfo("Tic Tac Toe", "Player O wins!")
                self.reset_board()
                return
            if check_draw(self.board):
                tkinter.messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
                return
        self.player_turn = True
        self.turn_label.config(text="Player 1's Turn")

def center_window(window):
    photo = tk.PhotoImage(file='icon.png')
    window.iconphoto(False, photo)
    window.update_idletasks()  # Ensure that geometry information is up-to-date
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()

    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    window.geometry(f"+{x_coordinate}+{y_coordinate}")


root = tk.Tk()
app = TicTacToeApp(root)
root.mainloop()
