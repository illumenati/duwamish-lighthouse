#!/usr/bin/env python2.7  
# script by Alex Eames http://RasPi.tv  
#http://RasPi.tv/2013/how-to-use-soft-pwm-in-rpi-gpio-pt-2-led-dimming-and-motor-speed-control  
# Using PWM with RPi.GPIO pt 2 - requires RPi.GPIO 0.5.2a or higher  
      
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  

GPIO.setup(26, GPIO.OUT)# set GPIO 25 as output for white led  
# GPIO.setup(24, GPIO.OUT)# set GPIO 24 as output for red led  

# GPIO is 26
white = GPIO.PWM(26, 100)    # create object white for PWM on port 25 at 100 Hertz  

white.start(0)              # start white led on 0 percent duty cycle (off)  

# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  
pause_time = 0.01           # you can change this to slow down/speed up  

# TODO: Make this a human breathe rate
try:  
    while True:  
        # white.ChangeDutyCycle(50)  
        for i in range(0,101):      # 101 because it stops when it finishes 100  
            white.ChangeDutyCycle(i)  
            # red.ChangeDutyCycle(100 - i)  
            sleep(pause_time)  
        for i in range(100,-1,-1):      # from 100 to zero in steps of -1  
            white.ChangeDutyCycle(i)  
            # red.ChangeDutyCycle(100 - i)  
            sleep(pause_time)  
            
except KeyboardInterrupt:  
    white.stop()            # stop the white PWM output  
    # red.stop()              # stop the red PWM output  
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit  
