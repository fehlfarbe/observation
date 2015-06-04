'''
Created on 04.06.2015

@author: kolbe
'''
import cv2
import picamera
import picamera.array


if __name__ == '__main__':
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            #camera.resolution = (320, 240)
    
            while True:
                camera.capture(stream, 'bgr', use_video_port=True)
                # stream.array now contains the image data in BGR order
                cv2.imshow('frame', stream.array)
                k = cv2.waitKey(1)
                if k == 27:
                    break
                # reset the stream before the next capture
                stream.seek(0)
                stream.truncate()
    
            cv2.destroyAllWindows()