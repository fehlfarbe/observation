'''
Created on 08.05.2015

@author: kolbe
'''
#from spycam import DISTANCE_ECHO, DISTANCE_TRIGGER

#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from numpy import median

class HCSR04(object):
    
    trigger = 0
    echo = 0
    
    # maximum distance in meter
    maximum_distance = 3
    
    def __init__(self, trigger_pin = 18, echo_pin = 24):
        self.trigger = trigger_pin
        self.echo = echo_pin

    def distance(self):
        # setze Trigger auf HIGH
        GPIO.output(self.trigger, True)
        
        # setze Trigger nach 0.01ms aus LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        
        t0 = time.time()
        start_time = time.time()
        stop_time = time.time()
        
        # speichere Startzeit
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
            if start_time-t0 >= 0.5:
                return self.maximum_distance
        
        # speichere Ankunftszeit
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()
            # abort after maximum distance
            if stop_time - start_time >= self.get_maximum_distance_time():
                break
        
        # Zeit Differenz zwischen Start und Ankunft
        TimeElapsed = stop_time - start_time
        # mit der Schallgeschwindigkeit (343 m/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        return (TimeElapsed * 343) / 2
    
    def set_maximum_distance(self, dist):
        self.maximum_distance = dist
        
    def get_maximum_distance_time(self):
        return (2.0*self.maximum_distance) / 343.0
 
    def average_distance(self, len=5):
        values = []
        for i in range(len):
            values.append(self.distance())
            
        return min(median(values), self.maximum_distance)
    
    def __enter__(self):
        #GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
         
        #Richtung der GPIO-Pins festlegen (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        
        # setze Trigger auf LOW
        GPIO.output(self.trigger, False)
        
        return self
    
    def __exit__(self, type, value, traceback):
        GPIO.cleanup()

if __name__ == '__main__':
    
    with HCSR04() as sensor:
        try:
            while True:
                abstand = sensor.distance()
                print ("Gemessene Entfernung = %.2f m" % abstand)
                #time.sleep(1)
        # Beim Abbruch durch STRG+C resetten
        except KeyboardInterrupt:
            print("Messung vom User gestoppt")