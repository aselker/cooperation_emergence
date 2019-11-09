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



    def __init__(self, n=20, m=20, u=0.3, do_mutation = False, do_silent = False, ):

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

        self.inherent_fitness_increment_prob = 0.001
        self.inherent_fitness_increment_prob = 0.1


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
        cooperate_array = self.make_cooperate_array()
        pd_results = np.correlate(cooperate_array, self.kernel, mode="same")
        inherent_fitnesses = np.array([[agent.inherent_fitness for agent in row] for row in self.array])

        return pd_results + inherent_fitnesses

    def neighborhood_look(self, loc, fitness_array):
        pass

    def step(self):
        # make fitness array
        arr = self.make_fitness_array()

        # determine who conquers whom in the local area
        # ORIGINAL IMPLEMENTATION:
        # for "conquering", we look at every cell in a random order
        # after picking a cell we then look at ONE OF the four "direct" neighbors (cardinal directions)
        # we compare fitnesses. If our current cell is higher, do nothing.
        # If our current cell has lower fitness we can be replaced with the other cell
        for (x,y) in np.ndenumerate(arr).shuffle():



        # have conquering happen [update matrices/agents] -> mutation at odds mut_chance or whatever

        # Increment random inherent_fitness vars
        for agent in [agent for agent in self.rows for row in self.array]:
            if np.random.random < self.inherent_fitness_increment_prob:
                agent.inherent_fitness += inherent_fitness_increment_amt



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

    def draw(self, frames, interval=None, step=None):
        """
        Gets the current np array state then draws the array
        """
        arr = self.make_cooperate_array()
        self.draw_array(arr)

    def animate(self, frames, interval=None, step=None):
        """Animate the automaton.

        frames: number of frames to draw
        interval: time between frames in seconds
        iters: number of steps between frames
        """
        if step is None:
            step = self.step

        plt.figure()
        try:
            for i in range(frames-1):
                self.draw()
                plt.show()
                if interval:
                    sleep(interval)
                step()
                clear_output(wait=True)
            self.draw()
            plt.show()
        except KeyboardInterrupt:
            pass





class Agent():

    def __init__(self,  strategy=Strategy.d, time_to_cooperate = None):
        self.inherent_fitness = 0
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
