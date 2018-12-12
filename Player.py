class Player:

    def __init__(self, heuristic, disk):
        self.heuristic = heuristic
        self.disk = disk

    def get_heuristic(self):
        return self.heuristic

    def get_disk(self):
        return self.disk

    def compare_players(self, player1, player2):
