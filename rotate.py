# import the necessary packages
import numpy as np
import cv2
# import ImageProcessing
POINTS = None


def set_points(four_points):
    global POINTS
    POINTS = four_points
    # print(POINTS)



def show_image(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    if type(pts) != np.ndarray:
        pts = np.array(pts)

    pts = pts.reshape(4,2)

    # print("pts: \n", pts)
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    # print("s:\n",s)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

down_th = 100
size_of_board = np.array([ [0,0],[320,0],[320,320],[0,320] ],np.float32)


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def find_points(gray,voodoo):
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(useless))
    # print(contours)
    # print(len(hierarchy))
    biggest = None
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > down_th:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.06 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    # print(type(biggest), biggest.shape)
    return biggest

def draw_points(four_points,colord_pic):
    four_points = four_points.reshape(4, 2)
    for i in range(4):
        point = tuple(four_points[i])
        # print(point)
        cv2.waitKey(30)
        color = [0, 0, 0]
        if i !=3:
            color[i] = 255
        else:
            color = [255, 0 ,255]
        color = tuple(color)
        cv2.circle(colord_pic, point, 2, color, 3)

def cut_picture1(gray_pic , colord_pic, voodoo= 0.05):
    points = find_points(gray_pic,voodoo)
    points = POINTS
    points = points.reshape(4, 2)
    # for i in points:
    #     point = tuple(i)
    #     cv2.circle(colord_pic, point, 2, (0, 0, 255), 3)
    # show_image(colord_pic)
    points = order_points(points)
    return four_point_transform(colord_pic, points)


# points = points.reshape(4, 2)
# for i in points:
#     point = tuple(i)
#     cv2.circle(c, point, 2, (0, 0, 255), 3)
# show_image(c)
#
# points = order_points(points)
# c = four_point_transform(c, points)
#
# show_image(c)

    # end = False
# voodoo = 0.06
# while not end:
#     colored_pic = cv2.imread('board(1).jpg')
#     img = cv2.imread('board(1).jpg', 0)
#     show_image(colored_pic)
#     img = cut_picture1(img, img,voodoo)
#     colored_pic = cut_picture1(cv2.cvtColor(colored_pic, cv2.COLOR_RGB2GRAY),colored_pic,voodoo)
#     show_image(colored_pic)
#     ans = input("end or voodoo?")
#     if ans =="1":
#         end = True
#     else:
#         voodoo = float(input("set voodoo"))