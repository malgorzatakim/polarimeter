import os
import numpy as np

for filename in os.listdir("/Users/maglorzatanguyen/Desktop/results_trace1"):
    if filename.endswith(".txt"):
        np.loadtxt(filename, delimiter=',', dtype=np.dtype('d'), unpack=True)
        

