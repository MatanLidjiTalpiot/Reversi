import cv2
import time
cam = None

def initialize_camera():
    global cam
    cam = cv2.VideoCapture(0)
    time.sleep(1)


def get_camera():
    return cam