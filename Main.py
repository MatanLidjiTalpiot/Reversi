import Game
# import ArduinoCommunication
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import camera
import Player
import motor
import HeuristicsSandbox
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
    table_player = Player.Player(type=Player.Player.PlayerTypes.TABLE,
                                 name="table", disk=-1 * ai.get_disk())
    our_move = BoardInformation.where_to_put(board=curr_board, our_player=ai,
                                             other_player=table_player)
    to_flip = BoardInformation.where_to_flip(board=curr_board, our_player=ai,
                                             other_player=table_player)
    next_board = BoardInformation.how_board_supposed_to_be_after_putting(
        board=curr_board, our_player=ai,
        other_player=table_player)
    return our_move, to_flip, next_board  # return to_put_down, to_flip, next board


def take_disk():
    arduinoSerial.write("getDisk".encode())
    time.sleep(2)  # not the real waiting time
    # return None (advance to putting down), does nothing in the MVP


def put_down(our_move):
    str_drop = "drop"+str(our_move[0])+str(our_move[1])
    print("in put down, our_move = ", our_move)
    arduinoSerial.write(str_drop.encode())
    time.sleep(0.5)  # not the real waiting time
    # return None (advance to flipping)


def flip(to_flip):
    for i in range(len(to_flip)):
        flip = "flip" + str(to_flip[i])  # build command that arduino read
        arduinoSerial.write(flip.encode())
        time.sleep(1)  # delay - the 2 seconds is not the real time needed
        # return None


def check_four_by_four(curr_board):
    print(curr_board)
    for i in range(len(curr_board)):
        for j in range(len(curr_board[i])):
            if curr_board[i][j] != 0 and (
                            i not in range(2, 6) or j not in range(2, 6)):
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
    arduinoName = 'COM10'
    port = 9600
    # global ArduinoSerial
    arduinoSerial = serial.Serial(arduinoName, port)

    time.sleep(1)
    take_disk()
    ai = Player.Player(heuristic=HeuristicsSandbox.palti_white_h, name="ai",
                       disk=Game.FIRST_COLOR)
    last_board = image_processing(None)
    while True:
        if input("Play your turn and then write 'Done' (or just 'D')") in {
            "Done", "done", 'D', 'd'}:
            motor.move_to_xy_with_monitoring((7, 0))
            curr_board = image_processing(last_board)
            print("curr_board", curr_board)
            if not check_four_by_four(curr_board):
                break

            our_move, to_flip, next_board = algorithm(ai, curr_board)
            print("our_move, to_flip", our_move, to_flip)
            motor.move_to_xy_with_monitoring(our_move)
            put_down(our_move)  # drops
            flip(to_flip)
            take_disk()  # take disk for the next move
            #
            last_board = curr_board  # board for next move
    human_player = Player.Player(type=Player.Player.PlayerTypes.HUMAN,
                                 name="human", disk=Game.SECOND_COLOR)
    winner = go_to_gui(curr_board, first_player=ai,
                       second_player=human_player)  # first player is the ai because the human player did the last move
    print("the winner is: " + winner.name)
