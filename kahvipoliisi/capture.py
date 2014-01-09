import cv2, time
import numpy as np
from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep

cam = None

camera_index = 0
width = 320
height = 240

current_capture = None

def initialize_camera():
	global cam
	global width
	global height
        cam = cv2.VideoCapture()
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        cam.open(0)
        height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)

def release_camera():
	cam.release()

def cap():
	#time.sleep(3)
	f,image = cam.read()
	if not f:
		exit(1)
	#f,image = cam.read()
	global current_capture
#	current_capture = numpy.array(cv2.imencode('jpg', image))
#	buf = np.array([1, 2, 3], ndmin=2)
	#buf = cv2.fromarray(np.zeros((width, height), np.uint8))
#	print buf
	_, buf = cv2.imencode('.jpeg', image)
	current_capture = np.array(buf).tostring()
	#print buf
	#cv2.imwrite("capture.jpg", image)
	print "Captured", width, height

def capture_forever():
	while True:
		cap()
		time.sleep(1)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
	try:
		if self.path.endswith("capture.jpg"):
			#f = open(curdir + sep + self.path, 'rb')
		        self.send_response(200)
        		self.send_header("Content-type", "image/jpeg")
		        self.end_headers()
			self.wfile.write(current_capture)
	       	 	#self.wfile.write(f.read())
			#f.close()
			return
	except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def serve_on_port(host, port):
	print "Serving in", host, port
	server = ThreadingHTTPServer((host, port), Handler)
	server.serve_forever()
	
if __name__ == "__main__":
	t = Thread(target=serve_on_port, args=["0.0.0.0", 1111])
	t.daemon = True
	t.start()
	initialize_camera()
	capture_forever()
	release_camera()
	
