
import math
def minimax(game, depth, heuristic,maximizing_player, disk, path):
    if depth == 0 or game.is_board_full():
        return [get_score(heuristic, game),path]
    options = game.get_legal_moves(disk)
    if maximizing_player == disk:
        val = []
        val[0] = -1 * math.inf
        val[1] = []
        for op in options:
            temp_game = game
            m = minimax(temp_game.do_move(disk, op),depth - 1, heuristic, False, disk,
                                   [path, True])
            if m[0] > val[0]:
                val = m
        return val
    else:
        val = []
        val[0] = math.inf
        val[1] = []
        for op in option:
            temp_game = game
            m = minimax(temp_game.do_move(-disk, op), depth - 1, heuristic, True, -disk,
                        [path, False])
            if m[0] < val[0]:
                val = m
        return val




def get_score(heuristic, game):
    pass #TODO write this function