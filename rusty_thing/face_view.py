#!/usr/bin/env python
'''
Created on 20.08.2015

@author: kolbe
'''
import os
import time
import cv2
import numpy
from optparse import OptionParser

FILE_TYPES = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')
WINDOW_NAME = 'image'

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory",
                      help="Directory where images will be saved", default="./")
    parser.add_option("-p", "--prefix", dest="prefix",
                      help="Filename prefix", default="")
    parser.add_option("-f", "--fullscreen", dest="fullscreen",
                      help="Fullscreen window", action="store_true")
    parser.add_option("-t", "--time", dest="time",
                      help="Time between check for new images in seconds", default=1, type="int")

    (options, args) = parser.parse_args()
    
    if options.fullscreen:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    
    while True:
        directory = os.listdir(options.directory)
        filtered = []
        for f in directory:
            if f.startswith(options.prefix) and f.endswith(FILE_TYPES):
                filtered.append(f)
        filtered = sorted(filtered)
        
        if len(filtered) == 0:
            print "no images with prefix '%s' found in %s, waiting %ds" % \
                    (options.prefix, os.path.abspath(options.directory), options.time)
            time.sleep(options.time)
            continue
        
        try:
            img = cv2.imread(os.path.join(options.directory, filtered[-1]))
            t_size = cv2.getTextSize(filtered[-1], cv2.FONT_HERSHEY_COMPLEX, 0.5, 1)
            print t_size
            img_size = img.shape[:2]
            pos = (img_size[1]/2 - t_size[0][0] /2, img_size[0] - t_size[0][1] / 2)
            cv2.putText(img, filtered[-1], pos, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255))
        except:
            img = numpy.zeros((800, 600))
            
        cv2.imshow(WINDOW_NAME, img)
        k = cv2.waitKey(options.time*1000)
        if k == 27:
            break
        
    print "done."
        
        