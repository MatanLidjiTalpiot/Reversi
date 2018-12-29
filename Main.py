import Game
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import camera
import Player
import HeuristicsSandbox
import BoardInformation
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


def move_to_xy(our_move):  # tuple (int, char)
    y, x = our_move
    move = "move" + str(y) + str(x)  # build move command
    arduinoSerial.write(move.encode())
    time.sleep(2)  # not the real waiting time


def put_down():
    arduinoSerial.write("drop".encode())
    time.sleep(0.5)  # not the real waiting time
    # return None (advance to flipping)


def flip(to_flip):
    for i in range(len(to_flip)):
        y, x = to_flip[i]
        flip = "flip" + str(y) + str(x)
        arduinoSerial.write(flip.encode())
        time.sleep(2)  # delay - the 2 seconds is not the real time needed
        # return None


if __name__ == '__main__':
    arduinoName = 'COM10'
    port = 9600
    camera.func.cam = camera.func.initialCamera()
    rval, frame = camera.func.cam.read()
    # camera.func.show_image(frame)
    # global ArduinoSerial
    arduinoSerial = serial.Serial(arduinoName, port)

    time.sleep(2)

    # take_disk()
    ai = Player.Player(heuristic=HeuristicsSandbox.palti_white_h, name="ai",
                       disk=Game.FIRST_COLOR)
    last_board = None
    print("Done initializing")
    while True:
        if input("Play your turn and then write 'Done' (or just 'D')") in\
                {"Done", "done", 'D', 'd'}:
            # ArduinoSerial.write()
            # for debugging - working
            curr_board = image_processing(last_board)
            print(curr_board)
            our_move, to_flip, next_board = algorithm(ai, curr_board)
        print("move: ", our_move, "to flip: ", to_flip, "\nnext board:\n",
              next_board)
        # move_to_xy(our_move)
        # put_down()  # drops
        flip(to_flip)
        take_disk()  # take disk for the next move
        #
        last_board = curr_board  # board for next move
