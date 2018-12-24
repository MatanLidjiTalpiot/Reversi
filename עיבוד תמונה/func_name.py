import cv2
import numpy as np
import math
#variables
#circles
r = 8 #min radius
R = 11 #max radius
circles_param = 2 #circles thrashhold
up_th = 100
down_th = 0
#images
global cam
img2 = cv2.imread("data1175.jpg", 0)
# img2 = img2[50:390, 165:500]
# cimg = 0
# s_img = 0
#lines
lines_param = 200
angle_param = np.pi / 720
max_rho = 280
min_rho = 0
y_angle = np.pi / 2
y_thrash_hold = 0.4
x_angle = 0.0
x_thrash_hold = 0.5
min_d_rho = 20
max_d_theta = 0.5

#colors
thrash_hold = 30


#functio for help
def cimg_def(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def cutPicture(img):
    return img[30:370, 70:440]

def myKey(line):
    return abs(line[0][0])




def img2_def(img):
    # img = cv2.medianBlur(img, 5)
    # img = cv2.medianBlur(img, 5)
    return img


def get_color(x,y,img):
    x = int(x)
    y = int(y)
    sum = 0
    window = 25
    for i in range(int(math.sqrt(window))):
        for j in range(int(math.sqrt(window))):
            c = img[y-i][x-j]
            sum += img[y-i][x-j]
    if float(sum)/window < thrash_hold:
        return 1
    else:
        return -1

def initialCamera():
    return cv2.VideoCapture(0)


def get_y_line_formula(dot1, dot2):
    def g(x):

        m = float((dot1[1]-dot2[1]))/(dot1[0] - dot2[0])
        c = dot1[1] - m * dot1[0]
        return x * m + c
    return g

def get_x_line_formula(dot1, dot2):
    def g(y):
        if (dot1[0] - dot2[0]) == 0:
            return dot1[0]
        m = float((dot1[1]-dot2[1]))/(dot1[0] - dot2[0])
        if m ==0:
            return dot1[1]
        c = dot1[1] - m * dot1[0]
        return (y-c)/m
    return g

def get_new_point(x,y):
    return ((x-10)*0.8, (y-10)*0.8)

def first_editing(image):
   image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0.001)
   return image

def show_image(image):
   cv2.imshow("image", image)
   cv2.waitKey(0)

def resize(image):
   shape = image.shape
   if len(shape) == 2:
      height, width = shape
   else:
      height, width, chanels = shape
   image = image[10:height, 10:width] #cut the edge of the image
   image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
   return image

def bolding(image):
   kernel = np.ones((5, 5), np.uint8)
   image = 255 - image
   dilation = cv2.dilate(image, kernel, iterations=1)
   dilation = 255 - dilation
   return dilation




def find_circles(img2):
    return cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT, circles_param, 20, param1=50, param2=30, minRadius=r, maxRadius=R)


def filter_circles(circles, img):
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    filtered_circles = []
    if type(circles) != np.ndarray:
        return
    for circle in circles[0, :]:
        x = int(circle[0])
        y = int(circle[1])
        sum = 0
        window = 25
        for i in range(int(math.sqrt(window))):
            for j in range(int(math.sqrt(window))):
                c = img[y - i][x - j]
                sum += img[y - i][x - j]
        m = float(sum)/window
        if m <up_th and m >down_th:
            filtered_circles.append(circle)
    return filtered_circles


def draw_circles(circles_ , cimg):
    if len(circles_) == 0:
        return
    for i in range(len(circles_)):
        # draw the center of the circle
        cv2.circle(cimg, (circles_[i][0], circles_[i][1]), 2, (0, 0, 255), 3)
        # draw the outer circle
        cv2.circle(cimg, (circles_[i][0], circles_[i][1]), circles_[i][2], (0, 255, 0), 2)


def find_lines(img):
    s_img = resize(img)
    gray = cv2.cvtColor(s_img, cv2.COLOR_RGB2GRAY)
    gray = first_editing(gray)
    gray = 255 - gray
    # cv2.imshow('cacc', gray)
    # cv2.waitKey(0)
    lines = cv2.HoughLines(gray, 1, angle_param, lines_param)
    return sorted(lines,key = myKey)



def filter_lines(lines):
    lines_filtered = []
    for i in range(len(lines)):
        selected = False
        rho1, theta1 = lines[i][0]
        if abs(rho1) > max_rho or abs(rho1) < min_rho:
            continue
        if np.tan(theta1) != 0 and abs((np.tan(theta1)**-1) - (np.tan(y_angle)**(-1))) < y_thrash_hold:
            selected = True
        if abs((np.tan(theta1)) - (np.tan(x_angle))) < x_thrash_hold:
            selected = True
        if len(lines_filtered) == 0 and selected:
            lines_filtered.append(lines[i])
        for j in range(len(lines_filtered)):
            rho2, theta2 = lines_filtered[j][0]
            if abs((np.sin(theta1)) - (np.sin(theta2))) < max_d_theta and abs(abs(rho1) - abs(rho2)) < min_d_rho:
                selected = False
        if selected:
            lines_filtered.append(lines[i])
    return lines_filtered


def draw_lines(lines_filtered,s_img):
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
            if abs(abs(np.tan(theta)) - abs(np.tan(x_angle))) < x_thrash_hold:
                cv2.line(s_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            else:
                cv2.line(s_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)


def classified_lines(filtered_lines):
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
            if np.tan(theta) != 0 and  abs(abs(np.tan(theta)**(-1)) - abs(np.tan(y_angle)**(-1))) < y_thrash_hold:
                red_form.append(get_y_line_formula((x1, y1), (x2, y2)))
            else:
                green_form.append(get_x_line_formula((x1, y1), (x2, y2)))
    # print(len(green_form)," - greens " , len(red_form)," - reds ")
    return red_form , green_form


def create_board(red, green):
    table = []
    sub = []
    for i in range(len(red) - 1):
        sub = []
        for i in range(len(green) - 1):
            sub.append(0)
        table.append(sub)
    return table


def find_board(circles, red_form,green_form, img):
    table = create_board(red_form, green_form)
    if len(circles) == 0:
        return table
    for i in range(len(circles)):
        color = get_color(circles[i][0], circles[i][1], img)
        circle = get_new_point(circles[i][0], circles[i][1])
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


def get_board(img2):
    img = img2_def(img2)
    circles = find_circles(img)
    circles = filter_circles(circles,img)
    c = cimg_def(img)
    lines = find_lines(c)
    filtered = filter_lines(lines)
    red_forms , green_forms = classified_lines(filtered)
    board = find_board(circles, red_forms, green_forms, img)
    return board


def takepic():
    rval , frame = cam.read()
    cv2.imwrite('board.jpg',frame)
    board_img = cv2.imread('board.jpg', 0)
    return board_img



if __name__ == '__main__':
    cam = initialCamera()
    print('hi')
    key = "enter"
    while True:
        print("press key to continue")
        key = input()
        if key == 'e':
            break
        if key == 't':
            thrash_hold = int(input('set color thrash hold'))
        if key == 'u':
            up_th = int(input('set up_th'))
            down_th = float(input('set down_th'))
        if key =='R':
            p = input('set max radius')
            R = int(p)
        if key =='r':
            p = input('set min radius')
            r = int(p)
        if key =='p':
            p = input('set circles_parameter')
            circles_param = float(p)
        img = takepic()

        #### check
        # img = cv2.imread('data100.jpg' , 0)


        print("working...")
        img = cutPicture(img)
        if key == 'a' or key == 'd':
            show_image(img)
        if key == 'b' or key == 'a':
            board = get_board(img)
            board1 = np.array(board)
            print(board1)
            if key == 'b':
                continue
        if key == 'c' or key == 'a':
            circles = find_circles(img)
            circles = filter_circles(circles,img)
        c = cimg_def(img)
        if key == 'c' or key == 'a':
            draw_circles(circles,c)
        lines = find_lines(c)
        filtered = filter_lines(lines)
        classified_lines(filtered)
        s = resize(c)
        draw_lines(filtered,s)
        if key == 'c' or key == 'a':
            cv2.imshow("sad3", s)
            cv2.waitKey(0)





