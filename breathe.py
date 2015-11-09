from time import sleep
from multiprocessing import Process
import RPi.GPIO as GPIO


class Breathe(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # We can also choose a BOARD numbering schemes.
        GPIO.setup(21, GPIO.OUT)  # set GPIO 21 as output
        self.light = GPIO.PWM(21, 100)  # create object for PWM on port 21 at 100 Hertz
        self.p = Process(target=calm, args=(self.light,))
        self.state = BreatheState(('CALM', 'ERRATIC', 'STOP'))
        self.restart_state = self.state.CALM

    def shutdown(self):
        if self.p.is_alive():
            self.p.terminate()
        self.light.stop()
        GPIO.cleanup()
        print("breathing shut down.")

    def restart(self):
        print("restarting breathing!")
        if self.p.is_alive():
            self.p.terminate()
        self.light.stop()
        GPIO.cleanup()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        self.light = GPIO.PWM(21, 100)
        self.light.start(0)
        if self.restart_state == self.state.CALM:
            self.p = Process(target=calm, args=(self.light,))
            self.p.start()
        elif self.restart_state == self.state.ERRATIC:
            self.p = Process(target=erratic, args=(self.light,))
            self.p.start()
        else:
            self.shutdown()

    def calm(self):
        if self.p.is_alive():
            self.p.terminate()
        self.light.stop()
        self.p = Process(target=calm, args=(self.light,))
        self.p.start()
        print("calm breathing")

    def erratic(self):
        if self.p.is_alive():
            self.p.terminate()
        self.light.stop()
        self.p = Process(target=erratic, args=(self.light,))
        self.p.start()
        print("erratic breathing")

    def set_state(self, state):
        self.restart_state = state
        print("state has been set:", self.restart_state)

    def get_state(self):
        print("state has been set:", self.restart_state)
        return self.state


class BreatheState(object):
    def __init__(self, tupleList):
        self.tupleList = tupleList

    def __getattr__(self, name):
        return self.tupleList.index(name)


def pulse_light(light, pause_time, pulse_sequence):
    for values in pulse_sequence:
        range_start, range_end, step = values

        for i in range(range_start, range_end, step):
            light.ChangeDutyCycle(i)
            sleep(pause_time)


def calm(light):
    print("starting calm breathing...")
    light.start(0)
    pause_time = 0.02
    pulse_sequence = [(0, 101, 1), (100, -1, -1)]

    try:
        while True:
            pulse_light(light, pause_time, pulse_sequence)
    finally:
        print("stopping calm breathing")
        light.stop()
        GPIO.cleanup()


def erratic(light):
    print("starting erratic breathing...")
    light.start(0)
    pause_time = 0.007
    pulse_sequence = [(0, 75, 1), (75, 15, -1), (15, 45, 1), (45, 25, -1), (25, 70, 1), (70, 10, -1), (10, 30, 1),
                      (30, 5, -1), (5, 75, 1), (75, 10, -1), (10, 50, 1), (50, 25, -1), (25, 100, 1), (100, 0, -1),
                      (0, 15, 1), (15, 0, -1), (0, 35, 1), (35, 0, -1)]

    try:
        while True:
            pulse_light(light, pause_time, pulse_sequence)
    finally:
        print("stopping erratic breathing")
        light.stop()
        GPIO.cleanup()
