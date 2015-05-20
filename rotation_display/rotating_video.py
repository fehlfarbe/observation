'''
Created on 18.05.2015

@author: kolbe
'''
import cv2
import mma7455

def current_rotation():
    # ToDo: read data from accellerometer :)
    rotation = 0.0
    while True:
        yield rotation
        rotation += 0.1
        rotation %= 360

if __name__ == '__main__':
    
    # open first video device
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    # show fullscreen image
    cv2.namedWindow("Image", cv2.WINDOW_OPENGL)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, 1)
    
    # open accelerometer
    mma = mma7455.MMA7455()
    # enter capture loop
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