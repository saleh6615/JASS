'''
This module generates an SOS message in Morse code on an LED. 
The message is controlled with a switch mapped to pin number 14

Timing convention used in this demonstration are as follows: 
    - Each dot/dash is followed by a gap equal to 1 dot duration. 
    - A dash is the length of 3 dots.
    - The gap between characters of a word is equal to 3 dots.
    - Two words are separated by a gap equal to 7 dots.

To avoid ambiguity each dot is set to 50ms. 
The time interval to regenerate the message is set to 7 dots, equal to the time interval between words.
'''
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)        # please refer to the wiki page  for 
                                # more info on the mapping methods  https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
DOT = 0.05
DASH = DOT * 3
SPACE = DOT * 7

switch = 14
led = 15
system = False

def init():
    GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(led, GPIO.OUT)
    GPIO.add_event_detect(switch, GPIO.FALLING, callback = toggle, bouncetime = 200)
def a_dot():
    GPIO.output(led, GPIO.HIGH)
    time.sleep(DOT)
    GPIO.output(led, GPIO.LOW)
    time.sleep(DOT)
def a_dash():
    GPIO.output(led, GPIO.HIGH)
    time.sleep(DASH)
    GPIO.output(led, GPIO.LOW)
    time.sleep(DOT)
def char_gap():                         #time interval between each character -> 3 dots
    GPIO.output(led, GPIO.LOW)
    time.sleep(DASH)
def big_gap():
    GPIO.output(led, GPIO.LOW)
    time.sleep(SPACE)
def letter_s():
    a_dot() a_dot() a_dot() char_gap()
def letter_o():
    a_dash() a_dash() a_dash() char_gap()
def toggle():
    system = system ^ True
def main():
    init()
    while(True):
        if(system):
            letter_s()
            letter_o()
            letter_s()
            big_gap()
if __name__ == "__main__":
    main()
