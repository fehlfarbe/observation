#!/usr/bin/env python
import sys
sys.path.append(sys.path[0]+"/..")
from optparse import OptionParser
import cv2
#from sensors.potentiometer import Potentiometer

WINDOW_NAME = "frame"

def zoom(frame, f):
    h, w = frame.shape[:2]
    h_m = h/2
    w_m = w/2
    h_new = max(1, int(h - h*f))
    w_new = max(1, int(w - w*f))
    h_new_m = h_new/2
    w_new_m = w_new/2
    #print h_m-h_new_m, h_new, h, h_m-h_new_m+h_new
    #print w_m-w_new_m, w_new, w, w_m-w_new_m+w_new
    #cv2.rectangle(frame, (w_m-w_new_m, h_m-h_new_m),
    #                        (w_m-w_new_m+w_new, h_m-h_new_m+h_new),
    #                        (0, 255, 0), 2)
    return frame[h_m-h_new_m:h_m+h_new_m,
                 w_m-w_new_m:w_m+w_new_m]
    

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--camera", dest="camera", type="int", default=0,
                      help="Camera ID")
    parser.add_option("-f", "--fullscreen", dest="fullscreen",
                      help="Fullscreen window", action="store_true")
    parser.add_option("-l", "--limit", dest="limit", type="float", default=0.9,
                      help="Upper limit for zoom (0-1.0)")    

    (options, args) = parser.parse_args()
    
    ### open capture device
    cap = cv2.VideoCapture(options.camera)
    ret, frame = cap.read()
    
    if options.fullscreen:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

    #r = Potentiometer()
    rot = 0.0
    step = 0.005
    upper_limit = options.limit-step
    while ret:
        if rot >= upper_limit or rot < 0:
            step = -step
        rot += step
        zoomed = zoom(frame, rot)
        cv2.imshow(WINDOW_NAME, zoomed)
        #cv2.imshow("frame", frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
        ret, frame = cap.read()
