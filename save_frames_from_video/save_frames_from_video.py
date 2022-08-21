import cv2
import os

def save_frames_from_video(video_path, start_sec, stop_sec, duration_sec, step_fps,
                     dir_path, base_name, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video couldn't be opened.")
        return

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps == 0:
        print("Error: Video fps is 0.")
        return

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_len_sec = frame_count / video_fps
    
    print("Video info:")
    print("  FPS:", video_fps)
    print("  Video length [s]:", video_len_sec)

    if start_sec < 0.0 or start_sec >= video_len_sec:
        print("Error: Start time is out of video length.")
        return
    
    if duration_sec > 0.0:
        stop_sec = start_sec + duration_sec

    if stop_sec == start_sec:
        stop_sec += 1 / video_fps
    elif stop_sec < start_sec:
        print("Error: Stop time should be more than or equal to start time.")
        return
    
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, base_name)

    digit = len(str(int(frame_count)))

    if step_fps <= 0.0:
        step_fps = video_fps
    elif step_fps > video_fps:
        print("Warning: step fps is more than video fps. So, video fps will be used.")
        step_fps = video_fps
    
    step_sec = 1.0 / step_fps

    print("Reading frames...")
    sec = start_sec
    while sec < stop_sec:
        n = round(video_fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
        else:
            return
        sec += step_sec

video_path = 'sample.MP4'
start_sec = 0.0 # [s]
stop_sec = 0.0 # [s]
duration_sec = 0.0 # If duration_sec is more than 0.0, stop_sec will be ignored. [s]
step_fps = 1.0 # If step_fps is 0.0, video fps will be used.
dir_path = 'data/temp/result'
base_name = 'video_frame'

save_frames_from_video(video_path, start_sec, stop_sec, duration_sec, step_fps, dir_path, base_name)