from polarimeter_fortest import Polarimeter
import time
import os
from simulator import simulate_signals
import numpy as np

phase_difference = 60
p = Polarimeter(source=simulate_signals, sourceargs={'phase_difference': phase_difference})
#p = Polarimeter()
x = 6 # how many flushes to file, no of data points
y = 10 # experiments taken into mean
timestamp = int(time.time())
results_file = os.path.join("/Users/maglorzatanguyen/Desktop/results/" + str(timestamp) + ".txt")
#results_file = os.path.join("C:\\polarimeter\\results\\" + str(timestamp) + ".txt")
#### build string from 3 parts: path to file (basic name), timestamp, ".txt"

with open(results_file, "w") as f:
    for _ in range(x):
        t = int(time.time())
        data = []
        for _ in range(y):
            p.measure()
            data.append([p.last_measured, p.phase_difference, p.stdeviation])
        phase = []
        stdev = []
        for i in range(len(data)):
            phase.append(data[i][1])
            stdev.append(data[i][2])
        f.write("{},{},{}\n".format(t, np.mean(phase), np.mean(stdev)))
        f.flush()