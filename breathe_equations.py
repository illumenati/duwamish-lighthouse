import math
from time import sleep

# General equation:
# v = a * e ^ ( (b * t) )

# Inhale:
# v = a_in * e ^ ( (b_in * t) )
# Exhale:
# v = a_ex * e ^ ( (b_ex * t) )

# We require that this function pass through two points:
# (t_A; v_A) and (t_B; v_B)

# Custom Params:
CALM_INTERVAL = 0.02  # in seconds
INHALE_TIME = 2.0
INHALE_HOLD = 0.5
EXHALE_TIME = 3.0
EXHALE_HOLD = 0.5
TOTAL_TIME = INHALE_HOLD + INHALE_TIME + EXHALE_TIME + EXHALE_HOLD

STEP_DURATION = 0.02

V_MIN = 2
V_MAX = 100

INHALE_T_A = 0
INHALE_V_A = V_MIN
INHALE_T_B = INHALE_TIME
INHALE_V_B = V_MAX

EXHALE_T_A = 0
EXHALE_V_A = V_MAX
EXHALE_T_B = EXHALE_TIME
EXHALE_V_B = V_MIN


# Solving general equation for a:
# a = e ^ ( (t_a * ln(v_b)) - (t_b * ln(v_a)) / (t_a - t_b) )
def calc_a_coefficient(t_a, v_a, t_b, v_b):
    return math.exp((t_a * math.log(v_b)) - (t_b * math.log(v_a)) /
                    (t_a - t_b))


# Solving general equation for b:
# b = ( (ln(v_A) - ln(v_B)) / (t_a - t_b) )
def calc_b_coefficient(t_a, v_a, t_b, v_b):
    return (math.log(v_a) - math.log(v_b)) / (t_a - t_b)

A_IN = calc_a_coefficient(INHALE_T_A, INHALE_V_A, INHALE_T_B, INHALE_V_B)
B_IN = calc_b_coefficient(INHALE_T_A, INHALE_V_A, INHALE_T_B, INHALE_V_B)

A_EX = calc_a_coefficient(EXHALE_T_A, EXHALE_V_A, EXHALE_T_B, EXHALE_V_B)
B_EX = calc_b_coefficient(EXHALE_T_A, EXHALE_V_A, EXHALE_T_B, EXHALE_V_B)


def inhale(time):
    return A_IN * math.exp(B_IN * time)


def exhale(time):
    return A_EX * math.exp(B_EX * time)


def calm_times_generator():
    t = 0
    while t < TOTAL_TIME:
        yield t
        t += STEP_DURATION


def breathe_calm(t):
    if t < INHALE_TIME:
        return math.floor(inhale(t))
    elif t < INHALE_TIME + INHALE_HOLD:
        return V_MAX
    elif t < INHALE_TIME + INHALE_HOLD + EXHALE_TIME:
        exhale_time_offset = t - (INHALE_TIME + INHALE_HOLD)
        return math.floor(exhale(exhale_time_offset))
    else:
        return 1


def calm_generator():
    for current_time in calm_times_generator():
        sleep(CALM_INTERVAL)
        current_time += STEP_DURATION
        yield breathe_calm(current_time)


def get_calm_times():
    return [t for t in calm_times_generator()]


ERRATIC_INTERVAL = 0.007
ERRATIC_SEQUENCE = [(0, 75, 1), (75, 15, -1), (15, 45, 1), (45, 25, -1),
                    (25, 70, 1), (70, 10, -1), (10, 30, 1),
                    (30, 5, -1), (5, 75, 1), (75, 10, -1),
                    (10, 50, 1), (50, 25, -1), (25, 100, 1),
                    (100, 0, -1), (0, 15, 1), (15, 0, -1),
                    (0, 35, 1), (35, 0, -1)]


def erratic_generator():
    for values in ERRATIC_SEQUENCE:
        range_start, range_end, step = values
        for i in range(range_start, range_end, step):
            yield i
            sleep(ERRATIC_INTERVAL)
