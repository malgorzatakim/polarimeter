from polarimeter import Polarimeter
import time
import os

p = Polarimeter()

x = 150 # how many flushes to file
y = 5 # experiment count per one flush
timestamp = int(time.time())
results_file = os.path.join("C:\\polarimeter\\results\\" + str(timestamp) + ".txt")
#### build string from 3 parts: path to file (basic name), timestamp, ".txt"

with open(results_file, "w") as f:
  for _ in range(x):
    for _ in range(y):
      p.measure()
      f.write("{},{}\n".format(p.last_measured, p.phase_difference,))
      time.sleep(60)
  f.flush()