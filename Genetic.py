import Game
from random import *
ALL_FUNCTIONS = []
NUM_OF_PARAMS = len(ALL_FUNCTIONS)
import copy
def play_game(h1, h2):
    """
    A function that plays a game between two heuristics
    :param h1: heuristic number 1
    :param h2: heuristic number 2
    :return: the winning heuristic and the grades of each heuristic in the game
    """
    pass


def evolve_N_time(h_list, n, q):
    """
    A function that gets a list if heuristics and evolves them n times
    :param h_list: a list of heuristics
    :param n: the number of new heuristics to return
    :param q: the quality of the evolution - the number of evolutions it goes trough
    :return: the list after the evolution
    """
    pass

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


def add_noise(feture, max_noise):
    lim = feture[0]
    noise = max_noise*lim*random()
    feture[0] += noise



print(random())