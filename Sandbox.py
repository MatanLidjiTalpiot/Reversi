import Game
import Minimax
import Player
game = Game.Game()
h = [[1, lambda game: game.get_black_number()], [-1, lambda game: game.get_white_number()]]
player1 = Player.Player(heuristic=h, disk= 1, name = "computer")
player2 = Player.Player(type = 2, name = "human")
game.play_game(player1, player2, to_print=True)