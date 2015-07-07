'''
Created on 08.06.2015

@author: kolbe
'''
import os, sys
import subprocess
import time
from optparse import OptionParser
from asciiprinter import image2ascii, print_ascii_image

def send_to_printer(text):
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.stdin.write(text)
    lpr.stdin.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dir",
                      help="Looks for new image files (jpg|png) in this directory", metavar="FILE")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print images in ascii format to stdout")
    (options, args) = parser.parse_args()
    
    print options, args
    
    if options.dir is None:
        print "no directory to look for images...exit"
        sys.exit()
    
    printed_files = []
    while True:
        files = os.listdir(options.dir)
        new_files = list(set(files) - set(printed_files))
        for f in new_files:
            print "new file ", f
            f_path = os.path.join(options.dir, f)
            try:
                ascii_image = image2ascii(f_path, chars=list(" .10@$"), size=(80,68), reverse=True)
                send_to_printer(ascii_image)
                if options.verbose:
                    print_ascii_image(ascii_image)
                printed_files.append(f)
            except Exception, e:
                print e
        
        time.sleep(0.5)
        
    