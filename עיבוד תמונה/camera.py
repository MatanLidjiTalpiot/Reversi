import cv2, time
import timeit
#initilize  the process
# create a video object
cam = cv2.VideoCapture(0)
if __name__ == '__main__':
    while True:
        # one turn
        # take a picture
        check, frame = cam.read()
        # frame = cv2.cut_by_lines(Picture)imread('WIN_20181129_13_33_33_Pro.jpg')


        #cut the picture
        red_dots = find_red_dots(frame)
        up_part = cut_to_the_up_part(frame)
        if not is_the_up_part_clean(frame):
            continue

        ## if there is nothing in side the board we go to analyse it
        #cut the board
        board = cut_to_the_board(frame)
        squares_table = cut_by_lines(board)
        #crate the table of that represents the board
        board_table = [[]*8]*8
        #fill the table with information
        for x in range(8):
            for y in range(8):
                if how_many_circles_in_it(board_table[x][y]) == 2:
                    board_table[x][y]find_circle_color(square)

        #returning the table
        print(board_table)
        break


def find_red_dots(frame):
    return
def cut_to_the_up_part(frame):
    return
def is_the_up_part_clean(frame):
    return
def cut_by_lines(Picture):
    return
def find_junction(frame):
    return
def how_many_circles_in_it(Picture):
    return
def find_circle_color(picture):
    return