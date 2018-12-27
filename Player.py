import Game
import Minimax
import copy
from enum import Enum
import random

POS_INT = 1
NEG_INT = -1


class Player:
    class PlayerTypes(Enum):
        MINIMAX = 1
        HUMAN = 2
        NBOARD = 3
        RANDOM = 4
        FOUR_BY_FOUR = 5

    NUM_OF_PLAYERS = 0
    ALL_PLAYERS = []
    ALL_FUNCTIONS = [lambda game, player: game.get_color_disk_num(player.get_disk()),
                     lambda game, player: game.get_opponent_disk_num(player.get_disk())]
    DEPTH = 4 # 4 is arbitrary
    HEURISTIC_LENGTH = len(ALL_FUNCTIONS)

    def __init__(self, heuristic=None, name=NUM_OF_PLAYERS, disk=None,
                 type=PlayerTypes.MINIMAX):
        if type not in [Player.PlayerTypes.HUMAN, Player.PlayerTypes.NBOARD,
                        Player.PlayerTypes.MINIMAX, Player.PlayerTypes.RANDOM]:
            raise ValueError(type, " is not a valid type")
        if type == Player.PlayerTypes.MINIMAX:
            self.type = Player.PlayerTypes.MINIMAX
            if heuristic == None:
                heuristic = [[1, lambda game, disk: game.get_color_disk_num(self.disk)],
                             [-1, lambda game, disk: game.get_opponent_disk_num(-1 * self.disk)]]
        self.type = type
        self.heuristic = heuristic
        self.disk = disk
        self.name = name
        if self.type == Player.PlayerTypes.MINIMAX and self not in Player.ALL_PLAYERS:
            Player.NUM_OF_PLAYERS += 1
            Player.ALL_PLAYERS.append(self)
        else:
            pass  # todo think if to do something

    def set_disk(self, disk):
        self.disk = disk

    def get_heuristic(self):
        return self.heuristic

    def get_disk(self):
        return self.disk

    def get_name(self):
        return self.name

    def compare_two_players(self, player1, player2):
        game = Game.Game()
        winning_player = game.play_game(player1, player2)
        if player1 == winning_player:
            return POS_INT
        elif player2 == winning_player:
            return NEG_INT
        else:
            raise ValueError("check your mother fucking code!")

    def players_list_to_winning_dict(self, players_list):
        """
        A method that gets a list of  players and returns a a dictionary of the players and how
        much wins each player had.
        each player plays against every other player twice - once starting and once when the
        other starts
        :param players_list: the list of players to play one against each other
        :return: the dictionary as explained above
        """
        game = Game.Game()
        players_dict = {}
        for player in players_list:
            players_dict[player] = 0
        for m in range(len(players_list)):
            main_player = players_list[m]
            for i in range(m + 1, len(players_list)):
                player = players_list[i]
                # run a game twice: each time a different player starts
                players_dict[game.play_game(main_player, player)] += 1
                game.reset_game()
                players_dict[game.play_game(player, main_player)] += 1
                game.reset_game()

        return players_dict

    def compare_players_list(self, players_list):
        """
        A function that gets a list of players and returns the list sorted by the most victorious
        player to the least
        :param players_list: the list of the players
        :return: a sorted list of the players from the most victorious to the least
        """
        players_dict = Player.players_list_to_winning_dict(players_list)
        players_list = []
        for player in players_dict:
            players_list.append([player, players_dict[player]])
        players_list = sorted(players_list, key=lambda x: x[1])
        sorted_list = []
        for i in range(len(players_list)):
            sorted_list.append(players_list[i][0])
        return sorted_list

    def __eq__(self, player2):
        player1_h = self.get_heuristic()
        player2_h = player2.get_heuristic()
        for i in range(Player.HEURISTIC_LENGTH):
            if player1_h[i][0] != player2_h[i][0]:
                return False
        return True

    def human_move(self, game):
        """
        A method that gets a coordinate for the user
        :return: the coordinate the user inputed
        """
        not_invalid_coordinates = list(range(8))
        text = str(self.name) + "enter a coordinate or None"
        coordinate = input(text)
        if coordinate == "None":
            if len(game.get_legal_moves(self.disk)) != 0:
                print("Eisner, do a move")
                return self.human_move(game)
            else:
                return (None, None)
        coordinate = coordinate.split(" ")
        coordinate[0] = int (coordinate[0])
        coordinate[1] = int (coordinate[1])
        coordinate=tuple(coordinate) #todo: better input
        if len(coordinate) != 2 or coordinate[0] not in not_invalid_coordinates or \
                        coordinate[1] not in not_invalid_coordinates:
            raise ValueError("not a valid coordinate")
        temp_game = copy.deepcopy(game)
        try:
            temp_game.do_move(self.disk, coordinate)
        except:
            print("not a legal move")
            return self.human_move(game)

        return (None,(coordinate[0], coordinate[1]))

    def random_move(self, game):
        all_moves = game.get_legal_moves(self.disk)
        if all_moves != []:
            return (None, random.choice(all_moves))
        else:
            return (None, None)

    def four_by_four_move(self, game):
        """
        A four by four move
        :param game: the game to play on
        :return: a valid move on a four by four move
        """
        legal_moves = game.get_legal_moves(disk)
        for move in legal_moves:
            if move[0] not in  range(2, 5) or move[0] not in range(2, 5):
                legal_moves.remove(move)
        if legal_moves != []:
            return random.choice(legal_moves)
        else:
            return [None, None]




    def choose_move(self, game):
        try:
            if self.type == Player.PlayerTypes.MINIMAX:
                return Minimax.alpha_beta(game, Player.DEPTH, self.get_heuristic(), True,
                                          self.get_disk())
            elif self.type == Player.PlayerTypes.HUMAN:
                return self.human_move(game)
            elif self.type == Player.PlayerTypes.NBOARD:
                pass  # todo add choose move for Nboard player
            elif self.type == Player.PlayerTypes.RANDOM:
                return self.random_move(game)
            elif self.type == Player.PlayerTypes.FOUR_BY_FOUR:
                return self.four_by_four_move(game)
        except Exception as e:
            print("do again")
            print(str(e))
            return self.choose_move(game)

Player.compare_two_players = staticmethod(Player.compare_two_players)
Player.compare_players_list = staticmethod(Player.compare_players_list)
Player.players_list_to_winning_dict = staticmethod(Player.players_list_to_winning_dict)
#Player.human_move = staticmethod(Player.human_move)
