from ImageProcessing import *
take_grayscale_pic()
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
    refrence = cut_picture_2(refrence)
    pic = cut_picture_2(pic)
    if distMap(pic, refrence) >= sdThresh:
        return True
    return False


font = cv2.FONT_HERSHEY_SIMPLEX


def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:, :, 0] ** 2 + diff32[:, :, 1] ** 2 + diff32[:, :, 2] ** 2) / np.sqrt(
        255 ** 2 + 255 ** 2 + 255 ** 2)
    dist = np.uint8(norm32 * 255)
    return dist


def num_of_circles():

    circles = filter_circles(find_circles())
    return

def is_our_turn(num_of_circles):
    gray_refrence = take_grayscale_pic()
    colored_refrence = take_color_pic()
    rval, colored_pic = cam.read()
    is_hand = is_hand_in_the_field(colored_refrence,colored_pic)
    our_turn = False
    while
    while is_hand is False:
        rval, colored_pic = cam.read()
        is_hand = is_hand_in_the_field(colored_refrence, colored_pic)

    while is_hand is True:
        rval, colored_pic = cam.read()
        is_hand = is_hand_in_the_field(colored_refrence, colored_pic)


