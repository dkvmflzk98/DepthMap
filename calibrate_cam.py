from NEU_StereoPair import StereoPair
from stereovision.calibration import StereoCalibrator
import cv2

rows, colums = 9, 6
square_size = 2.4
image_size = (640, 480)

img_left = cv2.imread('./left.jpg')
img_right = cv2.imread('./right.jpg')

calibrator = StereoCalibrator(rows, colums, square_size, image_size)

calibrator.add_corners((img_left, img_right), show_results=True)
calibration = calibrator.calibrate_cameras()
print(calibration)

avg_error = calibrator.check_calibration(calibration)
print(avg_error)

calibration.export('./calibration_result')