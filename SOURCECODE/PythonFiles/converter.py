# import modules
import os
import sys

import cv2

# import video and convert to ASCII frames
def import_vid(video_path, scale):    
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return

    # ASCII brightness characters
    Chars = " .,'\"*-=+oO0X%$#&@" # 18 chars for 255/15 = 17(+1) levels of brightness
    
    # resolution according to inputted scale
    w = 33*int(scale)
    h = 25*int(scale)

    # main()
    frames = []
    while True:

        # get each frame
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (w, h))

        # convert to ASCII
        ascii_frame = ""
        for y in range(h):
            for x in range(w):
                p = frame[y, x]
                ascii_frame += Chars[p // 15]
            if y < h - 1:
                ascii_frame += "\n"

        frames.append(ascii_frame)
    cap.release()

    # get name from video file
    name = os.path.splitext(os.path.basename(video_path))[0]

    # save animation.txt file
    animations_folder = os.path.join(base_dir, "Animations")
    output_path = os.path.join(animations_folder, "ANIM_" + name + ".txt")
    
    with open(output_path, "w") as f:
        for frame in frames:
            f.write(frame)
            f.write("\n===FRAME===\n")
