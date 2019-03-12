import cv2
import numpy as np
import time
import math
from MyCamera import MyCamera

row0 = [(128, 80), (166, 80), (204, 80), (242, 80), (280, 80), (317, 80),
        (356, 80), (391, 80)]
row1 = [(128, 117), (166, 117), (204, 117), (242, 117), (280, 117),
        (318, 117), (355, 117), (392, 117)]
row2 = [(127, 154), (166, 154), (205, 154), (243, 154), (280, 154),
        (318, 154), (354, 154), (393, 154)]
row3 = [(128, 193), (165, 193), (205, 193), (243, 193), (280, 193),
        (318, 193), (356, 191), (393, 192)]
row4 = [(128, 228), (167, 227), (204, 229), (243, 230), (281, 229),
        (317, 227), (355, 230), (393, 226)]
row5 = [(129, 268), (167, 268), (205, 267), (243, 268), (282, 267),
        (318, 267), (356, 264), (393, 267)]
row6 = [(129, 306), (167, 305), (206, 306), (244, 305), (280, 305),
        (319, 304), (356, 304), (394, 304)]
row7 = [(129, 344), (168, 344), (205, 343), (244, 343), (281, 344),
        (317, 339), (357, 341), (393, 341)]
squares_pixels = [row0, row1, row2, row3, row4, row5, row6, row7]
grey_threshold = 5


def takePicture(pic_name):
    rval, frame = MyCamera.get_camera().read()
    # cv2.imshow('yam_picture', frame)
    cv2.imwrite(pic_name, frame)


def save_green_mask(img, new_img_name):
    range_green = 30
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (
        105 - range_green, 206 - range_green, 53 - range_green),
                       (70 + range_green, 255 + range_green,
                        255 + range_green))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    ## save
    cv2.imwrite(new_img_name, green)


def get_center_of_masked_gray_pic(img, threshold_val=grey_threshold):
    row_sum = 0
    column_sum = 0
    row_count = 0
    column_count = 0
    for i in range(img.shape[0]):  # traverses through height of the image
        for j in range(img.shape[1]):  # traverses through width of the image
            if img[i][j] > threshold_val and i > 15 and i < 360:
                row_sum += i
                column_sum += j
                row_count += 1
                column_count += 1
    y_center = row_sum / row_count
    x_center = column_sum / column_count
    y_center = round(y_center)  # center of grey
    x_center = round(x_center)  # center of grey
    y_center += 69  # center of drop point
    x_center += 3  # center of drop point

    return x_center, y_center


def convert_pixel_to_centimeter(pixels_num):
    square_centimeter = 7.0
    square_pixels = 37.0
    ratio_centimeter_to_pixel = square_centimeter / square_pixels
    return pixels_num * ratio_centimeter_to_pixel


def get_obj_location_pixels():
    takePicture('find_center0.png')
    img = cv2.imread('find_center0.png')
    save_green_mask(img, 'find_center1.png')
    img = cv2.imread('find_center1.png', 0)  # already grey
    return get_center_of_masked_gray_pic(img, 50)


def get_move_and_dist(square_num):
    '''
    :param obj_loc: object location in pixels
    :param square_num: which square we want to go, look like: (x,y)
    :return: tuple indicate needed move in x, y in centimeters
    '''
    obj_loc = get_obj_location_pixels()
    square_pixels = squares_pixels[square_num[0]][square_num[1]]
    x_diff = obj_loc[1] - square_pixels[1]  # in pixels
    y_diff = obj_loc[0] - square_pixels[0]  # in pixels
    x_diff = convert_pixel_to_centimeter(x_diff)  # in centimeters
    y_diff = convert_pixel_to_centimeter(y_diff)  # in centimeters
    dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
    return x_diff, y_diff, dist


if __name__ == '__main__':
    takePicture('yoav')
