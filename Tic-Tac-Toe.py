# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 23:30:36 2019

@author: patel
"""
# A Program for Tic-Tac-Toe Game with Artificial Intelligence Algorithm
#by : Akshay P Patel
##################################################################################################################
#Importing all the libraries needed for the application
from tkinter import *
import tkinter.font as font
from operator import itemgetter
import copy
##################################################################################################################
#Creating a class for the Tic-Tac-Toe game
class TicTacToe:
    ##################################################################################################################
    #Creating Array for GUI buttons
    buttons = []
    # Declaring all the Winning Combination of the TicTacToe for the MinMax Algorithm
    winning_combinations = [[0, 1, 2], [0, 3, 6], [0, 4, 8], [1, 4, 7], [2, 5, 8], [2, 4, 6], [3, 4, 5], [6, 7, 8] ]
    ##################################################################################################################
    #Creating Constructor for the class TicTacToe
    def __init__(self):
        #Board Variable to maintain the status of all the 9 boxes
        self.board = [" "] * 9
        #Creating the List comprehension is needed so that each StringVar will not point to the same object
        self.moves = [StringVar() for _ in range(9)]
        #Crating variable X win
        self.x_wins = 0
        # Crating variable O win
        self.o_wins = 0
        # Crating variable Current Player
        self.curr_player = "X"
        # Crating variable Move Number
        self.move_number = 0
        # Crating variable for Winning Squares
        self.winning_squares = []
        # Crating variable to check Game is Over or not
        self.game_over = False
        #Creating Iterator for updating all the boxes
        self.apply_to_each_box(lambda x: x.set(" "), self.moves)
    ##################################################################################################################
    # Function for making a move
    def make_move(self, move):
        #By default the AI will be disabled and first turn is always for 'X'
        ai_on.config(state='disabled')
        self.move_number += 1
        #Checking if the current player is 'X'
        if self.curr_player == "X":
            #Updaing move into the board
            self.board[move] = "X"
            info_text.set("It is O's turn")
            self.curr_player = "O"
            # If the AI is turned on then tell the AI to take its turn
            if ai_on_off.get() and self.move_number < 9:
                self.ai_mm_init()
        else:
            self.board[move] = "O"
            info_text.set("It is X's turn")
            self.curr_player = "X"
        # Checking if the game is over or not, so that the win will not be counted twice for in AI mode
        if self.game_over:
            return
        self.buttons[move].config(state="disabled")
        # Checking for a winner
        winner = self.game_won(self.board)
        if winner is not None:
            self.who_won(winner)
            self.game_over = True
        # Check for a Tie game, Because there are maximum 9 moves possible
        elif self.move_number == 9 and self.board_full(self.board):
            #Setting up Status Label
            info_text.set("It's a tie!")
            #Chaning the color of all the boxes Text
            self.apply_to_each_box(lambda x: x.config(disabledforeground="red"), self.buttons)
            self.game_over = True
        self.update_board()
    ##################################################################################################################
    # Apply the given function to each state of boxes on the board like map but does not return anything
    def apply_to_each_box(self, func, some_list):
        for l in some_list:
            func(l)
    ##################################################################################################################
    # Function for returning the state of boxes
    def any_return(self, iterable):
        for e in iterable:
            if e:
                return e
        return False
    ##################################################################################################################
    # Function for checking who won the game, and change the GUI state accordingly
    def who_won(self, winner):
        #Checking if 'X' is winner
        if winner == "X":
            info_text.set("X wins!!!")
            self.x_wins += 1
        else:
            info_text.set("O wins!!!")
            self.o_wins += 1
        #Updating the Counter Label and changing the each boxes
        count_text.set("X: " + str(self.x_wins) + "\tO: " + str(self.o_wins))
        self.apply_to_each_box(lambda x: x.config(disabledforeground="red"),
                               [self.buttons[s] for s in self.winning_squares])
        #Game is Over so all buttons will be disabled until restart button is pressed
        for b in self.buttons:
            b.config(state="disabled")
    ##################################################################################################################
    # Function to reset the game to its base state
    def reset(self):
        ai_on.config(state='normal')
        self.curr_player = "X"
        self.move_number = 0
        self.game_over = False
        info_text.set("It is X's turn")
        self.board = [" " for _ in self.board]
        self.update_board()
        for b in self.buttons:
            b.config(state="normal")
            b.config(disabledforeground="black")
    ##################################################################################################################
    # Function to update the GUI to reflect the moves in the board attribute
    def update_board(self):
        for i in range(9):
            self.moves[i].set(self.board[i])
    ##################################################################################################################
    # Function to Check each of the winning combinations to check if anyone has won
    def game_won(self, gameboard):
        # Check if any of the winning combinations have been used
        check = self.any_return([self.three_in_a_row(gameboard, c) for c in TicTacToe.winning_combinations])
        if check:
            return check
        else:
            return None
    ##################################################################################################################
    # Function to Check if the three given squares are owned by the same player's Fork
    def three_in_a_row(self, gameboard, squares):
        # Get the given squares from the board are check if they are all equal
        combo = set(itemgetter(squares[0], squares[1], squares[2])(gameboard))
        if len(combo) == 1 and combo.pop() != " ":
            self.winning_squares = squares
            return gameboard[squares[0]]
        else:
            return None
    ##################################################################################################################
    # Function to Get the opposite player
    def get_enemy(self, curr_player):
        if curr_player == "X":
            return "O"
        else:
            return "X"
    ##################################################################################################################
    #Function which Returns true if the board is full
    def board_full(self, board):
        for s in board:
            if s == " ":
                return False
        return True
    ##################################################################################################################
    # Function to initialize the Minimax algorithm
    def ai_mm_init(self):
        player = "O"
        #Intializing the weights for the Minimax Algorith, Profit and Loss
        a = -1000
        b = 1000
        board_copy = copy.deepcopy(self.board)
        best_outcome = -100
        best_move = None
        #Running the minimax algorithm for all the 9 boxes of the board
        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.get_enemy(player), board_copy, a, b)
                board_copy[i] = " "
                #Checking for the best move
                if player == "O":
                    if val > best_outcome:
                        best_outcome = val
                        best_move = i
                else:
                    if val < best_outcome:
                        best_outcome = val
                        best_move = i
        #Making a move with the best_move got by the minimax algorithm
        self.make_move(best_move)
    ##################################################################################################################
    # Function for the Minimax algorithm, with alpha-beta pruning
    def minimax(self, player, board, alpha, beta):
        board_copy = copy.deepcopy(board)
        # Check for a win
        winner = self.game_won(board_copy)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.board_full(board_copy):
            return 0
        best_outcome = -100 if player == "O" else 100
        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.get_enemy(player), board_copy, alpha, beta)
                board_copy[i] = " "
                #Doing Alpha-Pruning(maximum profit)
                if player == "O":
                    best_outcome = max(best_outcome, val)
                    alpha = min(alpha, best_outcome)
                #Doing Beta_Pruning (minimim loss)
                else:
                    best_outcome = min(best_outcome, val)
                    beta = max(beta, best_outcome)
                #Getting the Best Possible Profit
                if beta <= alpha:
                    return best_outcome
        return best_outcome
##################################################################################################################
#Main(Driver) code for the application
#Creating Window using Tkinter
root = Tk()
root.title("Akshay's Tic-Tac-Toe Game")
game = TicTacToe()
#Creating Customize Fonts for Button Text and Label Text
myFont = font.Font(family='Helvetica', size=36, weight=font.BOLD)
myFont1 = font.Font(family='Helvetica', size=20)
##################################################################################################################
#Setting up the GUI for the Game
# Creating Welcome Label
welcome_text = StringVar()
welcome_text.set("Akshay's Tic-Tac-Toe Game! You won't beat my AI!!")
welcome = Label(root, textvariable=welcome_text)
welcome['font'] = myFont1
#Placing Label on the Grid
welcome.grid(row=0, column=0, columnspan=3)
##################################################################################################################
# Creating Label used to display the current scores
count_text = StringVar()
count_text.set("X: " + str(game.x_wins) + "\tO: " + str(game.o_wins))
count = Label(root, textvariable=count_text)
count['font'] = myFont1
#Placing Label on the Grid
count.grid(row=1, column=0, columnspan=3)
##################################################################################################################
#Creating Label used to give the user information
info_text = StringVar()
info_text.set("It is X's turn")
info = Label(root, textvariable=info_text)
info['font'] = myFont1
#Placing Label on the Grid
info.grid(row=2, column=0, columnspan=3)
##################################################################################################################
#Creating buttons for the Tic Tac Toe board
for square in range(9):
    #Giving command of make_move if any button will be pressed
    temp_button = Button(root, bg='white', textvariable=game.moves[square], command=lambda s=square: game.make_move(s))
    # Divide by 3 to get row number, modulus by 3 to get column number
    #Creating Temporary Button
    temp_button.grid(row=int((square / 3) + 3), column=(square % 3), sticky=NSEW)
    temp_button['font'] = myFont
    # Placing Button on the Grid
    game.buttons.append(temp_button)
##################################################################################################################
# Creating Button for resetting the game
restart_button_text = StringVar()
restart_button_text.set("Restart")
restart_button = Button(root, textvariable=restart_button_text, command=game.reset, bg='white')
restart_button['font'] = myFont1
#Placing Button on the Grid
restart_button.grid(row=1, column=0)
##################################################################################################################
#Creating Checkbox for turning the AI on/off
ai_on_off = IntVar()
ai_on = Checkbutton(root, text="Turn on AI", variable=ai_on_off)
ai_on['font'] = myFont1
#Placing Button on the Grid
ai_on.grid(row=1, column=2)
##################################################################################################################
#Setting the size of the rows and columns
root.columnconfigure(0, minsize=200)
root.columnconfigure(1, minsize=200)
root.columnconfigure(2, minsize=200)
root.rowconfigure(3, minsize=200)
root.rowconfigure(4, minsize=200)
root.rowconfigure(5, minsize=200)
# Start the GUI loop
root.mainloop()
##################################################################################################################