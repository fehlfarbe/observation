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
    def getAngleXY(self):
            x = self.getValueX()
            y = self.getValueY()
            angle = 0.0
            
            # measured bounds 0-45 and 183-255
            if x > 127:
                x = max(183, x)
            else:
                x = min(45, x)
            
            # measured bounds 0-34 and 230-255
            if y > 127:
                y = max(170, y)
            else:
                y = min(34, y)
            
            # UR
            if x <= 240 and x >= 183 and (y <= 34 or y >= 230):
                x_relative = (x-183) / 57.0
                angle = 270 + (90 - math.acos(x_relative) * (180.0/math.pi))
                #print "UR ", x, (x-183), x_relative
            # UL
            elif (x <= 45 or x >= 240) and (y <= 34 or y >= 230):
                x_relative = 1-(((x+15)%255) / 60.0)
                angle = math.acos(x_relative) * (180.0/math.pi)
                #print "UL ", x, ((x+15)%255), x_relative
            # BL
            elif (x <= 45 or x >= 240) and y < 230 and y > 170:
                x_relative = 1-(((x+15)%255) / 60.0)
                angle = 90 + (90 - math.acos(x_relative) * (180.0/math.pi))
                #print "BL", x, ((x+15)%255), x_relative
            # BR
            elif x <= 240 and x >= 183 and y >= 170 and y <= 230:
                x_relative = (x-183) / 57.0
                angle = 180 + math.acos(x_relative) * (180.0/math.pi)
                #print "BR", x, ((x+15)%255), x_relative
                
            return angle