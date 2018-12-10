import Game
import copy
import Minimax
from random import *
ALL_FUNCTIONS = []
NUM_OF_PARAMS = len(ALL_FUNCTIONS)
DEPTH = 1 # for the meanwhile

class Player:

    def __init__(self, heuristic, disk):
        self.heuristic = heuristic
        self.disk = disk

    def get_heuristic(self):
        return self.heuristic

    def get_disk(self):
        return self.disk


def play_game(p1, p2):
    """
    A function that plays a game between two heuristics
    :param p1: player number 1
    :param p2: player number 2
    :return: the winning player and the grades of each heuristic in the game
    """
    players = (p1, p2)
    if p1.disk == p2.disk:
        raise ValueError("two players can't have the same color")
    game = Game.Game()
    turn = 0
    while not game.is_board_full():
        disk = players[turn % 2].get_disk()
        heuristic = players[i].get_heuristic()
        op = Minimax.minimax(game, DEPTH, DEPTH, heuristic, True, disk, None)[1]
        game.do_move(disk, op)



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

def add_noise(feature, max_noise):
    lim = feature[0]
    noise = max_noise*lim*random()
    feature[0] += noise


arr = [0,1]
for i in range (7):
    j = i%2
    print(arr[j])
