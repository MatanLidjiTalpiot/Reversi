from random import *
import Player
import numpy as np
import sys
import copy
import Game
import time

palti_n = np.log(10) / np.log(1.5)  # a somewhat arbitrary constant
palti_A = 1 / (40 ** palti_n)  # a somewhat arbitrary constant
ALL_FUNCTIONS = [
    lambda game, player: game.get_color_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n),
    # pos
    lambda game, player: -(game.get_opponent_disk_num(player) * palti_A * np.power(game.get_number_of_turns(), palti_n)),
    # neg
    lambda game, player: game.get_num_of_corners(player),  # pos
    lambda game, player: -game.get_opponent_num_of_corners(player),  # neg
    lambda game, player: game.get_num_of_sides(player),  # pos
    lambda game, player: -game.get_opponent_num_of_sides(player),  # neg
    lambda game, player: -game.get_num_of_options_for_other(player),  # neg
    lambda game, player: game.is_winner_score(player)]  # pos

NUM_OF_PARAMS = len(ALL_FUNCTIONS)
PALTI_PLAYER_4 = Player.Player.load_player('pklFiles/palti_player_d4.pkl')
RANDOM_PLAYER = Player.Player.load_player('pklFiles/random_player.pkl')

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
            add_noise(feature, 0.3)  # todo 0.3 is arbitrary
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
    for i in range(NUM_OF_PARAMS):
        weight = random() * 100
        tup = [weight, ALL_FUNCTIONS[i]]
        heuristic.append(tup)
    player = Player.Player(heuristic=heuristic, p_type=Player.Player.PlayerTypes.MINIMAX)
    return player


def selection(players_list, scores_list):
    """
    The idea of selection phase is to select the fittest individuals and let them pass their genes to the next generation.
    Two pairs of individuals (parents) are selected based on their fitness scores. Individuals with high fitness have more
    chance to be selected for reproduction.
    in short - takes a list of players and decide which players pass their genes
    :param players_list: a list of players
    :param scores_list: the scores of the players in players_list (same order)
    :return: a list of players that are chosen to create the new generation
    """
    total_score = sum(scores_list)
    new_gen = []
    for i in range(len(players_list)):
        score_sum = 0
        parent1_score = total_score * random()
        parent2_score = total_score * random()
        parent1 = 0
        parent2 = 0
        for j in range(len(players_list)):
            if score_sum < parent1_score <= score_sum + scores_list[i]:
                parent1 = j
            if score_sum < parent2_score <= score_sum + scores_list[i]:
                parent2 = j
            score_sum += scores_list[i]
        new_gen.append(crossover(players_list[parent1], players_list[parent2], scores_list[parent1], scores_list[parent2]))
    return new_gen


def crossover(player1, player2, score1, score2):
    """
    Crossover is the most significant phase in a genetic algorithm.
    For each pair of parents to be mated, a crossover point is chosen at random from within the genes.
    in short - creating the new generation from two parents
    :param player1: player 1
    :param player2: player 2
    :param score1: score of player 1
    :param score2: score of player 2
    :param gen_number: the number of the generation that we are running
    :param folder_name: the name of the folder to save the player
    :return: a new player that is the "child" of the two players
    """
    heuristic = player1.heuristic
    h_other = player2.heuristic
    for i in range(len(heuristic)):
        if random() > 0.5:
            heuristic[i][0] = h_other[i][0]
    p = Player.Player(heuristic=heuristic)
    return p

def mutation(player, n=1):
    """
    In certain new offspring formed, some of their genes can be subjected to a mutation with a low random probability.
    This implies that some of the bits in the bit string can be flipped.
    in short - creating a mutation from a player
    :param player: a player to mutate from
    :param gen_number: the number of the generation that we are running
    :param folder_name: the name of the folder to save the player
    :return: a mutated player
    """
    heuristic = player.heuristic
    feature = randint(0, len(heuristic) - 1)  # the feature to mutate
    heuristic[feature][0] *= (2 * random())  # mutation ratio
    p = Player.Player(heuristic=heuristic)
    return p


def fitness_level(p_list):
    """
    a basic function which determies the fitness level of the player
    :param p: the index of the player we want to evaluate the fitness of
    :param p_list: a shuffled list of players
    :return: a basic fitness level (a number)
    """
    # print("########################################")
    # for i in range(len(p.heuristic)):
    #     print(p.heuristic[i][0])
    # print("########################################")
    for i in range(len(p_list)):
        curr_player = p_list[i]
        last_player = p_list[(i-1)]
        game = Game.Game(curr_player, last_player)
        game.final_board_in_game()
        curr_player.grade += game.get_color_disk_num(curr_player)/4
        last_player.grade += game.get_color_disk_num(last_player)/4
        print("finished half evaluation number ", i, " of ", len(p_list))
        game.reset_game(last_player, curr_player)
        game.final_board_in_game()
        curr_player.grade += game.get_color_disk_num(curr_player)/4
        last_player.grade += game.get_color_disk_num(last_player)/4
        print("finished evaluation number ", i, " of ", len(p_list))


def termination(p_list, threshold = 15):
    """
        The algorithm terminates if the population has converged
        (does not produce offspring which are significantly different from the previous generation).
        Then it is said that the genetic algorithm has provided a set of solutions to our problem.
        in short  - determines whether to "kill" the player or not
        :param p_list: the list of players to kill or help survive
        :return: the list of players that didn't die
        """
    ret_list = []
    for player in p_list:
        if player.grade > threshold:
            ret_list.append(player)
    print("finished terminating, terminated: ", len(p_list) - len(ret_list), " players")
    return ret_list


def genetic_main(num_p, folder_name, gen_number, depth_number, prob = 0.1, players_list = None, term_threshold = 0):

    #creating a list with p new player
    if depth_number == 0:
        print("finished")
    else:
        p_list = players_list
        if p_list == None:
            #create p_list
            p_list = []
            for i in range(num_p):
                p = create_player_with_heuristic()
                p_list.append(p)
            fitness_level(p_list)
            termination(p_list, term_threshold)
            p_list.sort(key = lambda p: p.grade, reverse=True)
            for i in range (len(p_list)):
                print(p_list[i].grade ,end = ", " )
            Player.Player.save_sorted_list_to_folder(p_list, folder_name + "/gen" + str(gen_number))
            gen_number += 1

        counter = 0
        mutations = []
        for player in p_list:
            #choose whether a player goes through a mutation
            if random() < prob:
                counter += 1
                mute = mutation(player)
                mutations.append(mute)
        print("created ", counter, "mutations")
        scores_list = []
        for  i in range (len(p_list)):
            scores_list.append(p_list[i].grade)
        new_gen = selection(p_list, scores_list)
        print("created ", len(new_gen)," new generation players")
        mutations.extend(new_gen)
        shuffle(mutations)
        fitness_level(mutations)
        after_termination = termination(p_list)
        after_termination.sort(key = lambda p: p.grade, reverse=True)
        for i in range (len(after_termination)):
            print(after_termination[i].grade, end = ", ")
        Player.Player.save_sorted_list_to_folder(after_termination, folder_name+"/gen"+str(gen_number))
        print("finished gen", gen_number)
        if (mutations[int(len(after_termination)/(-10))].grade >= term_threshold):
            term_threshold = min(term_threshold + 1, after_termination[int(len(mutations) / (-10))].grade)
        genetic_main(0, folder_name, gen_number+1, depth_number - 1, prob, after_termination, term_threshold)

