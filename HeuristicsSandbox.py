import numpy as np
import sys
import Genetic
import Gui
import Player
import Game
import Move_Helper
import time
import cProfile
import Minimax
import copy
import dill
import Legal_Moves_Helper

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

# Legal_Moves_Helper.Legal_Moves_Helper.create_new("shit happened we need a new one")
# Move_Helper.Move_Helper.create_new("shit happened we need a new one")

random = Player.Player.load_player('pklFiles/random_player.pkl')
palti_4 = Player.Player.load_player('pklFiles/palti_player_d4.pkl')
palti_4_two = Player.Player.load_player('pklFiles/palti_player_d4.pkl')
aron = Player.Player.load_player('pklFiles/human_player.pkl')
savta = Player.Player.load_player('pklFiles/human_player.pkl')
# game1 = Game.Game(palti_4, palti_4_two, use_move_helper=False)
aron.name= "matan "
savta.name = "ripp "
# game2 = Game.Game(savta, aron, use_move_helper=True)
game2 = Game.Game(aron, palti_4, use_move_helper=True)

gui = Gui.Gui(game2)
winner = gui.play_game()
print(winner.name)








# game2.MOVE_HELPER.save_move_helper()
# game2.LEGAL_MOVES_HELPER.save_legal_moves_helper()
# print(t3-t2)



