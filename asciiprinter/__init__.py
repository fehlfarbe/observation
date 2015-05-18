import sys
from PIL import Image
import numpy as np

def image2ascii(filename, chars=list(' .,:;irsXA253hMHGS#@'), size=None):
    
    c_len = len(chars)
    # convert image to grayscale
    img = Image.open(filename).convert('L')
    # resize image if size is set
    if size is not None:
        img.thumbnail(size, Image.ANTIALIAS)
    # load image data to buffer
    imgdata = img.load()
    width, height = img.size
    
    text = ""
    for h in xrange(height):
        for w in xrange(width):
            value = imgdata[w, h]
            text += chars[int(value / 256.0 * c_len)]
        text += "\n"

    return text
    
    
if __name__ == '__main__':
    ### test it :)
    ascii = image2ascii("../res/about_01.jpg", size=(150,150))
    print ascii
    with open("../res/ascii.txt", "w") as f:
        f.write(ascii)
        
        