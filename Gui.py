import Game
import Player
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy


# Method for drawing the gridlines
def drawGridBackground(outline=False):
    # If we want an outline on the board then draw one
    if outline:
        screen.create_rectangle(50, 50, 450, 450, outline="#111")

    # Drawing the intermediate lines
    for i in range(7):
        lineShift = 50 + 50 * (i + 1)

        # Horizontal line
        screen.create_line(50, lineShift, 450, lineShift, fill="#111")

        # Vertical line
        screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

    screen.update()


def play_game(game, to_print=False):
    """
    A function that plays a game between two heuristics
    :param p1: player number 1 (the first to play)
    :param p2: player number 2 (the second to play)
    :return: the winning player and the grades of each heuristic in the game
    """
    outline = False
    root = Tk()
    screen = Canvas(root, width=500, height=600, background="#222", highlightthickness=0)
    screen.pack()


    players = game.players
    p1 = players[0]
    p2 = players[1]
    p1.set_disk(Game.FIRST_COLOR)
    p2.set_disk(Game.SECOND_COLOR)
    if p1.get_disk() == p2.get_disk():
        raise ValueError("two players can't have the same color")
    turn = 0
    while not game.is_board_full():
        if turn == 0:
            for x in range(8):
                for y in range (8):
                    screen.create_text((68 + 50 * x + 32 + 50 * (x + 1)) / 2, (68 + 50 * y + 32 +
                                                                               50 * (y + 1)) / 2,
                                       text=str(y) + "," + str(x))
            # Restart button
            # Background/shadow
            screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
            screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

            # Arrow
            screen.create_arc(5, 5, 45, 45, fill="#000088", width="2", style="arc", outline="white",
                              extent=300)
            screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

            # Quit button
            # Background/shadow
            screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
            screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")
            # "X"
            screen.create_line(455, 5, 495, 45, fill="white", width="3")
            screen.create_line(495, 5, 455, 45, fill="white", width="3")
            if outline:
                screen.create_rectangle(50, 50, 450, 450, outline="#111")

            # Drawing the intermediate lines
            for i in range(7):
                lineShift = 50 + 50 * (i + 1)

                # Horizontal line
                screen.create_line(50, lineShift, 450, lineShift, fill="#111")

                # Vertical line
                screen.create_line(lineShift, 50, lineShift, 450, fill="#111")
                create_buttons()
        oldarray = game.board
        screen.delete("highlight")
        screen.delete("tile")
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if oldarray[y][x] == Game.WHITE:

                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#aaa",
                                       outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#fff",
                                       outline="#fff")

                elif oldarray[y][x] == Game.BLACK:
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#000",
                                       outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#111",
                                       outline="#111")
        # Animation of new tiles
        screen.update()
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if game.board[y][x] != oldarray[y][x] and game.board[y][x] == Game.WHITE:
                    screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                           96 - i + 50 * y, tags="tile animated", fill="#000",
                                           outline="#000")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                           94 - i + 50 * y, tags="tile animated", fill="#111",
                                           outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                           96 - i + 50 * y, tags="tile animated", fill="#aaa",
                                           outline="#aaa")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                           94 - i + 50 * y, tags="tile animated", fill="#fff",
                                           outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile", fill="#aaa", outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile", fill="#fff", outline="#fff")
                    screen.update()

                elif game.board[y][x] != oldarray[y][x] and game.board[y][x] == Game.BLACK:
                    screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                           96 - i + 50 * y, tags="tile animated", fill="#aaa",
                                           outline="#aaa")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                           94 - i + 50 * y, tags="tile animated", fill="#fff",
                                           outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                           96 - i + 50 * y, tags="tile animated", fill="#000",
                                           outline="#000")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                           94 - i + 50 * y, tags="tile animated", fill="#111",
                                           outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")

                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile", fill="#000", outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile", fill="#111", outline="#111")
                    screen.update()
                    # Drawing of highlight circles
        for x in range(8):
            for y in range(8):
                if (y, x) in game.get_legal_moves(players[turn % 2].get_disk()):
                    screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1),
                                       32 + 50 * (y + 1), tags="highlight", fill="#008000",
                                       outline="#008000")
                    screen.create_text((68 + 50 * x + 32 + 50 * (x + 1)) / 2, (68 + 50 * y + 32 +
                                        50 * (y + 1)) / 2, text=str(y) + "," + str(x))

                    screen.update()  #todo if what to not show highlight comment
        op = players[turn % 2].choose_move(game)
        if op[1] == None:
            if players[(turn + 1) % 2].choose_move(game)[1] == None:
                break
        else:
            game.do_move(players[turn % 2].get_disk(), op[1])

        if to_print:
            print(players[turn % 2].name, " played: ", op[1])
            print(players[(turn + 1) % 2].name +" it is now your turn")
        turn += 1


    """
    maybe add here somehow to get a value of winning and not just a winner - when the module is 
    more advanced! 
    """

    oldarray = game.board
    screen.delete("highlight")
    screen.delete("tile")
    for x in range(8):
        for y in range(8):
            # Could replace the circles with images later, if I want
            if oldarray[y][x] == Game.WHITE:

                screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                   tags="tile {0}-{1}".format(x, y), fill="#aaa",
                                   outline="#aaa")
                screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                   tags="tile {0}-{1}".format(x, y), fill="#fff",
                                   outline="#fff")

            elif oldarray[y][x] == Game.BLACK:
                screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                   tags="tile {0}-{1}".format(x, y), fill="#000",
                                   outline="#000")
                screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                   tags="tile {0}-{1}".format(x, y), fill="#111",
                                   outline="#111")
    # Animation of new tiles
    screen.update()
    for x in range(8):
        for y in range(8):
            # Could replace the circles with images later, if I want
            if game.board[y][x] != oldarray[y][x] and game.board[y][x] == Game.WHITE:
                screen.delete("{0}-{1}".format(x, y))
                # 42 is width of tile so 21 is half of that
                # Shrinking
                for i in range(21):
                    screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                       96 - i + 50 * y, tags="tile animated", fill="#000",
                                       outline="#000")
                    screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                       94 - i + 50 * y, tags="tile animated", fill="#111",
                                       outline="#111")
                    if i % 3 == 0:
                        sleep(0.01)
                    screen.update()
                    screen.delete("animated")
                # Growing
                for i in reversed(range(21)):
                    screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                       96 - i + 50 * y, tags="tile animated", fill="#aaa",
                                       outline="#aaa")
                    screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                       94 - i + 50 * y, tags="tile animated", fill="#fff",
                                       outline="#fff")
                    if i % 3 == 0:
                        sleep(0.01)
                    screen.update()
                    screen.delete("animated")
                screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                   tags="tile", fill="#aaa", outline="#aaa")
                screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                   tags="tile", fill="#fff", outline="#fff")
                screen.update()

            elif game.board[y][x] != oldarray[y][x] and game.board[y][x] == Game.BLACK:
                screen.delete("{0}-{1}".format(x, y))
                # 42 is width of tile so 21 is half of that
                # Shrinking
                for i in range(21):
                    screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                       96 - i + 50 * y, tags="tile animated", fill="#aaa",
                                       outline="#aaa")
                    screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                       94 - i + 50 * y, tags="tile animated", fill="#fff",
                                       outline="#fff")
                    if i % 3 == 0:
                        sleep(0.01)
                    screen.update()
                    screen.delete("animated")
                # Growing
                for i in reversed(range(21)):
                    screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x,
                                       96 - i + 50 * y, tags="tile animated", fill="#000",
                                       outline="#000")
                    screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x,
                                       94 - i + 50 * y, tags="tile animated", fill="#111",
                                       outline="#111")
                    if i % 3 == 0:
                        sleep(0.01)
                    screen.update()
                    screen.delete("animated")

                screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                   tags="tile", fill="#000", outline="#000")
                screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                   tags="tile", fill="#111", outline="#111")
                screen.update()
    if game.get_winner_disk() == players[0].get_disk():
        screen.create_text(250, 550, anchor="c", font=("Consolas", 15),
                           text="The game is done!")
        return players[0]
    elif game.get_winner_disk() == players[1].get_disk():
        screen.create_text(250, 550, anchor="c", font=("Consolas", 15),
                           text="The game is done!")
        return players[1]
    else:
        raise ValueError("something went wrong! check your code!")


    # if not self.won:
    #     # Draw the scoreboard and update the screen
    #     Board.drawScoreBoard()
    #     screen.update()
    #     # If the computer is AI, make a move
    #     if self.player == 1:
    #         startTime = time()
    #         self.oldarray = self.array
    #         alphaBetaResult = self.alphaBeta(self.array, depth, -float("inf"), float("inf"), 1)
    #         self.array = alphaBetaResult[1]
    #
    #         if len(alphaBetaResult) == 3:
    #             position = alphaBetaResult[2]
    #             self.oldarray[position[0]][position[1]] = "b"
    #
    #         self.player = 1 - self.player
    #         deltaTime = round((time() - startTime) * 100) / 100
    #         if deltaTime < 2:
    #             sleep(2 - deltaTime)
    #         nodes = 0
    #         # Player must pass?
    #         self.passTest()
    # else:
    #     screen.create_text(250, 550, anchor="c", font=("Consolas", 15),
    #                        text="The game is done!")


# ~~~~~~~~~~~~~~~~#
# Othello Program
# John Fish
# Updated from May 29, 2015 - June 26, 2015
#
# Has both basic AI (random decision) as well as
# educated AI (minimax).
#
# ~~~~~~~~~~~~~~~~#

# Library import
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy

# Variable setup
nodes = 0
depth = 4
moves = 0

# Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#222", highlightthickness=0)
screen.pack()


class Board:
    def _init_(self):
        # White goes first (0 is white and player,1 is black and computer)
        self.player = 0
        self.passed = False
        self.won = False
        # Initializing an empty board
        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)

        # Initializing center values
        self.array[3][3] = "w"
        self.array[3][4] = "b"
        self.array[4][3] = "b"
        self.array[4][4] = "w"

        # Initializing old values # Updating the board to the screen


    # METHOD: Draws scoreboard to screen
    def drawScoreBoard(self):
        global moves
        # Deleting prior score elements
        screen.delete("score")

        # Scoring based on number of tiles
        player_score = 0
        computer_score = 0
        for x in range(8):
            for y in range(8):
                if self.array[x][y] == "w":
                    player_score += 1
                elif self.array[x][y] == "b":
                    computer_score += 1

        if self.player == 0:
            player_colour = "green"
            computer_colour = "gray"
        else:
            player_colour = "gray"
            computer_colour = "green"

        screen.create_oval(5, 540, 25, 560, fill=player_colour, outline=player_colour)
        screen.create_oval(380, 540, 400, 560, fill=computer_colour, outline=computer_colour)

        # Pushing text to screen
        screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="white",
                           text=player_score)
        screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black",
                           text=computer_score)

        moves = player_score + computer_score

    # METHOD: Test if player must pass: if they do, switch the player
    def passTest(self):
        mustPass = True
        for x in range(8):
            for y in range(8):
                if valid(self.array, self.player, x, y):
                    mustPass = False
        if mustPass:
            self.player = 1 - self.player
            if self.passed == True:
                self.won = True
            else:
                self.passed = True
            self.update()
        else:
            self.passed = False






# When the user clicks, if it's a valid move, make the move
def clickHandle(event):
    global depth
    xMouse = event.x
    yMouse = event.y
    if running:
        if xMouse >= 450 and yMouse <= 50:
            root.destroy()
        elif xMouse <= 50 and yMouse <= 50:
            playGame()
        else:
            # Is it the player's turn?
            if board.player == 0:
                # Delete the highlights
                x = int((event.x - 50) / 50)
                y = int((event.y - 50) / 50)
                # Determine the grid index for where the mouse was clicked

                # If the click is inside the bounds and the move is valid, move to that location
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if valid(board.array, board.player, x, y):
                        board.boardMove(x, y)
    else:
        # Difficulty clicking
        if 300 <= yMouse <= 350:
            # One star
            if 25 <= xMouse <= 155:
                depth = 1
                playGame()
            # Two star
            elif 180 <= xMouse <= 310:
                depth = 4
                playGame()
            # Three star
            elif 335 <= xMouse <= 465:
                depth = 6
                playGame()


def keyHandle(event):
    symbol = event.keysym
    if symbol.lower() == "r":
        playGame()
    elif symbol.lower() == "q":
        root.destroy()


def create_buttons():
    # Restart button
    # Background/shadow
    screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
    screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

    # Arrow
    screen.create_arc(5, 5, 45, 45, fill="#000088", width="2", style="arc", outline="white",
                      extent=300)
    screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

    # Quit button
    # Background/shadow
    screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
    screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")
    # "X"
    screen.create_line(455, 5, 495, 45, fill="white", width="3")
    screen.create_line(495, 5, 455, 45, fill="white", width="3")


def runGame():
    global running
    running = False
    # Title and shadow
    screen.create_text(250, 203, anchor="c", text="Othello", font=("Consolas", 50), fill="#aaa")
    screen.create_text(250, 200, anchor="c", text="Othello", font=("Consolas", 50), fill="#fff")

    # Creating the difficulty buttons
    for i in range(3):
        # Background
        screen.create_rectangle(25 + 155 * i, 310, 155 + 155 * i, 355, fill="#000", outline="#000")
        screen.create_rectangle(25 + 155 * i, 300, 155 + 155 * i, 350, fill="#111", outline="#111")

        spacing = 130 / (i + 2)
        for x in range(i + 1):
            # Star with double shadow
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 326, anchor="c", text="\u2605",
                               font=("Consolas", 25), fill="#b29600")
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 327, anchor="c", text="\u2605",
                               font=("Consolas", 25), fill="#b29600")
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 325, anchor="c", text="\u2605",
                               font=("Consolas", 25), fill="#ffd700")

    screen.update()


def playGame():
    global board, running
    running = True
    screen.delete(ALL)
    create_buttons()
    board = 0

    # Draw the background
    drawGridBackground()

    # Create the board and update it
    board = Board()
    board.update()


# runGame()
#
# # Binding, setting
# screen.bind("<Button-1>", clickHandle)
# screen.bind("<Key>", keyHandle)
# screen.focus_set()
#
# # Run forever
# root.wm_title("Othello")
# root.mainloop()