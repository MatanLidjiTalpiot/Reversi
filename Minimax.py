import copy
import Game
SCORE_MEMO = {}
def get_score(game, player):
    """
    A method that gives a score to a certin state of the board
    :param heuristic: a list of tuples that contain two objects the first is the weight and the
    second is the call for the function that returns the wanted parameter
    :param game: the game
    :return: the score of the state of the board according to the heuristic
    """
    global SCORE_MEMO
    key =  (tuple(map(tuple, game.board)))
    if key not in SCORE_MEMO:
        sum = 0
        for feature in player.get_heuristic():
            sum += feature[0] * feature[1](game, player)
        SCORE_MEMO[key] = sum
        return sum
    else:
        return SCORE_MEMO[key]


def minimax(game, depth, player, maximizing_player, disk):
    """
    :param game: the current game
    :param depth: lookup depth
    :param player: the player that holds a heuristic that according to his heuristic his chooses his move
    :param maximizing_player: True if this is the max player, False if this is the min player
    :param disk: player's disk
    :return: a 2-tuple (best score, best move)
    """
    return minimax_in(game, depth, depth, player, maximizing_player, disk, None)


def alpha_beta(game, depth, player, maximizing_player, disk):
    """
    :param game: the current game
    :param depth: lookup depth
    :param player: the player that holds a heuristic that according to his heuristic his chooses his move
    :param maximizing_player: True if this is the max player, False if this is the min player
    :param disk: player's disk
    :return: a 2-tuple (best score, best move)
    """
    return alpha_beta_in(game, depth, depth, player, float("-inf"), float("inf"), maximizing_player, disk, None)


def minimax_in(game, depth, initial_depth, player, maximizing_player, disk, chosen_op):
    """
:param game: the current game
    :param depth: lookup depth
    :param initial_depth: the initial depth of the search tree
    :param player: the player that holds a heuristic that according to his heuristic his chooses his move
    :param maximizing_player: True if this is the max player, False if this is the min player
    :param disk: player's disk
    :param chosen_op: the operation that is chosen - the first operation in the decision tree
    :return: a 2-tuple (best score, best move)
    """
    if depth == 0 or game.is_board_full():
        return get_score(game, player), chosen_op

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

WHITE_OPTIONS = {}
BLACK_OPTIONS = {}
def alpha_beta_in(game, depth, initial_depth, player, a, b, maximizing_player, disk, chosen_op):
    """
    :param game: the current game
    :param depth: the depth that is left to look into
    :param initial_depth: the initial depth
    :param player: the player on which his heuristic is used
    :param a: todo ripstein
    :param b: todo ripstein
    :param maximizing_player: a boolean parameter
    :param disk: the color of the disk of the player
    :param chosen_op: the first operation in the decision tree
    :return: a tuple (score, op)
    """
    global WHITE_OPTIONS, BLACK_OPTIONS
    key = tuple(map(tuple, game.board))
    if disk == Game.WHITE:
        if key not in WHITE_OPTIONS:
            options = game.get_legal_moves(disk)
            WHITE_OPTIONS[key] = options
        else:
            options = WHITE_OPTIONS[key]
    else:
        if key not in BLACK_OPTIONS:
            options = game.get_legal_moves(disk)
            BLACK_OPTIONS[key] = options
        else:
            options = BLACK_OPTIONS[key]
    if options != game.get_legal_moves(disk):
        print("options: ", options)
        print("Get legal moves: ", game.get_legal_moves(disk))

    # options = game.get_legal_moves(disk)
    if depth == 0 or game.is_board_full() or options == []:  # todo options == [] is a patch -
        # todo think if we need to do something smarter
        return get_score(game, player), chosen_op

    if maximizing_player:
        val = [float("-inf"), None]
        for op in options:
            temp_game = copy.deepcopy(game)
            temp_game.do_move(disk, op)
            if depth == initial_depth:
                chosen_op = op
            m = alpha_beta_in(temp_game, depth - 1, initial_depth, player, a, b, False, -disk, chosen_op)
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
            m = alpha_beta_in(temp_game, depth - 1, initial_depth, player, a, b, True, -disk, chosen_op)
            if m[0] < val[0]:
                val = m
                b = m[0]
            if a >= b:
                break
        return val
