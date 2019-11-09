import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from IPython.display import clear_output
from Cell2D.py import Cell2D
from enum import Enum

# Here's how animate works
# https://stackoverflow.com/questions/24816237/ipython-notebook-clear-cell-output-in-code
# https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.clear_output


class Strategy(Enum):
    c = "Cooperate"
    d = "Defect"
    s = "Silent"

def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d


class BasicWorld(Cell2D):



    def __init__(self, n=20, m=20, u=0.3, do_mutation = False, do_silent = False):

        self.array = [[Agent() for _ in range(m)] for _ in range(n)]

        self.curr_step = 0

        self.u = u
        self.kernel= np.array([
                        [1/3, 1/3, 1/3, 1/3, 1/3, 1/3, 1/3],
                        [1/3, 1/2, 1/2, 1/2, 1/2, 1/2, 1/3],
                        [1/3, 1/2, 1,   1,   1,   1/2, 1/3],
                        [1/3, 1/2, 1,  -u,   1,   1/2, 1/3],
                        [1/3, 1/2, 1,   1,   1,   1/2, 1/3],
                        [1/3, 1/2, 1/2, 1/2, 1/2, 1/2, 1/3],
                        [1/3, 1/3, 1/3, 1/3, 1/3, 1/3, 1/3],
                        ])

    def make_cooperate_array(self):
        """
        Makes an n x m array, where an element is 1 if the agent there
        cooperates this timestep, and 0 if it defects
        """
        return np.array([[1 if agent.cooperate_p(self.curr_step) else 0 for agent in row] for row in self.array])

    def make_fitness_array(self):
        """
        Makes an n x m array, where each element is that agent's fitness,
        derived from its and others' behaviors and their inherent fitnesses.
        """
        cooperate_array = self.make_cooperate_array(t)
        pd_results = np.convolve


    def step(self):
        return

    def loop(self, t=1):
        """
        loops through t number of steps
        """
        for x in range(t):
            step()
        return

    def draw_array(self, array, **options):
        """Draws the cells."""
        n, m = array.shape
        options = underride(options,
                            cmap='Greens',
                            alpha=0.7,
                            vmin=0, vmax=1,
                            interpolation='none',
                            origin='upper',
                            extent=[0, m, 0, n])

        plt.axis([0, m, 0, n])
        plt.xticks([])
        plt.yticks([])

        return plt.imshow(array, **options)

    def draw(self):
        """
        Gets the current np array state then draws the array
        """
        arr = self.make_cooperate_array()
        self.draw_array(arr)

    def animate(self, t):
        pass





class Agent():

    def __init__(self, fitness = 1, strategy=Strategy.d, time_to_cooperate = None):
        self.fitness = fitness
        self.strategy = strategy
        self.time_to_cooperate = time_to_cooperate

        if self.strategy = Strategy.s:
            assert not (time_to_cooperate is None)

    def cooperate_p(self, t):
        if self.strategy = Strategy.c:
            return True
        if self.strategy = Strategy.d:
            return False
        if self.strategy = Strategy.s:
            return selt.time_to_cooperate < t
