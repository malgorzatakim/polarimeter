import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime

source = sys.stdin.read()
source = source.rstrip()
data = np.array([line.split(',') for line in source.split('\n')], dtype='float')

ax = plt.axes()
ax.plot(data[:,0], data[:,1], 'rx', label='ch A')
ax.plot(data[:,0], data[:,2], 'bx', label='ch B')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
plt.legend()

timestamp = datetime.datetime.now()
ax.set_title(timestamp.isoformat(' '))

output_file = 'plots/' + timestamp.isoformat(' ') + '.pdf'
plt.savefig(output_file, bbox_inches='tight')
print output_file