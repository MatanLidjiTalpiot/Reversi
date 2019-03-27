import cv2
import time


cam = cv2.VideoCapture(0)
print('ready')
i = 0
while True:
    _, frame = cam.read()
    cv2.imshow('img',frame)
    cv2.waitKey(10)
    if i % 100 == 0:
        cv2.imwrite('data_for_palti' + str(i)+'.jpg', frame)
    i += 1

