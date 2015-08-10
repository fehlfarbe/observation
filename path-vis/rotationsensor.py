import RPi.GPIO as GPIO
import time
import numpy

GPIO.setmode(GPIO.BCM)

a_pin = 18
b_pin = 23

class RotationSensor():

	def discharge(self):
	    GPIO.setup(a_pin, GPIO.IN)
	    GPIO.setup(b_pin, GPIO.OUT)
	    GPIO.output(b_pin, False)
	    time.sleep(0.005)
	
	def charge_time(self):
	    GPIO.setup(b_pin, GPIO.IN)
	    GPIO.setup(a_pin, GPIO.OUT)
	    count = 0
	    GPIO.output(a_pin, True)
	    while not GPIO.input(b_pin):
	        count = count + 1
	    return count
	
	def analog_read(self):
	    self.discharge()
            return self.charge_time()

	def value(self):
            l = []
            for i in range(5):
                l.append(self.analog_read())
	    return numpy.median(l)