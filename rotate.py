# import the necessary packages
import numpy as np
import cv2
# import ImageProcessing


def show_image(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")


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


def find_points(gray):
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
            approx = cv2.approxPolyDP(i, 0.06* peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    # print(type(biggest), biggest.shape)
    return biggest






# def rotate(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
#     _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     # print(len(useless))
#     # print(contours)
#     # print(len(hierarchy))
#     biggest = None
#     max_area = 0
#     for i in contours:
#         area = cv2.contourArea(i)
#         if area > down_th:
#             peri = cv2.arcLength(i, True)
#             approx = cv2.approxPolyDP(i, 0.02 * peri, True)
#             if area > max_area and len(approx) == 4:
#                 biggest = approx
#                 max_area = area
#     biggest = rectify(biggest)
#     print(biggest)
#     ImageProcessing.show_image(img)
#     point = tuple(biggest[1])
#     color = (0, 0, 255)
#     cv2.circle(img, point, 2, color, 3)
#     points1 = [biggest[0],biggest[1]]
#     points2 = [biggest[2],biggest[3]]
#     ImageProcessing.show_image(img)
#
#     h, status = cv2.findHomography(np.array(points1), np.array(points2))
#
#     # retval = cv2.getPerspectiveTransform(biggest, size_of_board)
#     print(gray.shape)
#     print(gray.dtype)
#     warp = cv2.warpPerspective(gray, h, (450, 450))
#     return warp


# c  = cv2.imread('board.jpg')
# gray = cv2.imread('board.jpg',0)
# show_image(c)
#
# points = find_points(gray)
# print(points)
#
# points = points.reshape(4,2)
# for i in points:
#     point = tuple(i)
#     cv2.circle(c,point,2,(0,0,255),3)
# show_image(c)
#
# points = order_points(points)
# c = four_point_transform(c,points)
#
# show_image(c)

def cut_picture1(gray_pic , colord_pic):
    points = find_points(gray_pic)
    points = order_points(points)
    return four_point_transform(colord_pic, points)

# k = cut_picture1(gray,c)

# ImageProcessing.show_image(k)