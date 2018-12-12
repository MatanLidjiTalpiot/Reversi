import Game
import copy
import numpy as np


def minimax(game, initial_depth, heuristic, maximizing_player, disk):
    return minimax_in(game, initial_depth, initial_depth, heuristic, maximizing_player, disk, None)


def minimax_in(game, depth, initial_depth, heuristic, maximizing_player, disk, chosen_op):
    if (depth == 0) or (game.is_board_full()):
        return [get_score(heuristic, game), chosen_op]

    options = game.get_legal_moves(disk)
    if maximizing_player:
        val = [float("-inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = minimax_in(temp_game, depth - 1, initial_depth, heuristic, False,
                           -disk, chosen_op)
            if m[0] > val[0]:
                val = m
        return val
    else:
        val = [float("inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)  # todo maybe deepcopy
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = minimax_in(temp_game, depth - 1, initial_depth, heuristic, True, \
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
        sum += feature[0] * feature[1](game)
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
heuristic = [(-1, lambda game: game.get_white_number()), (1, lambda game: game.get_black_number())]
m = minimax(game, 1, heuristic, True, Game.BLACK)
print(m)
