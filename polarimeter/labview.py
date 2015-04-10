import socket
import time
import numpy as np

socket.setdefaulttimeout(60) # seconds

def acquire(acq_time, IP='155.198.231.92', port=5020):
	"""Sends a TCP/IP request to the computer at the specified
	IP address and port to initiate data capture (with acq_time
	in seconds). Computer will then use WinSCP to copy the file
	back to this computer in:
		/home/dcb/polarimeter/data/
	Function uses returned filename of CSV file to get and return
	numpy arrays:
		t, ch A (V), and ch B (V)
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((IP, port))
	sock.send('%.2f\r' % acq_time)
	assert sock.recv(1024) == 'acquiring'
	time.sleep(acq_time + 1)
	filename = sock.recv(1024)
	assert filename[-3:] == 'csv'
	sock.close()
	data = np.loadtxt('data/' + filename, delimiter=',')
	return (data[:,0], data[:,1], data[:,2])
