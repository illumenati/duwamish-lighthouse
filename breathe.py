from enum import Enum
from multiprocessing import Process, Manager
import RPi.GPIO as GPIO
import breathe_equations


class BreatheState(Enum):
    calm = 1
    erratic = 2


def pulse_light(light, pulse_generator):
    for value in pulse_generator:
        light.ChangeDutyCycle(value)


def breathe_calm(light):
    pulse_light(light, breathe_equations.calm_generator())


def breathe_erratic(light):
    pulse_light(light, breathe_equations.erratic_generator())


def breathe_loop(state):
    light = None

    while True:
        if state.get('stop'):
            light.stop()
            GPIO.cleanup()
            break
        elif light is None:
            GPIO.setmode(GPIO.BCM)  # We can also choose a BOARD numbering schemes.
            GPIO.setup(21, GPIO.OUT)  # set GPIO 21 as output
            light = GPIO.PWM(21, 100)  # create object for PWM on port 21 at 100 Hertz
            light.start(0)

        breathe_state = state['breathe_state']

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
        self.process = None
        self.start()
        
    def stop(self):
        if not self.state['stop']:
            self.state['stop'] = True
            self.process.join()

    def start(self):
        self.state['stop'] = False
        self.process = Process(target=breathe_loop, args=(self.state,))
        self.process.start()

    def restart(self):
        self.stop()
        self.start()

    def calm(self):
        self.state['breathe_state'] = BreatheState.calm

    def erratic(self):
        self.state['breathe_state'] = BreatheState.erratic
