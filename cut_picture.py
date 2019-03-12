import cv2;
import numpy as np;
import math

i


def get_color(x, y, img):
    x = int(x)
    y = int(y)
    thrash_hold = 80
    sum = 0
    window = 25
    for i in range(int(math.sqrt(window))):
        for j in range(int(math.sqrt(window))):
            c = img[y - i][x - j]
            sum += img[y - i][x - j]
    if float(sum) / window < thrash_hold:
        return -1
    else:
        return 1


def get_y_line_formula(dot1, dot2):
    def g(x):
        m = float((dot1[1] - dot2[1])) / (dot1[0] - dot2[0])
        c = dot1[1] - m * dot1[0]
        return x * m + c

    return g


def get_x_line_formula(dot1, dot2):
    def g(y):
        m = float((dot1[1] - dot2[1])) / (dot1[0] - dot2[0])
        c = dot1[1] - m * dot1[0]
        return (y - c) / m

    return g


def get_new_point(x, y):
    return ((x - 10) * 0.8, (y - 10) * 0.8)


def first_editing(image):
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((4, 4)))
    image = cv2.medianBlur(image, 3)
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
    image = image[10:height, 10:width]  # cut the edge of the image
    image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
    return image


def bolding(image):
    kernel = np.ones((5, 5), np.uint8)
    image = 255 - image
    dilation = cv2.dilate(image, kernel, iterations=1)
    dilation = 255 - dilation
    return dilation


img2 = cv2.imread("WIN_20181129_13_32_56_Pro.jpg", 0)

img2 = cv2.medianBlur(img2, 5)
img2 = cv2.medianBlur(img2, 5)
cimg = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=35)
# for i in range(len(circles):

# circles = np.uint16(np.around(circles))


for i in circles[0, :]:
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)

img = cimg
s_img = resize(img)
gray = cv2.cvtColor(s_img, cv2.COLOR_RGB2GRAY)
gray = first_editing(gray)
gray = 255 - gray
lines = cv2.HoughLines(gray, 1, np.pi / 720, 180)
lines_filtered = [lines[0]]
for i in range(len(lines)):
    selected = False
    rho1, theta1 = lines[i][0]
    if abs(rho1) > 850 or abs(rho1) < 60:
        continue
    if abs(abs(np.sin(theta1)) - abs(np.sin(np.pi / 2 + 0.0125))) < 0.01:
        selected = True
    if abs(abs(np.sin(theta1)) - abs(np.sin(0.0))) < 0.2:
        selected = True
    for j in range(len(lines_filtered)):
        rho2, theta2 = lines_filtered[j][0]
        if abs(abs(np.sin(theta1)) - abs(np.sin(theta2))) < 0.2 and abs(abs(rho1) - abs(rho2)) < 30:
            selected = False
    if selected:
        lines_filtered.append(lines[i])
print(len(lines_filtered))

red_lines = []
green_lines = []
red_form = []
green_form = []
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
        if abs(abs(np.sin(theta)) - abs(np.sin(np.pi / 2 + 0.0125))) < 0.1:
            cv2.line(s_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            red_lines.append(line)
            red_form.append(get_y_line_formula((x1, y1), (x2, y2)))
        else:
            cv2.line(s_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            green_lines.append(line)
            green_form.append(get_x_line_formula((x1, y1), (x2, y2)))

table = []
sub = []
for i in range(8):
    sub = []
    for i in range(8):
        sub.append(0)
    table.append(sub)

for circle in circles[0, :]:
    color = get_color(circle[0], circle[1], img2)
    circle = get_new_point(circle[0], circle[1])
    x = -1
    y = -1
    for i in range(len(red_lines)):
        y1 = red_form[i](circle[0])
        print(y1)
        if y1 < circle[1]:
            y += 1
    for i in range(len(green_lines)):
        x1 = green_form[i](circle[1])
        if x1 < circle[0]:
            x += 1
    table[y][x] = color
for x in table:
    print(x)
cv2.imwrite("blabla.jpg", s_img)
cv2.imshow("sad", s_img)
cv2.waitKey(0)
