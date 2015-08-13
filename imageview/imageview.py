'''
Created on 13.08.2015

@author: kolbe
'''
import socket
import cv2
import numpy
import time
from optparse import OptionParser
from threading import Thread


images = {}
running = True

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def recieve_and_save(port):
    global running
    global images
    s = None
    conn = None
    while running:
        if s is None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('localhost', port))
                s.listen(True)
                conn, addr = s.accept()
            except:
                s = None
        
        if conn is not None:
            length = recvall(conn,16)
            if length is None:
                continue
            stringData = recvall(conn, int(length))
            data = numpy.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            images[port] = decimg
            

    if s is not None:
        s.close()
        
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--ports", dest="ports",
                  help="Listen on ports...", default="")
    parser.add_option("-t", "--time", dest="time",
                  help="Time between images", default=3, type="int")

    (options, args) = parser.parse_args()
    ports = options.ports.split(',')
    
    ### setup window
    cv2.namedWindow("SERVER", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("SERVER", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    
    ### start listener threads
    threads = []
    for p in ports:
        p = int(p)
        images[p] = numpy.zeros((100,100))
        t = Thread(target=recieve_and_save, args=(p,))
        t.start()
        threads.append(t)
    
    ### show images
    keys = images.keys()
    current = 0
    key = keys[current]
    t0 = time.time()
    while True:
        if time.time()-t0 >= options.time:
            t0 = time.time()
            current += 1
            key = keys[current % len(keys)]
            print "show port %s" % key
        cv2.imshow('SERVER', images[key])
        k = cv2.waitKey(1)
        if k == 27:
            break
    
    print "shutdown..."
    running = False
    for t in threads:
        t.join()
    cv2.destroyAllWindows() 

