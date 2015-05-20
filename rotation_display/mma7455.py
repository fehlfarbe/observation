'''
Created on 20.05.2015

@author: kolbe
'''
import smbus
import time
import os
import math

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
        return self.bus.read_byte_data(0x1D, 0x06)
    def getValueY(self):
        return self.bus.read_byte_data(0x1D, 0x07)
    def getValueZ(self):
        return self.bus.read_byte_data(0x1D, 0x08)