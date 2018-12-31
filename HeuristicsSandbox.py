import numpy as np
import sys
import Player
import Game
import Gui

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

palti_black_h = [[10, lambda game: (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [-10, lambda game: (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [1000, lambda game: game.get_num_of_corners(1)],
                 [-10000, lambda game: game.get_num_of_corners(-1)],
                 [50, lambda game: game.get_num_of_sides(1)],
                 [-200, lambda game: game.get_num_of_sides(-1)],
                 [-500, lambda game: game.get_num_of_options_for_other(1)],
                 [sys.maxsize / 128, lambda game: game.is_winner_score(1)]]

palti_white_h = [[-10, lambda game: (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [10, lambda game: (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [1000, lambda game: game.get_num_of_corners(-1)],
                 [-10000, lambda game: game.get_num_of_corners(1)],
                 [50, lambda game: game.get_num_of_sides(-1)],
                 [-200, lambda game: game.get_num_of_sides(1)],
                 [-500, lambda game: game.get_num_of_options_for_other(-1)],
                 [sys.maxsize / 128, lambda game: game.is_winner_score(-1)]]

palti_h = [[10, (lambda game, player: (game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)))],
           [-10, lambda game, player: (game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n))],
           [1000, lambda game, player: game.get_num_of_corners(player)],
           [-10000, lambda game, player: game.get_opponent_num_of_corners(player)],
           [50, lambda game, player: game.get_num_of_sides(player)],
           [-200, lambda game, player: game.get_opponent_num_of_sides(player)],
           [-500, lambda game, player: game.get_num_of_options_for_other(player)],
           [sys.maxsize / 128, lambda game, player: game.is_winner_score(player)]]

human = Player.Player(p_type=Player.Player.PlayerTypes.HUMAN, name = "humam", disk = Game.SECOND_COLOR)
computer = Player.Player(p_type = Player.Player.PlayerTypes.MINIMAX, name = "computer", disk = Game.FIRST_COLOR, heuristic=palti_h)

game = Game.Game(human, computer)
winner = Gui.play_game(game, to_print=True)
print(winner.name)
