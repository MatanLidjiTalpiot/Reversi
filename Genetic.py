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
    players_list = Player.compare_players_list(players_list)
    if q == 0:
        while len(players_list) >  n:
            players_list.pop(-1) # popping the worst players

    if q == 0 and len(players_list) == n: #recursive end condition
        return players_list

    while len(players_list) < n:
        for i in range (len(players_list)):
            player = players_list[i]
            for p in evolve(player, (5 - (i * 4)/len(players_list))):
                players_list.append(p)

    players_list = Player.compare_players_list(players_list)

    while len(players_list) > n-1 and q != 0:
        players_list.pop(-1) # popping the worst players

    return players_list, n, q - 1




def evolve(player, n):
    """
    A function that evolves a heuristic
    :param player: the player to evolve
    :param n: the number of players after evolutions
    :return: a list of new evolved players
    """
    heuristic = player.get_heuristic()
    players_list = []
    for i in range (n):
        h = heuristic # todo maybe need deepcopy
        for feature in h:
            add_noise(feature, 0.3) # 0.3 is arbitrary
        player = Player.Player(h)
        players_list.append(player)
    return players_list

def add_noise(feature, max_noise):
    """
    :param feature: a tuple- the first element is the weight the second is the function to call
    in order to get the parameter
    :param max_noise: precentage (between 0 and 1)
    """
    lim = feature[0]
    rand = 2*(random() - 0.5) # a random number between -1 and 1
    noise = max_noise * lim * rand
    feature[0] += noise


arr = [0,1]
for i in range (7):
    j = i%2
    print(arr[j])
