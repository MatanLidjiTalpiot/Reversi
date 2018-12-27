import Game
import Minimax
import Player
import Gui
import numpy as np
import sys

game = Game.Game()
# game.set_board(np.array([[0, 0, 0, 1, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 0, 0, 0],
# [0, 1, 1, 1, 1, 1, 0, 0],
# [0, 0, 0, 1, 1, 1, 0, 0],
# [0, 0, 0, 1, 1, 1, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0]]))
# game.set_board(np.array([[-1, -1, -1, -1, -1, -1, -1, -1],
#                 [-1,  1, -1, -1,  1,  0, -1,  0],
#                 [-1, -1, -1,  1,  1,  1,  0,  0],
#                 [-1, -1,  1,  1,  1,  1,  1,  0],
#                 [ 0,  0,  1,  1,  1,  1,  0,  0],
#                 [ 0,  0,  1,  1,  1,  1,  1,  0],
#                 [ 0,  0,  0,  1,  0,  0,  0,  0],
#                 [ 0,  0,  1,  0,  0,  0,  0,  0]]))
# print("legal", game.get_legal_moves(1))

# [[ 0  0  0  0  0  0  0  0]
#  [ 0  0  0  0  0  0  0  0]
#  [-1  1  1  1  0  0  1  0]
#  [-1 -1  1  1  1  1  0  0]
#  [-1 -1 -1  1 -1  1  0  0]
#  [-1 -1  1 -1  1  1  1  0]
#  [-1 -1 -1 -1 -1 -1 -1 -1]
#  [-1 -1 -1 -1 -1 -1 -1 -1]]


# game.set_board(np.array([[ 0,  0, -1,  1, -1, -1, -1, -1],
#  [ 0,  0, -1, -1,  1, -1, -1, -1],
#  [ 1,  0, -1, -1, -1,  1, -1,  1],
#  [ 1,  0, -1, -1, -1 , 1 ,-1 , 1],
#  [ 1, -1, -1, -1, -1, -1, -1 , 1],
#  [ 0,  0, -1, -1, -1, -1, -1,  1],
#  [ 0,  0, -1,  0 , 0,  0,  1,  1],
#  [ 0,  0, -1,  0 , 0,  1,  1,  1]]))


h1_black = [[1, lambda game: game.get_black_number()],
            [-1, lambda game: game.get_white_number()],
            [100, lambda game: game.get_num_of_corners(1)],
            [-1000, lambda game: game.get_num_of_corners(-1)],
            [50, lambda game: game.get_num_of_sides(1)],
            [-200, lambda game: game.get_num_of_sides(-1)],
            [-200, lambda game: game.get_num_of_options_for_other(1)]]

h2 = [[1, lambda game: game.get_black_number()],
      [-1, lambda game: game.get_white_number()],
      [100, lambda game: game.get_num_of_corners(1)],
      [-1000, lambda game: game.get_num_of_corners(-1)],
      [50, lambda game: game.get_num_of_sides(1)],
      [-200, lambda game: game.get_num_of_sides(-1)]]

h1_white = [[-1, lambda game: game.get_black_number()],
            [1, lambda game: game.get_white_number()],
            [100, lambda game: game.get_num_of_corners(-1)],
            [-1000, lambda game: game.get_num_of_corners(1)],
            [50, lambda game: game.get_num_of_sides(-1)],
            [-200, lambda game: game.get_num_of_sides(1)],
            [-200, lambda game: game.get_num_of_options_for_other(-1)]]

h4 = [[1, lambda game: game.get_black_number()],
      [-1, lambda game: game.get_white_number()],
      [100, lambda game: game.get_num_of_corners(-1)],
      [-1000, lambda game: game.get_num_of_corners(1)],
      [50, lambda game: game.get_num_of_sides(-1)],
      [-200, lambda game: game.get_num_of_sides(1)]]

palti_n = np.log(10) / np.log(1.5)
palti_A = 1 / (40 ** palti_n)
palti_black = [
    [10, lambda game: (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(

    ), palti_n))],
    [-10, lambda game: (game.get_white_number() * palti_A * np.power(
        game.get_number_of_turns(

        ), palti_n))],
    [1000, lambda game: game.get_num_of_corners(1)],
    [-10000, lambda game: game.get_num_of_corners(-1)],
    [50, lambda game: game.get_num_of_sides(1)],
    [-200, lambda game: game.get_num_of_sides(-1)],
    [-500, lambda game: game.get_num_of_options_for_other(1)],
    [sys.maxsize / 128, lambda game: game.is_winner_score(1)]]

palti_white = [[-10, lambda game: (game.get_black_number() * palti_A * np.power(
    game.get_number_of_turns(

    ), palti_n))],
               [10,
                lambda game: (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(

                ), palti_n))],
               [1000, lambda game: game.get_num_of_corners(-1)],
               [-10000, lambda game: game.get_num_of_corners(1)],
               [50, lambda game: game.get_num_of_sides(-1)],
               [-200, lambda game: game.get_num_of_sides(1)],
               [-500, lambda game: game.get_num_of_options_for_other(-1)],
               [sys.maxsize / 128, lambda game: game.is_winner_score(-1)]]

palti_black = Player.Player(heuristic=palti_black, disk=1, name="Computer")

palti_white = Player.Player(heuristic=palti_white, disk=1, name="Computer")
h1_white = Player.Player(disk=-1, name="h1 white", heuristic=h1_white)
h1_black = Player.Player(disk=-1, name="h1 black", heuristic=h1_black)
eisner = Player.Player(disk=-1, name="Eisner", type=Player.Player.PlayerTypes.HUMAN)

dic = {palti_black.name: 0, palti_white.name: 0, h1_black.name: 0, h1_white.name: 0}
for i in range(1):
    """
    winner = Gui.play_game(game, palti_black, h1_white, to_print = False)
    print ("winner of the ", i, "game is: ", winner.name)
    dic[winner.name] += 1
    game.reset_game()
    winner = Gui.play_game(game, h1_black, palti_white, to_print = False)
    dic[winner.name] += 1
    print("winner of the ", i, "game is: ", winner.name)
    game.reset_game()
    """
    print(eisner.name + " vs " + palti_white.name)
    winner = Gui.play_game(game, eisner, palti_white, to_print=True)
    dic[winner.name] += 1
    print("winner of the ", i, "game is: ", winner.name)
    # print(dic)
    while True:
        pass
