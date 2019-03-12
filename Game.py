import numpy as np

DEPTH = 1  # for the meanwhile - the searching depth in the heuristic
BLACK = 1
WHITE = -1
FIRST_COLOR = WHITE
SECOND_COLOR = BLACK


# WHITE = -BLACK

class Game:
    def __init__(self, player1, player2, size=8):
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
        self.number_of_turns_attempted = 0
        player1.set_disk(FIRST_COLOR) #todo if works good! else remove
        player2.set_disk(SECOND_COLOR) #todo if works good! else remove

        try:
            if player1.get_disk() == player2.get_disk():
                raise ValueError("both players have the same color")
            if player1.get_disk() != WHITE and player1.get_disk() != BLACK:
                raise ValueError("not a valid color for " + player1.name)
            if player2.get_disk() != WHITE and player2.get_disk() != BLACK:
                raise ValueError("not a valid color for " + player2.name)
        except Exception as e:
            print("problem with colors")
            print(str(e))
            print("initializing: " + player1.name + " is white, " + player2.name +
                  " is black")
            player1.set_disk(FIRST_COLOR)
            player2.set_disk(SECOND_COLOR)

        self.player1 = player1
        self.player2 = player2
        if player1.get_disk() == FIRST_COLOR:
            self.players = (self.player1, self.player2)
        else:
            self.players = (self.player2, self.player1)

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

        if disk not in (WHITE, BLACK):
            raise ValueError("Illegal move! disk should be -1 or 1")
        if self.size <= coordinate[0] or self.size <= coordinate[1]:
            raise ValueError("Illegal move! coordinate exceeds board")
        if self.board[coordinate] != 0:
            print(coordinate)
            input()
            raise ValueError("Illegal move! coordinate already occupied")
        to_flip = self.to_flip(disk, coordinate)
        if len(to_flip) == 0:
            print(coordinate)
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

        to_flip = to_flip_up + to_flip_down + to_flip_left + to_flip_right + to_flip_left_up + to_flip_left_down + to_flip_right_up + to_flip_right_down
        return to_flip

    def to_flip_in_line(self, disk, line):  # line is a nparray of tuples (y,x)
        if len(line) == 0 or self.board[line[0]] != -disk:  # if line doesnt start with the opponent's disk
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

    def get_color_disk_num(self, player):
        """
        A function that gets a disk and returns the number of disks of the same color on the board
        :param player: the player that  we are interested in
        :return: the number of disks of the same color on the board
        :error: if the disk parameter is not a valid color
        """

        disk = player.get_disk()
        if disk == WHITE:
            return self.get_white_number()

        elif disk == BLACK:
            return self.get_black_number()
        else:
            raise ValueError("not a valid disk color")

    def get_opponent_disk_num(self, player):
        """
        A function that gets a disk color and returns the number of disks the opponents has on
        the board
        :param player: the player that we are interested in
        :return: the number of the opponent disks on the board
        """
        disk = -player.get_disk()
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
        if self.is_board_full() or (self.get_legal_moves(BLACK) == [] and self.get_legal_moves(WHITE) == []):
            if self.get_black_number() > self.get_white_number():
                return BLACK
            elif self.get_black_number() == self.get_white_number():
                return None  # todo find something more informative then None
            else:
                return WHITE

        else:
            raise ValueError("the game is not finished yet!")

    def get_current_player(self):
        return self.players[self.number_of_turns_attempted % 2]

    def play_game(self, to_print=False):
        """
        A function that plays the
        :param p1: player number 1 (the first to play)
        :param p2: player number 2 (the second to play)
        :return: the winning player and the grades of each player in the game
        """
        p1 = self.players[0]
        p2 = self.players[1]
        if p1.get_disk() == p2.get_disk():
            raise ValueError("two players can't have the same color")

        self.number_of_turns_attempted = 0
        while not self.is_board_full():
            op = self.players[self.number_of_turns_attempted % 2].choose_move(self)

            if op[1] is None:
                if self.players[(self.number_of_turns_attempted + 1) % 2].choose_move(self)[1] is \
                        None:
                    break
            else:
                self.do_move(self.players[self.number_of_turns_attempted % 2].get_disk(), op[1])

            if to_print:
                print("player, ", self.players[self.number_of_turns_attempted % 2].name,
                      " played ", op[1])
                #fprint(self.board)
            self.number_of_turns_attempted += 1

        """
        maybe add here somehow to get a value of winning and not just a winner - when the module is 
        more advanced! 
        """
        if self.get_winner_disk() == self.players[0].get_disk():
            self.players[0].number_of_wins += 1
            return self.players[0]
        elif self.get_winner_disk() == self.players[1].get_disk():
            self.players[1].number_of_wins += 1
            return self.players[1]
        else:
            return self.players[0] #todo remember that this state is a tie
    def reset_game(self, player1, player2):
        # empty cell: 0
        # AI (black): 1
        # Player (white): -1
        self.board = np.zeros((self.size, self.size)).astype(int)
        self.board[(3, 4)] = BLACK  # maybe need to make player class and then player.number
        self.board[(4, 3)] = BLACK
        self.board[(3, 3)] = WHITE
        self.board[(4, 4)] = WHITE
        self.num_of_turns = 0
        self.number_of_turns_attempted = 0
        player1.set_disk(FIRST_COLOR) #todo if works good! else remove
        player2.set_disk(SECOND_COLOR) #todo if works good! else remove
        try:
            if player1.get_disk() == player2.get_disk():
                raise ValueError("both players have the same color")
            if player1.get_disk() != WHITE and player1.get_disk() != BLACK:
                raise ValueError("not a valid color for " + player1.name)
            if player2.get_disk() != WHITE and player2.get_disk() != BLACK:
                raise ValueError("not a valid color for " + player2.name)
        except Exception as e:
            print("problem with colors")
            print(str(e))
            print("initializing: " + player1.name + " is black, " + player2.name +
                  " is white")
            player1.set_disk(FIRST_COLOR)
            player2.set_disk(SECOND_COLOR)

        self.player1 = player1
        self.player2 = player2
        if player1.get_disk() == FIRST_COLOR:
            self.players = (self.player1, self.player2)
        else:
            self.players = (self.player2, self.player1)
            # board is shown transposed: coordinate = (y,x)

    def get_num_of_corners(self, player):
        """
        A function that returns the number of corners of a specific disk
        :param player: the player we are interested to know how many corners he has
        :return: the number of corners if the color of the disk
        """
        disk = player.get_disk()
        num_of_corners = 0
        if self.board[0][0] == disk:
            num_of_corners += 1
        if self.board[0][self.size - 1] == disk:
            num_of_corners += 1
        if self.board[self.size - 1][self.size - 1] == disk:
            num_of_corners += 1
        if self.board[self.size - 1][0] == disk:
            num_of_corners += 1
        return num_of_corners

    def get_opponent_num_of_corners(self, player):
        """

        :param player: the player we are interested in getting his opponents number of concurred corners
        :return: the number of corners the players opponent holds
        """
        disk = -player.get_disk()
        num_of_corners = 0
        if self.board[0][0] == disk:
            num_of_corners += 1
        if self.board[0][self.size - 1] == disk:
            num_of_corners += 1
        if self.board[self.size - 1][self.size - 1] == disk:
            num_of_corners += 1
        if self.board[self.size - 1][0] == disk:
            num_of_corners += 1
        return num_of_corners

    def get_num_of_sides(self, player):
        """
        A function that find how many places on the side of the board the inputed player has
        :param player: the player we are interested to know how many places on the sides of the board he has
        :return: the number of places on the side of the board the player mentioned has
        """
        disk = player.get_disk()
        num_of_sides = 0
        for spot in self.board[0]:
            if spot == disk:
                num_of_sides += 1
        for spot in self.board:
            if spot[0] == disk:
                num_of_sides += 1
        for spot in self.board[self.size - 1]:
            if spot == disk:
                num_of_sides += 1
        for spot in self.board:
            if spot[self.size - 1] == disk:
                num_of_sides += 1
        num_of_sides -= self.get_num_of_corners(player)

        return num_of_sides

    def get_opponent_num_of_sides(self, player):
        """

        :param player: the player we are interested in getting his opponents number of disks on the side of the board
        :return: the player we are intersted to know about his opponent
        """
        disk = -player.get_disk()
        num_of_sides = 0
        for spot in self.board[0]:
            if spot == disk:
                num_of_sides += 1
        for spot in self.board:
            if spot[0] == disk:
                num_of_sides += 1
        for spot in self.board[self.size - 1]:
            if spot == disk:
                num_of_sides += 1
        for spot in self.board:
            if spot[self.size - 1] == disk:
                num_of_sides += 1
        num_of_sides -= self.get_num_of_corners(player)
        return num_of_sides

    def get_num_of_options_for_other(self, player):
        """
        A function that find how many options the other player has
        :param player: the player that we want to know about his opponent
        :return: the number of options the opponent of the player we inputted has
        """
        disk = player.get_disk()
        num = len(self.get_legal_moves(-disk))
        return num

    def is_winner_score(self, player):
        """
        A function that determines wheter the player won and by how much
        :param player: the player we are interested to know if he won
        :return: a number that is proportional to the number of disks he has if he wins and that is proportional to the nube rof disks that the opponent has if he loses.
        """
        disk = player.get_disk()

        try:
            if disk == self.get_winner_disk():
                return self.get_color_disk_num(disk)
            elif disk == -1 * self.get_winner_disk():
                return -1 * self.get_opponent_disk_num(disk)
        except:
            return 0

    def __hash__(self):
        hash_val = hash(tuple(map(tuple,self.board)))
        return hash_val


