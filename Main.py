import Camera
import new_move_detaction
# import ArduinoCommunication
import shit
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import Player
import cv2
import HeuristicsSandbox
import Gui
import numpy as np
import rotate
from image_control_xy_movement import move_monitored, junk_string, put_and_back_square
import Game

HUMAN = Player.Player(p_type=Player.Player.PlayerTypes.TABLE)
OUR_PLAYER = Player.Player(heuristic=HeuristicsSandbox.palti_h)
print("h")
GAME = Game.Game(HUMAN, OUR_PLAYER)

end_point_in_board = (7, 6)


def check_if_move_is_legal(board_to_check):
    for i in range(GAME.size):
        for j in range(GAME.size):
            if GAME.board[i][j] != board_to_check[i][j] and GAME.board[i][j] == 0:
                if (i, j) not in GAME.get_legal_moves(HUMAN.disk):
                    return False
    return True


def algorithm(curr_board):
    return algorithm_in(OUR_PLAYER, curr_board)


def algorithm_in(ai, curr_board):  # fix!!!!!!!!!!!!!
    """
    A function that gets the current board and finds our systems move
    :param ai: our ai
    :param curr_board: the board on which the ai finds the move
    :return: to_put_down, to_flip, next board
    """
    GAME.board = curr_board
    to_put_down = OUR_PLAYER.choose_move(GAME)[1]
    to_flip = GAME.to_flip(OUR_PLAYER.disk, to_put_down)
    GAME.do_move(OUR_PLAYER.disk, to_put_down)
    next_board = GAME.board
    return to_put_down, to_flip, next_board  # return to_put_down, to_flip, next board


def image_processing(last_board):
    return new_move_detaction.continue_when_it_is_our_turn(np.count_nonzero(last_board))


def take_disk():
    arduinoSerial.write("take".encode())
    time.sleep(0.2)  # not the real waiting time


def put_down(our_move):
    str_drop = "drop" + str(our_move[0]) + str(our_move[1])
    arduinoSerial.write(str_drop.encode())
    time.sleep(0.5)


def flip(to_flip):  # confirm outputs
    flip = to_flip_in_format(to_flip)  # build command that arduino read
    arduinoSerial.write(flip.encode())
    time.sleep(0.5)  # delay - the 2 seconds is not the real time needed


def go_to_gui(curr_board, first_player, second_player):
    """
    A function that gets a board and continues a game from it
    :param curr_board: the board to start from
    :param first_player: the player that plays first
    :param second_player: the player that plays second
    :return The winner of the game
    """
    gui = Gui.Gui(GAME)
    gui.intro = False
    gui.play_game()


def stack_to_end_point():
    command = "move76"
    arduinoSerial.write(command.encode())
    # msg = arduinoSerial.readline()
    # while True:
    #     msg = arduinoSerial.readline()
    #     print(msg)
    #     print(type(msg))
    while "done plotter_move_motors" not in arduinoSerial.readline().decode("utf-8"):
        continue
    print(junk_string)
    arduinoSerial.write(junk_string.encode())


def end_point_to_stack():
    command = "back76"
    arduinoSerial.write(command.encode())
    while "done plotter_move_motors" not in arduinoSerial.readline().decode("utf-8"):
        continue
    arduinoSerial.write(junk_string.encode())


def to_flip_in_format(to_flip):
    string = "flip"
    for square in to_flip:
        string += str(square[0]) + str(square[1])
    print("flipstring", string)
    return string


if __name__ == '__main__':
    # initiazetion
    Camera.initialize_camera()
    cam = Camera.get_camera()
    print('the camera is ready')
    OK = 0
    CUT_R = 0
    while OK != "go":
        _, frame = cam.read()
        time.sleep(0.01)
        _, frame = cam.read()
        # TODO
        # TODO
        # TODO
        # TODO
        # TODO
        # TODO
        # TODO
        # frame = shit.cut_edges(frame, CUT_R)
        points = rotate.find_points(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), 0.05)
        # print(points)
        if type(points) != np.ndarray:
            continue
        rotate.draw_points(points, frame)
        cv2.imshow('test', frame)
        cv2.waitKey(0)
        OK = input("OK ??")
    print(points)
    rotate.set_points(points)
    # cv2.imshow('m', frame)
    # cv2.waitKey(0)
    last_board = shit.extract_board(frame)
    print("the board: \n", last_board)

    arduinoName = 'COM6'
    port = 9600
    # global ArduinoSerial
    print("arduino connection")
    arduinoSerial = serial.Serial(arduinoName, port)
    print("arduino connection successful")
    ai = Player.Player(heuristic=HeuristicsSandbox.palti_white_h, name="ai",
                       disk=Game.FIRST_COLOR)

    # _, frame = cam.read()
    # frame = shit.cut_edges(frame,CUT_R)
    # last_board = shit.extract_board(frame)
    # print("the board: \n", last_board)
    our_turn = True
    print("done init")
    while True:
        if our_turn:
            print("hello")
            curr_board = image_processing(last_board)
            print("curr_board", curr_board)
            our_move, to_flip, next_board = algorithm(curr_board)
            print("our_move, to_flip", our_move, to_flip)
            put_and_back_square(arduinoSerial, our_move[0], our_move[1])
            flip(to_flip)
            last_board = next_board  # board for next move
        else:
            pass
        # if game done - break
    human_player = Player.Player(p_type=Player.Player.PlayerTypes.HUMAN,
                                 name="human", disk=Game.SECOND_COLOR)
    winner = go_to_gui(curr_board, first_player=ai,
                       second_player=human_player)  # first player is the ai because the human player did the last move
    print("the winner is: " + winner.name)
