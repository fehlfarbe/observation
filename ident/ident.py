import os, time, sys
sys.path.insert(1,'..')
from datetime import datetime
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from sensors import hcsr04
import webbrowser
import tempfile
from jinja2 import Template
import base64
from PIL import Image
import cStringIO
import gtk
import webkit

DISTANCE_TRIGGER = 18
DISTANCE_ECHO = 24
MIN_DISTANCE = 1.0

def createHTML(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    file_like = cStringIO.StringIO()
    img.save(file_like, 'png')
    file_like.seek(0)
    img = base64.b64encode(file_like.read())    
    with open( os.path.dirname(os.path.abspath(__file__))+"/template_bloed/template.html", 'r') as r:
        template = Template(r.read())

    return template.render(image=img)

def showHTML(html):
    _, filename = tempfile.mkstemp(suffix=".html")
    with open(filename, 'w') as f:
        f.write(html)
        
    #webbrowser.open(filename, autoraise=False)
    print filename
    #web.open(filename)


if __name__ == '__main__':
    
    win = gtk.Window()
    web = webkit.WebView()
    win.add(web)
    web.show()
    win.show_all()
    #win.fullscreen()
    #web.open("http://www.google.de")
    gtk.main()
        
    with hcsr04.HCSR04(trigger_pin=DISTANCE_TRIGGER, echo_pin=DISTANCE_ECHO) as d:
        
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.vflip = False
        camera.hflip = False
        camera.resolution = (1024, 768)
    
        # allow the camera to warmup
        time.sleep(0.1)
        
        # capture initial frame
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
    
        # init variables
        detected = False
        detected_dt = datetime.now().isoformat()
        distance = 0
        
        # start loop
        while True:
            distance = d.average_distance()
            #print "distance ", distance
            print distance, "m"
            if distance <= MIN_DISTANCE:
                print "grab"
                rawCapture = PiRGBArray(camera)
                # grab an image from the camera
                camera.capture(rawCapture, format="bgr")
                image = rawCapture.array
                # display the image on screen and wait for a keypress
                #cv2.imshow("Image", image)
                #cv2.waitKey(100)
                
                html = createHTML(image)
                #showHTML(html)
                web.open(os.path.dirname(os.path.abspath(__file__))+"/template_bloed/template.html")
