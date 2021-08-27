from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import sys
import numpy as np
import cv2
import os

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
        count = 1
        with open('data\\body_joints.csv','w') as f:
            f.close()

        while not self._done:

            # --- Getting frames and body joints
            if self._kinect.has_new_color_frame():
                IR_frame = self._kinect.get_last_infrared_frame()
                RGB_frame = self._kinect.get_last_color_frame()
                self._bodies = self._kinect.get_last_body_frame()

                XY_points = []
                if self._bodies is not None:
                    for i in range(0, self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                    
                        joints = body.joints 
                        # convert joint coordinates to color space 
                        joint_points = self._kinect.body_joints_to_color_space(joints)
                       
                        XY_points = self.draw_body(joint_points)
                    if not XY_points:
                        XY_points = [(0,0)]*25
                    with open('data\\body_joints.csv','ab') as f:
                        f.write(','.join([str(x) +' '+ str(y) for x,y in XY_points])+'\n')

                RGB_frame = self._kinect.get_last_color_frame()
                RGB_frame = RGB_frame.reshape((self._kinect.color_frame_desc.Height, self._kinect.color_frame_desc.width, 4),order='C')
                frame = cv2.cvtColor(RGB_frame, cv2.COLOR_BGRA2BGR)
                #cap.write(frame)
                cv2.imshow('frame',frame)
                
                if cv2.waitKey(1) & 0xFF == ord('w'):
                    IR_f8 = np.uint8(IR_frame.clip(1,4000)/16.)
                    IR_frame8bit = np.dstack((IR_f8,IR_f8,IR_f8))
                    IR_RGB = np.array(IR_frame8bit)
                    IR_RGB = IR_RGB.reshape((self._kinect.infrared_frame_desc.Height, self._kinect.infrared_frame_desc.Width, 3),order='C')
                    cv2.imwrite("data\IR_"+ str(count)+".png", IR_RGB)

                    RGB_frame = RGB_frame.reshape((self._kinect.color_frame_desc.Height, self._kinect.color_frame_desc.width, 4),order='C')
                    cv2.imwrite("data\RGB_"+ str(count)+".png", cv2.cvtColor(RGB_frame, cv2.COLOR_BGRA2BGR))
                    print "Images saved!"
                    #break
                    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    #cap.release()
                    cv2.destroyAllWindows()
                    self._kinect.close()
                    print "End!!"
                    break
                
                count += 1
        self._kinect.close()

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    game = KinectRuntime();
    game.run();
