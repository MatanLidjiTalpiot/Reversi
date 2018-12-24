import cv2
# cam = cv2.VideoCapture(0)
# while True:
#     check, frame = cam.read()
#
#     cv2.imshow('blabka', frame)
#     cv2.waitKey(0)

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
i = 0
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    i += 1
    if i%100 == 0:
        cv2.imwrite('data' + i.__str__() + '.jpg',frame)
        img =cv2.imread('data' + i.__str__() + '.jpg', 0)
        cv2.imwrite('data_' + i.__str__() + '_gray' + '.jpg', img)
cv2.destroyWindow("preview")