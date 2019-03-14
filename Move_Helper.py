import Game
import dill
import numpy as np


class Move_Helper:

    def __init__(self):
        self.bmdw = {}
        self.bmdb = {}
        self.init_board = np.zeros((8, 8)).astype(int)
        self.init_board[(3, 4)] = Game.BLACK  # maybe need to make player class and then player.number
        self.init_board[(4, 3)] = Game.BLACK
        self.init_board[(3, 3)] = Game.WHITE
        self.init_board[(4, 4)] = Game.WHITE

    def get_state(self, before_move_game, move, disk):
        before_move_board = before_move_game.board
        tup = (tuple(map(tuple, before_move_board)), move)
        if disk == Game.WHITE:
            if tup not in self.bmdw:
                return [] #will add it in the do move part with the get move function
            else:
                if (np.count_nonzero(before_move_board) + 1 != np.count_nonzero(self.bmdw[tup])):
                    print("**************************")
                    print(self.bmdw[tup])
                    print(move)
                    print(before_move_board)
                    print("**************************")
                    raise ValueError("shit happens")
                return self.bmdw[tup]
        else: #disk is black
            if tup not in self.bmdb:
                return [] #will add it in the do move part with the get move function
            else:
                if (np.count_nonzero(before_move_board) + 1 != np.count_nonzero(self.bmdb[tup])):
                    raise ValueError("shit happens")
                return self.bmdb[tup]


    def get_new_move(self, game_before_move, move, disk, board_after_move):
        tup = (tuple(map(tuple, game_before_move.board)), move)

        if game_before_move.get_number_of_turns() + 1 != np.count_nonzero(board_after_move):
            raise  ValueError("not supposed to happen")
        if disk == Game.WHITE:
            self.bmdw[tup] = board_after_move
        else:
            self.bmdb[tup] = board_after_move

    def save_move_helper(self):
        filename = 'Move_Helper'
        with open('move_helper/' + filename+'.pkl', 'wb') as output:
            dill.dump(self, output, dill.HIGHEST_PROTOCOL)

    def size(self):
        return len(self.bmdw) + len(self.bmdb)



    @staticmethod
    def create_new(password):
        """
        a function that we need if we can't load the player
        """
        p_word = "shit happened we need a new one"
        if password != p_word:
            raise ValueError("wrong password")
        mh = Move_Helper()
        mh.save_move_helper()

    @staticmethod
    def update():
        old = Game.Game.load_move_helper()
        new = Move_Helper()
        new.bmdb = old.bmdb
        new.bmdw = old.bmdw
        new.save_move_helper()
        return new
