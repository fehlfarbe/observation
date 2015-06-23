#!/usr/bin/env python
import os
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from datetime import datetime
import zipfile
import StringIO
import requests
import threading
from sensors import hcsr04
#from hcsr04 import HCSR04

UPLOAD_URL = 'http://edgi:5000/upload'

#DISTANCE_PIN = 4
DISTANCE_TRIGGER = 18
DISTANCE_ECHO = 24
MIN_DISTANCE = 1.0

def save_image(directory):
	if not os.path.exists(directory):
		try:
			os.mkdir(directory)
		except Exception, e:
			print e

	cv2.imwrite(os.path.join(directory, "%s.jpg" % datetime.now().isoformat()), image)
	
def compress_and_upload(directory):
	f = StringIO.StringIO()
	with zipfile.ZipFile(f, "w") as zf:
		os.chdir(directory)
		for img in os.listdir('.'):
			zf.write( img )
		os.chdir('..')

	r = requests.post(UPLOAD_URL, files={directory : f.getvalue()})
	print "uploaded"


if __name__ == '__main__':
	
	with hcsr04.HCSR04(trigger_pin=DISTANCE_TRIGGER, echo_pin=DISTANCE_ECHO) as d:
		
		# initialize the camera and grab a reference to the raw camera capture
		camera = PiCamera()
		camera.vflip = False
		camera.hflip = False
	
		# allow the camera to warmup
		time.sleep(0.1)
		
		# capture initial frame
		rawCapture = PiRGBArray(camera)
		camera.capture(rawCapture, format="bgr")
		image = rawCapture.array
	
		# init variables
		detected = False
		detected_dt = datetime.now().isoformat()
		distance = 0
		
		# start loop
		while True:
			distance = d.average_distance()
			#print "distance ", distance
			print distance, "m"
			if distance <= MIN_DISTANCE:
				print "grab"
				rawCapture = PiRGBArray(camera)
				# grab an image from the camera
				camera.capture(rawCapture, format="bgr")
				image = rawCapture.array
				# display the image on screen and wait for a keypress
				#cv2.imshow("Image", image)
				#cv2.waitKey(1)
				print "detected...save image"
				if not detected:
					detected_dt = datetime.now().isoformat()
				detected = True
				save_image(detected_dt)
				time.sleep(0.25)
			elif detected:
				print "detection stopped...upload images"
				t = threading.Thread(target=compress_and_upload, args=(detected_dt,))
				t.start()
				detected = False
