import numpy as np
import dill

DEPTH = 1  # for the meanwhile - the searching depth in the heuristic
BLACK = 1
WHITE = -1
RED = -1
FIRST_COLOR = BLACK
SECOND_COLOR = RED


# RED = -BLACK

class Game:
    global MOVE_HELPER, LEGAL_MOVES_HELPER

    def __init__(self, player1, player2, size=8, use_move_helper=True, use_legal_moves_helper=True):
        self.size = size
        # empty cell: 0
        # AI (black): 1
        # Player (white): -1
        self.fixed_disks = np.zeros((self.size, self.size)).astype(int)
        self.board = np.zeros((self.size, self.size)).astype(int)
        self.board[(3, 4)] = BLACK  # maybe need to make player class and then player.number
        self.board[(4, 3)] = BLACK
        self.board[(3, 3)] = RED
        self.board[(4, 4)] = RED
        self.num_of_turns = 0
        self.number_of_turns_attempted = 0
        player1.set_disk(FIRST_COLOR)
        player2.set_disk(SECOND_COLOR)
        self.use_move_helper = use_move_helper
        self.use_legal_moves_helper = use_legal_moves_helper
        self.player1 = player1
        self.player2 = player2
        self.players = (self.player1, self.player2)
        self.safe_white = 0
        self.safe_black = 0
        self.white_sequences = []
        self.black_sequences = []
        if use_move_helper:
            with open('move_helper/Move_Helper.pkl', 'rb') as input:
                Game.MOVE_HELPER = dill.load(input)
                # Game.MOVE_HELPER.update()

        if use_legal_moves_helper:
            with open('legal_moves_helper/Legal_Moves_Helper.pkl', 'rb') as input:
                Game.LEGAL_MOVES_HELPER = dill.load(input)
                Game.LEGAL_MOVES_HELPER.update()
                # board is shown transposed: coordinate = (y,x)

    def set_board(self, board):
        """
        A function that sets the board
        :param board: the board to set
        :return: nothing
        """
        self.board = board

    def calculate_move(self, disk, coordinate):
        """
        assumptions: we assume that the disk and the coordinate are legal
        a function that calculates a move
        :param disk: the color of the disk that we place in this move
        :param coordinate: the coordinate that we place the disk in
        :return: the board after the placement of the disk
        """
        board = np.copy(self.board)
        to_flip = self.to_flip(disk, coordinate)
        if len(to_flip) == 0:
            print(coordinate)
            raise ValueError("Illegal move! nothing to flip")

        Game.put_disk_on_board(disk, coordinate, board)
        return Game.flip_on_board(to_flip, board)

    def do_move(self, disk, coordinate):
        """
        A function that does a move
        :param disk: 1 or -1 according to the color
        :param coordinate: the (y,x) coordinate to place the disk (has to be a tuple)
        :return:
        """

        if disk not in (RED, BLACK):
            raise ValueError("Illegal move! disk should be -1 or 1")
        if self.size <= coordinate[0] or self.size <= coordinate[1]:
            raise ValueError("Illegal move! coordinate exceeds board")
        if self.board[coordinate] != 0:
            raise ValueError("Illegal move! coordinate already occupied")

        if self.use_move_helper:
            state = Game.MOVE_HELPER.get_state(self, coordinate, disk)
            if state == []:
                board_after_move = self.calculate_move(disk, coordinate)
                Game.MOVE_HELPER.get_new_move(self, coordinate, disk, board_after_move)
                self.board = board_after_move
                self.num_of_turns += 1
            else:
                self.board = state
                self.num_of_turns += 1
        else:
            self.board = self.calculate_move(disk, coordinate)
        (self.white_sequences, self.black_sequences) = self.find_sequences()

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

    def to_flip_in_line(self, disk, line):  # line is a nparray of tuples (y,x) todo see if we can make this faster
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

    def calculate_legal_moves(self, disk):
        legal_moves = []
        for row in range(self.size):
            for column in range(self.size):
                square = (row, column)
                if self.board[square] == 0 and not self.to_flip(disk, square) == []:
                    legal_moves.append(square)
        return legal_moves

    def get_legal_moves(self, disk):
        if self.use_legal_moves_helper:
            state = Game.LEGAL_MOVES_HELPER.get_state(self, disk)
            if state == []:
                calculate_legal_moves = self.calculate_legal_moves(disk)
                Game.LEGAL_MOVES_HELPER.get_new_legal_moves(self, disk, calculate_legal_moves)
                return calculate_legal_moves
            else:
                return state
        else:
            return self.calculate_legal_moves(disk)
            # legal_moves = []
            # for row in range(self.size):
            #     for column in range(self.size):
            #         square = (row, column)
            #         if self.board[square] == 0 and not self.to_flip(disk, square) == []:
            #             legal_moves.append(square)
            # return legal_moves

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
                if piece == RED:
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
        if disk == RED:
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
        if disk == RED:
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
        if self.is_board_full() or (self.get_legal_moves(BLACK) == [] and self.get_legal_moves(RED) == []):
            if self.get_black_number() > self.get_white_number():
                return BLACK
            elif self.get_black_number() == self.get_white_number():
                return None  # todo find something more informative then None
            else:
                return RED

        else:
            raise ValueError("the game is not finished yet!")

    def get_current_player(self):
        return self.players[self.number_of_turns_attempted % 2]

    def final_board_in_game(self, to_print=False):
        """
        a function that plays the game and returns the final board of the game
        :param to_print: whether to print during the game
        :return: the final board of the game
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
            self.number_of_turns_attempted += 1
        return self.board

    def play_game(self, to_print=False):
        """
        A function that plays the
        :param p1: player number 1 (the first to play)
        :param p2: player number 2 (the second to play)
        :return: the winning player and the grades of each player in the game
        """
        self.board = self.final_board_in_game(to_print=to_print)
        if self.get_winner_disk() == self.players[0].get_disk():
            self.players[0].number_of_wins += 1
            return self.players[0]
        elif self.get_winner_disk() == self.players[1].get_disk():
            self.players[1].number_of_wins += 1
            return self.players[1]
        else:
            return self.players[0]  # todo remember that this state is a tie

    def reset_game(self, player1, player2):
        # empty cell: 0
        # AI (black): 1
        # Player (white): -1
        self.board = np.zeros((self.size, self.size)).astype(int)
        self.board[(3, 4)] = BLACK  # maybe need to make player class and then player.number
        self.board[(4, 3)] = BLACK
        self.board[(3, 3)] = RED
        self.board[(4, 4)] = RED
        self.num_of_turns = 0
        self.fixed_disks = np.zeros((self.size, self.size)).astype(int)
        self.safe_black = 0
        self.safe_white = 0
        self.number_of_turns_attempted = 0
        player1.set_disk(FIRST_COLOR)
        player2.set_disk(SECOND_COLOR)
        self.player1 = player1
        self.player2 = player2
        self.players = (self.player1, self.player2)

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
    def get_num_of_options(self, player):
        return len(self.get_legal_moves(player.disk))

    def is_winner_score(self, player):
        """
        A function that determines wheter the player won and by how much
        :param player: the player we are interested to know if he won
        :return: a number that is proportional to the number of disks he has if he wins and that is proportional to the nube rof disks that the opponent has if he loses.
        """
        disk = player.get_disk()

        try:
            if disk == self.get_winner_disk():
                # return self.get_color_disk_num(disk)
                return 1
            elif disk == -1 * self.get_winner_disk():
                # return -1 * self.get_opponent_disk_num(disk)
                return -1
        except:
            return 0

    def update_safe_number(self):
        def horizontal_check(game, color, y, x):
            """
            :param game: the game we want to check on
            :param color: the color which we are checking
            :param y: the y coordinate
            :param x: the x coordinate
            :return: if the disks with the color and the coordinate is safe in the horizontal side
            """
            if ((game.fixed_disks[y][x + 1] == color) or (game.fixed_disks[y][x - 1]) == color) \
                    or ((game.fixed_disks[y][x + 1] == -color) and (game.fixed_disks[y][x - 1] == -color)):
                return True
            else:
                return False

        def vertical_check(game, color, y, x):
            """
            :return: if the disks with the color and the coordinate is safe in the vertical side
            """
            if ((game.fixed_disks[y - 1][x] == color) or (game.fixed_disks[y + 1][x] == color)) \
                    or ((game.fixed_disks[y - 1][x] == -color) and (game.fixed_disks[y + 1][x] == -color)):
                return True
            else:
                return False

        def diagonal_check(game, color, y, x):
            """
            :return: if the disks with the color and the coordinate is safe in the first diagonal side
            """
            if ((game.fixed_disks[y + 1][x + 1] == color) or (game.fixed_disks[y - 1][x - 1] == color)
                or ((game.fixed_disks[y + 1][x + 1] == -color) and (game.fixed_disks[y - 1][x - 1] == -color))):
                return True
            else:
                return False

        def other_diagonal_check(game, color, y, x):
            """
            :return: if the disk with the color and the coordinate is safe in the other diagonal side
            """
            if ((game.fixed_disks[y + 1][x - 1] == color) or (game.fixed_disks[y - 1][x + 1] == color)
                or ((game.fixed_disks[y + 1][x - 1] == -color) and (game.fixed_disks[y - 1][x + 1] == -color))):
                return True
            else:
                return False

        def check_sequences(game, sequences, color):
            """
            a function that gets a list of sequences and checks returns the safe sequences that are in them
            """
            safe_sequences = []
            for seq in sequences:

                (first_y, first_x) = seq[0]
                (last_y, last_x) = seq[-1]
                safe = True
                if seq[1][0] - seq[0][0] == 0:
                    # direction is horizontal
                    y = first_y
                    if (first_x == 0 or game.fixed_disks[y][first_x - 1] == color or last_x == 7 or game.fixed_disks[y][last_x + 1] == color):
                        safe = True

                    elif not (game.fixed_disks[y][first_x - 1] == -color and game.fixed_disks[y][last_x + 1] == -color):
                        safe = False

                    for x in range(first_x, last_x + 1):
                        if not safe:
                            break
                        if y == 0 or y == 7:
                            break

                        if not (game.fixed_disks[y - 1][x] == color or game.fixed_disks[y + 1][x] == color or (game.fixed_disks[y - 1][x] == -color and game.fixed_disks[y + 1][x] == -color)):
                            safe = False
                        if x == 0 or x == 7:
                            pass
                        elif not (game.fixed_disks[y - 1][x - 1] == color or game.fixed_disks[y + 1][x + 1] == color or (
                                game.fixed_disks[y - 1][x - 1] == -color and game.fixed_disks[y + 1][x + 1] == -color)):
                            safe = False
                        if x == 0 or x == 7:
                            pass
                        elif not (game.fixed_disks[y + 1][x - 1] == color or game.fixed_disks[y - 1][x + 1] == color) or (
                                game.fixed_disks[y + 1][x - 1] == -color and game.fixed_disks[y - 1][x + 1] == -color):
                            safe = False

                elif seq[1][1] - seq[0][1] == 0:
                    # direction is vertical
                    x = first_x
                    # check up and down
                    if (first_y == 0 or last_y == 7 or game.fixed_disks[first_y - 1][x] == color or game.fixed_disks[last_y + 1][x] == color):
                        safe = True
                    elif not (game.fixed_disks[first_y - 1][x] == -color and game.fixed_disks[last_y + 1][x] == -color):
                        safe = False
                    for y in range(first_y, last_y + 1):
                        if x == 0 or x == 7:
                            break
                        if not (game.fixed_disks[y][x - 1] == color or game.fixed_disks[y][x + 1] == color) or (game.fixed_disks[y][x - 1] == - color and - color == game.fixed_disks[y][x + 1]):
                            safe = False
                        if y == 0 or y == 7:
                            pass
                        elif not (game.fixed_disks[y - 1][x - 1] == color or game.fixed_disks[y + 1][x + 1] == color or (
                                game.fixed_disks[y - 1][x - 1] == -color and - color == game.fixed_disks[y + 1][x + 1])):
                            safe = False
                        if y == 0 or y == 7:
                            pass
                        elif not (game.fixed_disks[y - 1][x + 1] == color or game.fixed_disks[y + 1][x - 1] or (game.fixed_disks[y - 1][x + 1] - color and -color == game.fixed_disks[y + 1][x - 1])):
                            safe = False

                elif seq[1][0] - seq[0][0] == 1:
                    # direction left_up
                    # next = (curr_y, curr_x) + (-1, 1)
                    # before = (curr_y, curr_x) - (-1,1)
                    if not (first_y == 7 or first_x == 0 or last_y == 0 or last_x == 7 or game.fixed_disks[first_y + 1][first_x - 1] == color or game.fixed_disks[last_y - 1][last_x + 1] == color
                            or (game.fixed_disks[last_y - 1][last_x + 1] == -color and - color == game.fixed_disks[first_y + 1][first_x - 1])):
                        safe = False

                    for coordinate in seq:
                        curr_x = coordinate[1]
                        curr_y = coordinate[0]
                        if not safe:
                            break
                        if curr_x == 0 or curr_x == 7:
                            pass
                        elif not (game.fixed_disks[curr_y][curr_x - 1] == color or game.fixed_disks[curr_y][curr_x + 1] == color or (
                                game.fixed_disks[curr_y][curr_x - 1] == - color and game.fixed_disks[
                            curr_y][curr_x + 1] == -color)):
                            safe = False
                        if curr_y == 0 or curr_y == 7:
                            pass
                        elif not (game.fixed_disks[curr_y - 1][curr_x] == color or game.fixed_disks[curr_y + 1][curr_x] == color or (game.fixed_disks[curr_y - 1][curr_x] == -color and - color ==
                            game.fixed_disks[curr_y + 1][curr_x])):
                            safe = False
                        if curr_y == 0 or curr_y == 7 or curr_x == 0 or curr_x == 7:
                            pass
                        elif not (game.fixed_disks[curr_y - 1][curr_x - 1] == color or game.fixed_disks[curr_y + 1][curr_x + 1] == color or (game.fixed_disks[curr_y - 1][curr_x - 1] == -color and
                                                                                                                                                     game.fixed_disks[curr_y + 1][
                                                                                                                                                             curr_x + 1] == -color)):
                            safe = False

                else:
                    # direction left_down
                    # next = (curr_y, curr_x) + (1, -1)
                    # before = (curr_y, curr_x) - (1,-1)
                    if not (first_x == 0 or last_x == 7 or first_y == 0 or last_y == 7 or game.fixed_disks[first_y - 1][first_x - 1] == color or game.fixed_disks[last_y + 1][last_x + 1] == color or (
                                    game.fixed_disks[last_y + 1][last_x + 1] == -color and game.fixed_disks[first_y - 1][first_x - 1] == -color)):
                        safe = False
                    for coordinate in seq:
                        if safe == False:
                            break
                        curr_x = coordinate[1]
                        curr_y = coordinate[0]
                        if curr_x == 0 or curr_x == 7:
                            pass
                        elif not (game.fixed_disks[curr_y][curr_x - 1] == color or game.fixed_disks[curr_y][curr_x + 1] == color or (game.fixed_disks[curr_y][curr_x - 1] == - color and - color ==
                            game.fixed_disks[curr_y][curr_x + 1])):
                            safe = False
                        if curr_y == 0 or curr_y == 7:
                            pass
                        elif not (game.fixed_disks[curr_y - 1][curr_x] == color or game.fixed_disks[curr_y + 1][curr_x] == color or (game.fixed_disks[curr_y + 1][curr_x] == -color and -color ==
                            game.fixed_disks[curr_y - 1][curr_x])):
                            safe = False
                        if curr_x == 0 or curr_x == 7 or curr_y == 0 or curr_y == 7:
                            pass
                        elif not (game.fixed_disks[curr_y + 1][curr_x - 1] == color or game.fixed_disks[curr_y - 1][curr_x + 1] == color or (
                                game.fixed_disks[curr_y - 1][curr_x + 1] == -color and -color ==
                            game.fixed_disks[curr_y + 1][curr_x - 1])):
                            safe = False

                if safe:
                    safe_sequences.append(seq)
            return safe_sequences

        # the block of code that finds the safe disks (that are not with a sequence)
        for y in range(self.size):
            for x in range(self.size):

                if self.fixed_disks[y][x] != 0:
                    continue

                color = self.board[y][x]
                if color not in (RED, BLACK):
                    continue
                counter = 0
                if (x == 0 and y == 0) or (x == 7 and y == 7) or (x == 0 and y == 7) or (y == 0 and x == 7):  # dealt with corners
                    counter += 4

                elif (x == 0) or (x == 7):
                    if vertical_check(self, color, y, x):
                        counter += 4

                elif (y == 0) or (y == 7):
                    if horizontal_check(self, color, y, x):
                        counter += 4

                else:
                    if vertical_check(self, color, y, x):
                        counter += 1
                    if horizontal_check(self, color, y, x):
                        counter += 1
                    if diagonal_check(self, color, y, x):
                        counter += 1
                    if other_diagonal_check(self, color, y, x):
                        counter += 1
                if counter >= 4:
                    self.fixed_disks[y][x] = color
        (white_sequences, black_sequences) = (self.white_sequences, self.white_sequences)

        if white_sequences != []:
            safe_white = check_sequences(self, white_sequences, RED)
            for seq in safe_white:
                for coordinate in seq:
                    self.fixed_disks[coordinate[0]][coordinate[1]] = RED
        if black_sequences != []:
            safe_black = check_sequences(self, black_sequences, BLACK)
            for seq in safe_black:
                for coordinate in seq:
                    self.fixed_disks[coordinate[0]][coordinate[1]] = BLACK
        if white_sequences != []:
            safe_white = check_sequences(self, white_sequences, RED)
            for seq in safe_white:
                for coordinate in seq:
                    self.fixed_disks[coordinate[0]][coordinate[1]] = RED
        if black_sequences != []:
            safe_black = check_sequences(self, black_sequences, BLACK)
            for seq in safe_black:
                for coordinate in seq:
                    self.fixed_disks[coordinate[0]][coordinate[1]] = BLACK

        white_counter = 0
        black_counter = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.fixed_disks[i][j] == RED:
                    white_counter += 1
                elif self.fixed_disks[i][j] == BLACK:
                    black_counter += 1

        self.safe_white = white_counter
        self.safe_black = black_counter

    def find_sequences(self):
        """
        a function that finds all the sequecnes in the board
        :param game: the game to check on
        :return: a tuple (white sequences, black sequences)
        """

        def horizontal(board, color, y, x):
            """
            a function that checks if the disk is a part of a horizontal sequence
            """
            return board[y][x - 1] == color

        def vertical(board, color, y, x):
            """
            a function that checks if a disk is a part of a vertical sequence
            """
            return board[y - 1][x] == color

        def left_up(board, color, y, x):
            """
            a function that checks if a disk is a part of a left_up sequence
            """
            return board[y + 1][x - 1] == color

        def left_down(board, color, y, x):
            """
            a function that returns if the disk is a part of a left_down sequence
            """
            return board[y - 1][x - 1] == color

        seq_list_white = []
        seq_list_black = []
        horizontal_list_white = []
        horizontal_list_black = []
        vertical_list_white = []
        vertical_list_black = []
        left_up_list_white = []
        left_up_list_black = []
        left_down_list_white = []
        left_down_list_black = []
        # going through the board and seeing checking if a spot is a part of a sequence in every direction
        for y in range(self.size):
            for x in range(self.size):
                color = self.board[y][x]
                if color not in (RED, BLACK):
                    continue

                if x != 0 and y != 0 and y != 7:

                    # checking the horizontal side of the (y,x) coordinate
                    if horizontal(self.board, color, y, x):
                        if color == RED:
                            if (y, x - 1) not in horizontal_list_white:
                                horizontal_list_white.append((y, x - 1))
                            horizontal_list_white.append((y, x))
                        else:
                            if (y, x - 1) not in horizontal_list_black:
                                horizontal_list_black.append((y, x - 1))
                            horizontal_list_black.append((y, x))

                    # checking the vertical side of the (y,x) coordinate
                    if vertical(self.board, color, y, x):
                        if color == RED:
                            if (y - 1, x) not in vertical_list_white:
                                vertical_list_white.append((y - 1, x))
                            vertical_list_white.append((y, x))
                        else:
                            if (y - 1, x) not in vertical_list_black:
                                vertical_list_black.append((y - 1, x))
                            vertical_list_black.append((y, x))

                    # checking the left_down side of the (y,x) coordinate
                    if left_down(self.board, color, y, x):
                        if color == RED:
                            if (y - 1, x - 1) not in left_down_list_white:
                                left_down_list_white.append((y - 1, x - 1))
                            left_down_list_white.append((y, x))
                        else:
                            if (y - 1, x - 1) not in left_down_list_black:
                                left_down_list_black.append((y - 1, x - 1))
                            left_down_list_black.append((y, x))

                    # checking the left_up side of the (y,x) coordinate
                    if left_up(self.board, color, y, x):
                        if color == RED:
                            if (y + 1, x - 1) not in left_up_list_white:
                                left_up_list_white.append((y + 1, x - 1))
                            left_up_list_white.append((y, x))
                        else:
                            if (y + 1, x - 1) not in left_up_list_black:
                                left_up_list_black.append((y + 1, x - 1))
                            left_up_list_black.append((y, x))

                else:
                    if (x == 0) and (y != 0):
                        # check only vertical
                        if vertical(self.board, color, y, x):
                            if color == RED:
                                if ((y - 1, x) not in vertical_list_white):
                                    vertical_list_white.append((y - 1, x))
                                vertical_list_white.append((y, x))
                            else:
                                if ((y - 1, x) not in vertical_list_black):
                                    vertical_list_black.append((y - 1, x))
                                vertical_list_black.append((y, x))

                    elif (y == 0) and (x != 0):
                        # check horizontal and left_up
                        if horizontal(self.board, color, y, x):
                            if color == RED:
                                if (y, x - 1) not in horizontal_list_white:
                                    horizontal_list_white.append((y, x - 1))
                                horizontal_list_white.append((y, x))
                            else:
                                if (y, x - 1) not in horizontal_list_black:
                                    horizontal_list_black.append((y, x - 1))
                                horizontal_list_black.append((y, x))

                        if left_up(self.board, color, y, x):
                            if color == RED:
                                if (y + 1, x - 1) not in left_up_list_white:
                                    left_up_list_white.append((y + 1, x - 1))
                                left_up_list_white.append((y, x))
                            else:
                                if (y + 1, x - 1) not in left_up_list_black:
                                    left_up_list_black.append((y + 1, x - 1))
                                left_up_list_black.append((y, x))

                    elif (y == 7) and (x != 0):
                        # check horizontal and left_down
                        if horizontal(self.board, color, y, x):
                            if color == RED:
                                if (y, x - 1) not in horizontal_list_white:
                                    horizontal_list_white.append((y, x - 1))
                                horizontal_list_white.append((y, x))
                            else:
                                if (y, x - 1) not in horizontal_list_black:
                                    horizontal_list_black.append((y, x - 1))
                                horizontal_list_black.append((y, x))

                        if left_down(self.board, color, y, x):
                            if color == RED:
                                if (y - 1, x - 1) not in left_down_list_white:
                                    left_down_list_white.append((y - 1, x - 1))
                                left_down_list_white.append((y, x))
                            else:
                                if (y - 1, x - 1) not in left_down_list_black:
                                    left_down_list_black.append((y - 1, x - 1))
                                left_down_list_black.append((y, x))

        # creating horizontal sequences white
        used_horizontal_white = []
        for place in horizontal_list_white:
            if place in used_horizontal_white:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = x_val
            end = x_val
            curr_seq.append(place)
            used_horizontal_white.append(place)
            while (beginning != 0 and (y_val, beginning - 1) in horizontal_list_white):
                beginning -= 1
                curr_seq.append((y_val, beginning))
                used_horizontal_white.append((y_val, beginning))
            while (end != 7 and (y_val, end + 1) in horizontal_list_white):
                end += 1
                curr_seq.append((y_val, end))
                used_horizontal_white.append((y_val, end))
            curr_seq.sort(key=lambda place: place[1])
            seq_list_white.append(curr_seq)

        # creating horizontal sequences black
        used_horizontal_black = []
        for place in horizontal_list_black:
            if place in used_horizontal_black:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = x_val
            end = x_val
            curr_seq.append(place)
            used_horizontal_black.append(place)
            while (beginning != 0 and (y_val, beginning - 1) in horizontal_list_black):
                beginning -= 1
                curr_seq.append((y_val, beginning))
                used_horizontal_black.append((y_val, beginning))
            while (end != 7 and (y_val, end + 1) in horizontal_list_black):
                end += 1
                curr_seq.append((y_val, end))
                used_horizontal_black.append((y_val, end))
            curr_seq.sort(key=lambda place: place[1])
            seq_list_black.append(curr_seq)

        # creating vertical sequences white
        used_vertical_white = []
        for place in vertical_list_white:
            if place in used_vertical_white:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = y_val
            end = y_val
            curr_seq.append(place)
            while (beginning != 0 and (beginning - 1, x_val) in vertical_list_white):
                beginning -= 1
                curr_seq.append((beginning, x_val))
                used_vertical_white.append((beginning, x_val))
            while (end != 7 and (end + 1, x_val) in vertical_list_white):
                end += 1
                curr_seq.append((end, x_val))
                used_vertical_white.append((end, x_val))
            curr_seq.sort(key=lambda place: place[0])
            seq_list_white.append(curr_seq)

        # creating vertical sequences black
        used_vertical_black = []
        for place in vertical_list_black:
            if place in used_vertical_black:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = y_val
            end = y_val
            curr_seq.append(place)
            while (beginning != 0 and (beginning - 1, x_val) in vertical_list_black):
                beginning -= 1
                curr_seq.append((beginning, x_val))
                used_vertical_black.append((beginning, x_val))
            while (end != 7 and (end + 1, x_val) in vertical_list_black):
                end += 1
                curr_seq.append((end, x_val))
                used_vertical_black.append((end, x_val))
            curr_seq.sort(key=lambda place: place[0])
            seq_list_black.append(curr_seq)

        # creating left_up sequences white
        used_left_up_white = []
        for place in left_up_list_white:
            if place in used_left_up_white:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = (y_val, x_val)
            end = (y_val, x_val)
            curr_seq.append(place)
            while ((beginning[0] != 7 and beginning[1] != 0) and (beginning[0] + 1, beginning[1] - 1) in left_up_list_white):
                beginning = (beginning[0] + 1, beginning[1] - 1)
                curr_seq.append(beginning)
                used_left_up_white.append(beginning)
            while ((end[0] != 0 and end[1] != 7) and ((end[0] - 1, end[1] + 1) in left_up_list_white)):
                end = (end[0] - 1, end[1] + 1)
                curr_seq.append(end)
                used_left_up_white.append(end)
            curr_seq.sort(key=lambda place: place[1])
            seq_list_white.append(curr_seq)

        # creating left_up sequences black
        used_left_up_black = []
        for place in left_up_list_black:
            if place in used_left_up_black:
                continue
            curr_seq = []
            (y_val, x_val) = place
            curr_seq.append(place)
            beginning = (y_val, x_val)
            end = (y_val, x_val)
            while ((beginning[0] != 7 and beginning[1] != 0) and (beginning[0] + 1, beginning[1] - 1) in left_up_list_black):
                beginning = (beginning[0] + 1, beginning[1] - 1)
                curr_seq.append(beginning)
                used_left_up_black.append(beginning)
            while ((end[0] != 0 and end[1] != 7) and ((end[0] - 1, end[1] + 1) in left_up_list_black)):
                end = (end[0] - 1, end[1] + 1)
                curr_seq.append(end)
                used_left_up_black.append(end)
            curr_seq.sort(key=lambda place: place[1])
            seq_list_black.append(curr_seq)

        # creating left_down sequences white
        used_left_down_white = []
        for place in left_down_list_white:
            if place in used_left_down_white:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = (y_val, x_val)
            end = (y_val, x_val)
            curr_seq.append(place)
            while (beginning[0] != 0 and beginning[1] != 0) and (beginning[0] - 1, beginning[1] - 1) in left_down_list_white:
                beginning = (beginning[0] - 1, beginning[1] - 1)
                curr_seq.append(beginning)
                used_left_down_white.append(beginning)
            while (end[0] != 7 and end[1] != 7) and (end[0] + 1, end[1] + 1) in left_down_list_white:
                end = (end[0] + 1, end[1] + 1)
                curr_seq.append(end)
                used_left_down_white.append(end)
            curr_seq.sort(key=lambda place: place[1])
            seq_list_white.append(curr_seq)

        # creating left_down sequences black
        used_left_down_black = []
        for place in left_down_list_black:
            if place in used_left_down_black:
                continue
            curr_seq = []
            (y_val, x_val) = place
            beginning = (y_val, x_val)
            end = (y_val, x_val)
            curr_seq.append(place)
            while (beginning[0] != 0 and beginning[1] != 0) and (beginning[0] - 1, beginning[1] - 1) in left_down_list_black:
                beginning = (beginning[0] - 1, beginning[1] - 1)
                curr_seq.append(beginning)
                used_left_down_black.append(beginning)
            while (end[0] != 7 and end[1] != 7) and (end[0] + 1, end[1] + 1) in left_down_list_black:
                end = (end[0] + 1, end[1] + 1)
                curr_seq.append(end)
                used_left_down_black.append(end)
            curr_seq.sort(key=lambda place: place[1])
            seq_list_black.append(curr_seq)

        return seq_list_white, seq_list_black

    def num_of_seq(self, player):
        if player.disk == WHITE:
            return len(self.white_sequences)
        else:
            return len(self.black_sequences)

    def bad_places_without_corner(self, player):
        counter = 0
        #left up corner
        if self.board[0][0] == 0 and self.board[1][1] == player.disk:
            #checking right
            for i in range(1,self.size):
                if self.board[0][i] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break
            #checking downwards
            for i in range (1,self.size):
                if self.board[i][0] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -=7
                else:
                    break
        #left down corner
        if self.board[7][0] == 0 and self.board[6][1] == player.disk:
            #checking right
            for i in range (1,self.size):
                if self.board[7][i] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break
            #checking upwards
            for i in range (1,self.size):
                if self.board[7-i][0] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break

        #right up corner
        if self.board[0][7] == 0 and self.board[1][6] == player.disk:
            #checking downwards
            for i in range (1,self.size):
                if self.board[i][7] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break
            #checking left
            for i in range(1,self.size):
                if self.board[0][7-i] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break

        #right down corner
        if self.board[7][7] == 0 and self.board[6][6] == player.disk:
            #checking left
            for i in range(1,self.size):
                if self.board[7,7-i] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break
            for i in range(1,self.size):
                #checking up
                if self.board[7-i][7] == player.disk:
                    counter += 1
                    if i == 7:
                        counter -= 7
                else:
                    break
        return counter/24

    def opponent_bad_places_without_corner(self, player):
        if player is self.player1:
            return self.bad_places_without_corner(self.player2)
        else:
            return self.bad_places_without_corner(self.player1)


    def num_of_opponent_seq(self, player):
        if player is self.player1:
            return self.num_of_seq(self.player2)
        else:
            return self.num_of_seq(self.player1)


    def get_number_of_opponent_safe_disks(self, player):
        """
        :param player: the player we want to get the number of his opponent's safe disks
        :return: the number of safe disks the player's opponent has
        """
        self.update_safe_number()
        if (player.disk) == RED:
            return self.safe_black
        else:
            return self.safe_white

    def get_number_of_safe_disks(self, player):
        """
        :param player: the player we want to get the number of safe disks he has
        :return: the number of the safe disks of the player
        """
        self.update_safe_number()
        if (player.disk == RED):
            return self.safe_white
        else:
            return self.safe_black

    def get_number_of_semi_safe_disks(self, player):
        pass

    def get_number_of_unsafe_disks(self, player):
        pass

    def next_to_untaked_corner(self,player):
        """
        a function that counts the number of cooridnates that the player has taked next to an unataken corner
        :param player: the player we are interested to know
        :return: the number said above normalized to one
        """
        counter = 0
        corner_counter = 0
        #corner1
        if self.board[0][0] == 0:
            corner_counter += 1
            if self.board[1][0] == player.disk:
                counter += 1
            if self.board[0][1] == player.disk:
                counter += 1
            if self.board[1][1] == player.disk:
                counter += 1
        # corner2
        if self.board[7][7] == 0:
            corner_counter += 1
            if self.board[7][6] == player.disk:
                counter += 1
            if self.board[6][7] == player.disk:
                counter += 1
            if self.board[6][6] == player.disk:
                counter += 1
        # corner3
        if self.board[7][0] == 0:
            corner_counter += 1
            if self.board[7][1] == player.disk:
                counter += 1
            if self.board[6][0] == player.disk:
                counter += 1
            if self.board[6][1] == player.disk:
                counter +=1
        # corner4
        if self.board[0][7] == 0:
            corner_counter += 1
            if self.board[0][6] == player.disk:
                counter += 1
            if self.board[1][7] == player.disk:
                counter += 1
            if self.board[1][6] == player.disk:
                counter += 1
        if corner_counter == 0:
            return 0
        return counter/(corner_counter*3)

    def next_to_untaken_corner_opponent(self, player):
        if player is self.player1:
            return self.next_to_untaked_corner(self.player2)
        else:
            return self.next_to_untaked_corner(self.player1)

    def get_digonal_score(self, player):
        counter = 0
        for i in range(3, self.size - 1):
            if self.board[i][i] == player.disk:
                counter += 1
            if self.board[self.size-i][i] == player.disk:
                counter += 1
        if self.board[6][1] == player.disk and self.board[7][0] != player.disk:
            counter -= 4
        if self.board[1][6] == player.disk and self.board[0][7] != player.disk:
            counter -=4
        if self.board[1][1] == player.disk and self.board[0][0] != player.disk:
            counter -= 8
        if self.board[6][6] == player.disk and self.board[7][7] != player.disk:
            counter -= 8

        return counter/8
    def get_opponent_diagonal_score(self, player):
        if player is self.player1:
            return self.get_digonal_score(self.player2)
        else:
            return self.get_digonal_score(self.player1)



    @staticmethod
    def load_move_helper():
        with open('move_helper/Move_Helper.pkl', 'rb') as input:
            r_obj = dill.load(input)
            input.close()
            return r_obj

    @staticmethod
    def load_legal_moves_helper():
        with open('legal_moves_helper/Legal_Moves_Helper.pkl', 'rb') as input:
            r_obj = dill.load(input)
            input.close()
            return r_obj

    @staticmethod
    def put_disk_on_board(disk, coordinate, board):
        board[coordinate] = disk
        return board

    @staticmethod
    def flip_on_board(to_flip, board):
        for square in to_flip:
            board[square] = -board[square]
        return board
