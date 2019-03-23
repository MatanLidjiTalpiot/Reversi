from ImageProcessing import *
take_grayscale_pic()
import time
sdThresh = 10
x_min = 0
x_max = 0
y_min = 0
y_max = 0
Relevant_area =[x_min, x_max, y_min, y_max]


def cut_picture_2(img):
    #TODO check if it is [x_min:x_max , y_min:y_max] or [y_min:y_max , x_min:x_max]
    return img[y_min : y_max , x_min : x_max]


def is_hand_in_the_field(refrence, pic):
    if distMap(pic, refrence) >= sdThresh:
        return True
    return False


def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:, :, 0] ** 2 + diff32[:, :, 1] ** 2 + diff32[:, :, 2] ** 2) / np.sqrt(
        255 ** 2 + 255 ** 2 + 255 ** 2)
    dist = np.uint8(norm32 * 255)
    return dist


def num_of_circles(board_pic):
    return len(filter_circles(find_circles(board_pic)))


def continue_when_it_is_our_turn(last_num_of_circles):
    ##take refrence picture
    take_grayscale_pic()
    colored_refrence = take_color_pic()
    #cut the refrence
    refrence = cut_picture_2(colored_refrence)

    ##take picture
    rval, colored_pic = cam.read()
    #cut it
    pic = cut_picture_2(pic)

    #initial values
    is_hand = is_hand_in_the_field(refrence,pic)
    our_turn = False

    while our_turn is False:
        print('not our turn yet')
        #wait until there is a hand in the board
        while is_hand is False:
            rval, colored_pic = cam.read()
            pic = cut_picture_2(pic)
            is_hand = is_hand_in_the_field(colored_refrence, colored_pic)
            time.sleep(0.1)

        # wait until there is no hand in the board
        while is_hand is True:
            rval, colored_pic = cam.read()
            pic = cut_picture_2(pic)
            is_hand = is_hand_in_the_field(colored_refrence, colored_pic)
            time.sleep(0.1)

        #check
        board_pic = cutPicture(colored_pic)
        circles_N = num_of_circles(board_pic)
        #if legal
        if circles_N == last_num_of_circles + 1:
            return True
        elif circles_N == last_num_of_circles:
            rval, colored_pic = cam.read()
            pic = cut_picture_2(pic)
            is_hand = is_hand_in_the_field(colored_refrence, colored_pic)
            while is_hand is True:
                rval, colored_pic = cam.read()
                pic = cut_picture_2(pic)
                is_hand = is_hand_in_the_field(colored_refrence, colored_pic)
                time.sleep(0.1)

            board_pic = cutPicture(colored_pic)
            circles_N = num_of_circles(board_pic)
            if circles_N == last_num_of_circles + 1:
                return True
            elif circles_N == last_num_of_circles:
                continue

        #if illegal we check again
        else :
            rval, colored_pic = cam.read()
            pic = cut_picture_2(pic)
            is_hand = is_hand_in_the_field(colored_refrence, colored_pic)
            while is_hand is True:
                rval, colored_pic = cam.read()
                pic = cut_picture_2(pic)
                is_hand = is_hand_in_the_field(colored_refrence, colored_pic)
                time.sleep(0.1)

            board_pic = cutPicture(colored_pic)
            circles_N = num_of_circles(board_pic)
            if circles_N == last_num_of_circles + 1:
                return True
            elif circles_N == last_num_of_circles:
                our_turn = False
            else:
                print ('illegal move')
                return True

    return our_turn

