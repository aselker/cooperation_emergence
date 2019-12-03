#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from IPython.display import clear_output
from enum import Enum
import copy
from scipy.signal import correlate2d
import random
import time
import datetime
import json

"""
TODO:
Nick -- Experiments 2/3

Adam -- Graphing of type of person over time

"""


class Strategy(Enum):
    c = 0
    d = 1
    s = 2


def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d


class BasicWorld:
    def __init__(
        self,
        n=50,
        m=None,
        u=0.09,
        do_mutation=False,
        do_silent=False,
        bounds=None,
        mutate_rate=0,
        silent_coop=False,
    ):
        """
        bounds is a tuple of (x_start, y_start, x_end, y_end) for a block of
        cooperators among the sea of defectors.
        """

        def agent_at_pos(x, y):
            if bounds is None:
                return Agent(silent_coop=silent_coop)
            else:
                if (bounds[0] < x < bounds[2]) and (bounds[1] < y < bounds[3]):
                    return Agent(strategy=Strategy.c, silent_coop=silent_coop)
                else:
                    return Agent(silent_coop=silent_coop)

        self.curr_step = 0

        self.mutate_rate = mutate_rate

        self.n = n
        if m is None:
            m = self.n
        self.m = m

        self.array = [
            [agent_at_pos(x, y) for x in range(self.m)] for y in range(self.n)
        ]

        self.u = u
        self.kernel = np.array(
            [
                [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3],
                [1 / 3, 1 / 2, 1 / 2, 1 / 2, 1 / 2, 1 / 2, 1 / 3],
                [1 / 3, 1 / 2, 1, 1, 1, 1 / 2, 1 / 3],
                [1 / 3, 1 / 2, 1, 0, 1, 1 / 2, 1 / 3],
                [1 / 3, 1 / 2, 1, 1, 1, 1 / 2, 1 / 3],
                [1 / 3, 1 / 2, 1 / 2, 1 / 2, 1 / 2, 1 / 2, 1 / 3],
                [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3],
            ]
        )
        self.kernel[2][2] = -u * np.sum(self.kernel)

        self.inherent_fitness_increment_prob = 0.001
        self.inherent_fitness_increment_amt = 0.1
        self.normalization_constant = 24 * (1 + self.u)

    def make_pd_results(self):
        """
        Makes an n x m array, where elements are the fitnesses that agents get
        from playing the PD, both from defecting and from having others
        cooperate with them.  Boundary conditions are periodic, i.e. agents at
        the far left play against agents at the far right.
        """
        coop_array = np.array(
            [
                [1 if agent.cooperate_p(self.curr_step) else 0 for agent in row]
                for row in self.array
            ]
        )

        pd_results = correlate2d(coop_array, self.kernel, mode="same", boundary="wrap")
        return pd_results

    def make_fitness_array(self):
        """
        Makes an n x m array, where each element is that agent's fitness,
        derived from its and others' behaviors and their inherent fitnesses.
        """
        inherent_fitnesses = np.array(
            [[agent.inherent_fitness for agent in row] for row in self.array]
        )
        pd_results = self.make_pd_results()
        return pd_results + inherent_fitnesses

    def step(self):
        """
        Runs a step of the simulation.
        * Calculate fitness of each agent
        * Figure out who conquers whom, and let them conquer
        * Randomly increment inherent fitnesses
        """
        # make fitness array
        arr = self.make_fitness_array()

        # determine who conquers whom in the local area
        # ORIGINAL IMPLEMENTATION:
        # for "conquering", we look at every cell in a random order
        # after picking a cell we then look at ONE OF the four "direct" neighbors (cardinal directions)
        # we compare fitnesses. If our current cell is higher, do nothing.
        # If our current cell has lower fitness we can be replaced with the other cell

        conquering_pairs = []  # Pairs of (conqueror, to_be_conquered)
        locs = [(x, y) for x in range(self.m) for y in range(self.m)]
        np.random.shuffle(locs)
        for x, y in locs:
            cells_to_compare = [
                ((x - 1) % self.m, y),
                ((x + 1) % self.m, y),
                (x, (y - 1) % self.n),
                (x, (y + 1) % self.n),
            ]
            look_loc = cells_to_compare[random.randint(0, 3)]

            invader_val = arr[look_loc[0]][look_loc[1]]
            curr_val = arr[x][y]

            if invader_val > curr_val:
                if (
                    invader_val - curr_val
                ) / self.normalization_constant > np.random.rand(1, 1):
                    conquering_pairs.append((look_loc, (x, y)))

        # have conquering happen [update matrices/agents] -> mutation at odds mut_chance or whatever
        for x in conquering_pairs:
            conqueror_loc = x[0]
            conquered_loc = x[1]
            self.array[conquered_loc[0]][conquered_loc[1]] = copy.deepcopy(
                self.array[conqueror_loc[0]][conqueror_loc[1]]
            )
            self.array[conquered_loc[0]][conquered_loc[1]].mutate(
                mutate_rate=self.mutate_rate, curr_step=self.curr_step
            )

        # Increment random inherent_fitness vars
        for agent in [agent for row in self.array for agent in row]:
            if np.random.random() < self.inherent_fitness_increment_prob:
                agent.inherent_fitness += self.inherent_fitness_increment_amt

        self.curr_step += 1

        return

    def draw_array(self, array, **options):
        """Draws the cells."""
        n, m = array.shape
        options = underride(
            options,
            cmap="binary",
            alpha=0.7,
            vmin=0,
            vmax=1,
            interpolation="none",
            origin="upper",
            extent=[0, m, 0, n],
        )

        plt.axis([0, m, 0, n])
        plt.xticks([])
        plt.yticks([])
        plt.title(f"World state on turn {self.curr_step}")

        return plt.imshow(array/2, **options)

    def draw(self, interval=None, step=None):
        """
        Gets the current np array state then draws the array
        """
        arr = np.asarray(
            [[agent.strategy.value for agent in row] for row in self.array]
        )
        self.draw_array(arr)

    def animate(self, frames, interval=None, skip=0, step=None):
        """Animate the automaton.

        frames: number of frames to draw
        interval: time between frames in seconds
        iters: number of steps between frames
        """
        if step is None:
            step = self.step

        if interval is None:
            interval = 0.01

        plt.figure()
        try:
            for i in range(frames - 1):
                self.draw()
                # plt.show(block=False)
                plt.pause(interval)
                for _ in range(skip + 1):
                    step()
                plt.clf()
                # clear_output(wait=True)
            self.draw()
            plt.show()
        except KeyboardInterrupt:
            pass

    def get_stats(self):
        """
        Get some summary statistics that might be useful for graphing.  Stats
        are returned as a dict.
        Stats are:
        * "time" : current timestep
        * "num_c", "num_d", "num_s": Number of agents in each state
        TODO: Should we refactor this so it returns lists or something?
        """

        stats = {"time": self.curr_step}

        def count_strat(s):
            return np.sum(
                [
                    (1 if agent.strategy == s else 0)
                    for row in self.array
                    for agent in row
                ]
            )

        stats["num_c"] = count_strat(Strategy.c)
        stats["num_d"] = count_strat(Strategy.d)
        stats["num_s"] = count_strat(Strategy.s)

        return stats


class Agent:
    def __init__(self, strategy=Strategy.d, silent_coop=False):

        self.silent_coop_chance = 1e-4
        self.inherent_fitness = 0
        self.strategy = strategy
        self.coop_valid = silent_coop

        if silent_coop:
            if np.random.random() < self.silent_coop_chance:
                self.silent_coop = True
                self.time_to_cooperate = int(np.random.exponential(200))
                self.strategy = Strategy.s
                # print(self.time_to_cooperate)
            else:
                self.time_to_cooperate = None
                self.silent_coop = False
        else:
            self.time_to_cooperate = None
            self.silent_coop = False

    def __tostr__(self):
        return str(self.strategy)

    def cooperate_p(self, t):
        if self.strategy == Strategy.c:
            return True
        if self.strategy == Strategy.d:
            return False
        if self.strategy == Strategy.s:
            return self.time_to_cooperate < t

    def mutate(self, mutate_rate, curr_step):
        """
        Placeholder function; fort the first type of world we do not have a mutate function,
        so we will come back to implmenet later
        """
        num = np.random.rand()
        if num < mutate_rate:
            if self.coop_valid:
                self.strategy = Strategy.s
                self.time_to_cooperate = int(np.random.exponential(200)) + curr_step
                # print("that worked?!", self.time_to_cooperate)
            else:
                if self.strategy == Strategy.d:
                    self.strategy = Strategy.c


if __name__ == "__main__":
    mutate_rate = 1e-2
    # world = BasicWorld(n=50, mutate_rate=mutate_rate, bounds=(17, 17, 22, 22), silent_coop=False)
    world = BasicWorld(n=50, mutate_rate=mutate_rate, silent_coop=True)

    stats = {"time": [], "num_c": [], "num_d": [], "num_s": []}
    num = 10000
    for x in range(num):
        world.step()
        for key, value in world.get_stats().items():
            if type(value) == np.int64:
                stats[key].append(int(value))
            else:
                stats[key].append(value)

        if x % 1000 == 0:
            world.animate(1)
            print(x / num * 100)

    world.animate(1)

    plt.plot(stats["time"], stats["num_c"], label="Cooperators")
    plt.plot(stats["time"], stats["num_d"], label="Defectors")
    plt.plot(stats["time"], stats["num_s"], label="Silents")

    plt.xlabel("Time (steps)")
    plt.ylabel("Number of agents")
    plt.legend()

    file = f'{num}_timesteps_on_{datetime.datetime.now().strftime("%B %d %Y at %I:%M:%S%p")}.json'
    json.dump(stats, open("jsons/" + file, "w"), sort_keys=True, indent=4)

    plt.show()
