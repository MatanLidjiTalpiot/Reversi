import numpy as np
import random
BLACK = 1
WHITE = -1

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
        :param coordinate: the [y,x] coordinate to place the disk
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
        x,y = coordinate # todo let ריפשטיין know that i changed that from y,x = coordinate

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
        if len(line) == 0 or self.board[line[0]] != -disk:  # if line doesnt start with the opponent's disk
            return []
        ret = []
        for square in line:# TODO what happens if we run out of board
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

    def get_legal_moves(self, disk):
        """
        A method that returns a list with all the valid moves
        :param disk: the color of the disk to place
        :return: a list of all the valid coordinates to place the disk
        """
        legal_moves = []
        coordinate = [-1, -1]
        for row in self.board:
            coordinate[1] = 0
            coordinate[0] += 1
            for piece in row:
                if piece == -disk:
                    neighbor_moves = self.get_valid_neighbors_assingments(
                        [coordinate[1], coordinate[0]]
                        , disk)
                    if neighbor_moves != []:
                        for move in neighbor_moves:
                            if move not in legal_moves:
                                legal_moves.append(move)


                coordinate[1] += 1
        return legal_moves

    def get_valid_neighbors_assingments(self, coordinate, disk):
        """
        A method that gets a cooridnate (x,y) and returns true if it is
        legal to put a disk there
        :param coordinate:
        :param disk:
        :return:
        """
        valid_moves = []

        if coordinate[0] != 0:#checking right line
            check = (coordinate[0]-1, coordinate[1])
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_right(check[1],
                                                         check[0])) != []:
                valid_moves.append(check)

        if coordinate[0] != 7: #checking left line
            check = (coordinate[0] + 1, coordinate[1])
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_left(check[1],check[0]))\
                    != []:
                    valid_moves.append(check)

        if coordinate[1] != 0: #checking down line
            check = (coordinate[0], coordinate[1] - 1)
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_down(check[1], check[0]))\
                    != []:
                valid_moves.append(check)

        if coordinate[1] != 7: #checking up line
            check = (coordinate[0], coordinate[1] + 1)
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_up(check[1], check[0])) \
                    != []:
                valid_moves.append(check)

        if coordinate[0] != 0 and coordinate[1] != 7: #checking the up
    # right line
            check = (coordinate[0] - 1, coordinate[1] + 1)

            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_right_up(check[1],
                                                            check[0])) != []:
                valid_moves.append(check)
        if coordinate[0] != 7 and coordinate[1] != 7:
        #checking the up left line
            check = (coordinate[0] + 1, coordinate[1] + 1)
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_left_up(check[1],
                                                           check[0])) != []:
                valid_moves.append(check)

        if coordinate[0] != 0 and coordinate[1] != 0: #checking the down
    # right line
            check = (coordinate[0] - 1, coordinate[1] - 1)
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_right_down(check[1],
                                                              check[0])) != []:
                valid_moves.append(check)

        if coordinate[0] != 7 and coordinate[1] != 0: #checking the down
    # left line
            check = (coordinate[0] + 1, coordinate[1] - 1)
            if self.board[check[0], check[1]] != 0:
                pass
            elif self.to_flip_in_line(disk, self.get_left_down(check[1],
                                                             check[0])) != []:
                valid_moves.append(check)

        return valid_moves

    def is_board_full(self):
        return self.num_of_turns == 60


game = Game()
# print(game.board)
# print("##########")
# game.do_move(1, (5, 4))
# print(game.board)
# game.do_move(-1, (5, 5))
# print("##########")
# print(game.board)
# game.do_move(1, (6, 6))  # should throw an error
# print("##########")
# print(game.board)
# game.do_move(1, (5, 6))
# print("##########")
# print(game.board)
# game.do_move(-1, (6, 6))
# print("##########")
# print(game.board)
# game.do_move(-1, (5, 3))
# print(game.get_legal_moves(1))
# print("##########")
black = 0
white = 0
while(black + white < 64):
    if game.get_legal_moves(-1) == [] and game.get_legal_moves(1) == []:
        break
    if game.get_legal_moves(1) != []:
        game.do_move(1,random.choice(game.get_legal_moves(1)))
    #print (game.board)
    #print(game.get_legal_moves(-1))
    #print("##########")
    if game.get_legal_moves(-1) != []:
       game.do_move(-1, random.choice(game.get_legal_moves(-1)))


    #print(game.board)
    #print("##########")
    black = 0
    white = 0
    for j in range(8):
        for k in range(8):
            if game.board[j, k] == 1:
                black += 1
            if game.board[j, k] == -1:
                white += 1
    print("black: ", black, "white: ", white)

print(game.board)