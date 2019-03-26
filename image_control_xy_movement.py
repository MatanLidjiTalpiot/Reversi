import cv2
import numpy as np
import time
import math
from MyCamera import MyCamera
import image_cutting


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
    print("saved picture as '"+pic_name+"'")
    return frame


def save_blue_mask(frame, new_img_name):
    POINTS = [[182, 82], [177, 362], [459, 372], [467, 89]]
    POINTS = np.array(POINTS)
    POINTS = image_cutting.order_points(POINTS)
    # for i in POINTS:
    #     point = tuple(i)
    #     cv2.circle(frame, point, 2, (0, 0, 255), 3)
    # image_cutting.show_image(frame)
    frame = image_cutting.four_point_transform(frame, POINTS)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([150, 250, 250])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.waitKey(0)
    cv2.imwrite(new_img_name, mask)
    return mask

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

    return x_center, y_center

def convert_pixel_to_centimeter(pixels_num):
    square_centimeter = 7.0
    square_pixels = 36.0
    ratio_centimeter_to_pixel = square_centimeter / square_pixels
    return pixels_num * ratio_centimeter_to_pixel


def get_obj_location_pixels():
    img = takePicture('find_center0.png')
    img = save_blue_mask(img, 'find_center1.png')
    return get_center_of_masked_gray_pic(img, grey_threshold)


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

def move_monitored(square_num):
    move = get_move_and_dist(square_num)
    x_diff = move[0]
    y_diff = move[1]
    dist = move[2]
    while(dist>2.0):
        #send_to_arduino_motors x_diff, y_diff and wait for response when they're done
        move = get_move_and_dist(square_num)
        x_diff = move[0]
        y_diff = move[1]
        dist = move[2]
if __name__ == '__main__':
    # img = takePicture('find_blue2.png')
    img = cv2.imread('find_blue2.png')
    img = save_blue_mask(img, 'findblue1_after.png')
    print(get_center_of_masked_gray_pic(img, grey_threshold))
