'''
Created on 29.06.2015

@author: kolbe
'''
import time
import cv2
import numpy as np

    
frontal_face_cascade = cv2.CascadeClassifier('../res/haarcascade_frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier('../res/haarcascade_profileface.xml')

IMAGE_SIZE = (320, 240)

def getAngle(pos_x):
    return (2.0 / IMAGE_SIZE[0]) * pos_x - 1

def drawEye(frame, angle):
    m = (frame.shape[1]/2, frame.shape[0]/2)
    r = min(frame.shape[1]/2, frame.shape[0]/2)
    offset = int(r*angle)
    cv2.circle(frame, m, r, (255,255,255), -1)
    cv2.circle(frame, m, r, (0,0,0), 2)
    cv2.circle(frame, (m[0]-offset, m[1]), r/2, (255,130,100), -1)
    cv2.circle(frame, (m[0]-offset, m[1]), r/3, (0,0,0), -1)
    


def getROI(face):
    x,y,w,h = face
    m_x = x + w/2
    m_y = y + h/2
    w = int(w*1.5)
    h = int(h*1.5)
    x = max(0, m_x-w/2)
    y = max(0, m_y-h/2)
    return (x,y,w,h)


def detectFrontal(frame):
    return frontal_face_cascade.detectMultiScale(frame, 1.3, 1,
                                                      (cv2.cv.CV_HAAR_DO_CANNY_PRUNING + 
                                                       cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + 
                                                       cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),
                                                      (40,40),
                                                      tuple([x/2 for x in IMAGE_SIZE]))
    
def detectProfile(frame):
    return profile_face_cascade.detectMultiScale(frame, 1.3, 1,
                                                          (cv2.cv.CV_HAAR_DO_CANNY_PRUNING + 
                                                           cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + 
                                                           cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),
                                                          (40,40),
                                                          tuple([x/2 for x in IMAGE_SIZE]))

def detectFaces(frame):
    faces = detectFrontal(frame)
    if faces == ():
        faces = detectProfile(frame)
    return faces

if __name__ == '__main__':
    
    cam = cv2.VideoCapture(3)

    
    ret, frame = cam.read()

    
    lastface = None
    lastangle = 0
    offset = (0, 0)
    
    while ret:
        t0 = time.time()
        frame = cv2.resize(frame, IMAGE_SIZE)
        eye = np.zeros(frame.shape, np.uint8)

        faces = ()        
        if lastface is not None:
            roi = getROI(lastface)
            rx,ry,rw,rh = roi
            offset = rx, ry
            cv2.rectangle(frame, (rx,ry), (rx+rw, ry+rh), (255,255,255), 1)
            faces = detectFaces(frame[ry:ry+rh, rx:rx+rw])
        if faces == ():
            color = np.random.randint(0,255,3).tolist()
            lastface = None
            offset = (0, 0)
            faces = detectFaces(frame)
            

        last = None
        for f in faces:
            if last is None:
                last = f
                continue
            x,y,w,h = f
            if w*h > last[2]*last[3]:
                last = f
        lastface = last
        if lastface is not None:
            lastface[0] += offset[0]
            lastface[1] += offset[1]            
        # draw face
        if lastface is not None:
            x,y,w,h = lastface
            cv2.circle(frame, offset, 2, (255, 255, 255), 3)
            cv2.circle(frame, (x+w/2, y+h/2), w/2, color, 2)
            #print x,y,w,h
            
        # draw eye
        if lastface is not None:
            lastangle = getAngle(lastface[0])
        drawEye(eye, lastangle)
        
        cv2.imshow("frame", frame)
        cv2.imshow("eye", eye)
        k = cv2.waitKey(1)
        if k == 27:
            break
        print "%.2ffps" % (1.0/(time.time()-t0))
        #print frame.shape
        ret, frame = cam.read()
