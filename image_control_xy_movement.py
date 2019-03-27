import cv2
import numpy as np
import time
import serial
import math
import Camera as MyCamera
import rotate
import shit

SHOW = False

junk_string = "junk"

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
# squares_pixels = [row0, row1, row2, row3, row4, row5, row6, row7]
squares_pixels = np.load('measurement_final.npy')
grey_threshold = 5


def takePicture(pic_name):
    rval, frame = MyCamera.get_camera().read()
    time.sleep(0.01)
    rval, frame = MyCamera.get_camera().read()
    # cv2.imshow('yam_picture', frame)
    cv2.imwrite(pic_name, frame)
    # print("saved picture as '" + pic_name + "'")
    return frame


def extand_square_by_d(four_points, d):
    new_points = np.zeros((4, 2))
    m1 = (four_points[0][1] - four_points[2][1]) / (four_points[0][0] - four_points[2][0])
    m2 = (four_points[3][1] - four_points[1][1]) / (four_points[3][0] - four_points[1][0])
    # print(four_points)
    voodoo = 3.5
    new_points[0] = [round(four_points[0][0] - d), round(four_points[0][1] - d * m1)]
    new_points[2] = [round(four_points[2][0] + (d + 0.8 * voodoo)), round(four_points[2][1] + (d + 0.6 * voodoo) * m1)]
    new_points[1] = [round(four_points[1][0] + (d + voodoo)), round(four_points[1][1] + (d + voodoo) * m2)]
    new_points[3] = [round(four_points[3][0] - d), round(four_points[3][1] - d * m2)]
    # print(new_points)
    # print(type(new_points), new_points.shape)
    return new_points


def save_blue_mask(frame, new_img_name):
    # POINTS = rotate.POINTS
    # print(POINTS)
    # POINTS = rotate.order_points(POINTS)
    # print(type(POINTS), POINTS.shape)
    # POINTS = extand_square_by_d(POINTS, 50)
    # print(type(POINTS))
    # print(POINTS.shape)
    # for i in POINTS:
    #     point = tuple(i)
    #     cv2.circle(frame, point, 2, (0, 0, 255), 3)
    # image_cutting.show_image(frame)
    # if type(POINTS) != np.ndarray:
    # POINTS = np.array(POINTS)
    # frame = rotate.four_point_transform(frame, POINTS)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 40, 40])
    upper_blue = np.array([130, 250, 250])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    if SHOW == True:
        cv2.imshow('frame', frame)
        cv2.imwrite('yam.jpg', frame)
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
            if img[i][j] > threshold_val and i > 35 and i < 400 and j>140 and j<500:
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
    # cv2.imshow('wisg',img)
    # cv2.waitKey(0)
    img = save_blue_mask(img, 'find_center1.png')
    a = img.shape
    return get_center_of_masked_gray_pic(img, grey_threshold)


def get_move_and_dist(square_num):
    '''
    :param obj_loc: object location in pixels
    :param square_num: which square we want to go, look like: (x,y)
    :return: tuple indicate needed move in x, y in centimeters
    '''
    obj_loc = get_obj_location_pixels()
    print('obj_loc = ', obj_loc)
    square_pixels = squares_pixels[square_num[0]][square_num[1]]
    x_diff = obj_loc[1] - square_pixels[1]  # in pixels
    y_diff = obj_loc[0] - square_pixels[0]  # in pixels
    # print('x_diff = ', x_diff)
    x_diff = convert_pixel_to_centimeter(x_diff)  # in centimeters
    y_diff = convert_pixel_to_centimeter(y_diff)  # in centimeters
    print('x_diff (cm) = ', x_diff)
    dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
    print('x_diff = ', x_diff.item(), 'y_diff = ', y_diff.item())
    return x_diff.item(), y_diff.item(), dist


def cm_to_steps(cm):
    return round(cm / 7.0 * 338.0)


def write_move_motors_x(arduinoSerial, diff):
    string = "u+"
    if diff < 0:
        string = "d+"
    string += str(cm_to_steps(diff))
    arduinoSerial.write(string.encode())


def write_move_motors_y(arduinoSerial, diff):
    string = "r+"
    if diff < 0:
        string = "l+"
    string += str(cm_to_steps(diff))
    arduinoSerial.write(string.encode())


def move_monitored(arduinoSerial, square_num):
    move = get_move_and_dist(square_num)
    print("in move monitored after got move")
    x_diff = move[0]
    y_diff = move[1]
    dist = move[2]
    while dist > 2.0:
        print("dist>2")
        x_diff = cm_to_steps(x_diff)
        y_diff = cm_to_steps(y_diff)
        move_xy(arduinoSerial, x_diff, y_diff)
        # send_to_arduino_motors x_diff, y_diff and wait for response when they're done
        time.sleep(1)
        move = get_move_and_dist(square_num)
        x_diff = move[0]
        y_diff = move[1]
        dist = move[2]


def move_xy(arduinoSerial, x_diff, y_diff):
    string = "_movexy" + str(x_diff) + "," + str(-y_diff)
    print("movexy string:", string)
    # time.sleep(1)
    arduinoSerial.write(string.encode())
    # time.sleep(1)
    while "done plotter_move_motors" not in str(arduinoSerial.readline().decode("utf-8")):
        continue
    # arduinoSerial.write(junk_string.encode())
    print("after movement")


def save_indexes(file_name):
    array = np.load(file_name)
    # array = np.load(file_name)
    # x = input("to continue press something- ")
    # obj_loc = get_obj_location_pixels()
    # array[4][1][0] = array[4][1][0]#obj_loc[0][0]
    # array[4][1][1] = array[4][1][1]#obj_loc[0][1]
    # array[4][1][2] = obj_loc[1][0]  # y size of the image
    # array[4][1][3] = obj_loc[1][1]  # x size of the image
    # np.save(file_name, array)

    for i in range(4, 8):
        for j in range(0, 8):
            print(i, ",", j)
            x = input("to continue press something- ")
            obj_loc = get_obj_location_pixels()
            array[i][j][0] = obj_loc[0]
            array[i][j][1] = obj_loc[1]
            # array[i][j][2] = obj_loc[1][0]  # y size of the image
            # array[i][j][3] = obj_loc[1][1]  # x size of the image
            np.save(file_name, array)


if __name__ == '__main__':
    # TODO
    MyCamera.initialize_camera()
    print("camera is ready")
    time.sleep(2)
    arduinoName = 'COM6'
    port = 9600
    # global ArduinoSerial
    arduinoSerial = serial.Serial(arduinoName, port)

    # print(get_obj_location_pixels())
    get_move_and_dist((1, 2))
    move_monitored(arduinoSerial, (3, 6))
    move_monitored(arduinoSerial, (5, 5))
    # save_indexes('measurement_final.npy')
    # takePicture('yam_test.png')
