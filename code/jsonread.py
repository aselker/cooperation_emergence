
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from time import sleep
from enum import Enum
import copy
from scipy.signal import correlate2d
import random
import time
import datetime
import json
import os

stats = json.load(open('jsons/100000_timesteps_on_December 10 2019 at 11:48:20AM.json'))

if max(stats["num_c"]) > 0:
	plt.plot(stats["time"], stats["num_c"], label="Cooperators")
if max(stats["num_d"]) > 0:
	plt.plot(stats["time"], stats["num_d"], label="Defectors")
if max(stats["num_s"]) > 0:
	plt.plot(stats["time"], stats["num_s"], label="Silents")
# if max(stats["num_t"]) > 0:
# 	plt.plot(stats["time"], stats["num_t"], label="Tit-For-Tats")

plt.xlabel("Time (steps)")
plt.ylabel("Number of agents")
plt.legend()
plt.show()
