'''
Created on 13.08.2015

@author: kolbe
'''
import cv2
import numpy as np
import time
import sys
import socket
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--cam", dest="camera",
                  help="Camera number", default=0, type="int")
    parser.add_option("-w", "--window", dest="window",
                      help="Show windows", action="store_true")
    parser.add_option("-n", "--network", dest="network",
                      help="Write images to ip:port")       

    (options, args) = parser.parse_args()
    
    # if network
    sock = None
    if options.network:
        ip, port = options.network.split(':')
        sock = socket.socket()
        print "trying to connect to ", options.network
        try:
            sock.connect((ip, int(port)))
        except Exception, e:
            print "no connection %s" % str(e)
            sock = None
            
    cap = cv2.VideoCapture(options.camera)
    ret, frame = cap.read()
    
    while ret:
        if options.window:
            cv2.imshow("frame", frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
        if sock is not None:
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(imgencode)
            stringData = data.tostring()
            try:
                sock.send( str(len(stringData)).ljust(16))
                sock.send( stringData )
            except Exception, e:
                print "Can't send image data to %s\n%s" % (options.network, e)
        print "send image.."
        
        ret, frame = cap.read()