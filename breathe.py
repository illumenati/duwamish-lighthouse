import RPi.GPIO as GPIO
from time import sleep 
from multiprocessing import Process
import os

class Breathe(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM) # We can also choose a BOARD numbering schemes.
        GPIO.setup(21, GPIO.OUT) # set GPIO 21 as output
        self.light = GPIO.PWM(21, 100) # create object for PWM on port 21 at 100 Hertz
        self.p = Process(target=calm, args=(self.light,))

    def shutdown(self):
        if (self.p.is_alive()):
            self.p.terminate()
        self.light.stop()
        GPIO.cleanup()
        print("breathing shut down.")
        
    def restart(self):
        print("restarting breathing!")
        if (self.p.is_alive()):
            self.p.terminate()
        self.light.stop()
        GPIO.cleanup()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        self.light = GPIO.PWM(21, 100)
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
    light.start(0)
    pause_time = 0.02
    try:
        while True:
            for i in range(0,101):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(100,-1,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
    finally:
        print("stopping calm breathing")
        light.stop()
        GPIO.cleanup()

def erratic(light):
    print("starting erratic breathing...")
    light.start(0)
    pause_time = 0.007

    try:
        while True:
            for i in range(0,75):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(75,15,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(15,45):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(45,25,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(25,70):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(70,10,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(10,30):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(30,5,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(5,75):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(75,10,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(10,50):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(50,25,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(25,100):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(100,0,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(0,15):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(15,0,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(0,35):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
            for i in range(35,0,-1):
                light.ChangeDutyCycle(i)
                sleep(pause_time)
    finally:
        print("stopping erratic breathing")
        light.stop()
        GPIO.cleanup()
