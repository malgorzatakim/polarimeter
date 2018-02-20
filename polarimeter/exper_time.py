from polarimeter_fortest import Polarimeter
import time
import os
#from simulator import simulate_signals

#phase_difference = 60
#p = Polarimeter(source=simulate_signals, sourceargs={'phase_difference': phase_difference})
p = Polarimeter()
x = 5 # how many flushes to file
y = 10 # experiment count per one flush
timestamp = int(time.time())
#results_file = os.path.join("/Users/maglorzatanguyen/Desktop/results/" + str(timestamp) + ".txt")
results_file = os.path.join("C:\\polarimeter\\results\\" + str(timestamp) + ".txt")
#### build string from 3 parts: path to file (basic name), timestamp, ".txt"

with open(results_file, "w") as f:
    for _ in range(x):
        for _ in range(y):
            p.measure()
            f.write("{},{},{}\n".format(p.last_measured, p.phase_difference, p.stdeviation))
        #time.sleep(300)
        f.flush()