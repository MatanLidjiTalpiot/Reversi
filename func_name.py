import cv2
import numpy as np
import math
import time
from MyCamera import MyCamera

# variables

# circles variables
r = 8  # min radius of disc
R = 11  # max radius of disc
circles_param = 1.5  # the bigger this parameter the more circles it would find
up_th = 80  # thrash hold to check if a circle is black enough
down_th = 0  # not relevant any more leav it zero
red_color_majority = 50 # when checking if a circle is red its red value must be bigger then the others


# images
# img2 = cv2.imread("data1175.jpg", 0)
lines_param = 200 # the smaller it is the more lines it finds
angle_param = np.pi / 720 # the resolution of the angle searching
max_rho = 280 # biggest distance of line from the origin
min_rho = 0 # smallest distance of line from the origin
y_angle = np.pi / 2 # the angle of the y lines (red lines)
y_thrash_hold = 0.4 # the thrash hold for the y lines
x_angle = 0.0 # the angle of the y lines (green lines)
x_thrash_hold = 0.5 # the thrash hold for the x lines
min_d_rho = 20 # when filtering the lines if to lines are closer then this parameter (and they are parallel) only one
#  will stay
max_d_theta = 0.5 # when filtering the lines angles are closer then this parameter (and they are close to each other)
# only one will stay


# functio for help
def cimg_def(img):
    """
    do not touche it, its for the circles drawing
    :param img: gray scale img
    :return: img converted it to RGB img
    """
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def cutPicture(img):
    """
    do not touch it you can update the numbers when built the system again
    :param img: an img
    :return: cut img
    """
    return img[30:370, 70:440]


def myKey(line):
    """
    :param line:
    :return:the lines absolute radius
    """
    return abs(line[0][0])



def get_color(x, y, img):
    """
    finds the average color around a dot
    :param x: the x coordinate of the dot
    :param y: the y coordinate of the dot
    :param img: RGB picture
    :return: if its red -1, 1 otherwise
    """
    x = int(x) # convert to int so it will be picsell
    y = int(y) # convert to int so it will be picsell
    sum0 = 0 # blue color
    sum1 = 0 # green color
    sum2 = 0 # red color
    window = 25 # area of averaging
    for i in range(int(math.sqrt(window))):
        for j in range(int(math.sqrt(window))):
            sum0 += img[y - i][x - j][0]
            sum1 += img[y - i][x - j][1]
            sum2 += img[y - i][x - j][2]
    m0 = float(sum0) / window # blue average
    m1 = float(sum1) / window # green average
    m2 = float(sum2) / window # red average
    if m2 - (m1 + m0) / 2 < red_color_majority:
        return 1
    else:
        return -1


def initialCamera():
    """initial canera"""
    print("initializing camera")
    camera = cv2.VideoCapture(0)
    print("camera ", camera)
    time.sleep(0.5)
    return camera


def get_y_line_formula(dot1, dot2):
    """
    get to dots in a line
    :return: return the line formula (green lines)
    """
    def g(x):
        m = float((dot1[1] - dot2[1])) / (dot1[0] - dot2[0])
        c = dot1[1] - m * dot1[0]
        return x * m + c

    return g


def get_x_line_formula(dot1, dot2):
    """
        get to dots in a line
        :return: return the line formula (red lines)
        """
    def g(y):
        if (dot1[0] - dot2[0]) == 0:
            return dot1[0]
        m = float((dot1[1] - dot2[1])) / (dot1[0] - dot2[0])
        if m == 0:
            return dot1[1]
        c = dot1[1] - m * dot1[0]
        return (y - c) / m

    return g


def get_new_point(x, y):
    """
    do not touch, convert the dots cto the small picture
    :param x: אthe original x
    :param y: the original y
    :return: new dot
    """
    return ((x - 10) * 0.8, (y - 10) * 0.8)


def first_editing(image):
    #palties bulshit...
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 0.001)
    return image


def show_image(image):
    #showin img
    cv2.imshow("image", image)
    cv2.waitKey(0)


def resize(image):
    #change the size of a picture, do not touche
    shape = image.shape
    if len(shape) == 2:
        height, width = shape
    else:
        height, width, chanels = shape
    image = image[10:height, 10:width]  # cut the edge of the image
    image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
    return image


def bolding(image):
    # palti's bulshit...
    kernel = np.ones((5, 5), np.uint8)
    image = 255 - image
    dilation = cv2.dilate(image, kernel, iterations=1)
    dilation = 255 - dilation
    return dilation


def find_circles(img2):
    """
    do not touche the parameters
    :param img2: Gray scale
    :return: ndarray of circles
    """
    return cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT, circles_param, 20,
                            param1=50, param2=30, minRadius=r, maxRadius=R)


def filter_circles(circles, img):
    """
    filter the sircles
    :param circles: dnarray of circles
    :param img: RGB picture
    :return: a list of circles after filtering
    """
    print('type = ' , type(circles),'\n circles = ' , circles)
    filtered_circles = []
    if type(circles) != np.ndarray:
        return
    for circle in circles[0, :]:
        x = int(circle[0])
        y = int(circle[1])
        sum0 = 0
        sum1 = 0
        sum2 = 0
        window = 25
        for i in range(int(math.sqrt(window))):
            for j in range(int(math.sqrt(window))):
                sum0 += img[y - i][x - j][0]
                sum1 += img[y - i][x - j][1]
                sum2 += img[y - i][x - j][2]
        m0 = float(sum0) / window # blue average
        m1 = float(sum1) / window # green average
        m2 = float(sum2) / window # red average
        m = (m0 + m2 + m1) / 3
        # if its red enough or black enough its OK
        if (m2 - (m1 + m0) / 2) > red_color_majority or m < up_th:
            filtered_circles.append(circle)
            # print ('m0 = ', m0, 'm1 = ', m1, 'm2 = ', m2)
    return filtered_circles


def draw_circles(circles_, cimg):
    """
    draws the circles
    :param circles_: list of circles
    :param cimg: RGB picture
    :return: None
    """
    if len(circles_) == 0:
        return
    for i in range(len(circles_)):
        # draw the center of the circle
        cv2.circle(cimg, (circles_[i][0], circles_[i][1]), 2, (0, 0, 255), 3)
        # draw the outer circle
        cv2.circle(cimg, (circles_[i][0], circles_[i][1]), circles_[i][2],
                   (0, 255, 0), 2)


def find_lines(img):
    """
    find lines
    :param img: gray scale img
    :return: a list of lines
    """
    #palties bulshit...
    s_img = resize(img)
    gray = cv2.cvtColor(s_img, cv2.COLOR_RGB2GRAY)
    gray = first_editing(gray)
    gray = 255 - gray
    # cv2.imshow('cacc', gray)
    # cv2.waitKey(0)
    lines = cv2.HoughLines(gray, 1, angle_param, lines_param)
    return sorted(lines, key=myKey)


def filter_lines(lines):
    """
    filters the lines by radius and angle
    :param lines: the lines we have found
    :return: filtered lines
    """
    lines_filtered = []
    for i in range(len(lines)):
        selected = False
        rho1, theta1 = lines[i][0]
        # check the radius
        if abs(rho1) > max_rho or abs(rho1) < min_rho:
            #if to big or to small goes on
            continue
        #check if fit in as y lines
        if np.tan(theta1) != 0 and abs((np.tan(theta1) ** -1) - (
                    np.tan(y_angle) ** (-1))) < y_thrash_hold:
            selected = True
        #check if fit in as x line
        if abs((np.tan(theta1)) - (np.tan(x_angle))) < x_thrash_hold:
            selected = True
        # make surethe filtered lines list is not empty
        if len(lines_filtered) == 0 and selected:
            lines_filtered.append(lines[i])
        # if there is a similar line in the filtered lines it dose not get in
        for j in range(len(lines_filtered)):
            rho2, theta2 = lines_filtered[j][0]
            if abs((np.sin(theta1)) - (
                    np.sin(theta2))) < max_d_theta and abs(
                        abs(rho1) - abs(rho2)) < min_d_rho:
                selected = False
        if selected:
            lines_filtered.append(lines[i])
    return lines_filtered


def draw_lines(lines_filtered, s_img):
    """
    draw the lines
    :param lines_filtered: filtered lines
    :param s_img: RGB picture
    :return: None
    """
    for line in lines_filtered:
        for rho, theta in line:
            sin = math.cos(theta)
            cos = math.sin(theta)
            x0 = sin * rho
            y0 = cos * rho
            x1 = (x0 + 1000 * (-cos))
            y1 = (y0 + 1000 * (sin))
            x2 = (x0 - 1000 * (-cos))
            y2 = (y0 - 1000 * (sin))
            if abs(abs(np.tan(theta)) - abs(
                    np.tan(x_angle))) < x_thrash_hold:
                cv2.line(s_img, (int(x1), int(y1)), (int(x2), int(y2)),
                         (0, 255, 0), 2)
            else:
                cv2.line(s_img, (int(x1), int(y1)), (int(x2), int(y2)),
                         (0, 0, 255), 2)


def classified_lines(filtered_lines):
    """
    divides the lines to two lists of formulas, the green (x) and red (y)
    :param filtered_lines: list of filtered lines
    :return: tuple of two lists (red_form , green_firm)
    """
    red_form = []
    green_form = []
    for line in filtered_lines:
        for rho, theta in line:
            sin = math.cos(theta)
            cos = math.sin(theta)
            x0 = sin * rho
            y0 = cos * rho
            x1 = (x0 + 1000 * (-cos))
            y1 = (y0 + 1000 * (sin))
            x2 = (x0 - 1000 * (-cos))
            y2 = (y0 - 1000 * (sin))
            # filter by angle
            if np.tan(theta) != 0 and abs(abs(np.tan(theta) ** (-1)) - abs(
                            np.tan(y_angle) ** (-1))) < y_thrash_hold:
                red_form.append(get_y_line_formula((x1, y1), (x2, y2)))
            else:
                green_form.append(get_x_line_formula((x1, y1), (x2, y2)))
    # print(len(green_form)," - greens " , len(red_form)," - reds ")
    return red_form, green_form


def create_board(red, green):
    """
    create the board
    """
    table = []
    for i in range(8):
        sub = []
        for i in range(8):
            sub.append(0)
        table.append(sub)
    return table


def find_board(circles, red_form, green_form, img):
    """
    :param circles:circles after filtered
    :param red_form: the y lines
    :param green_form: the x lines
    :param img: RGB img
    :return: table represents the board
    """
    table = create_board(red_form, green_form)
    if len(circles) == 0:
        return table
    for i in range(len(circles)):
        color = get_color(circles[i][0], circles[i][1], img)
        circle = get_new_point(circles[i][0], circles[i][1])
        # do not change it!!! it keeps things in range
        x = -1
        y = -1
        for j in range(len(red_form)):
            y1 = red_form[j](circle[0])
            if y1 < circle[1]:
                y += 1
        for k in range(len(green_form)):
            x1 = green_form[k](circle[1])
            if x1 < circle[0]:
                x += 1
        table[y][x] = color
    return table


def get_board(img, colored_img):
    """
    final function
    :param img: gray picture
    :param colored_img: RGB picture
    :return: matrix of the board
    """
    circles = find_circles(img)
    circles = filter_circles(circles, colored_img)
    c = cimg_def(img)
    lines = find_lines(c)
    filtered = filter_lines(lines)
    red_forms, green_forms = classified_lines(filtered)
    board = find_board(circles, red_forms, green_forms, colored_img)
    return board


def take_pic():
    """
    take picture
    :return: img of the board in gray scale
    """
    rval, frame = MyCamera.get_camera().read()
    cv2.imwrite('board.jpg', frame)
    board_img = cv2.imread('board.jpg', 0)
    return board_img


def take_color_pic():
    """
    call it only after the "take_pic()" function
    :return: the same color as the "take_pic()" function in RGB
    """
    frame = cv2.imread('board.jpg')
    return frame


if __name__ == '__main__':
    # cam = MyCamera.get_camera()
    print('hi')
    key = "enter"
    while True:
        print("press key to continue")
        key = input()
        if key == 'e':
            break
        if key == 'u':
            up_th = int(input('set up_th'))
            down_th = int(input('set down_th'))
        if key == 'R':
            p = input('set max radius')
            R = int(p)
        if key == 'r':
            p = input('set min radius')
            r = int(p)
        if key == 'p':
            p = input('set circles_parameter')
            circles_param = float(p)
        # img = cv2.imread('calibrate.jpg',0)
        # colored_pic = cv2.imread('calibrate.jpg')
        img = take_pic()
        colored_pic = take_color_pic()
        if key == 'red':
            red_color_majority = int(input('set red_color_majority'))

        print("working...")
        img = cutPicture(img)
        colored_pic = cutPicture(colored_pic)

        if key == 'a' or key == 'd':
            show_image(img)
        if key == 'b' or key == 'a':
            s_bord = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])
            for i in range(1):
                img = take_pic()
                colored_pic = take_color_pic()
                img = cutPicture(img)
                colored_pic = cutPicture(colored_pic)
                board = get_board(img, colored_pic)
                board1 = np.array(board)
                s_bord += board1
            s_bord = s_bord
            for i in range(8):
                for j in range(8):
                    if s_bord[i][j] > 0.5:
                        s_bord[i][j] = int(1)
                    elif s_bord[i][j] < - 0.5:
                        s_bord[i][j] = int(-1)
                    else:
                        s_bord[i][j] = int(0)
            print(s_bord)
            if key == 'b':
                continue
        if key == 'c' or key == 'a':
            circles = find_circles(img)
            circles = filter_circles(circles, colored_pic)
        c = cimg_def(img)
        if key == 'c' or key == 'a':
            draw_circles(circles, c)
        lines = find_lines(c)
        filtered = filter_lines(lines)
        classified_lines(filtered)
        s = resize(c)
        draw_lines(filtered, s)
        if key == 'c' or key == 'a':
            cv2.imshow("sad3", s)
            cv2.waitKey(0)
