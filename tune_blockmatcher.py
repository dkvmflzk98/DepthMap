import cv2

from stereovision.blockmatchers import StereoBM, StereoSGBM
from stereovision.calibration import StereoCalibration
from stereovision.ui_utils import find_files, BMTuner, STEREO_BM_FLAG


if __name__ == '__main__':
    calibration = StereoCalibration(input_folder='.\\calibration_result')
    input_files = find_files('.\\test')

    use_stereobm = False

    if use_stereobm:
        block_matcher = StereoBM()
    else:
        block_matcher = StereoSGBM()
    image_pair = [cv2.imread(image) for image in input_files[:2]]
    input_files = input_files[2:]
    rectified_pair = calibration.rectify(image_pair)
    tuner = BMTuner(block_matcher, calibration, rectified_pair)

    while input_files:
        image_pair = [cv2.imread(image) for image in input_files[:2]]
        rectified_pair = calibration.rectify(image_pair)
        tuner.tune_pair(rectified_pair)
        input_files = input_files[2:]

    for param in block_matcher.parameter_maxima:
        print("{}\n".format(tuner.report_settings(param)))

    block_matcher.save_settings('bm_setting')
