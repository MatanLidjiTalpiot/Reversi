import Game
import Minimax
import copy
from enum import Enum
import random
import dill
import numpy as np
import os
POS_INT = 1
NEG_INT = -1


class Player:
    class PlayerTypes(Enum):
        MINIMAX = 1
        HUMAN = 2
        NBOARD = 3
        RANDOM = 4
        FOUR_BY_FOUR = 5
        TABLE = 6

    NUM_OF_PLAYERS = 0
    ALL_PLAYERS = []
    #ALL_FUNCTIONS = [lambda game, player: game.get_color_disk_num(player.get_disk()), lambda game, player: game.get_opponent_disk_num(player.get_disk())] todo - this is before blind to color
    palti_n = np.log(10) / np.log(1.5)  # a somewhat arbitrary constant
    palti_A = 1 / (40 ** palti_n)  # a somewhat arbitrary constant
    ALL_FUNCTIONS =[lambda game, player: game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n),
                    lambda game, player: (game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)),
                    lambda game, player: game.get_num_of_corners(player),
                    lambda game, player: game.get_opponent_num_of_corners(player),
                    lambda game, player: game.get_num_of_sides(player),
                    lambda game, player: game.get_opponent_num_of_sides(player),
                    lambda game, player: game.get_num_of_options_for_other(player),
                    lambda game, player: game.is_winner_score(player)]
    DEPTH = 4  # 4 is arbitrary
    HEURISTIC_LENGTH = len(ALL_FUNCTIONS)

    def __init__(self, heuristic=None, name=None, disk=None, p_type=PlayerTypes.MINIMAX):
        if name is None:
            name = Player.NUM_OF_PLAYERS  # credit for benny
        if p_type not in [Player.PlayerTypes.HUMAN, Player.PlayerTypes.NBOARD, Player.PlayerTypes.MINIMAX, Player.PlayerTypes.RANDOM, Player.PlayerTypes.TABLE]:
            raise ValueError(p_type, " is not a valid p_type")

        if p_type == Player.PlayerTypes.MINIMAX:
            self.type = Player.PlayerTypes.MINIMAX

            if heuristic is None:
                raise ValueError("no heuristic was inputted")

        self.type = p_type
        self.heuristic = heuristic
        self.disk = disk
        self.name = str(name)
        self.number_of_wins = 0

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

    def rename(self, new_name):
        self.name = new_name

    def compare_two_players(self, player1, player2):
        game = Game.Game(player1, player2)
        winning_player = game.play_game()
        if player1 == winning_player:
            return POS_INT
        elif player2 == winning_player:
            return NEG_INT
        else:
            raise ValueError("check your mother fucking code!")

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
                print(self.name + ", do a move")
                return self.human_move(game,)
            else:
                return (None, None)
        coordinate = coordinate.split(" ")
        coordinate[0] = int(coordinate[0])
        coordinate[1] = int(coordinate[1])
        coordinate = tuple(coordinate)
        if len(coordinate) != 2 or coordinate[0] not in not_invalid_coordinates or coordinate[1] not in not_invalid_coordinates:
            raise ValueError("not a valid coordinate")
        temp_game = copy.deepcopy(game)
        try:
            temp_game.do_move(self.disk, coordinate)
        except:
            print("not a legal move")
            return self.human_move(game)
        return (None, (coordinate[0], coordinate[1]))

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
            if move[0] not in range(2, 5) or move[0] not in range(2, 5):
                legal_moves.remove(move)
        if legal_moves != []:
            return random.choice(legal_moves)
        else:
            return [None, None]

    def choose_move(self, game):
         # try:
            if self.type == Player.PlayerTypes.MINIMAX:
                return Minimax.alpha_beta(game, Player.DEPTH, self, True,
                                          self.get_disk())
            elif self.type == Player.PlayerTypes.HUMAN:
                return self.human_move(game)
            elif self.type == Player.PlayerTypes.NBOARD:
                pass  # todo add choose move for Nboard player
            elif self.type == Player.PlayerTypes.RANDOM:
                return self.random_move(game)
            elif self.type == Player.PlayerTypes.FOUR_BY_FOUR:
                return self.four_by_four_move(game)
            elif self.type == Player.PlayerTypes.TABLE:
                raise ValueError("not supposed to do a move")
         # except Exception as e:
         #     print("do again")
         #     print(str(e))
         #     return self.choose_move(game)

    @staticmethod
    def players_list_to_winning_dict(players_list):
        """
        A method that gets a list of  players and returns a a dictionary of the players and how
        much wins each player had.
        each player plays against every other player twice - once starting and once when the
        other starts
        :param players_list: the list of players to play one against each other
        :return: the dictionary as explained above
        """
        players_dict = {}
        for player in players_list:
            players_dict[player] = 0
        for m in range(len(players_list)):
            main_player = players_list[m]
            for i in range(m + 1, len(players_list)):
                curr_player = players_list[i]
                if m == 0 and i == 1:
                    game = Game.Game(main_player, curr_player)
                else:
                    game.reset_game(main_player, curr_player)

                # run a game twice: each time a different player starts
                winner = game.play_game(to_print=False)
                players_dict[winner]+= 1
                game.reset_game(curr_player, main_player)
                winner = game.play_game(to_print = False)
                players_dict[winner] += 1
        return players_dict

    @staticmethod
    def compare_players_list(players_list):
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
        players_list.sort(key = lambda x: x[1], reverse=True)
        sorted_list = []
        for i in range(len(players_list)):
            sorted_list.append(players_list[i][0])
        return sorted_list



    @staticmethod
    def load_player(filename):
        """
        a method that loads a player from a file of a player.
        :param filename: the path for the file of the object.
        :return: the object of the player that is saved in the file.
        """
        with open(filename, 'rb') as input:
            player = dill.load(input)
            input.close()
            player.number_of_wins = 0
        return player

    @staticmethod
    def save_to_folder(player, folder_name = "pklFiles"):
        """
        a function that gets a folder name and saves a player object to it
        if a folder does not exists it creates a new one
        :param folder_name: the name of the folder to save the player in
        :param player: the player to save
        """

        filename = player.get_name()
        with open(folder_name + '/' + filename + '.pkl', 'wb') as output:
            dill.dump(player, output, dill.HIGHEST_PROTOCOL)

        with open(folder_name + '/' + filename + '_copy.pkl', 'wb') as output_copy:
            output_copy = copy.deepcopy(output)
            output.close()
            output_copy.close()
        # except:
        #     os.mkdir(folder_name)
        #     with open(folder_name + '/' + filename + '.pkl', 'wb') as output:
        #         dill.dump(player, output, dill.HIGHEST_PROTOCOL)

    @staticmethod
    def save_sorted_list_to_folder(sorted_list, folder_name):
        dir = './' + folder_name
        if not (os.path.isdir(dir)):
            os.mkdir(folder_name)
        for i in range (len(sorted_list)):
            p = sorted_list[i]
            p.rename(str(len(os.listdir(folder_name))))
            Player.save_to_folder(p, folder_name = folder_name)

    @staticmethod
    def number_of_saved_players():
        number_of_saved_players = len(os.listdir('pklFiles'))
        return number_of_saved_players


    def __eq__(self, player2):
        player1_h = self.get_heuristic()
        player2_h = player2.get_heuristic()
        for i in range(Player.HEURISTIC_LENGTH):
            if player1_h[i][0] != player2_h[i][0]:
                return False
        return True

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __cmp__(self, other_player):
        if(self.number_of_wins > other_player.number_of_wins):
            return POS_INT
        if(self.number_of_wins < other_player.number_of_wins):
            return NEG_INT
        return 0 #equal



Player.compare_two_players = staticmethod(Player.compare_two_players)
#Player.compare_players_list = staticmethod(Player.compare_players_list)
