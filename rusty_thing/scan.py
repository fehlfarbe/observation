#!/usr/bin/env python
import sys
sys.path.append(sys.path[0]+"/..")
from optparse import OptionParser
import cv2
#from sensors.potentiometer import Potentiometer

WINDOW_NAME = "frame"

def scan(frame, f):
    h, w = frame.shape[:2]
    h_start = int(h*f)
    cv2.rectangle(frame, (0, h_start), (w, h), (0,0,0), -1)
    
    return frame
    
STEP = 0.01

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--camera", dest="camera", type="int", default=0,
                      help="Camera ID")
    parser.add_option("-f", "--fullscreen", dest="fullscreen",
                      help="Fullscreen window", action="store_true") 

    (options, args) = parser.parse_args()
    
    ### open capture device
    cap = cv2.VideoCapture(options.camera)
    ret, frame = cap.read()
    
    if options.fullscreen:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

    f = 0.0
    while ret:
        if f >= 1:
            f = 0.0
        f += STEP
        scan(frame, f)
        cv2.imshow(WINDOW_NAME, frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
        ret, frame = cap.read()
