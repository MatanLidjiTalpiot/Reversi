import cv2
import rotate
import numpy as np
import matplotlib.pyplot as plt

BORD_SIZE = (8, 8)
SHOW_IMAGES = False


# black = 0
# red = 50
# empty = 100

def get_square(four_points, colord_pic):
    return rotate.four_point_transform(colord_pic, rotate.order_points(four_points))


def create_board_table(row_num, col_num):
    table = []
    for i in range(row_num):
        sub = []
        for i in range(col_num):
            sub.append(0)
        table.append(sub)
    return table


def avarage_of_squar(square_pic):
    size = square_pic.shape
    color = np.array([0, 0, 0])
    area = size[0] * size[1]
    for i in range(size[0]):
        for j in range(size[1]):
            color = color + np.array(square_pic[i][j])

    return np.array([color[0] / area, color[1] / area, color[2] / area])


def cut_edges(img, crop_ratio):
    """
    cut a precent of the edges of the picture and return the center part
    :param img: the picture
    :param crop_ratio: the ratio to crop from each size up to 0.5!!!
    :return:
    """
    sh = img.shape
    if len(sh) == 3:  # colord picture
        h, w, chanels = img.shape
    if len(sh) == 2:  # gray scale picture
        h, w = img.shape
    top_y = int(h * crop_ratio)
    bot_y = h - top_y
    top_x = int(w * crop_ratio)
    bot_x = w - top_x
    crop_img = img[top_y:bot_y, top_x:bot_x]
    return crop_img


def cut_board(colord_pic):
    table = create_board_table(BORD_SIZE[0], BORD_SIZE[1])
    pic_shape = colord_pic.shape
    # print(pic_shape)
    # print(pic_shape[0])
    # print(pic_shape[1])
    square = (pic_shape[0] / BORD_SIZE[0], pic_shape[1] / BORD_SIZE[1])
    for j in range(BORD_SIZE[0]):
        for i in range(BORD_SIZE[1]):
            points = [(i * square[1], j * square[0]),
                      (i * square[1], (j + 1) * square[0]),
                      ((i + 1) * square[1], j * square[0]),
                      ((i + 1) * square[1], (j + 1) * square[0])
                      ]
            square_pic = get_square(points, colord_pic)
            table[j][i] = square_pic
    return table


def send_to_palti(cutBoard, crop_ratio):
    to_palti = create_board_table(BORD_SIZE[0], BORD_SIZE[1])
    for i in range(BORD_SIZE[0]):
        for j in range(BORD_SIZE[1]):
            if j >= 5:  # black
                square_color = 0
            elif j >= 3:  # red
                square_color = 50
            else:  # empty
                square_color = 100
            cutBoard[i][j] = cv2.cvtColor(cutBoard[i][j], cv2.COLOR_RGB2HSV)
            to_palti[i][j] = np.append(avarage_of_squar(cut_edges(cutBoard[i][j], crop_ratio)), square_color)
            # print(to_palti[i][j])
            if SHOW_IMAGES:
                # cv2.imshow(str(i)+str(j),cutBoard[i][j])
                # cv2.waitKey(0)
                cv2.imshow("croped", cut_edges(cutBoard[i][j], crop_ratio))
                cv2.waitKey(0)
    return to_palti


def draw_destributions(images):
    for i in range(BORD_SIZE[0]):
        for j in range(BORD_SIZE[1]):
            img = cut_edges(images[i][j], 0.2)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            color = ('b', 'g', 'r')
            for k, col in enumerate(color):
                plt.subplot(8, 8, i * 8 + j + 1)
                if j >= 5:  # black
                    plt.title("black")
                elif j >= 3:  # red
                    plt.title("red")
                else:  # empty
                    plt.title("empty")
                histr = cv2.calcHist([img], [k], None, [256], [0, 256])
                plt.plot(histr, color=col)
                plt.xlim([0, 256])
    plt.show()


def take_picure_and_crop(cam):
    while True:
        oper1 = input("take pic??")
        if oper1 == "y":
            rval, frame = cam.read()
            cv2.imwrite('temp_pic.jpg', frame)
            gray = cv2.imread('temp_pic.jpg', 0)
            color = cv2.imread('temp_pic.jpg')
            # rotate.show_image(frame)
            basic_crop_ratio = float(input("enter crop ratio"))
            gray = cut_edges(gray, basic_crop_ratio)
            color = cut_edges(color, basic_crop_ratio)
            pic = rotate.cut_picture1(gray, color)
            # rotate.show_image(pic)
            oper2 = input("save?")
            if oper2 == "y":
                file_name = input("ente_file_name")
                cv2.imwrite(file_name, frame)
                return file_name
        elif oper1 == "n":
            return


def try_cropping_squares(img):
    while True:
        crop_ratio_squares = float(input("enter crop ratio"))
        if crop_ratio_squares != "0":
            color_avg_array = send_to_palti(board, crop_ratio_squares)
            blue_avg = np.array([])
            green_avg = np.array([])
            red_avg = np.array([])
            square_color = np.array([])
            # print(BORD_SIZE[0], BORD_SIZE[1])
            for i in range(BORD_SIZE[0]):
                for j in range(BORD_SIZE[1]):
                    # print(color_avg_array[i][j])
                    blue_avg = np.append(blue_avg, color_avg_array[i][j][0])
                    green_avg = np.append(green_avg, color_avg_array[i][j][1])
                    red_avg = np.append(red_avg, color_avg_array[i][j][2])
                    square_color = np.append(square_color, color_avg_array[i][j][3])
            plt.scatter(red_avg, blue_avg, c=square_color)
            plt.xlabel("V")
            plt.ylabel("H")
            plt.title("green red scatter")
            plt.colorbar()
            plt.show()
        else:
            return


def stram_pictur(cam):
    while True:
        rval, frame = cam.read()
        cv2.imshow("image", frame)
        cv2.waitKey(1)


def extract_board(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    color = img
    pic = rotate.cut_picture1(gray, color)
    if SHOW_IMAGES:
        rotate.show_image(pic)
    board = cut_board(pic)
    # rotate.show_image(pic)
    new_board = []
    for i in range(BORD_SIZE[0]):
        row = np.array([])
        for j in range(BORD_SIZE[1]):
            croped = cut_edges(board[i][j], 0.1)
            row = np.append(row, deside_what_is_in_the_square(croped))
        new_board.append(row)
        # print(row)
    new_board = np.array(new_board)
    # print(new_board)
    return new_board


RED = -1
BLACK = 1
EMPTY = 0


def deside_what_is_in_the_square(square_img):
    hsv = cv2.cvtColor(square_img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([2, 0, 70])
    upper_red = np.array([34, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    res_red = cv2.bitwise_and(square_img, square_img, mask=mask_red)

    red_pixels = cv2.countNonZero(mask_red)
    if red_pixels > 50:
        return RED

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 65])

    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    black_pixels = cv2.countNonZero(mask_black)
    # print("black pixels: " + str(black_pixels))
    if black_pixels > 60:
        return BLACK
    return EMPTY


if __name__ == '__main__':
    # cam = cv2.VideoCapture(0)
    # print('ready')
    # wait = True
    # while wait:
    #     # rval, frame = cam.read()
    #     # cv2.imwrite('board1.jpg', frame)
    #     gray = cv2.imread('board1.jpg',0)
    #     color = cv2.imread('board1.jpg')
    #     rotate.show_image(color)
    #     # cv2.imshow("image", frame)
    #     # cv2.waitKey(1)
    #     print(color.shape)
    #     basic_crop_ratio = 0.1
    #     gray = cut_edges(gray, basic_crop_ratio)
    #     color = cut_edges(color, basic_crop_ratio)
    #     if SHOW_IMAGES:
    #         cv2.imshow("croped", color)
    #         cv2.waitKey(0)
    #     pic = rotate.cut_picture1(gray, color)
    #     # pic = cv2.imread("cutt.jpg")
    #     cv2.imwrite("new_cutt.jpg", pic)
    #     rotate.show_image(pic)
    #     blabla = input("wait?")
    #     basic_crop_ratio = float(blabla)
    #     if blabla == '0':
    #         wait = False
    flag = True
    while flag:
        # file_name = take_picure_and_crop(cam)
        file_name = "board1.jpg"
        if file_name is not None:
            gray = cv2.imread('board1.jpg', 0)
            color = cv2.imread('board1.jpg')
        extract_board(color)
        pic = rotate.cut_picture1(gray, color)
        board = cut_board(pic)
        # print(type(board[0]))
        # for i in board:
        #     for j in i:
        #         rotate.show_image(j)
        try_cropping_squares(board)
        draw_destributions(board)
        oper3 = input("go back to taking images?")
        # if oper3 == "n":
        # flag = False

    # # plt.scatter(blue_avg, red_avg,c=square_color)
    # # plt.xlabel("blue")
    # # plt.ylabel("red")
    # # plt.title("blue red scatter")
    # # plt.show()
    # plt.scatter(green_avg, red_avg,c=square_color)
    # plt.xlabel("green")
    # plt.ylabel("red")
    # plt.title("green red scatter")
    # plt.colorbar()
    # plt.show()
    # # plt.scatter(blue_avg, green_avg,c=square_color)
    # # plt.xlabel("blue")
    # # plt.ylabel("green")
    # # plt.title("green blue scatter")
    # # plt.show()
