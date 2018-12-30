import Game
# import ArduinoCommunication
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import camera
import Player
import Sandbox
import BoardInformation
import Gui
import numpy as np


def image_processing(last_board):  # last_board is only to make sure
    return camera.return_board()
    # return curr_board


def algorithm(ai, curr_board):  # fix!!!!!!!!!!!!!
    """
    A function that gets the current board and finds our systems move
    :param ai: our ai
    :param curr_board: the board on which the ai finds the move
    :return: to_put_down, to_flip, next board
    """
    table_player = Player.Player(type=Player.Player.PlayerTypes.TABLE, name="table", disk=-1 * ai.get_disk())
    our_move = BoardInformation.where_to_put(board=curr_board, our_player=ai, other_player=table_player)
    to_flip = BoardInformation.where_to_flip(board=curr_board, our_player=ai, other_player=table_player)
    next_board = BoardInformation.how_board_supposed_to_be_after_putting(board=curr_board, our_player=ai,
                                                                         other_player=table_player)
    return our_move, to_flip, next_board  # return to_put_down, to_flip, next board


def take_disk():
    ArduinoSerial.write("getDisk".encode())
    time.sleep(2)  # not the real waiting time
    # return None (advance to putting down), does nothing in the MVP


def move_to_xy(our_move):  # tuple (int, char)
    move = "move" + our_move  # build move command
    ArduinoSerial.write(move.encode())
    time.sleep(2)  # not the real waiting time


def put_down():
    ArduinoSerial.write("drop".encode())
    time.sleep(0.5)  # not the real waiting time
    # return None (advance to flipping)


def flip(to_flip):
    for i in range(len(to_flip)):
        flip = "flip" + to_flip[i]  # build command that arduino read
        ArduinoSerial.write(flip)
        time.sleep(2)  # delay - the 2 seconds is not the real time needed
        # return None


def check_four_by_four(curr_board):
    for i in range(len(curr_board)):
        for j in range(len(curr_board[i])):
            if curr_board[i][j] != 0 and (i not in range(3, 7) or j not in range(3, 7)):
                return False
    return True


def go_to_gui(curr_board, first_player, second_player):
    """
    A function that gets a board and continues a game from it
    :param curr_board: the board to start from
    :param first_player: the player that plays first
    :param second_player: the player that plays second
    :return The winner of the game
    """
    game = Game.Game(first_player, second_player)
    game.set_board(curr_board)
    return Gui.play_game(game, to_print=True)

if __name__ == '__main__':
    arduinoName = 'COM6'
    port = 9600
    # global ArduinoSerial
    # ArduinoSerial = serial.Serial(arduinoName, port)

    time.sleep(2)
    # take_disk()
    ai = Player.Player(heuristic=Sandbox.palti_white_h, name="ai", disk=Game.FIRST_COLOR)
    last_board = image_processing(None)
    while True:
        if input("Play your turn and then write 'Done' (or just 'D')") in {"Done", "done", 'D', 'd'}:
            # ArduinoSerial.write()
            curr_board = image_processing(last_board)

            if not check_four_by_four(curr_board):
                human_player = Player.Player(type=Player.Player.PlayerTypes.HUMAN, name="human", disk=Game.SECOND_COLOR)
                winner = go_to_gui(curr_board, first_player=ai, second_player=human_player)#first player is the ai because the human player did the last move
                break

            our_move, to_flip, next_board = algorithm(ai, curr_board)

            if not check_four_by_four(next_board):
                human_player = Player.Player(type=Player.Player.PlayerTypes.HUMAN, name="human", disk=Game.SECOND_COLOR)
                winner = go_to_gui(next_board, first_player=human_player, second_player=ai)#first player is the ai because the human player did the last move
                break

            move_to_xy(our_move)
            put_down()  # drops
            # flip(to_flip)
            take_disk()  # take disk for the next move
            #
            last_board = curr_board  # board for next move
    print ("the winner is: " + winner.name)