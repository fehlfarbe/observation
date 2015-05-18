'''
Created on 18.05.2015

@author: kolbe
'''
import cv2

if __name__ == '__main__':
    
    # open first video device
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    # show fullscreen image
    cv2.namedWindow("Image", cv2.WINDOW_OPENGL)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, 1)
    
    rotation = 0.0
    
    # enter capture loop
    while ret:
        # calculate rotation matrix
        mat = cv2.getRotationMatrix2D((frame.shape[1]/2, frame.shape[0]/2), rotation, 1.0)
        # apply rotation matrix
        frame = cv2.warpAffine(frame, mat, (frame.shape[1], frame.shape[0]))
        
        rotation += 0.2
        rotation %= 360
        
        # show image, abort when ESC key pressed
        cv2.imshow("Image", frame)
        k = cv2.waitKey(1)
        if k == 27: #ESC
            break
        
        # capture next frame
        ret, frame = cap.read()
        
    cap.release()