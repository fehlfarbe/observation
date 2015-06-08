import sys, time
from PIL import Image
import numpy as np

def image2ascii(filename, chars=list(' .,:;irsXA253hMHGS#@'), size=None, reverse=True):
    
    # reverse chars
    tmp = chars
    if reverse:
        tmp.reverse()
    # get len of chars
    c_len = len(chars)
    # convert image to grayscale
    img = Image.open(filename).convert('L')
    # resize image if size is set
    if size is not None:
        img.thumbnail(size, Image.ANTIALIAS)
    # load image data to buffer
    imgdata = img.load()
    # get dimensions of (resized) image
    width, height = img.size
    
    text = ""
    for h in xrange(height):
        for w in xrange(width):
            value = imgdata[w, h]
            text += tmp[int(value / 256.0 * c_len)]
        text += "\n"

    return text

def print_ascii_image(ascii_image, period=0.2):
    for line in ascii_image.split("\n"):
        print line
        time.sleep(period)
    
    
if __name__ == '__main__':
    ### test it :)
    ascii = image2ascii("../res/about_01.jpg", size=(150,150), chars=list('.10@$'))
    #print ascii
    with open("../res/ascii.txt", "w") as f:
        f.write(ascii)
    for x in range(10):
        for i in ascii.split("\n"):
            print i
            time.sleep(0.2)
        
        