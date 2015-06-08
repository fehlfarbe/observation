import cv2
import numpy as np


cap = cv2.VideoCapture(0)
ret, frame = cap.read()

average = np.float32(frame)

while ret:
    
    frame_blurred = cv2.GaussianBlur(frame, (5,5), 5.0 )
    cv2.accumulateWeighted(frame_blurred, average, 0.05)
    diff = cv2.absdiff(frame_blurred, cv2.convertScaleAbs(average))
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, diff = cv2.threshold(diff_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    if ret >= 5:
        contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) >= 10:
                rect = cv2.boundingRect(c)
                cv2.drawContours(frame, [c], -1, (255, 0, 0), 1)
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 0), 1)
    
    
    cv2.imshow("frame", frame)
    cv2.imshow("frame_blurred", frame_blurred)
    cv2.imshow("diff", diff)
    cv2.waitKey(1)
    
    
    ret, frame = cap.read()