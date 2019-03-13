from random import *
import Player
import numpy as np
import sys
import copy
import Game
palti_n = np.log(10) / np.log(1.5)  # a somewhat arbitrary constant
palti_A = 1 / (40 ** palti_n)  # a somewhat arbitrary constant
ALL_FUNCTIONS =[lambda game, player: game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n), #pos
                lambda game, player: -(game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)),#neg
                lambda game, player: game.get_num_of_corners(player), #pos
                lambda game, player: -game.get_opponent_num_of_corners(player), #neg
                lambda game, player: game.get_num_of_sides(player), #pos
                lambda game, player: -game.get_opponent_num_of_sides(player), #neg
                lambda game, player: -game.get_num_of_options_for_other(player), #neg
                lambda game, player: game.is_winner_score(player)] #pos

NUM_OF_PARAMS = len(ALL_FUNCTIONS)


def evolve_q_time(players_list, n, q):
    """
    A function that gets a list if heuristics and evolves them n times
    :param players_list: a list of players
    :param n: the number of new heuristics to return
    :param q: the quality of the evolution - the number of evolutions it goes trough
    :return: the list after the evolution
    """
    players_list = Player.Player.compare_players_list(players_list)
    if q == 0:
        while len(players_list) > n:
            players_list.pop(-1)  # popping the worst players

        return players_list

    while len(players_list) < n:
        for i in range(len(players_list)):
            player = players_list[i]
            for p in evolve(player, (5 - (i * 4) / len(players_list))):  # todo 5 - (i * 4) is arbitrary
                players_list.append(p)

    players_list = Player.Player.compare_players_list(players_list)

    while len(players_list) > n - 1 and q != 0:
        players_list.pop(-1)  # popping the worst players

    return evolve_q_time(players_list, n, q - 1)


def evolve(player, n):
    """
    A function that evolves a heuristic
    :param player: the player to evolve
    :param n: the number of players after evolutions
    :return: a list of new evolved players
    """
    heuristic = player.get_heuristic()
    players_list = []
    for i in range(n):
        h = copy.deepcopy(heuristic)
        for feature in h:
            add_noise(feature, 0.3)  #todo 0.3 is arbitrary
        p = Player.Player(h)
        players_list.append(p)
    players_list.append(player)
    return players_list


def add_noise(feature, max_noise):
    """
    :param feature: a list- the first element is the weight the second is the function to call
    in order to get the parameter
    :param max_noise: precentage (between 0 and 1)
    """
    lim = feature[0]
    rand = 2 * (random() - 0.5)  # a random number between -1 and 1
    noise = max_noise * lim * rand
    feature[0] += noise  # todo make sure that feature is a list and not a tuple, worst case return

def create_player_with_heuristic():
    """
    a function that creates a player with a random heuristic
    :return: a player with a random heuristic
    """
    heuristic = []
    for i in range (NUM_OF_PARAMS):
        weight = randrange(0, sys.maxsize, 1)/128
        tup = [weight, ALL_FUNCTIONS[i]]
        heuristic.append(tup)
    player = Player.Player(heuristic = heuristic, name= str(Player.Player.number_of_saved_players() + 1), p_type = Player.Player.PlayerTypes.MINIMAX)
    return player

def selection(players_list, precentage, n):
    """
    The idea of selection phase is to select the fittest individuals and let them pass their genes to the next generation.
    Two pairs of individuals (parents) are selected based on their fitness scores. Individuals with high fitness have more
    chance to be selected for reproduction.
    in short - takes a list of players and decide which players pass their genes
    :param players_list: a list of players
    :return: a list of players that are chosen to create the new generation
    """
    pass


def crossover(p1, p2):
    """
    Crossover is the most significant phase in a genetic algorithm.
    For each pair of parents to be mated, a crossover point is chosen at random from within the genes.
    in short - creating the new generation from two parents
    :param p1: player 1
    :param p2: player 2
    :return: a new player that is the "child" of the two players
    """
    pass

def mutation(p):
    """
    In certain new offspring formed, some of their genes can be subjected to a mutation with a low random probability.
    This implies that some of the bits in the bit string can be flipped.
    in short - creating a mutation from a player
    :param p: a player to mutate from
    :return: a mutated player
    """


def fitness_level(p,n):
    """
    a basic function which determies the fitness level of the player
    :param p: the player we need to determine what it's fitness level
    :return: a basic fitness level (a number)
    """
    num_wins = 0
    random = Player.Player.load_player('pklFiles/random_player.pkl')
    game1 = Game.Game(p, random)
    game2 = Game.Game(random, p)
    for i in range(n):
        if(game1.play_game() == p):
            num_wins += 1
        else:
            num_wins -= 1
        if(game2.play_game() == p):
            num_wins += 1
        else:
            num_wins -=1
    return num_wins


def termination(p, precentage, n):
    """
        The algorithm terminates if the population has converged
        (does not produce offspring which are significantly different from the previous generation).
        Then it is said that the genetic algorithm has provided a set of solutions to our problem.
        in short  - determines whether to "kill" the player or not
        :param p: the player to decide if to "kill" or not
        :return: True we kill him, False otherwise .
        """
    return ((fitness_level(p,n)/n) <= precentage)
