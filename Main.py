# todo: import
import Game

def image_processing(last_board):  # last_board is only to make sure
    pass
    # return curr_board


def algorithm(curr_board):
    pass
    # return to_put_down, to_flip, next board


def take_disk():
    pass
    # return None (advance to putting down), does nothing in the MVP


def put_down(to_put_down):
    pass
    # return None (advance to flipping)


def flip(to_flip):
    pass
    # return None


if __name__ == '__main__':
    take_disk()
    last_board = image_processing(None)
    while True:
        if input("Play your turn and then write 'Done' (or just 'D')") in {"Done", "done", 'D', 'd'}:
            curr_board = image_processing(last_board)
            to_put_down, to_flip, next_board = algorithm(curr_board)
            put_down(to_put_down)
            flip(to_flip)
            take_disk()
            #
            last_board = curr_board
