import Game
import Minimax
import Player
import Gui
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


# game.set_board(np.array([[ 0,  0, -1,  1, -1, -1, -1, -1],
#  [ 0,  0, -1, -1,  1, -1, -1, -1],
#  [ 1,  0, -1, -1, -1,  1, -1,  1],
#  [ 1,  0, -1, -1, -1 , 1 ,-1 , 1],
#  [ 1, -1, -1, -1, -1, -1, -1 , 1],
#  [ 0,  0, -1, -1, -1, -1, -1,  1],
#  [ 0,  0, -1,  0 , 0,  0,  1,  1],
#  [ 0,  0, -1,  0 , 0,  1,  1,  1]]))



h1 = [[1, lambda game: game.get_black_number()],
     [-1, lambda game: game.get_white_number()],
     [100,lambda game: game.get_num_of_cornors(1)],
     [-1000, lambda game: game.get_num_of_cornors(-1)],
     [50, lambda game: game.get_num_of_sides(1)],
     [-200, lambda game: game.get_num_of_sides(-1)],
     [-200, lambda game: game.get_num_of_options_for_other(1)]]


h2 = [[1, lambda game: game.get_black_number()],
     [-1, lambda game: game.get_white_number()],
     [100,lambda game: game.get_num_of_cornors(1)],
     [-1000, lambda game: game.get_num_of_cornors(-1)],
     [50, lambda game: game.get_num_of_sides(1)],
     [-200, lambda game: game.get_num_of_sides(-1)]]


h3 = [[1, lambda game: game.get_black_number()],
     [-1, lambda game: game.get_white_number()],
     [100,lambda game: game.get_num_of_cornors(-1)],
     [-1000, lambda game: game.get_num_of_cornors(1)],
     [50, lambda game: game.get_num_of_sides(-1)],
     [-200, lambda game: game.get_num_of_sides(1)],
     [-100, lambda game: game.get_num_of_options_for_other(-1)]]


h4 = [[1, lambda game: game.get_black_number()],
     [-1, lambda game: game.get_white_number()],
     [100,lambda game: game.get_num_of_cornors(-1)],
     [-1000, lambda game: game.get_num_of_cornors(1)],
     [50, lambda game: game.get_num_of_sides(-1)],
     [-200, lambda game: game.get_num_of_sides(1)]]
player1 = Player.Player(heuristic=h1, disk= 1, name = "computer1")

player2 = Player.Player(disk = -1, name = "drori", type = Player.Player.PlayerTypes.HUMAN)

dic = {player1.name:0, player2.name:0}
for i in range (1):
    winner = Gui.play_game(game, player1, player2, to_print = False)
    print ("winner of the ", i, "game is: ", winner.name)
    dic[winner.name] += 1
    print(dic)
    while True:
        pass