#!/usr/bin/env python
'''
Created on 14.08.2015

@author: kolbe
'''
from threading import Thread
from optparse import OptionParser
import cv2
import numpy
import time
#import gtk


image_buffer = None
image_size = (800, 600)
run = True

def draw_text(text, frame):
    t_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)
    img_size = frame.shape[:2]
    pos = (img_size[1]/2 - t_size[0][0] /2, img_size[0] - t_size[0][1] / 2)
    
    cv2.rectangle(frame, (pos[0], pos[1]-t_size[0][1]), (pos[0]+t_size[0][0], pos[1]+2), (0, 0, 0), -1)
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255))
    
def update_buffer(frame, row, col):
    image_buffer[row*image_size[1]:row*image_size[1]+image_size[1],
                 col*image_size[0]:col*image_size[1]+image_size[0]] = frame
def update_image(addr, nr, show_text=False):
    global image_buffer
    global image_size
        
    row = nr / 2
    col = nr % 2
    
    if show_text:
        frame = numpy.ones((image_size[1], image_size[0], 3), numpy.uint8)
        draw_text("open..."+addr, frame)
        update_buffer(frame, row, col)
    
    ret = False
    while not ret and run:
        print "[%d] open video source %s" % (nr, addr)
        cam = cv2.VideoCapture(addr)
        ret, frame = cam.read()
        if not ret:
            print "[%d] cant't get frame from %s...retry in 2s" % (nr, addr)
            time.sleep(2)
    print "[%d] opened %s" % (nr, addr)

    while ret and run:
        frame = cv2.resize(frame, image_size)
        print "[%d] read frame.." % nr
        #print image_size
        #frame = numpy.ones(image_size, numpy.uint8) * 255
        if show_text:
            draw_text(addr, frame)
            
        update_buffer(frame, row, col)

        ret, frame = cam.read()
    
    print "[%d] shutdown... %s" % (nr, addr)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--addresses", dest="addr",
                  help="Look for streams at address", default="")
    parser.add_option("-f", "--fullscreen", dest="fullscreen",
                  help="Fullscreen", action="store_true")
    parser.add_option("-t", "--text", dest="text",
                  help="Show text (video source)", action="store_true")
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
    if len(addr) > 1:
        image_size = (image_buffer.shape[1]/2, image_buffer.shape[0]/rows)
    else:
        image_size = (image_buffer.shape[1], image_buffer.shape[0])
    
    print rows, image_size
    threads = []
    i=0
    for a in addr:
        t = Thread(target=update_image, args=(a, i, options.text))
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
