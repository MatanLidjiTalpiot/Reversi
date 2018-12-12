import numpy as np
import random
import Minimax

DEPTH = 1  # for the meanwhile - the searching depth in the heuristic
BLACK = 1
WHITE = -1
FIRST_COLOR = BLACK
SECOND_COLOR = WHITE


# WHITE = -BLACK

class Game:
    def __init__(self, size=8):
        self.size = size
        # empty cell: 0
        # AI (black): 1
        # Player (white): -1
        self.board = np.zeros((self.size, self.size)).astype(int)
        self.board[(3, 4)] = BLACK  # maybe need to make player class and then player.number
        self.board[(4, 3)] = BLACK
        self.board[(3, 3)] = WHITE
        self.board[(4, 4)] = WHITE
        self.num_of_turns = 0
        # board is shown transposed: coordinate = (y,x)

    def set_board(self, board):
        """
        A function that sets the board
        :param board: the board to set
        :return: nothing
        """
        self.board = board

    def do_move(self, disk, coordinate):
        """
        A function that does a move
        :param disk: 1 or -1 according to the color
        :param coordinate: the (y,x) coordinate to place the disk (has to be a tuple)
        :return:
        """
        # TODO: inheritance
        if disk not in (WHITE, BLACK):
            raise ValueError("Illegal move! disk should be -1 or 1")
        if self.size <= coordinate[0] or self.size <= coordinate[1]:
            raise ValueError("Illegal move! coordinate exceeds board")
        if self.board[coordinate] != 0:
            raise ValueError("Illegal move! coordinate already occupied")
        to_flip = self.to_flip(disk, coordinate)
        if len(to_flip) == 0:
            raise ValueError("Illegal move! nothing to flip")

        self.put_disk(disk, coordinate)
        self.flip(to_flip)
        self.num_of_turns += 1

    def put_disk(self, disk, coordinate):
        self.board[coordinate] = disk

    def flip(self, to_flip):
        for square in to_flip:
            self.board[square] = -self.board[square]

    def to_flip(self, disk, coordinate):
        y, x = coordinate

        to_flip_up = self.to_flip_in_line(disk, self.get_up(y, x))
        to_flip_down = self.to_flip_in_line(disk, self.get_down(y, x))
        to_flip_left = self.to_flip_in_line(disk, self.get_left(y, x))
        to_flip_right = self.to_flip_in_line(disk, self.get_right(y, x))
        to_flip_left_up = self.to_flip_in_line(disk, self.get_left_up(y, x))
        to_flip_left_down = self.to_flip_in_line(disk, self.get_left_down(y, x))
        to_flip_right_up = self.to_flip_in_line(disk, self.get_right_up(y, x))
        to_flip_right_down = self.to_flip_in_line(disk, self.get_right_down(y, x))

        to_flip = to_flip_up + to_flip_down + to_flip_left + to_flip_right + \
                  to_flip_left_up + to_flip_left_down + to_flip_right_up + to_flip_right_down
        return to_flip

    def to_flip_in_line(self, disk, line):  # line is a nparray of tuples (y,x)
        if len(line) == 0 or self.board[
            line[0]] != -disk:  # if line doesnt start with the opponent's disk
            return []
        ret = []
        for square in line:  # TODO what happens if we run out of board
            if self.board[square] == -disk:  # if there is an empty disk
                ret += [square]
            elif self.board[square] == disk:  # if there is a disk in our color at the end
                return ret
            else:  # if self.board[square] == 0: (if there is an empty disk)
                return []
        return []

    def get_up(self, y, x):
        s_up = []
        while y > 0:
            y = y - 1
            s_up += [(y, x)]
        return s_up

    def get_down(self, y, x):
        s_down = []
        while y < self.size - 1:
            y = y + 1
            s_down += [(y, x)]
        return s_down

    def get_left(self, y, x):
        s_left = []
        while x > 0:
            x = x - 1
            s_left += [(y, x)]
        return s_left

    def get_right(self, y, x):
        s_right = []
        while x < self.size - 1:
            x = x + 1
            s_right += [(y, x)]
        return s_right

    def get_right_down(self, y, x):
        s_right_down = []
        while x < self.size - 1 and y < self.size - 1:
            x = x + 1
            y = y + 1
            s_right_down += [(y, x)]
        return s_right_down

    def get_right_up(self, y, x):
        s_right_up = []
        temp_x, temp_y = x, y
        while temp_x < self.size - 1 and temp_y > 0:
            temp_x = temp_x + 1
            temp_y = temp_y - 1
            s_right_up += [(temp_y, temp_x)]
        return s_right_up

    def get_left_down(self, y, x):
        s_left_down = []
        while x > 0 and y < self.size - 1:
            x = x - 1
            y = y + 1
            s_left_down += [(y, x)]
        return s_left_down

    def get_left_up(self, y, x):
        s_left_up = []
        while x > 0 and y > 0:
            x = x - 1
            y = y - 1
            s_left_up += [(y, x)]
        return s_left_up

    def get_legal_moves(self, disk):
        legal_moves = []
        for row in range(self.size):
            for column in range(self.size):
                square = (row, column)
                if self.board[square] == 0 and not self.to_flip(disk, square) == []:
                    legal_moves.append(square)
        return legal_moves

    def get_number_of_turns(self):
        return np.count_nonzero(self.board)

    def is_board_full(self):
        return self.get_number_of_turns() == self.size ** 2

    def get_black_number(self):
        number_of_blacks = 0
        for row in self.board:
            for piece in row:
                if piece == BLACK:
                    number_of_blacks += 1
        return number_of_blacks

    def get_white_number(self):
        number_of_whites = 0
        for row in self.board:
            for piece in row:
                if piece == WHITE:
                    number_of_whites += 1
        return number_of_whites

    def get_color_disk_num(self, disk):
        """
        A function that gets a disk and returns the number of disks of the same color on the board
        :param disk: the color of the disk we are interested in
        :return: the number of disks of the same color on the board
        :error: if the disk parameter is not a valid color
        """
        if disk == WHITE:
            return self.get_white_number()

        elif disk == BLACK:
            return self.get_black_number()
        else:
            raise ValueError("not a valid disk color")

    def get_winner_disk(self):
        """
        a function that returns the winner of the game. If the is not finished then an error is
        raised
        :return: the color of the winner
        """
        if self.is_board_full():
            if self.get_black_number() > self.get_white_number():
                return BLACK
            else:
                return WHITE
        else:
            raise ValueError("the game is not finished yet!")

    def play_game(self, p1, p2):
        """
        A function that plays a game between two heuristics
        :param p1: player number 1 (the first to play)
        :param p2: player number 2 (the second to play)
        :return: the winning player and the grades of each heuristic in the game
        """
        players = (p1, p2)
        p1.set_disk(FIRST_COLOR)
        p2.set_disk(SECOND_COLOR)
        if p1.get_disk() == p2.get_disk():
            raise ValueError("two players can't have the same color")
        turn = 0
        while not self.is_board_full():
            disk = players[turn % 2].get_disk()
            heuristic = players[turn % 2].get_heuristic()
            op = Minimax.minimax(self, DEPTH, DEPTH, heuristic, True, disk, None)[1]
            self.do_move(disk, op)
            turn += 1
        # finished playing the game - now getting the winner
        """
        maybe add here somehow to get a value of winning and not just a winner - when the module is 
        more advanced! 
        """
        if self.get_winner_disk() == players[0].get_disk():
            return players[0]
        elif self.get_winner_disk() == players[1].get_disk():
            return players[1]
        else:
            raise ValueError("something went wrong! check your code!")

    def reset_game(self):
        # empty cell: 0
        # AI (black): 1
        # Player (white): -1
        self.board = np.zeros((self.size, self.size)).astype(int)
        self.board[(3, 4)] = BLACK  # maybe need to make player class and then player.number
        self.board[(4, 3)] = BLACK
        self.board[(3, 3)] = WHITE
        self.board[(4, 4)] = WHITE
        self.num_of_turns = 0
        # board is shown transposed: coordinate = (y,x)


if __name__ == '__main__':
    game = Game()
    '''
    board = np.array([[0, 0, 0, 0, 0, -1, 0, 0],
                      [0, 0, 0, 0, 1, -1, 0, 0],
                      [1, 0, 1, -1, 1, -1, 0, 0],
                      [1, 1, -1, -1, 1, -1, 0, 0],
                      [1, 1, -1, -1, 1, -1, 0, 0],
                      [0, -1, 1, -1, 0, -1, -1, 0],
                      [0, 0, 1, 1, 1, 0, 1, 0],
                      [0, 1, 0, 0, 0, -1, 0, 0]]).astype(int)
    game.set_board(board)
    print("legal moves -1 (WHITE)", game.get_legal_moves(-1))
    print(game.board)
    '''
    while game.get_number_of_turns() < 64:
        if game.get_legal_moves(-1) == [] and game.get_legal_moves(1) == []:
            break
        if not game.get_legal_moves(1) == []:
            print("###########")
            print("# Turn", "%02d" % game.get_number_of_turns(), "#")
            print("###########")
            print(game.board)
            print("black: ", game.get_black_number(), "white: ", game.get_white_number())
            print("legal moves 1 (BLACK)", game.get_legal_moves(1))
            move = random.choice(game.get_legal_moves(1))
            game.do_move(1, move)
        if not game.get_legal_moves(-1) == []:
            print("###########")
            print("# Turn", "%02d" % game.get_number_of_turns(), "#")
            print("###########")
            print(game.board)
            print("black: ", game.get_black_number(), "white: ", game.get_white_number())
            print("legal moves -1 (WHITE)", game.get_legal_moves(-1))
            move = random.choice(game.get_legal_moves(-1))
            game.do_move(-1, move)
    print("###########")
    print("# Turn", "%02d" % game.get_number_of_turns(), "#")
    print("###########")
    print(game.board)
