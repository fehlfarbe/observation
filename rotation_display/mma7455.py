'''
Created on 20.05.2015

@author: kolbe
'''
import smbus
import time
import os
import math

FACTOR = 360.0 / 255.0

# Define a class for the accelerometer readings
class MMA7455():
    bus = smbus.SMBus(1)
    def __init__(self):
        self.bus.write_byte_data(0x1D, 0x16, 0x55) # Setup the Mode
        self.bus.write_byte_data(0x1D, 0x10, 0) # Calibrate
        self.bus.write_byte_data(0x1D, 0x11, 0) # Calibrate
        self.bus.write_byte_data(0x1D, 0x12, 0) # Calibrate
        self.bus.write_byte_data(0x1D, 0x13, 0) # Calibrate
        self.bus.write_byte_data(0x1D, 0x14, 0) # Calibrate
        self.bus.write_byte_data(0x1D, 0x15, 0) # Calibrate
    def getValueX(self):
        return int(self.bus.read_byte_data(0x1D, 0x06)*FACTOR)
    def getValueY(self):
        return int(self.bus.read_byte_data(0x1D, 0x07)*FACTOR)
    def getValueZ(self):
        return int(self.bus.read_byte_data(0x1D, 0x08)*FACTOR)
    def getHorizontal(self):
        x = self.getValueX()
        y = self.getValueY()
        if y < 360 and y > 180:
            return x
        else:
            return (x-(270-x)) % 360

if __name__ == '__main__':
	mma = MMA7455()

	while True:
		print mma.getValueX(), mma.getValueY(), mma.getValueZ(), mma.getHorizontal()
