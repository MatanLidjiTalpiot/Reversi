import numpy as np
import sys
import Genetic
import Gui
import Player
import Game
from random import *
import Move_Helper
import time
import cProfile
import Minimax
import copy
import dill
import Legal_Moves_Helper
import os

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
            lambda game, player: game.is_winner_score(player)],
           [0, lambda player, game: 0],
           [0, lambda player, game: 0],
           [0, lambda player, game: 0],
           [0, lambda player, game: 0]
           ]
palti_h_numbers = [10, -10, 1000, -10000, 50, -200, -500, sys.maxsize/128]
diff_h = [[10, (lambda game, player: (game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)) - (game.get_white_number() * palti_A * np.power(game.get_number_of_turns(), palti_n)))],
           [-10, lambda game, player: (game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)) - (game.get_black_number() * palti_A * np.power(game.get_number_of_turns(), palti_n))],
           [1000, lambda game, player: game.get_num_of_corners(player) - game.get_num_of_corners_with_disk(-1)],
           [-10000, lambda game, player: game.get_opponent_num_of_corners(player) - game.get_num_of_corners_with_disk(1)],
           [50, lambda game, player: game.get_num_of_sides(player) - game.get_num_of_sides_with_disk(-1)],
           [-200, lambda game, player: game.get_opponent_num_of_sides(player) - game.get_num_of_sides_with_disk(1)],
           [-500, lambda game, player: game.get_num_of_options_for_other(player) -  game.get_num_of_options_for_other_with_disk(-1)],
           [sys.maxsize / 128, lambda game, player: game.is_winner_score(player) - game.is_winner_score_with_disk(-1)]] #remove heuristic after debugging
lidji_1 = [[10,
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
            lambda game, player: game.is_winner_score(player)],
         [1000,
          lambda game, player: game.get_number_of_safe_disks(player)],
         [-10000,
          lambda game,  player: game.get_number_of_opponent_safe_disks(player)],
         [-1000,
         lambda game, player: game.next_to_untaked_corner(player)],
         [1000,
          lambda game,player: game.next_to_untaken_corner_opponent(player)]]

lidji_2 = \
    [
    [10, lambda game, player: game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)],
    # pos
    [10,lambda game, player: -(game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n))],
    # neg
    [100, lambda game, player: game.get_num_of_corners(player)],  # pos
    [100,lambda game, player: -game.get_opponent_num_of_corners(player)],  # neg
    [100/16, lambda game, player: game.get_num_of_sides(player)],  # pos
    [100/16,lambda game, player: -game.get_opponent_num_of_sides(player)],  # neg
    [60, lambda game, player: -game.get_num_of_options_for_other(player)],  # neg
    [1000, lambda game, player: game.is_winner_score(player)], #pos
    [100,lambda game, player: game.get_number_of_safe_disks(player)], #pos
    [100,lambda game, player: -game.get_number_of_opponent_safe_disks(player)], #neg
    [100/3, lambda game, player: -game.next_to_untaked_corner(player)], #neg
    [100/3,lambda game,player: game.next_to_untaken_corner_opponent(player)]]#pos

# lidji2 = Player.Player(heuristic=lidji_2)
# palti = Player.Player(heuristic=palti_h)
human1 = Player.Player.load_player('pklFiles/human_player.pkl')
human2 = Player.Player.load_player('pklFiles/human_player.pkl')
# palti = Player.Player.load_player('pklFiles/palti_player_d4.pkl')
# game = Game.Game(lidji1, human1)
# gui = Gui.Gui(game)
# gui.play_game()
# other_players = []
# for i in range(3):
#     other_players.append(Genetic.mutation(lidji1))
#     other_players.append(Genetic.mutation(palti))
#     other_players.append(Genetic.mutation(lidji2))
#
# p_list = [lidji1, palti, lidji2]
# p_list.extend(other_players)
# more_players = []
# for i in range (10):
#     more_players.append(Genetic.create_player_with_heuristic())
# p_list.extend(more_players)
# shuffle(p_list)
# Genetic.genetic_main(num_p = 0, folder_name = "23_3_2019", gen_number = 0, depth_number = 1000 , mutation_prob=0.1, players_list=p_list, term_threshold=32)
# new_h = [[1,lambda game,player: game.get_number_of_safe_disks(player)],
#          [100,lambda game,player: -game.get_number_of_opponent_safe_disks(player)]]
# new_p = Player.Player(heuristic=new_h, depth=5)

# easy_h = \
#     [[10,
#     (lambda game, player: (game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)))],
#     [10,
#     lambda game, player: -(game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n))],
#    [1000,
#     lambda game, player: game.get_num_of_corners(player)],
#    [10000,
#     lambda game, player: -game.get_opponent_num_of_corners(player)]]
# easy_p = Player.Player(heuristic=easy_h, name="easy_player")
# Player.Player.save_to_folder(player=easy_p, folder_name="pklFiles")
log_10_of_64_div_40 = 4.899
palti_A2 = 1.4*(10**-9)

palti_and_lidji = [
            [[70,70,0],
            (lambda game, player: ((2*game.get_color_disk_num(player)/(game.get_number_of_turns())) * palti_A2 * np.power(game.get_number_of_turns(), log_10_of_64_div_40)))],
           [[70,70,0],
               (lambda game, player: -((2*game.get_opponent_disk_num(player)/(game.get_number_of_turns())) * palti_A2 * np.power(game.get_number_of_turns(), log_10_of_64_div_40)))],
           [[60,60,0],
            lambda game, player: game.get_num_of_corners(player)/4],
           [[600,600,0],
            lambda game, player: -game.get_opponent_num_of_corners(player)/4],
           [[20,20,0],
            lambda game, player: game.get_num_of_sides(player)/28],
           [[20,20,0],
            lambda game, player: -game.get_opponent_num_of_sides(player)/28],
           [[90,90,0],
            lambda game, player: -game.get_num_of_options_for_other(player)/16], #16 is arbitrary
           [[sys.maxsize/10,0,0],
            lambda game, player: game.is_winner_score(player)],
         [[60,60,0],
          lambda game, player: game.get_number_of_safe_disks(player)/game.get_number_of_turns()],
         [[80,80,0],
          lambda game,  player: -game.get_number_of_opponent_safe_disks(player)/game.get_number_of_turns()],
         [[80,80,0],
         lambda game, player: -game.next_to_untaked_corner(player)],
         [[100,100,0],
          lambda game,player: game.next_to_untaken_corner_opponent(player)],
        [[50,50,0],
         lambda game, player: game.get_num_of_options(player)/16],
        [[0,20,20],
         lambda game,player : game.get_digonal_score(player)],
        [[0,20,20],
         lambda game,player: -game.get_opponent_diagonal_score(player)],
        [[0,10,0],
         lambda game, player: -game.num_of_seq(player)/16],
        [[0,10,0],
         lambda game,player: game.num_of_seq(player)/16],
        [[20,20,0],
         lambda game,player: -game.bad_places_without_corner(player)],
        [[20,20,0],
         lambda game,player: game.opponent_bad_places_without_corner(player)]]


#e()
# yam_and_lidji = [
#             [[70],
#             (lambda game, player: ((2*game.get_color_disk_num(player)/(game.get_number_of_turns())) * palti_A2 * np.power(game.get_number_of_turns(), log_10_of_64_div_40)))],
#            [[70],
#                (lambda game, player: -((2*game.get_opponent_disk_num(player)/(game.get_number_of_turns())) * palti_A2 * np.power(game.get_number_of_turns(), log_10_of_64_div_40)))],
#            [[300],
#             lambda game, player: game.get_num_of_corners(player)/4],
#            [[300],
#             lambda game, player: -game.get_opponent_num_of_corners(player)/4],
#            [[20],
#             lambda game, player: game.get_num_of_sides(player)/28],
#            [[20],
#             lambda game, player: -game.get_opponent_num_of_sides(player)/28],
#            [[50],
#             lambda game, player: -game.get_num_of_options_for_other(player)/16], #16 is arbitrary
#            [[sys.maxsize/10],
#             lambda game, player: game.is_winner_score(player)],
#          [[70],
#           lambda game, player: game.get_number_of_safe_disks(player)/game.get_number_of_turns()],
#          [[70],
#           lambda game,  player: -game.get_number_of_opponent_safe_disks(player)/game.get_number_of_turns()],
#          [[80],
#          lambda game, player: -game.next_to_untaked_corner(player)],
#          [[80],
#           lambda game,player: game.next_to_untaken_corner_opponent(player)],
#         [[50],
#          lambda game, player: game.get_num_of_options(player)/16]
#         ]
# p_palti_and_lidji = Player.Player(heuristic=palti_and_lidji, depth=5)
# p_yam_and_lidji = Player.Player(heuristic=yam_and_lidji, depth=5)
# lidji1 = Player.Player(heuristic=lidji_1, depth=5)
# cross = Player.Player.load_player("pklFiles/cross.pkl")
# mutant_2 = Player.Player.load_player("pklFiles/mutent_2.pkl")
p_new = Player.Player(heuristic=palti_and_lidji)
p_new_m = Genetic.mutation(Genetic.mutation(Genetic.mutation(Genetic.mutation(p_new))))
# cross_2 = Genetic.crossover(cross, mutant_2)
# cross_2.name = "cross_2"
# Player.Player.save_to_folder(mutant_2, 'pklFiles')
p_new_m.name = "check1"
Player.Player.save_to_folder(p_new_m, "pklFiles")
our_player = Player.Player.load_player("pklFiles/mutant_1.pkl")
game = Game.Game(our_player, human1)
gui = Gui.Gui(game)
gui.play_game()

