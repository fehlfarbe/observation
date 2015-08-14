import cv2
import Image
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import StringIO
import time
from threading import Thread

class MJPEGServer(HTTPServer):
	current_image = None
	
	def start_server(self):
		Thread(target=self.serve_forever).start()
	
	def update_image(self, frame):
		self.current_image = frame

class MJPEGHandler(BaseHTTPRequestHandler):
		
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
		self.end_headers()
		while True:
			try:
				img = self.server.current_image
				if img is None:
					continue
				imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
				jpg = Image.fromarray(imgRGB)
				tmpFile = StringIO.StringIO()
				jpg.save(tmpFile,'JPEG')
				self.wfile.write("--jpgboundary")
				self.send_header('Content-type','image/jpeg')
				self.send_header('Content-length',str(tmpFile.len))
				self.end_headers()
				jpg.save(self.wfile,'JPEG')
				time.sleep(0.05)
			except KeyboardInterrupt:
				break
		return
	
def getServer(port):
	return MJPEGServer(('0.0.0.0',port), MJPEGHandler)

if __name__ == '__main__':
	import sys
	print sys.argv[2]
	capture = cv2.VideoCapture(sys.argv[2])
	try:
		server = getServer(int(sys.argv[1]))
		server.start_server()
		while True:
			ret, img = capture.read()
			server.update_image(img)
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()