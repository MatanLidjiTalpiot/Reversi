import Game
import copy
import numpy as np
import time
import Player


def get_score(heuristic, game):
    """
    A method that gives a score to a certin state of the board
    :param heuristic: a list of tuples that contain two objects the first is the weight and the
    second is the call for the function that returns the wanted parameter
    :param game: the game
    :return: the score of the state of the board according to the heuristic
    """
    sum = 0
    for feature in heuristic:
        sum += feature[0] * feature[1](game)
    return sum


def minimax(game, depth, heuristic, maximizing_player, disk):
    """
    :param game: the current game
    :param depth: lookup depth
    :param heuristic: a list of tuples that contain two objects the first is the weight and the
    second is the call for the function that returns the wanted parameter
    :param maximizing_player: True if this is the max player, False if this is the min player
    :param disk: player's disk
    :return: a 2-tuple (best score, best move)
    """
    return minimax_in(game, depth, depth, heuristic, maximizing_player, disk, None)


def alpha_beta(game, depth, heuristic, maximizing_player, disk):
    """
    :param game: the current game
    :param depth: lookup depth
    :param heuristic: a list of tuples that contain two objects the first is the weight and the
    second is the call for the function that returns the wanted parameter
    :param maximizing_player: True if this is the max player, False if this is the min player
    :param disk: player's disk
    :return: a 2-tuple (best score, best move)
    """
    return alpha_beta_in(game, depth, depth, heuristic, float("-inf"), float("inf"), maximizing_player, disk, None)


def minimax_in(game, depth, initial_depth, heuristic, maximizing_player, disk, chosen_op):
    if depth == 0 or game.is_board_full():
        return get_score(heuristic, game), chosen_op

    options = game.get_legal_moves(disk)
    if maximizing_player:
        val = [float("-inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = minimax_in(temp_game, depth - 1, initial_depth, heuristic, False, -disk, chosen_op)
            if m[0] > val[0]:
                val = m
        return val
    else:
        val = [float("inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = minimax_in(temp_game, depth - 1, initial_depth, heuristic, True, -disk, chosen_op)
            if m[0] < val[0]:
                val = m
        return val


def alpha_beta_in(game, depth, initial_depth, heuristic, a, b, maximizing_player, disk, chosen_op):
    if depth == 0 or game.is_board_full():
        return get_score(heuristic, game), chosen_op

    options = game.get_legal_moves(disk)
    if maximizing_player:
        val = [float("-inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = alpha_beta_in(temp_game, depth - 1, initial_depth, heuristic, a, b, False, -disk, chosen_op)
            if m[0] > val[0]:
                val = m
                a = m[0]
            if a >= b:
                break
        return val
    else:
        val = [float("inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = alpha_beta_in(temp_game, depth - 1, initial_depth, heuristic, a, b, True, -disk, chosen_op)
            if m[0] < val[0]:
                val = m
                b = m[0]
            if a >= b:
                break
        return val


game = Game.Game()
game.set_board(np.array([[0, 0, 0, 0, 0, -1, 0, 0],
                         [0, 0, 0, 0, 1, -1, 0, 0],
                         [1, 0, 1, -1, 1, -1, 0, 0],
                         [1, 1, -1, -1, 1, -1, 0, 0],
                         [1, 1, -1, -1, 1, -1, 0, 0],
                         [0, -1, 1, -1, 0, -1, -1, 0],
                         [0, 0, 1, 1, 1, 0, 1, 0],
                         [0, 1, 0, 0, 0, -1, 0, 0]]).astype(int))


heuristic1 = [(-1, lambda game: game.get_white_number()), (1, lambda game:
game.get_black_number())]
start = time.time()
m = alpha_beta(game, 4, heuristic, True, Game.BLACK)
end = time.time()
print("best score:", m[0], "\nbest move:", m[1], "\nCalculation time:", round(end - start, 1), "seconds")