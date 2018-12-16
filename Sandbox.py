import Game
import Minimax
import Player
import numpy as np
game = Game.Game()
game.set_board(np.array([[-1, -1, -1, -1, -1, -1, -1, -1],
                [-1,  1, -1, -1,  1,  0, -1,  0],
                [-1, -1, -1,  1,  1,  1,  0,  0],
                [-1, -1,  1,  1,  1,  1,  1,  0],
                [ 0,  0,  1,  1,  1,  1,  0,  0],
                [ 0,  0,  1,  1,  1,  1,  1,  0],
                [ 0,  0,  0,  1,  0,  0,  0,  0],
                [ 0,  0,  1,  0,  0,  0,  0,  0]]))
print("legal", game.get_legal_moves(1))

h = [[1, lambda game: game.get_black_number()], [-1, lambda game: game.get_white_number()]]
player1 = Player.Player(heuristic=h, disk= 1, name = "computer")
player2 = Player.Player(disk = -1, type = Player.Player.PlayerTypes.HUMAN, name = "human")
game.play_game(player1, player2, to_print=True)