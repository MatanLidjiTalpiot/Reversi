import Game
import math
def minimax(game, depth, heuristic,maximizing_player, disk, path):
    if (depth == 0) or (game.is_board_full()):
        return [get_score(heuristic, game),path]
    options = game.get_legal_moves(disk)
    if maximizing_player == disk:
        val = []
        val.append(-1 * math.inf)
        val.append([])
        for op in options:
            temp_game = game
            m = minimax(temp_game.do_move(disk, op),depth - 1, heuristic, False, disk,
                                   [path, True])
            if m[0] > val[0]:
                val = m
        return val
    else:
        val = []
        val.append(math.inf)
        val.append([])
        for op in option:
            temp_game = game
            m = minimax(temp_game.do_move(-disk, op), depth - 1, heuristic, True, -disk,
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
    for feture in heuristic:
        sum += feture[0] * feture[1]()
    return sum

game = Game.Game()
heuristic = [[0.75, game.get_white_number()],[0.1, game.get_black_number()]]
print(minimax(game, 1, heuristic, Game.WHITE, Game.WHITE, []))
