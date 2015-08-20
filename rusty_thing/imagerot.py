#!/usr/bin/env python
import sys
sys.path.append(sys.path[0]+"/..")
import cv2
from sensors.potentiometer import Potentiometer


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    r = Potentiometer()
    while ret:
        rot = r.mapped()
        print rot
        mat = cv2.getRotationMatrix2D((frame.shape[1]/2, frame.shape[0]/2), rot, 1.0)
        frame = cv2.warpAffine(frame, mat, (frame.shape[1], frame.shape[0]))
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
        ret, frame = cap.read()


