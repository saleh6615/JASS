import RPi.GPIO as GPIO
import time

red = 11
green = 13
switch = 15
A0, A1, B0, B1  = [29, 31, 33, 35]
GPIO.setmode(GPIO.BOARD)

def init():
	GPIO.setup([red, green], GPIO.OUT)	
	GPIO.setup([A0, A1, B0, B1], GPIO.OUT)
	GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.output(red, GPIO.HIGH)
def flash(light):
	for _ in range(20):
		GPIO.output(light, (GPIO.input(light) ^ 1))
		time.sleep(.1)
def motor_delay():
    time.sleep(.01)
def motor_unlock():
        GPIO.output([A1, B1], GPIO.LOW)
        GPIO.output([A0, B0], GPIO.HIGH)
        motor_delay()
        GPIO.output([A0, B1], GPIO.LOW)
        GPIO.output([A1, B0], GPIO.HIGH)
        motor_delay()
        GPIO.output([A0, B0], GPIO.LOW)
        GPIO.output([A1, B1], GPIO.HIGH)
        motor_delay()
        GPIO.output([A1, B0], GPIO.LOW)
        GPIO.output([A0, B1], GPIO.HIGH)
        motor_delay()
def c_unlock():
	flash(red)
        for _ in range(50):
            motor_unlock()
	GPIO.output(red, GPIO.LOW)
	time.sleep(.5)
	GPIO.output(green, GPIO.HIGH)
def c_lock():
	flash(green)
	GPIO.output(green, GPIO.LOW)
	time.sleep(.5)
	GPIO.output(red, GPIO.HIGH)
	
init()
while(True):
	GPIO.wait_for_edge(switch, GPIO.FALLING)
	c_unlock()	
	GPIO.wait_for_edge(switch, GPIO.FALLING)
	c_lock()

 
