import time
import shit
import Camera
import cv2
import numpy as np
import rotate
sdThresh = 0.095
x_min = 143
x_max = 514
y_min = 43
y_max = 76
Relevant_area =[x_min, x_max, y_min, y_max]
CUT_R = 0.03


def cut_picture_2(img):
    #TODO check if it is [x_min:x_max , y_min:y_max] or [y_min:y_max , x_min:x_max]
    return img[y_min : y_max , x_min : x_max]

###############old recognition!!!##################
# def is_hand_in_the_field(refrence, pic):
#     # print(distMap(pic,refrence))
#     distMapMask(pic)
#     if distMap(pic, refrence) >= sdThresh:
#         return True
#     return False

############# new recognition ##############
def is_hand_in_the_field(refrence, pic):
    # print(distMap(pic,refrence))
    return is_hand_in_the_field_mask_check(pic)

# def calculateDistance_colordPictures(image1, image2):
#     distance = 0
#     for i in range(len(image1)):
#         for j in range(len(image1)):
#             for k in range(3):
#                 distance += (image1[i][j][k]-image2[i][j][k]) ** 2
#     distance = np.sqrt(distance)
#     return distance

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    # frame1_32 = np.float32(frame1)
    # frame2_32 = np.float32(frame2)
    # diff32 = frame1_32 - frame2_32
    # norm32 = np.sqrt(diff32[:, :, 0] ** 2 + diff32[:, :, 1] ** 2 + diff32[:, :, 2] ** 2)
    # dist = norm32
    # dist = calculateDistance_colordPictures(frame1, frame2)
    size = frame1.shape[0]*frame1.shape[1]
    dist = np.sqrt(np.sum((frame1 - frame2) ** 2))/size
    # print('dist = ' + str(dist))
    return dist

def is_hand_in_the_field_mask_check(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 100])
    upper_white = np.array([255, 40, 255])

    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    white_pixels = cv2.countNonZero(mask_white)
    # print(white_pixels) # full with no interferance = 12185 pixels with hand = 10099

    if white_pixels < 11500:
        return True
    return False

    # cv2.imshow("mask",mask_white)
    # cv2.imshow("pic",frame)
    # cv2.waitKey(0)

def num_of_circles(board_pic):
    return np.count_nonzero(shit.extract_board(board_pic))


def take_refrence(avg):
    _, refrence = Camera.get_camera().read()
    time.sleep(0.01)
    for i in range(avg):
        _, info = Camera.get_camera().read()
        time.sleep(0.01)
        refrence = refrence + info
    return refrence/(avg + 1)


def continue_when_it_is_our_turn(last_num_of_circles):
    cam = Camera.get_camera()
    ##take refrence picture
    _, refrence = cam.read()
    time.sleep(0.01)
    _, refrence = cam.read()
    time.sleep(0.01)
    #cut the refrence
    refrence = cut_picture_2(refrence)
    # cv2.imshow('refrence',refrence)
    ##take picture
    _, frame = cam.read()
    time.sleep(0.01)
    _, frame = cam.read()
    time.sleep(0.01)
    #cut it
    frame = cut_picture_2(frame)
    # cv2.imshow('frame',frame)
    # cv2.waitKey(0)

    #initial values
    is_hand = is_hand_in_the_field(refrence , frame)
    our_turn = False

    while our_turn is False:
        print('not our turn yet!')
        #wait until there is a hand in the board
        while is_hand is False:
            # print('hear1')
            _, frame = cam.read()
            time.sleep(0.01)
            _, frame = cam.read()
            time.sleep(0.01)
            frame = cut_picture_2(frame)
            is_hand = is_hand_in_the_field(refrence, frame)
        print("hand in")
        # wait until there is no hand in the board
        while is_hand is True:
            _, frame = cam.read()
            time.sleep(0.01)
            _, frame = cam.read()
            time.sleep(0.01)
            frame = cut_picture_2(frame)
            is_hand = is_hand_in_the_field(refrence, frame)
        print("hand out")

        #check
        _, frame = cam.read()
        time.sleep(0.01)
        _, frame = cam.read()
        time.sleep(0.01)
        # frame = shit.cut_edges(frame, CUT_R)
        circles_N = num_of_circles(frame)
        print("circles_N = " + str(circles_N))
        #if legal
        if circles_N == last_num_of_circles + 1:
            new_board = shit.extract_board(frame)
            return new_board
        else:
            print('not our turn yet')
            return continue_when_it_is_our_turn(last_num_of_circles)

    return shit.extract_board(frame)


