#!/usr/bin/env python
'''
Created on 06.05.2015

@author: kolbe
'''
from spycam import get_distance, setup_GPIO

if __name__ == '__main__':
    
    setup_GPIO()
    values = []
    while True:
        try:
            d = get_distance()
            print "distance ", d
            values.append(d)
        except KeyboardInterrupt:
            break
            
    '''
    with open("result.csv", "w") as f:
        for v in values:
            f.write("%d\n" % v)
    '''
            
            