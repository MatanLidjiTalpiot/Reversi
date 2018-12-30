import time
import timeit
import numpy as np
import func_name as func

# initilize  the process

global avarages_constant
avarages_constant = 10


def return_board():
    # crate the coard matrix
    s_bord = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

    # run avarages_constant times picture analasys
    for i in range(avarages_constant):
        img = func.take_pic()
        colored_pic = func.take_color_pic()
        img = func.cutPicture(img)
        colored_pic = func.cutPicture(colored_pic)
        board = func.get_board(img, colored_pic)
        board1 = np.array(board)
        s_bord += board1

    # avarges on the avarages_constant boards
    s_bord = (1 / avarages_constant) * s_bord

    # make every object in the board an int
    for i in range(8):
        for j in range(8):
            if s_bord[i][j] > 0.5:
                s_bord[i][j] = int(1)
            elif s_bord[i][j] < - 0.5:
                s_bord[i][j] = int(-1)
            else:
                s_bord[i][j] = int(0)
    return s_bord


#
func.cam = func.initialCamera()

if __name__ == '__main__':
    while True:
        key = input(
            'press \'b\' in order to get the board matrix \nto change the avarage constant press \'a\'\n')
        if key == 'b':
            t0 = time.time()
            p = return_board()
            t1 = time.time()
            print(p, '\n', 'the time it took is ', t1 - t0)
        if key == 'a':
            avarages_constant = int(input('choose avarge constant \n'))
        if key == 'e':
            break
