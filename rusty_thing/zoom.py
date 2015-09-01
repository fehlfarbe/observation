#!/usr/bin/env python
import sys
sys.path.append(sys.path[0]+"/..")
from optparse import OptionParser
import cv2
from sensors.potentiometer import Potentiometer

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
    
def mapped(low, up, value):
    val = value - low
    upper = up - low
    return max((0.95/upper) * float(val), 0)
    

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--camera", dest="camera", type="int", default=0,
                      help="Camera ID")
    parser.add_option("-f", "--fullscreen", dest="fullscreen",
                      help="Fullscreen window", action="store_true")
    parser.add_option("-l", "--limit", dest="limit", type="float", default=0.9,
                      help="Upper limit for zoom (0-1.0)")
    parser.add_option("--lower", dest="lower", type="float", default=100,
                      help="Lower limit for zoom sensor")
    parser.add_option("--upper", dest="upper", type="float", default=200,
                      help="Upper limit for zoom sensor")   

    (options, args) = parser.parse_args()
    
    ### open capture device
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    print "image size ", frame.shape
    
    if options.fullscreen:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

    with Potentiometer(minimum=options.lower, maximum=options.upper) as r:
        while ret:
            #if rot >= options.upper or rot < options.lower:
            #    step = -step
            #rot += step
            rot = r.value()
            print int(rot), options.upper
            rot = min(options.upper, rot)
            #rot = mapped(options.lower, options.upper, rot)
            rot_mapped = mapped(options.lower, options.upper, rot)
            print rot, rot_mapped
            zoomed = zoom(frame, rot_mapped)
            cv2.imshow(WINDOW_NAME, zoomed)
            #cv2.imshow("frame", frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
            ret, frame = cap.read()
