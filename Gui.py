import Game
import Player
from tkinter import *
from math import *
from time import *
from random import *
import numpy as np
import time

class Gui:

    def __init__(self, game, to_print = False):
        self.game = game
        self.game.number_of_turns_attempted = 0
        self.to_print = to_print
        self.root = Tk()
        self.screen = Canvas(self.root, width=500, height=600, background='green', highlightthickness=0)
        self.screen.pack()
        self.player1 = self.game.player1
        self.player2 = self.game.player2
        self.curr_player = self.player1
        self.curr_coordinate = None
        self.old_coordinate = None
        self.next_player = self.player2
        self.screen.bind("<Button-1>", self.click_handle)
        self.screen.bind("<Key>", self.key_handle)
        self.screen.focus_set()
        self.players = self.game.players
        self.intro = True
        self.old_board = self.game.board
        self.do_intro()
        self.board = self.game.board
        self.game_is_done = False
        self.root.mainloop()

    def create_buttons(self):
        # Restart button
        # Background/shadow
        self.screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
        self.screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

        # Arrow
        self.screen.create_arc(5, 5, 45, 45, fill="#000088", width="2", style="arc", outline="white",
                          extent=300)
        self.screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

        # Quit button
        # Background/shadow
        self.screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
        self.screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")
        # "X"
        self.screen.create_line(455, 5, 495, 45, fill="white", width="3")
        self.screen.create_line(495, 5, 455, 45, fill="white", width="3")

    def draw_score_board(self):
        global moves
        # Deleting prior score elements
        self.screen.delete("score")

        # Scoring based on number of tiles
        player1_score = self.game.get_color_disk_num(self.player1)
        player2_score = self.game.get_opponent_disk_num(self.player1)

        if self.curr_player is self.player2:
            player1_color = "green"
            player2_color = "gray"
        else:
            player1_color = "gray"
            player2_color = "green"

        self.screen.create_oval(5, 540, 25, 560, fill=player1_color, outline=player1_color)
        self.screen.create_oval(380, 540, 400, 560, fill=player2_color, outline=player2_color)

        # Pushing text to screen
        if Game.FIRST_COLOR == Game.RED:
            self.screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="red",
                               text=player1_score)
            self.screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black",
                               text=player2_score)
        else:
            self.screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black",
                                    text=player1_score)
            self.screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="red",
                                    text=player2_score)

        moves =  player1_score +  player2_score
        self.screen.update()

    def key_handle(self, event):
        symbol = event.keysym
        if symbol.lower() == "r":
            print("r")
            self.game.reset_game(self.player1, self.player2)
            self.reset(self.game)
        elif symbol.lower() == "q":
            self.quit()

    def quit(self):
        self.screen.delete(ALL)
        self.root.quit()

    def reset(self, game):
        self.game = game
        self.player1 = self.game.player1
        self.player2 = self.game.player2
        self.curr_player = self.player1
        self.next_player = self.player2
        self.old_board = game.board
        self.board = game.board
        self.update_board()
        print('reset')
        self.play_game()


    def do_intro(self):
        # Title and shadow
        self.screen.create_text(250, 203, anchor="c", text="Reversi", font=("Consolas", 50), fill="#aaa")
        self.screen.create_text(250, 200, anchor="c", text="Reversi", font=("Consolas", 50), fill="#fff")

        # Creating the difficulty buttons
        for i in range(3):
            # Background
            self.screen.create_rectangle(25 + 155 * i, 310, 155 + 155 * i, 355, fill="#000", outline="#000")
            self.screen.create_rectangle(25 + 155 * i, 300, 155 + 155 * i, 350, fill="#111", outline="#111")

            spacing = 130 / (i + 2)
            for x in range(i + 1):
                # Star with double shadow
                self.screen.create_text(25 + (x + 1) * spacing + 155 * i, 326, anchor="c", text="\u2605", font=("Consolas", 25), fill="#b29600")
                self.screen.create_text(25 + (x + 1) * spacing + 155 * i, 327, anchor="c", text="\u2605", font=("Consolas", 25), fill="#b29600")
                self.screen.create_text(25 + (x + 1) * spacing + 155 * i, 325, anchor="c", text="\u2605", font=("Consolas", 25), fill="#ffd700")

        self.screen.update()

    def click_handle(self, event):
        xMouse = event.x
        yMouse = event.y
        if self.game_is_done:
            sleep(0.5)
            self.quit()
        if not self.intro:
            if xMouse >= 450 and yMouse <= 50:
                self.quit()
            elif xMouse <= 50 and yMouse <= 50:
                self.game.reset_game(self.player1, self.player2)
                self.reset(self.game)
            else:
                # Is it the player's turn?
                if self.curr_player.type == Player.Player.PlayerTypes.HUMAN:
                    # Delete the highlights
                    x = int((event.x - 50) / 50)
                    y = int((event.y - 50) / 50)
                    # Determine the grid index for where the mouse was clicked
                    # If the click is inside the bounds and the move is valid, move to that location
                    legal_moves = self.game.get_legal_moves(self.curr_player.disk)
                    if legal_moves == []:
                        self.game.number_of_turns_attempted += 1
                        self.curr_player = self.game.players[self.game.number_of_turns_attempted % 2]
                        self.next_player = self.game.players[(self.game.number_of_turns_attempted + 1) % 2]
                        self.old_board = self.board
                        # self.update_board()
                        self.play_game()
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        if (y,x) in legal_moves and self.curr_player.type == Player.Player.PlayerTypes.HUMAN:
                            self.old_board = np.copy(self.game.board)
                            self.old_board[y][x] = self.curr_player.disk
                            self.game.do_move(self.curr_player.disk, (y,x))
                            self.board = self.game.board
                            self.game.number_of_turns_attempted += 1
                            self.curr_player = self.game.players[self.game.number_of_turns_attempted % 2]
                            self.next_player = self.game.players[(self.game.number_of_turns_attempted + 1) % 2]
                            self.update_board()
                            self.play_game()


        else:
            # Difficulty clicking
            if 300 <= yMouse <= 350:
                # One star
                if 25 <= xMouse <= 155:
                    self.intro = False
                    easy_player = Player.Player.load_player('pklFiles/easy_player.pkl')
                    self.game = Game.Game(easy_player, self.player2)
                    self.play_game()
                    # depth = 1 todo
                # Two star
                elif 180 <= xMouse <= 310:
                    self.intro = False
                    self.play_game()
                    # depth = 4
                    # playGame() todo
                # Three star
                elif 335 <= xMouse <= 465:
                    self.intro = False
                    self.play_game()
                    # depth = 6
                    # playGame() todo

    def draw_grid_background(self, outline=True):
        # If we want an outline on the board then draw one
        if outline:
            self.screen.create_rectangle(50, 50, 450, 450, outline="#111")

        # Drawing the intermediate lines
        for i in range(7):
            lineShift = 50 + 50 * (i + 1)

            # Horizontal line
            self.screen.create_line(50, lineShift, 450, lineShift, fill="#111")

            # Vertical line
            self.screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

        self.screen.update()

    def update_board(self):
        self.screen.delete("highlight")
        self.screen.delete("tile")
        for y in range(8):
            for x in range(8):
                # Could replace the circles with images later, if I want
                if self.old_board[x][y] == Game.RED:
                    self.screen.create_oval(54 + 50 * y, 54 + 50 * x, 96 + 50 * y, 96 + 50 * x, tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    # self.screen.create_oval(54 + 50 * y, 54 + 50 * x, 96 + 50 * y, 96 + 50 * x, tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    self.screen.create_oval(54 + 50 * y, 52 + 50 * x, 96 + 50 * y, 94 + 50 * x, tags="tile {0}-{1}".format(x, y), fill="red", outline="red")
                    # self.screen.create_oval(54 + 50 * y, 52 + 50 * x, 96 + 50 * y, 94 + 50 * x, tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif self.old_board[x][y] == Game.BLACK:
                    self.screen.create_oval(54 + 50 * y, 54 + 50 * x, 96 + 50 * y, 96 + 50 * x, tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    self.screen.create_oval(54 + 50 * y, 52 + 50 * x, 96 + 50 * y, 94 + 50 * x, tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")
        # Animation of new tiles
        self.screen.update()
        for y in range(8):
            for x in range(8):
                # Could replace the circles with images later, if I want
                if self.board[x][y] != self.old_board[x][y] and self.board[x][y] == Game.RED:
                    self.screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        self.screen.create_oval(54 + i + 50 * y, 54 + i + 50 * x, 96 - i + 50 * y, 96 - i + 50 * x, tags="tile animated", fill="#000", outline="#000")
                        self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="#111", outline="#111")
                        # self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        self.screen.create_oval(54 + i + 50 * y, 54 + i + 50 * x, 96 - i + 50 * y, 96 - i + 50 * x, tags="tile animated", fill="#000", outline="#000")
                        # self.screen.create_oval(54 + i + 50 * y, 54 + i + 50 * x, 96 - i + 50 * y, 96 - i + 50 * x, tags="tile animated", fill="#aaa", outline="#aaa")
                        self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="red", outline="red")
                        # self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    self.screen.create_oval(54 + 50 * y, 54 + 50 * x, 96 + 50 * y, 96 + 50 * x, tags="tile", fill="#000", outline="#000")
                    # self.screen.create_oval(54 + 50 * y, 54 + 50 * x, 96 + 50 * y, 96 + 50 * x, tags="tile", fill="#aaa", outline="#aaa")
                    self.screen.create_oval(54 + 50 * y, 52 + 50 * x, 96 + 50 * y, 94 + 50 * x, tags="tile", fill="red", outline="red")
                    # self.screen.create_oval(54 + 50 * y, 52 + 50 * x, 96 + 50 * y, 94 + 50 * x, tags="tile", fill="#fff", outline="#fff")
                    self.screen.update()

                elif self.board[x][y] != self.old_board[x][y] and self.board[x][y] == Game.BLACK:
                    self.screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        self.screen.create_oval(54 + i + 50 * y, 54 + i + 50 * x, 96 - i + 50 * y, 96 - i + 50 * x, tags="tile animated", fill="#000", outline="#000")
                        # self.screen.create_oval(54 + i + 50 * y, 54 + i + 50 * x, 96 - i + 50 * y, 96 - i + 50 * x, tags="tile animated", fill="#aaa", outline="#aaa")
                        self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="red", outline="red")
                        # self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        self.screen.create_oval(54 + i + 50 * y, 54 + i + 50 * x, 96 - i + 50 * y, 96 - i + 50 * x, tags="tile animated", fill="#000", outline="#000")
                        self.screen.create_oval(54 + i + 50 * y, 52 + i + 50 * x, 96 - i + 50 * y, 94 - i + 50 * x, tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")

                    self.screen.create_oval(54 + 50 * y, 54 + 50 * x, 96 + 50 * y, 96 + 50 * x, tags="tile", fill="#000", outline="#000")
                    self.screen.create_oval(54 + 50 * y, 52 + 50 * x, 96 + 50 * y, 94 + 50 * x, tags="tile", fill="#111", outline="#111")
                    self.screen.update()

        # Drawing of highlight circles
        valid_moves = self.game.get_legal_moves(self.curr_player.disk)
        for y in range(8):
            if self.curr_player.type == Player.Player.PlayerTypes.MINIMAX:
                break
            for x in range(8):
                    if (y,x) in valid_moves:
                        self.screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1), tags="highlight", fill="white", outline="white")
        self.screen.update()
        self.draw_score_board()

        if self.game_is_done:
            self.screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="The game is done!")
            self.old_board = self.game.board

    def do_next_turn(self):
        self.game.update_safe_number()
        print(self.game.fixed_disks)
        print("*********************")
        self.curr_player = self.game.players[self.game.number_of_turns_attempted % 2]
        self.next_player = self.game.players[(self.game.number_of_turns_attempted + 1) % 2]
        if self.curr_player.type != Player.Player.PlayerTypes.HUMAN:
            self.play_game()


    def play_game(self):

        if self.game.number_of_turns_attempted == 0:
            self.screen.delete(ALL)
            self.create_buttons()
            self.draw_score_board()
            self.draw_grid_background()
            self.update_board()

        if self.game.is_board_full() == True:
            self.game_is_done = True

        if not self.game_is_done:
            self.draw_score_board()
            self.curr_player = self.game.players[self.game.number_of_turns_attempted % 2]
            self.next_player = self.game.players[(self.game.number_of_turns_attempted + 1) % 2]
            if self.curr_player.type != Player.Player.PlayerTypes.HUMAN and not self.game_is_done:
                op = self.curr_player.choose_move(self.game)
                if op[1] is None:
                    if self.game.get_legal_moves(self.next_player.disk) == []:
                        self.game_is_done = True
                else:
                    self.old_board = np.copy(self.game.board)
                    self.old_board[op[1][0]][op[1][1]] = self.curr_player.disk
                    self.game.do_move(self.players[self.game.number_of_turns_attempted % 2].get_disk(), op[1])
                    self.board = np.copy(self.game.board)
                if self.to_print:
                    print("player, ", self.players[self.game.number_of_turns_attempted % 2].name,
                          " played ", op[1])
                self.game.number_of_turns_attempted += 1
                self.curr_player = self.game.players[self.game.number_of_turns_attempted % 2]
                self.next_player = self.game.players[(self.game.number_of_turns_attempted + 1) % 2]

                self.update_board()
                self.do_next_turn()
        else:
            self.game_is_fin()


    def game_is_fin(self):
        self.update_board()
        if self.game.get_winner_disk() == self.players[0].get_disk():
            # self.players[0].number_of_wins += 1
            return self.players[0]
        elif self.game.get_winner_disk() == self.players[1].get_disk():
            # self.players[1].number_of_wins += 1
            return self.players[1]
        else:
            print("tie")
            return self.players[0] #todo remember that this state is a tie






()