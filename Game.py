import numpy as np


class Game:
    def __init__(self, size=8):
        self.size = size
        # empty cell: 0
        # AI (black): 1
        # Player (white): -1
        self.board = np.zeros((self.size, self.size))
        self.board[(3, 4)] = 1  # maybe need to make player class and then player.number
        self.board[(4, 3)] = 1
        self.board[(3, 3)] = -1
        self.board[(4, 4)] = -1
        # board is shown transposed: coordinate = (y,x)

    def set_board(self, board):
        self.board = board

    def do_move(self, disk, coordinate):
        # TODO: inheritance
        if disk not in (-1, 1):
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
        for square in line:
            if self.board[square] == disk:  # if there is a disk in our color at the end
                return ret
            ret += [square]
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


game = Game()
game.do_move(1, (5, 4))
print(game.board)
game.do_move(-1, (5, 5))
print(game.board)
game.do_move(1, (6, 6))  # should throw an error
print(game.board)
game.do_move(1, (5, 6))
print(game.board)
game.do_move(-1, (6, 6))
print(game.board)
game.do_move(-1, (5, 3))
print(game.board)
