import numpy as np
from scipy.signal import correlate
from scipy.fftpack import fft, fftfreq

class PolarimeterData:
	def __init__(self, filename):
		self.t, self.chA, self.chB = self.load_file(filename)
		self.rotation = 360 * self.calc_time_delay() * self.calc_motor_freq()

	def load_file(self, filename):
		"""Return np arrays (time, chA, chB)"""
		f = open(filename, 'r').read().rstrip()
		data = [line.split(',') for line in f.split('\n')]
		data = np.array(data, dtype='float')
		return data[:,0], data[:,1], data[:,2]

	def calc_time_delay(self):
		"""Returns the time delay between the two signals.

		For a nice graph, you can plot time vs cross-correlation. But in
		this context we just want the time delay, which is the time at
		which the correlation is at its maximum.
		"""
		corr = correlate(self.chA, self.chB)
		t = np.concatenate((self.t[::-1]*-1,self.t[1::]))
		return t[corr.argmax()]

	def calc_motor_freq(self):
		"""Do FFT on both channels to get the frequency of the motor's
		rotation. They should be identical. If it isn't, something has
		gone very wrong.
		"""

		def calc_fft(time, signal):
			frequencies = fftfreq(signal.size, time[1]-time[0])
			F = fft(signal)
		
			"""Next few lines taken from:
			gribblelab.org/scicomp/09_Signals_sampling_filtering.html
			Need to double check that this is strictly acceptable.
			"""
			ipos = frequencies > 0 
			frequencies = frequencies[ipos] # only look at +ve freqs
			magnitudes = abs(F[ipos]) # magnitude spectrum
			return (frequencies, magnitudes)

		# Calculate frequency-magnitude from time-voltage
		chA_freq, chA_mag = calc_fft(self.t, self.chA)
		chB_freq, chB_mag = calc_fft(self.t, self.chB)

		# Get most intense frequency
		chA_motor_freq = chA_freq[chA_mag.argmax()]
		chB_motor_freq = chB_freq[chB_mag.argmax()]

		assert chA_motor_freq == chB_motor_freq
		return chA_freq[chA_mag.argmax()]
