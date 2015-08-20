'''
Created on 20.08.2015

@author: kolbe
'''
import RPi.GPIO as GPIO
import time
import numpy

class Potentiometer(object):

    a_pin = 18
    b_pin = 23

    def __init__(self, a=18, b=23, minimum=24, maximum=280):

        self.a_pin = a
        self.b_pin = b
        self.min = minimum
        self.max = maximum
        GPIO.setmode(GPIO.BCM)


    def discharge(self):
        GPIO.setup(self.a_pin, GPIO.IN)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.output(self.b_pin, False)
        time.sleep(0.005)

    def charge_time(self):
        GPIO.setup(self.b_pin, GPIO.IN)
        GPIO.setup(self.a_pin, GPIO.OUT)
        count = 0
        GPIO.output(self.a_pin, True)
        while not GPIO.input(self.b_pin):
            count += 1
        return count

    def analog_read(self):
        self.discharge()
        return self.charge_time()

    def value(self):
        vals = []
        for i in range(5):
            v = self.analog_read()
            v = min(self.max, v)
            v = max(self.min, v)
            vals.append(v)
        return numpy.median(vals)

    def mapped(self, minimum=0, maximum=360):
        val = self.value() - self.min
        interval = self.max-self.min
        val = float(maximum)/interval * val
        return val