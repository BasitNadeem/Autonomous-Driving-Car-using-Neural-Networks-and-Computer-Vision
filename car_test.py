import RPi.GPIO as gpio
import time

servo=7;
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(servo,gpio.OUT)
gpio.setup(11, gpio.OUT)	#Forward motor
gpio.setup(12, gpio.OUT)	#Reverse motor

p=gpio.PWM(servo, 50)
p.start(7.5)

gpio.output(11,True)
gpio.output(12,False)
time.sleep(2)
gpio.output(11,False)
p.ChangeDutyCycle(2.5)
time.sleep(2)
p.ChangeDutyCycle(7.5)
