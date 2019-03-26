import Game
import dill
import numpy as np
import copy

class Legal_Moves_Helper:

    def __init__(self):
        self.lmdw = {}
        self.lmdb = {}
        self.init_board = np.zeros((8, 8)).astype(int)
        self.init_board[(3, 4)] = Game.BLACK  # maybe need to make player class and then player.number
        self.init_board[(4, 3)] = Game.BLACK
        self.init_board[(3, 3)] = Game.RED
        self.init_board[(4, 4)] = Game.RED

    def get_state(self, before_move_game, disk):
        before_move_board = before_move_game.board
        tup = tuple(map(tuple, before_move_board))
        if disk == Game.RED:
            if tup not in self.lmdw:
                return [] #will add it in the do move part with the get move function
            else:
                return self.lmdw[tup]
        else: #disk is black
            if tup not in self.lmdb:
                return [] #will add it in the do move part with the get move function
            else:
                return self.lmdb[tup]


    def get_new_legal_moves(self, game_before_move, disk, legal_moves):
        tup = tuple(map(tuple, game_before_move.board))

        if disk == Game.RED:
            self.lmdw[tup] = legal_moves
        else:
            self.lmdb[tup] = legal_moves

    def save_legal_moves_helper(self):
        filename = 'Legal_Moves_Helper'
        with open('legal_moves_helper/' + filename+'.pkl', 'wb') as output:
            dill.dump(self, output, dill.HIGHEST_PROTOCOL)
        output.close()

    def size(self):
        return len(self.lmdw) + len(self.lmdb)



    @staticmethod
    def create_new(password):
        """
        a function that we need if we can't load the player
        """
        p_word = "shit happened we need a new one"
        if password != p_word:
            raise ValueError("wrong password")
        lmh = Legal_Moves_Helper()
        lmh.save_legal_moves_helper()

    @staticmethod
    def update():
        old = Game.Game.load_legal_moves_helper()
        new = Legal_Moves_Helper()
        new.bmdb = old.lmdb
        new.bmdw = old.lmdw
        new.save_legal_moves_helper()
        return new
