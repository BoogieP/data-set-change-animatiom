import os
import subprocess

import cv2
from tqdm import tqdm


# make a video from files found in the specified folder
# note : files should be in alphabetic order
# note : folder name should NOT end with /
# ONLY a path to the folder is needed
# todo maybe parallelise the video encoding process
def make_vid(folder_name, frame_Rate):
    list = os.listdir(folder_name)
    list.sort()
    frame_count = len(list)
    folder_name += '/'

    # video making code
    current_frame = 0
    im = cv2.imread(folder_name + list[0])
    height, width, layers = im.shape
    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    vid = cv2.VideoWriter('.vid.mkv', fourcc, frame_Rate, (width, height))
    for i in tqdm(list):
        im = cv2.imread(folder_name + i)
        vid.write(im)
        current_frame += 1

    cv2.destroyAllWindows()
    vid.release()


# function to dispose of used frames
# inside the specifed folder
def delete_files(folder_name):
    l = os.listdir(folder_name)
    folder_name += '/'
    for i in l:
        os.remove(folder_name + i)


# use ffmpeg for compression
def compress_to_vp9(video_in, output):
    print("Compressing video!")
    commands = 'ffmpeg -y -i {} -c:v libvpx-vp9 -crf 28 -c:a aac -b:a 128k {}' \
        .format(video_in, output) \
        .split(sep=' ')
    null_file = open(os.devnull, 'w')
    subprocess.run(commands, stdout=null_file, stderr=null_file, stdin=null_file)
