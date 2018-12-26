import Game
import copy

def how_board_supposed_to_be_after_putting(game):
    game_copy = copy.deepcopy(game)
    game_copy.do_move(where_to_put(game_copy, player))
    return game_copy

def where_to_put(game,player):
    return player.choose_move(game)

def where_to_flip(game, player):
    return game.to_flip(where_to_put(game, player))


