from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import RPi.GPIO as gpio
# initialize the camera and grab a reference to the raw camera capture
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
gpio.setup(7,gpio.OUT)
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	gpio.output(7,True)
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

#RED COLOR
	lower_range = np.array([169,100,100], dtype=np.uint8) 
      	upper_range = np.array([189,255,255], dtype=np.uint8)

#GREEN COLOR
#	lower_range = np.array([52,100,100], dtype=np.uint8) 
#	upper_range = np.array([79,255,255], dtype=np.uint8)


# create a mask for image

	mask = cv2.inRange(hsv, lower_range, upper_range)
	res = cv2.bitwise_and(image,image,mask=mask)

# display both the mask and the image side-by-side
	cv2.imshow("images" , np.hstack([image,res]))

	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

cv2.destroyAllWindows()
