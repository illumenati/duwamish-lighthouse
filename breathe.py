import RPi.GPIO as GPIO # always needed with RPi.GPIO
from time import sleep  # pull in the sleep function from time module
from multiprocessing import Process
import os
# https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process
# https://docs.python.org/2/library/multiprocessing.html

class Breathe(object):

    def __init__(self):
        print("initializing Breathe!")

        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM
        GPIO.setup(21, GPIO.OUT)# set GPIO 21 as output for white led
        self.light = GPIO.PWM(21, 100)    # create object white for PWM on port 21 at 100 Hertz
        # self.light.start(0)
        self.p = Process(target=calm, args=(self.light,))
        self.p.start()

    def shutdown(self):
        if (self.p.is_alive()):
            self.p.terminate()
        self.light.stop()
        GPIO.cleanup()
        
    def restart(self):
        if (self.p.is_alive()):
            self.p.terminate()
        self.light.stop()
        GPIO.cleanup()
        
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM
        GPIO.setup(21, GPIO.OUT)# set GPIO 21 as output for white led
        self.light = GPIO.PWM(21, 100)    # create object white for PWM on port 21 at 100 Hertz
        self.light.start(0)
        self.p = Process(target=calm, args=(self.light,))
        self.p.start()

    def calm(self):
        if (self.p.is_alive()):
            self.p.terminate()
        self.light.stop()
        self.p = Process(target=calm, args=(self.light,))
        self.p.start()
        
    def erratic(self):
        if (self.p.is_alive()):
            self.p.terminate()
        self.light.stop()
        self.p = Process(target=erratic, args=(self.light,))
        self.p.start()
        
def calm(light):
    print("starting calm breathing...")
    light.start(0)              # start white led on 0 percent duty cycle (off)
    pause_time = 0.02           # you can change this to slow down/speed up
    try:
        while True:
            for i in range(0,101):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(100,-1,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
    finally:
        print("stopping calm breathing")
        light.stop()            # stop the white PWM output
        GPIO.cleanup()          # clean up GPIO on CTRL+C exit

def erratic(light):
    light.start(0)              # start light led on 0 percent duty cycle (off)
    pause_time = 0.007           # you can change this to slow down/speed up

    try:
        while True:
            for i in range(0,75):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(75,15,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(15,45):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(45,25,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(25,70):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(70,10,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(10,30):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(30,5,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(5,75):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(75,10,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(10,50):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(50,25,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(25,100):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(100,0,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(0,15):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(15,0,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(0,35):      # 101 because it stops when it finishes 100
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(35,0,-1):      # from 100 to zero in steps of -1
                light.ChangeDutyCycle(i)
                sleep(pause_time)
    finally:
        print("stopping erratic breathing")
        light.stop()            # stop the light PWM output
        GPIO.cleanup()          # clean up GPIO on CTRL+C exit
