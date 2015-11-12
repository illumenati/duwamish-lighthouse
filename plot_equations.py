import matplotlib.pyplot as plt
import breathe_equations

x = breathe_equations.get_calm_times()
line, = plt.plot(x,
                 # For erratic graph:
                 [v for v in breathe_equations.calm_generator()],
                 # [v for v in breathe_equations.erratic_generator()],
                 '--',
                 linewidth=2)
plt.show()
