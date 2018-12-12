<<<<<<< Updated upstream
=======
import Game
import math
import copy

def minimax(game, depth, heuristic, maximizing_player, disk, path):
    if (depth == 0) or (game.is_board_full()):
        return [get_score(heuristic, game), path]

    options = game.get_legal_moves(disk)
    if maximizing_player:
        val = []
        val.append(-1 * math.inf)
        val.append([])
        print(game.board)
        print("options: ", options)
        print("current disk: ", disk)
        for op in options:
            temp_game = game #todo maybe deepcopy
            m = minimax(temp_game.do_move(disk, op), depth - 1, heuristic, False, -disk,
                        [path, True])
            if m[0] > val[0]:
                val = m
        return val
    else:
        val = []
        val.append(math.inf)
        val.append([])
        print(game.board)
        print("options: ", options)
        print("current disk: ", disk)
        for op in options:
            temp_game = game #todo maybe deepcopy
            m = minimax(temp_game.do_move(disk, op), depth - 1, heuristic, True, -disk,
                        [path, False])
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
heuristic = [[0.75, game.get_white_number], [0.1, game.get_black_number]]
print(minimax(game, 1, heuristic, True, Game.BLACK, []))
print(get_score(heuristic,game))
>>>>>>> Stashed changes
