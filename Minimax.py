import Game
import math
import copy
import numpy as np


def minimax(game, depth, initial_depth, heuristic, maximizing_player, disk, chosen_op):
    if (depth == 0) or (game.is_board_full()):
        return [get_score(heuristic, game), chosen_op]

    options = game.get_legal_moves(disk)
    if maximizing_player:
        val = []
        val.append(-1 * math.inf)
        val.append(None)
        # print(game.board)
        # print("options: ", options)
        # print("current disk: ", disk)
        for op in options:
            temp_game = copy.deepcopy(game) # todo maybe deepcopy
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
                print(op)
            m = minimax(temp_game, depth - 1, initial_depth, heuristic, False,
                        -disk, chosen_op)
            if m[0] > val[0]:
                val = m
        return val
    else:
        val = []
        val.append(math.inf)
        val.append(None)
        # print(game.board)
        # print("options: ", options)
        # print("current disk: ", disk)
        for op in options:
            temp_game = copy.deepcopy(game)  # todo maybe deepcopy
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
                print(options)
            m = minimax(temp_game, depth - 1, initial_depth, heuristic, True, \
                        -disk, chosen_op)
            if m[0] < val[0]:
                val = m
        return val


def get_score(heuristic, game):
    """
    A method that gives a score to a certin state of the board
    :param heuristic: a list of arrays that contain two objects the first is the wieght and the
    second is the call for the function that returns the wanted parameter
    :param game: the game
    :return: the score of the state of the board according to the heuristic
    """
    sum = 0
    for feature in heuristic:
        sum += feature[0] * feature[1]()
    return sum


game = Game.Game()
game.set_board(np.array([[0, 0, 0, 0, 0, -1, 0, 0],
                      [0, 0, 0, 0, 1, -1, 0, 0],
                      [1, 0, 1, -1, 1, -1, 0, 0],
                      [1, 1, -1, -1, 1, -1, 0, 0],
                      [1, 1, -1, -1, 1, -1, 0, 0],
                      [0, -1, 1, -1, 0, -1, -1, 0],
                      [0, 0, 1, 1, 1, 0, 1, 0],
                      [0, 1, 0, 0, 0, -1, 0, 0]]).astype(int))
heuristic = [[0, game.get_white_number], [1, game.get_black_number]]
print(get_score(heuristic,game))
m = (minimax(game, 2, 2, heuristic, True, Game.BLACK, None))
print(m)
game.do_move(Game.BLACK,m[1])
print(get_score(heuristic, game))