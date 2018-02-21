import os
import numpy as np
from polarimeter import Polarimeter

results_file = "/Users/maglorzatanguyen/Desktop/rerun.txt"
path = "/Users/maglorzatanguyen/Desktop/results_trace1"
for filename in os.listdir(path):
    with open(results_file, 'w') as f:
        if filename.endswith(".txt"):
            filepath = os.path.join(path + "/" + filename)
            data = np.loadtxt(filepath, delimiter=',', dtype=np.dtype('d'), unpack=True)
            p = Polarimeter(source=data, sourceargs={'capture_time': 1, })
            p.measure()
            f.write("{},{},{}\n".format(p.last_measured, p.phase_difference, p.stdeviation))