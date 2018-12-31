import numpy as np
import sys

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
palti_black_h = [[10, lambda game: (
game.get_black_number() * palti_A * np.power(game.get_number_of_turns(),
                                             palti_n))],
                 [-10, lambda game: (
                 game.get_white_number() * palti_A * np.power(
                     game.get_number_of_turns(), palti_n))],
                 [1000, lambda game: game.get_num_of_corners(1)],
                 [-10000, lambda game: game.get_num_of_corners(-1)],
                 [50, lambda game: game.get_num_of_sides(1)],
                 [-200, lambda game: game.get_num_of_sides(-1)],
                 [-500, lambda game: game.get_num_of_options_for_other(1)],
                 [sys.maxsize / 128, lambda game: game.is_winner_score(1)]]

palti_white_h = [
    [-10, lambda game: (game.get_black_number() * palti_A * np.power(
        game.get_number_of_turns(), palti_n))],
    [10,lambda game: (game.get_white_number() * palti_A * np.power(
        game.get_number_of_turns(), palti_n))],
    [1000, lambda game: game.get_num_of_corners(-1)],
    [-10000, lambda game: game.get_num_of_corners(1)],
    [50, lambda game: game.get_num_of_sides(-1)],
    [-200, lambda game: game.get_num_of_sides(1)],
    [-500, lambda game: game.get_num_of_options_for_other(-1)],
    [sys.maxsize / 128, lambda game: game.is_winner_score(-1)]]
"""
palti_black = Player.Player(heuristic=palti_black_h, disk=1, name="Computer")

palti_white = Player.Player(heuristic=palti_white_h, disk=1, name="Computer")
p1_white = Player.Player(disk=-1, name="h1 white", heuristic=h1_white)
p1_black = Player.Player(disk=-1, name="h1 black", heuristic=h1_black)
eisner = Player.Player(disk=-1, name="Eisner", type=Player.Player.PlayerTypes.HUMAN)
"""