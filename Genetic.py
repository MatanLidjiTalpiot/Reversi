import Game
import copy
import Minimax
import Player
from random import *
ALL_FUNCTIONS = []
NUM_OF_PARAMS = len(ALL_FUNCTIONS)


def evolve_N_time(h_list, n, q):
    """
    A function that gets a list if heuristics and evolves them n times
    :param h_list: a list of heuristics
    :param n: the number of new heuristics to return
    :param q: the quality of the evolution - the number of evolutions it goes trough
    :return: the list after the evolution
    """
    if q == 0 and len(h_list) == n: #recursive ending condition
        return h_list


    pass #todo finish


def evolve(heuristic, n):
    """
    A function that evolves a heuristic
    :param heuristic: the heuristic to evolve
    :param n: the number of heuristics after evolutions
    :return: a list of new evolved heuristics, the first one is the original heuristic
    """
    heuristic_list = []
    heuristic_list.append(heuristic)
    for i in range (n):
        h = heuristic # todo maybe need deepcopy
        for feature in h:
            add_noise(feature, 0.3) # 0.3 is arbitrary
        heuristic_list.append(h)
    return heuristic_list

def add_noise(feature, max_noise):
    lim = feature[0]
    noise = max_noise*lim*random()
    feature[0] += noise


arr = [0,1]
for i in range (7):
    j = i%2
    print(arr[j])
