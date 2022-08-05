import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.OUT)
gpio.setup(11,gpio.OUT)

gpio.output(7,True)
gpio.output(11,False)
time.sleep(5)
print("FORWARD")
gpio.output(7,False)

gpio.output(11,True)
time.sleep(5)
print("REVERSE")
gpio.output(11,False)

gpio.cleanup()

