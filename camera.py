import cv2, time
import timeit
import numpy as np
import func_name as func

# initilize  the process

avarages_constant = 10


def return_board():
    # crate the coard matrix
    s_board = np.zeros((8,8))

    # run avarages_constant times picture analasys
    for i in range(avarages_constant):
        img = func.take_pic()
        colored_pic = func.take_color_pic()
        img = func.cutPicture(img)
        colored_pic = func.cutPicture(colored_pic)
        board = func.get_board(img, colored_pic)
        board1 = np.array(board)
        s_board += board1

    # avarges on the avarages_constant boards
    s_board = (1 / avarages_constant) * s_board

    # make every object in the board an int
    s_board = round(s_board)
    s_board.astype(int)
    return s_board


func.cam = func.initialCamera()
while True:
    key = input('press \'b\' in order to get the board matrix \nto change the avarage constant press \'a\'\n')
    if key == 'b':
        t0 = time.time()
        p = return_board()
        t1 = time.time()
        print(p, '\n', 'the time it took is ', t1 - t0)
    if key == 'a':
        avarages_constant = int(input('choose avarge constant \n'))
    if key == 'e':
        break
