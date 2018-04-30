import RPi.GPIO as GPIO 
import time 
import threading
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

red = 7
white = 11
green = 13
switch = 15
A0, A1, B0, B1  = [29, 31, 33, 35]
GPIO.setmode(GPIO.BOARD)
system = True # True: Locked, False: Unlocked 
threads = []
myMQTTClient = AWSIoTMQTTClient("my_test_lock")
def init():
	GPIO.setup([white, green, red], GPIO.OUT)	
	GPIO.setup([A0, A1, B0, B1], GPIO.OUT)
	GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(switch, GPIO.FALLING, callback = check_breakin, bouncetime = 200)
	GPIO.output(white, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)
        myMQTTClient.configureEndpoint("XXX_PRIVATE_XXX", 
                8883) #Endpoint and the port number 
        myMQTTClient.configureCredentials("XXX_root-CA.crt_XXX",
                "XXX_private.pem.key_XXX", "XXX_certificate.pem.crt_XXX")
        myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
def flash(light):
	for _ in range(30):
		GPIO.output(light, (GPIO.input(light) ^ True))
		time.sleep(.1)
def motor_delay():
    time.sleep(.03)
def motor_unlock():
    time.sleep(.5)
    for _ in range(25):
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
def motor_lock():
    time.sleep(.5)
    for _ in range(25):
        GPIO.output([A1, B0], GPIO.LOW)
        GPIO.output([A0, B1], GPIO.HIGH)
        motor_delay()
        GPIO.output([A0, B0], GPIO.LOW)
        GPIO.output([A1, B1], GPIO.HIGH)
        motor_delay()
        GPIO.output([A0, B1], GPIO.LOW)
        GPIO.output([A1, B0], GPIO.HIGH)
        motor_delay()
        GPIO.output([A1, B1], GPIO.LOW)
        GPIO.output([A0, B0], GPIO.HIGH)
        motor_delay()
def c_unlock():
        print "unlocking..."
        t1 = threading.Thread(target = flash, args = (white, ))
        t2 = threading.Thread(target = motor_unlock)
        #threads.append(t1)
        #threads.append(t2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
	GPIO.output(white, GPIO.LOW)
	time.sleep(.5)
	GPIO.output(green, GPIO.HIGH)
def c_lock():
        print "locking..."
        t1 = threading.Thread(target = flash, args = (green, ))
        t2 = threading.Thread(target = motor_lock)
	#flash(green)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
	GPIO.output(green, GPIO.LOW)
	time.sleep(.5)
	GPIO.output(white, GPIO.HIGH)	
def operation(client, userdata, message):
    global system
#    system = system ^ True 
    command = message.payload.decode("utf-8")
    print command
    if command == "Locked":
        if not system:
            system = system ^ True
            c_lock()
    elif command == "Unlocked":
        if system:
            system = system ^ True
            c_unlock()
    elif command == "newSubscriber":
#        time.sleep(1)
        if(system):
            myMQTTClient.publish("LockStatus", "Locked", 0)
        else:
            myMQTTClient.publish("LockStatus", "Unlocked", 0)
def check_breakin(my_led):
        print "breakin..."
        while(system):
            GPIO.output(red, GPIO.input(red) ^ True)
            time.sleep(.1)
        GPIO.output(red, GPIO.LOW)
init()
myMQTTClient.connect()
myMQTTClient.subscribe("LockStatus", 1, operation)
while(True):
    time.sleep(1)
