# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform


def run():
    """
    Runs OpenPose on all videos in a specified directory. You are required to have OpenPose built, as well as OpenCV
    installed. This script currently only works on Windows. Future work will include building for MACOSX and Linux.
    Place the downloaded models in a models folder, and set the directory.
    """

    # Import Openpose (Windows)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release')
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        import pyopenpose as op

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../models/"

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Path to videos
    vids_path = '...'

    for filename in os.listdir(vids_path):
        key_point_list = []
        cap = cv2.VideoCapture(vids_path + filename)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                datum = op.Datum()
                datum.cvInputData = frame
                opWrapper.emplaceAndPop([datum])
                key_point_list.extend(datum.poseKeypoints.flatten())
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    run()
