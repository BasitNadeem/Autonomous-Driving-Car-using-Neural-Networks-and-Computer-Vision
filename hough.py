from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import cv2
import numpy as np
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
p= GPIO.PWM(7,50)
p.start(7.5)
theta=0
minLineLength = 5
maxLineGap = 50
camera = PiCamera()
camera.resolution = (640, 480)
#camera.rotation=90
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
#	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred=cv2.GaussianBlur(image, (5,5),0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#	blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
	low_black = np.array([0, 0, 0])
	up_black = np.array([50, 50, 50])
	mask = cv2.inRange(hsv, low_black, up_black)
	edged = cv2.Canny(mask, 75,150)
	lines = cv2.HoughLinesP(edged,1,np.pi/180,10,maxLineGap)
	if(lines !=None):
#		for x in range(0, len(lines)):
#			for x1,y1,x2,y2 in lines[x]:
		for line in lines:
				x1,y1,x2,y2 = line[0]
				cv2.line(image,(x1,y1),(x2,y2),(0,255,0),8)
				theta=theta+math.atan2((y2-y1),(x2-x1))
#print(theta)GPIO pins were connected to arduino for servo steering control
	threshold=6
	if(theta>threshold):
		GPIO.output(7,True)
		GPIO.output(8,False)
		print("left")
		p.ChangeDutyCycle(4.5)
		time.sleep(0.5)
	if(theta<-threshold):
		GPIO.output(8,True)
		GPIO.output(7,False)
		print("right")
		p.ChangeDutyCycle(10.5)
		time.sleep(1)
	if(abs(theta)<threshold):
		GPIO.output(8,False)
		GPIO.output(7,False)
		print "straight"
		p.ChangeDutyCycle(7.5) # 0
		time.sleep(1)
	theta=0
	cv2.imshow("Frame",image)
	cv2.imshow("edges",edged)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord("q"):
		break
