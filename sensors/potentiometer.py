'''
Created on 20.08.2015

@author: kolbe
'''
import RPi.GPIO as GPIO
import time
import numpy
from threading import Thread

class Potentiometer(object):

    a_pin = 18
    b_pin = 23

    values = [0, ]
    values_length = 60
    _thread = None
    _running = False

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
        '''
        vals = []
        for i in range(5):
            v = self.analog_read()
            v = min(self.max, v)
            v = max(self.min, v)
            vals.append(v)
        return numpy.median(vals)
        '''
        #return 0
        return numpy.median(self.values)

    def mapped(self, minimum=0, maximum=360):
        val = self.value() - self.min
        interval = self.max-self.min
        val = float(maximum)/interval * val
        return val

    def _update_values(self):
        print "start thread"
        self._running = True
        while self._running:
            v = self.analog_read()
            if len(self.values) > self.values_length:
                self.values.pop(0)
            self.values.append(v)
            time.sleep(0.001)
        print "stop thread"

    def __enter__(self):
        if self._thread is None:
            self._thread = Thread(target=self._update_values)
            self._thread.start()
        return self

    def __exit__(self, type, value, traceback):
        print "exit called"
        self._running = False
        if self._thread is not None:
            self._thread.join()
        return False

