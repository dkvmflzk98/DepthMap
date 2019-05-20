import cv2
import RPi.GPIO as gp
import copy


def change_cam(setting):

    for num, val in setting:
        gp.setup(num, val)

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

    def __init__(self, devices):
        """
        Initialize cameras.

        ``devices`` is an iterable containing the device numbers.
        """

        for num in devices.keys():
            self._setting[num] = copy.deepcopy(devices[num])
            self.capture = cv2.VideoCapture(0)

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
            change_cam(self._setting[c])
            frames.append(self.capture.read()[1])
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
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break