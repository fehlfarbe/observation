#!/usr/bin/env python
'''
Created on 14.08.2015

@author: kolbe
'''
from threading import Thread
from optparse import OptionParser
import cv2
import numpy
#import gtk


image_buffer = None
image_size = (800, 600)
run = True


def update_image(addr, nr):
    global image_buffer
    global image_size
    
    cam = cv2.VideoCapture(addr)
    ret, frame = cam.read()
    
    row = nr / 2
    col = nr % 2
    while ret and run:
        frame = cv2.resize(frame, image_size)
        print "[%d] read frame.." % nr
        #print image_size
        #frame = numpy.ones(image_size, numpy.uint8) * 255
        image_buffer[row*image_size[1]:row*image_size[1]+image_size[1],
                     col*image_size[0]:col*image_size[1]+image_size[0]] = frame
        ret, frame = cam.read()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--addresses", dest="addr",
                  help="Look for streams at address", default="")
    parser.add_option("-f", "--fullscreen", dest="fullscreen",
                  help="Fullscreen", action="store_true")

    (options, args) = parser.parse_args()
    addr = options.addr.split(',')
    
    ### get screen size
    #window = gtk.Window()
    # the screen contains all monitors
    #screen = window.get_screen()
    #screen_width, screen_height = gtk.gdk.screen_width(), gtk.gdk.screen_height()
    #print screen_width, screen_height
    screen_width, screen_height = (1280, 1024)
    image_buffer = numpy.zeros((screen_height, screen_width, 3), dtype=numpy.uint8)
    rows = max(len(addr) / 2, 1)
    image_size = (image_buffer.shape[1]/2, image_buffer.shape[0]/rows)
    
    print rows, image_size
    threads = []
    i=0
    for a in addr:
        t = Thread(target=update_image, args=(a, i))
        t.start()
        threads.append(t)
        i+=1
        
    ### setup screen
    if options.fullscreen:
        cv2.namedWindow("frames", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("frames", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
        
    while True:
        try:
            cv2.imshow("frames", image_buffer)
            k = cv2.waitKey(1)
            if k == 27:
                break
        except KeyboardInterrupt:
            break
    
    run = False
    for t in threads:
        print "stop thread", t
        t.join()
        
    print "done"
