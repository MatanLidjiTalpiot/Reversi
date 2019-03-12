import numpy as np
import sys
import Genetic
import Gui
import Player
import Game
import time
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

palti_n = np.log(10) / np.log(1.5)# a somewhat arbitrary constant
palti_A = 1 / (40 ** palti_n)     # a somewhat arbitrary constant

palti_black_h = [[10, lambda game: (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [-10, lambda game: (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [1000, lambda game: game.get_num_of_corners(1)],
                 [-10000, lambda game: game.get_num_of_corners(-1)],
                 [50, lambda game: game.get_num_of_sides(1)],
                 [-200, lambda game: game.get_num_of_sides(-1)],
                 [-500, lambda game: game.get_num_of_options_for_other(1)],
                 [sys.maxsize / 128,lambda game: game.is_winner_score(1)]]

palti_white_h = [[-10, lambda game, player: (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [10, lambda game, player: (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
                 [1000, lambda game, player: game.get_num_of_corners_with_disk(-1)],
                 [-10000, lambda game, player: game.get_num_of_corners_with_disk(1)],
                 [50, lambda game, player: game.get_num_of_sides_with_disk(-1)],
                 [-200, lambda game, player: game.get_num_of_sides_with_disk(1)],
                 [-500, lambda game, player: game.get_num_of_options_for_other_with_disk(-1)],
                 [sys.maxsize / 128, lambda game, player: game.is_winner_score_with_disk(-1)]]

palti_h = [[10,
            (lambda game, player: (game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)))],
           [-10,
            lambda game, player: (game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n))],
           [1000,
            lambda game, player: game.get_num_of_corners(player)],
           [-10000,
            lambda game, player: game.get_opponent_num_of_corners(player)],
           [50,
            lambda game, player: game.get_num_of_sides(player)],
           [-200,
            lambda game, player: game.get_opponent_num_of_sides(player)],
           [-500,
            lambda game, player: game.get_num_of_options_for_other(player)],
           [sys.maxsize / 128,
            lambda game, player: game.is_winner_score(player)]]
palti_h_numbers = [10, -10, 1000, -10000, 50, -200, -500, sys.maxsize/128]
diff_h = [[10, (lambda game, player: (game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)) - (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(), palti_n)))],
           [-10, lambda game, player: (game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)) - (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
           [1000, lambda game, player: game.get_num_of_corners(player) - game.get_num_of_corners_with_disk(-1)],
           [-10000, lambda game, player: game.get_opponent_num_of_corners(player) - game.get_num_of_corners_with_disk(1)],
           [50, lambda game, player: game.get_num_of_sides(player) - game.get_num_of_sides_with_disk(-1)],
           [-200, lambda game, player: game.get_opponent_num_of_sides(player) - game.get_num_of_sides_with_disk(1)],
           [-500, lambda game, player: game.get_num_of_options_for_other(player) -  game.get_num_of_options_for_other_with_disk(-1)],
           [sys.maxsize / 128, lambda game, player: game.is_winner_score(player) - game.is_winner_score_with_disk(-1)]] #remove heuristic after debugging

# palti = Player.Player.load_player('pklFiles/palti_player.pkl')
# evolution = Genetic.evolve(palti, 3)
# evolved_by_order = Player.Player.compare_players_list(evolution)
# Player.Player.save_sorted_list_to_folder(evolved_by_order, "evolve1")
all_players = []
random_players = []
for i in range(10):
    random_players.append(Genetic.create_player_with_heuristic())
for player in random_players:
    all_players.extend(Genetic.evolve(player,1))
s_list = Player.Player.compare_players_list(all_players)
Player.Player.save_sorted_list_to_folder(s_list, '12_3_2019')

