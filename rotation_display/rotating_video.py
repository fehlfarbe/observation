'''
Created on 18.05.2015

@author: kolbe
'''
import cv2
import numpy as np
import mma7455
from picamera.array import PiRGBArray
from picamera import PiCamera
import io

if __name__ == '__main__':
    
    # open first video device
    #cap = cv2.VideoCapture(0)
    #ret, frame = cap.read()
    camera = PiCamera()
    
    # show fullscreen image
    cv2.namedWindow("Image", cv2.WINDOW_OPENGL)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, 1)
    
    # open accelerometer
    mma = mma7455.MMA7455()
    # enter capture loop
    stream = io.BytesIO()
    for f in camera.capture_continuous(stream, format="bgr", use_video_port=True):
        stream.seek(0)
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        res = camera.resolution
        data = data.reshape((res[1], res[0], 3))
        
        # show image, abort when ESC key pressed
        cv2.imshow("Image", data)
        k = cv2.waitKey(1)
        if k == 27: #ESC
            break
        
        
        
    '''
    while ret:
        # calculate rotation matrix
        mat = cv2.getRotationMatrix2D((frame.shape[1]/2, frame.shape[0]/2), mma.getValueY(), 1.0)
        # apply rotation matrix
        frame = cv2.warpAffine(frame, mat, (frame.shape[1], frame.shape[0]))        
        
        # show image, abort when ESC key pressed
        cv2.imshow("Image", frame)
        k = cv2.waitKey(1)
        if k == 27: #ESC
            break
        
        # capture next frame
        ret, frame = cap.read()
        
    cap.release()
    '''