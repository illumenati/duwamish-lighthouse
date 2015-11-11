from enum import Enum
from time import sleep
from multiprocessing import Process, Manager
import RPi.GPIO as GPIO

CALM_PAUSE = 0.02
CALM_SEQUENCE = [(0, 101, 1), (100, -1, -1)]
ERRATIC_PAUSE = 0.007
ERRATIC_SEQUENCE = [(0, 75, 1), (75, 15, -1), (15, 45, 1), (45, 25, -1), (25, 70, 1), (70, 10, -1), (10, 30, 1),
                    (30, 5, -1), (5, 75, 1), (75, 10, -1), (10, 50, 1), (50, 25, -1), (25, 100, 1), (100, 0, -1),
                    (0, 15, 1), (15, 0, -1), (0, 35, 1), (35, 0, -1)]


class BreatheState(Enum):
    calm = 1
    erratic = 2


def pulse_light(light, pause_time, pulse_sequence):
    for values in pulse_sequence:
        range_start, range_end, step = values

        for i in range(range_start, range_end, step):
            light.ChangeDutyCycle(i)
            sleep(pause_time)


def breathe_calm(light):
    pulse_light(light, CALM_PAUSE, CALM_SEQUENCE)


def breathe_erratic(light):
    pulse_light(light, ERRATIC_PAUSE, ERRATIC_SEQUENCE)


def breathe_loop(state):
    while True:
        if state.get('stop'):
            break

        breathe_state = state['breathe_state']
        light = state['light']

        if breathe_state is BreatheState.calm:
            breathe_calm(light)
        elif breathe_state is BreatheState.erratic:
            breathe_erratic(light)


class Breathe:
    def __init__(self):
        self.manager = Manager()
        self.state = self.manager.dict()
        self.state['breathe_state'] = BreatheState.calm
        self.state['stop'] = False
        self.setup_light()
        self.process = None
        self.start()
        
    def setup_light(self):
        GPIO.setmode(GPIO.BCM)  # We can also choose a BOARD numbering schemes.
        GPIO.setup(21, GPIO.OUT)  # set GPIO 21 as output
        self.state['light'] = GPIO.PWM(21, 100)  # create object for PWM on port 21 at 100 Hertz
        self.state['light'].start(0)

    def cleanup_light(self):
        self.state['light'].stop()
        GPIO.cleanup()

    def stop(self):
        if not self.state['stop']:
            self.state['stop'] = True
            self.process.join()
            self.cleanup_light()
        
    def start(self):
        self.state['stop'] = False
        self.setup_light()
        self.process = Process(target=breathe_loop, args=(self.state,))
        self.process.start()

    def restart(self):
        self.stop()
        self.start()

    def calm(self):
        self.state['breathe_state'] = BreatheState.calm

    def erratic(self):
        self.state['breathe_state'] = BreatheState.erratic
