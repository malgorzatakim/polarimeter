"""
labview.py is a module to interface with a Windows PC running a LabVIEW
VI that acquires data with an NI-DAQ.

Using TCP/IP the VI listens for incoming connections. The requesting
computer sends a message requesting a capture time. The Windows PC
acquires the data, writes it to file, then uses the WinSCP utility to
copy the file to /home/dcb/polarimeter/data/YYYY-MM-DD-HHMMSS.csv.
The requesting computer then loads the file, which contais the time
and signals of the two channels.
"""
#import socket
import time
import numpy as np
import os

#socket.setdefaulttimeout(60) # seconds

def acquire(capture_time):
    """Aquires data for capture_time (seconds) via acquisition PC.
    Returns time, and signals of hannel A and channel B.
    ""
    trigger_path = 'C:\\Users\\jdmgroup\\Desktop\\trigger.txt'

    with open(trigger_path,'w') as f:
        f.write("{}".format(capture_time))

    while True:
        with open(trigger_path,'r') as f:
            if f.read() is "0":
                break
            time.sleep(0.1)
"""
    #signal_file = 'C:\\polarimeter\\trace.csv'
    signal_file = "/Users/maglorzatanguyen/Documents/IMPERIAL/Year_4/pol_combinations/trace_ref_7feb.csv"
    return np.loadtxt(signal_file, delimiter=',', dtype=np.dtype('d'), unpack=True)