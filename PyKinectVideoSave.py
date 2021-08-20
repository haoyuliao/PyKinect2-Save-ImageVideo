from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import sys
import numpy as np
import cv2
import os
import atexit

class KinectRuntime(object):
    def __init__(self):
        self._done = False
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Infrared | PyKinectV2.FrameSourceTypes_Body)
        self._bodies = None

    def draw_body(self, jointPoints):
        joints_data = []
        for joint_type in list(jointPoints):
            X,Y = (joint_type.x, joint_type.y)
            joints_data.append((X,Y))
        return joints_data

    def run(self):
        # -------- Main Program Loop -----------
        # --- Getting frames and body joints
        #if self._kinect.has_new_color_frame():
        ###videos###
        cap = cv2.VideoWriter('./Kinect_Color223.mp4', cv2.VideoWriter_fourcc(*'XVID'),50, (1920, 1080))
        while True:
            RGB_frame = self._kinect.get_last_color_frame()
            RGB_frame = RGB_frame.reshape((self._kinect.color_frame_desc.Height, self._kinect.color_frame_desc.width, 4),order='C')
            frame = cv2.cvtColor(RGB_frame, cv2.COLOR_BGRA2BGR)
            cap.write(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                self._kinect.close()
                break
            
filename = 'video111.avi'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')


    filen = 'video.mp4'
    frames_per_second = 24.0
    res = '720p'

    game = KinectRuntime();
    game.run();
