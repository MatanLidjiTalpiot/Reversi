import Game

POS_INT = 1
NEG_INT = -1


class Player:
    NUM_OF_PLAYERS = 0

    def __init__(self, heuristic, name = NUM_OF_PLAYERS, disk = None):
        self.heuristic = heuristic
        self.disk = disk
        self.name = name
        Player.NUM_OF_PLAYERS += 1

    def set_disk(self, disk):
        self.disk = disk

    def get_heuristic(self):
        return self.heuristic

    def get_disk(self):
        return self.disk

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
        players_list = sorted(players_list, key = lambda x: x[1])
        sorted_list = []
        for i in range(len(players_list)):
            sorted_list.append(players_list[i][0])
        return sorted_list


Player.compare_two_players = staticmethod(Player.compare_two_players)
Player.compare_players_list = staticmethod(Player.compare_players_list)
Player.players_list_to_winning_dict = staticmethod(Player.players_list_to_winning_dict)
