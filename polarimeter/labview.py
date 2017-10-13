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
import socket
import time
import numpy as np
import os

socket.setdefaulttimeout(60) # seconds

def acquire(capture_time, IP='155.198.231.92', port=5020, save_data=False):
    """Aquires data for capture_time (seconds) via acquisition PC.
    Returns time, and signals of hannel A and channel B.
    """
    if capture_time <= 0:
        raise ValueError('capture_time must be greater than zero.')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))
    sock.send(b'%.2f\r' % capture_time)
    assert sock.recv(1024) == b'acquiring'
    time.sleep(capture_time + 1)
    #filename = sock.recv(1024)
    #assert filename[-3:] == 'csv'
    sock.close()
    signal_file = 'C:\\polarimeter\\trace.csv'
    data = np.loadtxt(signal_file, delimiter=',',
                          dtype=np.dtype('d'), unpack=True)
    if save_data is False:
        os.remove(signal_file)
    return data
