from labview import acquire
import time
import csv
import numpy as np
import os

x = 7000 #how many flushes to file
y = 10 #no of experiments in a single flush
timestamp = int(time.time())
results_file = os.path.join(
	"C:\\polarimeter\\results\\" + str(timestamp) + "_stab.txt")

with open(results_file, "w") as f:
    for _ in range(x):
    	for _ in range(y):
            times = int(time.time())
            one_acq = acquire(1)
            chA = one_acq[:,1]
            chB = one_acq[:,2]
            chC = one_acq[:,3]
            final_chA = np.mean(chA)
            final_chB = np.mean(chB)
            final_chC = np.mean(chC)
            f.write("{},{},{},{}\n".format(times, final_chA, final_chB, final_chC))
    f.flush()