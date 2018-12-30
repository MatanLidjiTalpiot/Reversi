import cv2
import time


class MyCamera:  # a singelton of the camera
    _cam = None

    @staticmethod
    def get_camera():
        """return the camera instance"""
        if MyCamera._cam is None:  # make sure that the camera is initialized only once
            MyCamera._cam = MyCamera.__initial_camera()
        return MyCamera._cam

    @staticmethod
    def __initial_camera():
        """initialize the camera should be called only once from get_camera
        dont call it from the outside
        :return the camera after initialize (delay 0.5 sec)"""
        print("initializing camera")
        camera = cv2.VideoCapture(0)
        print("camera ", camera)
        time.sleep(0.5)
        return camera
