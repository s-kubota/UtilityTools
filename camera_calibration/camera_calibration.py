import numpy as np
import cv2
import os
import glob

dir_path_input = ''

def camera_calibration(dir_path_input):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    dir_path_corners = 'data/result/corners'
    base_name_corners = 'detected_corners'
    ext = 'jpg'

    os.makedirs(dir_path_corners, exist_ok=True)
    base_path_corners = os.path.join(dir_path_corners, base_name_corners)

    input_path = os.path.join(dir_path_input, '*.jpg')
    images = glob.glob(input_path)
    digit = len(str(len(images)))

    print("Processing...")
    n = 0
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7,6), corners2, ret)
            cv2.imwrite('{}_{}.{}'.format(base_path_corners,
                                        str(n).zfill(digit), ext), img)
        n += 1

# Call the main function
camera_calibration(dir_path_input)