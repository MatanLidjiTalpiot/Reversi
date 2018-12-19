import Game
import Minimax
import Player
import numpy as np
game = Game.Game()
#game.set_board(np.array([[0, 0, 0, 1, 0, 0, 0, 0],
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

h = [[1, lambda game: game.get_black_number()],
     [-1, lambda game: game.get_white_number()],
     [100,lambda game: game.get_num_of_cornors(1)],
     [-200, lambda game: game.get_num_of_cornors(-1)],
     [50, lambda game: game.get_num_of_sides(1)],
     [-100, lambda game: game.get_num_of_sides(-1)]]
player1 = Player.Player(heuristic=h, disk= 1, name = "computer")

player2 = Player.Player(disk = -1, name = "ferri", type = Player.Player.PlayerTypes.HUMAN)

dic = {player1.name:0, player2.name:0}
for i in range (1):
    winner = game.play_game(player1, player2, to_print = True)
    print ("winner of the ", i, "game is: ", winner.name)
    dic[winner.name] += 1
print(dic)