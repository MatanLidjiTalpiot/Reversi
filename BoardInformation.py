import Player
import Game
import copy
import Gui
import sys
import numpy as np


def how_board_supposed_to_be_after_putting(board, our_player, other_player):
    """
    A function returns how the board is supposed to look after our player is doing the move
    :param board: the board that our player needs to do a move on
    :param our_player: our_player
    :param other_player: the other player
    :return: the board after our player move
    """
    game_copy = Game.Game(our_player, other_player)
    game_copy.set_board(board)
    game_copy.do_move(our_player.get_disk(), where_to_put(game_copy.board, our_player, other_player))
    return game_copy.board


def where_to_put(board, our_player, other_player):
    """
    A function that returns where to put a new disk
    :param board: the board on which our player needs to decide where to put the disk
    :param our_player: our player
    :param other_player: the other player
    :return: the coordinate (y,x) to put the disk: 0 <= y,x <= 7
    """
    game_copy = Game.Game(our_player, other_player)
    game_copy.set_board(board)
    return our_player.choose_move(game_copy)[1]


def where_to_flip(board, our_player, other_player):
    """
    A function that returns where to flip the disks after our player move
    :param board: the board on which our player does the move
    :param our_player:  our player
    :param other_player: the other player
    :return: the  places to put flip the dis (a coordinate is y,x  - 0 <= y,x <= 7)
    """
    game_copy = Game.Game(our_player, other_player)
    game_copy.set_board(board)
    return game_copy.to_flip(our_player.get_disk(), where_to_put(game.board, our_player, other_player))

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

player1 = Player.Player(heuristic = palti_black,  name="player1")
player2 = Player.Player(type=Player.Player.PlayerTypes.HUMAN, name="player2")
game = Game.Game(player1, player2)
board = game.board
print(how_board_supposed_to_be_after_putting(board, player1, player2))
print(where_to_put(board, player1, player2))
print(where_to_flip(board, player1, player2))
