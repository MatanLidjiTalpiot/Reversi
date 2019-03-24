import ImageProcessing
import move_detaction
import numpy as np


def what_happend(board):
    num_of_circle = np.count_nonzero(board)
    move_detaction.continue_when_it_is_our_turn(num_of_circle)
    return ImageProcessing.return_board()