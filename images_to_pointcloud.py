import cv2
from stereovision.blockmatchers import StereoBM, StereoSGBM
from stereovision.calibration import StereoCalibration
from stereovision.stereo_cameras import CalibratedPair
from stereovision.ui_utils import STEREO_BM_FLAG

if __name__ == '__main__':
    image_pair = [cv2.imread(image) for image in ['./test/left_test.jpg', './test/right_test.jpg']]
    calib_folder = 'calibration_result'

    use_stereobm = False
    bm_settings = 'bm_setting'

    if use_stereobm:
        block_matcher = StereoBM()
    else:
        block_matcher = StereoSGBM()
    if bm_settings:
        block_matcher.load_settings(bm_settings)

    camera_pair = CalibratedPair(None,
                                 StereoCalibration(input_folder=calib_folder),
                                 block_matcher)
    rectified_pair = camera_pair.calibration.rectify(image_pair)
    points = camera_pair.get_point_cloud(rectified_pair)
    points = points.filter_infinity()
    points.write_ply('./test/test_poc')
