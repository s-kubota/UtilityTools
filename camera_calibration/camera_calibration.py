import numpy as np
import cv2
import os
import glob

cols = 7
rows = 6

dir_path_input = 'data/input'

def camera_calibration(cols, rows, dir_path_input, ext='jpg'):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((rows * cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    obj_points = [] # 3d point in real world space
    img_points = [] # 2d points in image plane.

    input_path = os.path.join(dir_path_input, '*.jpg')
    images = glob.glob(input_path)
    digit = len(str(len(images)))

    # Find pattern in chess board
    dir_path_corners = 'data/result/corners'
    base_name_corners = 'detected_corners'
    os.makedirs(dir_path_corners, exist_ok=True)
    base_path_corners = os.path.join(dir_path_corners, base_name_corners)
    print("Finding pattern...")
    n = 0
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            obj_points.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1), criteria)
            img_points.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (cols,rows), corners2, ret)
            cv2.imwrite('{}_{}.{}'.format(base_path_corners,
                                        str(n).zfill(digit), ext), img)
        n += 1
    
    # Calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,
                                                    gray.shape[::-1], None, None)
    
    # Undistortion
    dir_path_undistorted = 'data/result/undistorted'
    base_name_undistorted = 'undistorted_img'
    os.makedirs(dir_path_undistorted, exist_ok=True)
    base_path_undistorted = os.path.join(dir_path_undistorted, base_name_undistorted)
    print("Undistorting...")
    n = 0
    for fname in images:
        img = cv2.imread(fname)
        h,  w = img.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(
                                            mtx, dist, (w, h), 1, (w, h))
        
        # undistort
        dst = cv2.undistort(img, mtx, dist, None, new_camera_mtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite('{}_{}.{}'.format(base_path_undistorted,
                                        str(n).zfill(digit), ext), dst)
        n += 1

# Call the main function
camera_calibration(cols, rows, dir_path_input)