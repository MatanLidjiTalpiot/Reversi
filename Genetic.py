from random import *
import Player

ALL_FUNCTIONS = []
NUM_OF_PARAMS = len(ALL_FUNCTIONS)


def evolve_N_time(players_list, n, q):
    """
    A function that gets a list if heuristics and evolves them n times
    :param h_list: a list of heuristics
    :param n: the number of new heuristics to return
    :param q: the quality of the evolution - the number of evolutions it goes trough
    :return: the list after the evolution
    """
    if q == 0 and len(players_list) == n: #recursive end condition
        return players_list

    Player.compare_players_list(players_list)
    if len(players_list) < n:


    pass #todo finish


def evolve(player, n):
    """
    A function that evolves a heuristic
    :param heuristic: the heuristic to evolve
    :param n: the number of heuristics after evolutions
    :return: a list of new evolved heuristics, the first one is the original heuristic
    """
    heuristic = player.get_heuristic()
    heuristic_list = []
    heuristic_list.append(heuristic)
    for i in range (n):
        h = heuristic # todo maybe need deepcopy
        for feature in h:
            add_noise(feature, 0.3) # 0.3 is arbitrary
        heuristic_list.append(h)
    return heuristic_list

def add_noise(feature, max_noise):
    """
    :param feature:
    :param max_noise:
    :return:
    """
    lim = feature[0]
    rand = 2*(random() - 0.5) # a random number between -1 and 1
    noise = max_noise * lim * rand
    feature[0] += noise


arr = [0,1]
for i in range (7):
    j = i%2
    print(arr[j])
