import cv2
import os

def save_frames_from_video(video_path, start_frame, stop_frame, step_frame,
                     dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video couldn't be opened.")
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    print("Reading frames...")
    for n in range(start_frame, stop_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
        else:
            return

video_path = 'sample.MP4'
start_frame = 0
stop_frame = 100
step_frame = 10
dir_path = 'data/temp/result'
basename = 'video_frame'

save_frames_from_video(video_path, start_frame, stop_frame, step_frame, dir_path, basename)