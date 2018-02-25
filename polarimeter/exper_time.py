from polarimeter import Polarimeter
from data_acquirers import RealDataAcquirer
import time
import os

capture_time = 1
acquirer = RealDataAcquirer(capture_time)
p = Polarimeter()
x = 5 # how many flushes to file
y = 10 # experiment count per one flush
timestamp = int(time.time())
#results_file = os.path.join("/Users/maglorzatanguyen/Desktop/results/" + str(timestamp) + ".txt")
results_file = os.path.join("C:\\polarimeter\\results\\" + str(timestamp) + ".txt")

with open(results_file, "w") as f:
    for _ in range(x):
        for _ in range(y):
            data = acquirer.acquire()
            phase_diff, stdev = p.measure(*data)
            f.write("{},{},{}\n".format(acquirer.lastDataTimestamp(), phase_diff, stdev))
        #time.sleep(300)
        f.flush()