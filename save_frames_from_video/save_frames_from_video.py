import cv2
import os

def save_frames_from_video(video_path, start_time, stop_time, step_frame,
                     dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video couldn't be opened.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: fps is 0.")
        return

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_len_sec = frame_count / fps
    
    print("Video info:")
    print("  FPS:", fps)
    print("  Video length [s]:", video_len_sec)

    start_frame = int(start_time * fps)
    stop_frame = int(stop_time * fps)

    if start_frame < 0 or start_frame >= frame_count:
        print("Error: Start time is out of video length.")
        return

    if stop_frame > frame_count:
        stop_frame = frame_count
    
    if stop_frame == start_time:
        stop_frame += 1
    elif stop_frame < start_frame:
        print("Error: Stop time should be more than or equal to start time.")
        return
    
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(frame_count)))

    print("Reading frames...")
    for n in range(start_frame, stop_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
        else:
            return

video_path = 'sample.MP4'
start_time = 0.0 # [s]
stop_time = 0.0 # [s]
step_frame = 10
dir_path = 'data/temp/result'
basename = 'video_frame'

save_frames_from_video(video_path, start_time, stop_time, step_frame, dir_path, basename)