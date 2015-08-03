#!/usr/bin/env python
'''
Created on 29.06.2015

@author: kolbe

ToDo: extract faces
'''
import os
import time
import cv2
import numpy as np
import itertools
from optparse import OptionParser
import pigpio

basepath = os.path.dirname(os.path.realpath(__file__))
    
frontal_face_cascade = cv2.CascadeClassifier(os.path.join(basepath, '../res/haarcascade_frontalface_default.xml'))
profile_face_cascade = cv2.CascadeClassifier(os.path.join(basepath, '../res/haarcascade_profileface.xml'))

IMAGE_SIZE = (320, 240)
MINIMUM_FACE_TIME = 3
IMAGE_DESTINATION = "./"
CAMERA_NR = 0

FACE_TYPE_FRONTAL = "frontal"
FACE_TYPE_PROFILE = "profile"

SERVO_GPIO = 4
SERVO_OFFSET = 1100
SERVO_LIMIT = 1400


class Face(object):
    
    rect = (0,0,0,0)
    offset = (0, 0)
    newid = itertools.count().next
    relocated = 0
    t0 = 0
    saved = False
    face_type = None
    
    def __init__(self, rectangle, offset=(0, 0), face_type=None):
        self.rect = rectangle
        self.offset = offset
        self.id = Face.newid()
        self.color = np.random.randint(0,255,3).tolist()
        self.t0 = time.time()
        self.saved = False

        
    def __getitem__(self, key):
        return self.rect[key]
    
    def __setitem__(self, key, val):
        self.rect[key] = val
        
    def update(self, rect):
        self.rect = rect
        self.relocated += 1
        
    def scaled(self, factor, offset=True):
        scaled = []
        for r in self.rect:
            scaled.append(int(r*factor))
            
        if offset:
            scaled[0] += int(self.offset[0]*factor)
            scaled[1] += int(self.offset[1]*factor)
            
        return tuple(scaled)
    
    def cutFace(self, frame, scale_factor=None):
        rx, ry, rw, rh = self.extendedROI()
        if scale_factor is not None:
            rx = int(rx*scale_factor)
            ry = int(ry*scale_factor)            
            rw = int(rw*scale_factor)
            rh = int(rh*scale_factor)
        return frame[ry:ry+rh, rx:rx+rw].copy()
    
    def extendedROI(self, factor=1.5):
        x,y,w,h = self.rectWithOffset()
        m_x = x + w/2
        m_y = y + h/2
        w = int(w*factor)
        h = int(h*factor)
        x = max(0, m_x-w/2)
        y = max(0, m_y-h/2)
        return (x,y,w,h)
    
    def rectWithOffset(self):
        r = list(self.rect)
        r[0] += self.offset[0]
        r[1] += self.offset[1]
        return r
    
    def middlePoint(self, offset=True):
        if offset:
            return (self.rect[0] + self.rect[2]/2 + self.offset[0],
                    self.rect[1] + self.rect[3]/2 + self.offset[1])
        
        return (self.rect[0] + self.rect[2]/2,
                self.rect[1] + self.rect[3]/2)
        
    @property
    def period(self):
        return time.time()-self.t0
        

def getRelativePosition(pos_x, width):
    return (1.0/width) * pos_x

def drawEye(frame, angle):
    height, width = frame.shape[:2]
    m = (width/2, height/2)
    r = min(width/2, height/2)
    
    #reverse angle
    angle = 1.0 - angle
    
    cv2.circle(frame, m, r, (255,255,255), -1)
    cv2.circle(frame, m, r, (0,0,0), 2)
    cv2.circle(frame, (int(angle*width), m[1]), r/2, (255,130,100), -1)
    cv2.circle(frame, (int(angle*width), m[1]), r/3, (0,0,0), -1)
    
def setServoPosition(servo, angle):
    angle = 1.0 - angle
    pos = SERVO_LIMIT-SERVO_OFFSET
    pos *= angle
    pos += SERVO_OFFSET
    print "set servo to ", pos
    servo.set_servo_pulsewidth(SERVO_GPIO,pos)


def detectFrontal(frame):
    return frontal_face_cascade.detectMultiScale(frame, 1.3, 1,
                                                      (cv2.cv.CV_HAAR_DO_CANNY_PRUNING + 
                                                       cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + 
                                                       cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),
                                                      (20,20),
                                                      tuple([x/4 for x in IMAGE_SIZE]))
    
def detectProfile(frame, flipped=True):
    if flipped:
        frame.flip()
    
    faces = profile_face_cascade.detectMultiScale(frame, 1.3, 1,
                                                          (cv2.cv.CV_HAAR_DO_CANNY_PRUNING + 
                                                           cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + 
                                                           cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),
                                                          (20,20),
                                                          tuple([x/4 for x in IMAGE_SIZE]))
    # flip back
    if flipped:
        frame.flip()
        
    return faces

def detectFaces(frame):
    ftype = FACE_TYPE_FRONTAL
    faces = detectFrontal(frame)
    #if faces == ():
    #    faces = detectProfile(frame, flipped=False)
    #    if faces == ():
    #        faces = detectProfile(frame, flipped=False)        
    #    ftype = FACE_TYPE_PROFILE

    return faces, ftype

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--cam", dest="camera",
                  help="Camera number", default=0, type="int")
    parser.add_option("-t", "--tinme",
                  help="Minimum time to save detected face", dest="mintime", 
                  default=3, type="int")
    parser.add_option("-d", "--directory", dest="directory",
                      help="Directory where faces will be saved", default="./")
    parser.add_option("-w", "--window", dest="window",
                      help="Show windows", action="store_true")

    (options, args) = parser.parse_args()
    print options
    MINIMUM_FACE_TIME = options.mintime
    IMAGE_DESTINATION = options.directory
    CAMERA_NR = options.camera
    
    # init camera
    cam = cv2.VideoCapture(CAMERA_NR)    
    ret, frame = cam.read()
    
    # init servo
    servo = pigpio.pi()
    servo.set_mode(SERVO_GPIO, pigpio.OUTPUT)
    
    lastface = None
    lastangle = 0.5
    
    while ret:
        t0 = time.time()
        frame_full = frame
        frame = cv2.resize(frame, IMAGE_SIZE)
        eye = np.zeros(frame.shape, np.uint8)

        faces = ()        
        if lastface is not None:
            roi = lastface.extendedROI()
            rx,ry,rw,rh = roi
            offset = rx, ry
            faces, face_type = detectFaces(frame[ry:ry+rh, rx:rx+rw])
        if faces == ():
            lastface = None
            offset = (0, 0)
            faces, face_type = detectFaces(frame)            

        last = None
        for f in faces:
            if last is None:
                last = f
                continue
            x,y,w,h = f
            if w*h > last[2]*last[3]:
                last = f
        if lastface is not None and last is not None:
            lastface.update(last)
            lastface.offset = offset
            lastface.face_type = face_type
        elif last is not None:
            lastface = Face(last, offset=offset, face_type=face_type)
        else:
            lastface = None
            
        # cut face
        if lastface is not None and lastface.period >= MINIMUM_FACE_TIME and not lastface.saved:
            scale_factor = frame_full.shape[0] / float(frame.shape[0])
            face_image = lastface.cutFace(frame_full.copy(), scale_factor)
            if options.window:
                cv2.imshow("face", face_image)
            cv2.imwrite(os.path.join(IMAGE_DESTINATION, "statue_cam0_face%d_%d.jpg" % (lastface.id, lastface.t0)), face_image)
            lastface.saved = True
        
                   
        # draw face
        if lastface is not None:
            x,y,w,h = lastface
            rx, ry, rw, rh = lastface.extendedROI()
            cv2.circle(frame, lastface.offset, 2, (255, 255, 255), 3)
            cv2.rectangle(frame, (rx,ry), (rx+rw, ry+rh), lastface.color, 1)
            cv2.circle(frame, lastface.middlePoint(True), w/2, lastface.color, 2)
            cv2.putText(frame, 
                        "ID: %d, %s re: %d, %ds" % (lastface.id, lastface.face_type ,lastface.relocated, lastface.period), 
                        lastface.offset, 
                        1, 
                        1.0, 
                        lastface.color)
            
        # draw eye
        if lastface is not None:
            lastangle = getRelativePosition(lastface.middlePoint(True)[0], frame.shape[1])
            cv2.line(frame, 
                     (frame.shape[1]/2, frame.shape[0]/2),
                     lastface.middlePoint(True),
                     (255, 255, 255), 1)
        drawEye(eye, lastangle)
        setServoPosition(servo, lastangle)
        
        # show images
	if options.window:
	        cv2.imshow("frame", frame)
	        cv2.imshow("eye", eye)
	        k = cv2.waitKey(1)
	        if k == 27:
	            break
        
        # print frames per seconds
        print "%.2ffps" % (1.0/(time.time()-t0))
        
        # read new frame
        ret, frame = cam.read()
