import cv2
import RPi.GPIO as gp
import copy
import time
from picamera import PiCamera
from picamera.array import PiRGBArray


def change_cam(setting):

    for pin in setting.keys():
        gp.output(pin, setting[pin])

    return


class StereoPair(object):

    """
    A stereo pair of cameras.

    This class allows both cameras in a stereo pair to be accessed
    simultaneously. It also allows the user to show single frames or videos
    captured online with the cameras. It should be instantiated with a context
    manager to ensure that the cameras are freed properly after use.
    """

    #: Window names for showing captured frame from each camera
    windows = ["{} camera".format(side) for side in ("Left", "Right")]
    _setting = {}

    def __init__(self, devices, capture):
        """
        Initialize cameras.

        ``devices`` is an iterable containing the device numbers.
        """

        for num in devices.keys():
            self._setting[num] = copy.deepcopy(devices[num])
            # self.capture = cv2.VideoCapture(0)
        
        self.capture = capture
        self.capture.resolution = (640, 480)
        # self.capture.framerate = 90
        
        self.raw = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.capture.release()
        for window in self.windows:
            cv2.destroyWindow(window)

    def get_frames(self):
        """Get current frames from cameras."""
        frames = []
        for c in [0, 1]:
            # time.sleep(0.01)
            change_cam(self._setting[c])
            # frames.append(self.capture.read()[1])
            with PiRGBArray(self.capture) as raw:
                self.capture.capture(raw, 'bgr')
                frames.append(raw.array)
            # time.sleep(0.01)
        return frames

    def show_frames(self, wait=0):
        """
        Show current frames from cameras.

        ``wait`` is the wait interval in milliseconds before the window closes.
        """
        for window, frame in zip(self.windows, self.get_frames()):
            cv2.imshow(window, frame)
        cv2.waitKey(wait)

    def show_videos(self):
        """Show video from cameras."""
        while True:
            self.show_frames(1)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            
    def save_frame(self):
        time.sleep(3)
        frames = self.get_frames()
        cv2.imwrite('./left.jpg', frames[0])
        cv2.imwrite('./right.jpg', frames[1])
            
            
if __name__ == '__main__':
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)

    gp.setup(7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)

    setting = {0: {7: False, 11: False, 12: True}, 1: {7: False, 11: True, 12: False}}
    change_cam(setting[0])
    # cap = cv2.VideoCapture(0)
    #if cap.isOpened():
    with PiCamera() as camera:
        sp = StereoPair(setting, camera)
        
        sp.save_frame()
        # sp.show_videos()
        # cv2.destroyAllWindows()
    """
    sp = StereoPair(setting)
    
    sp.show_videos()
    sp.__exit__()
    """
    
    