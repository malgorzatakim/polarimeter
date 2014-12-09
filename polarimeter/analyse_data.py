from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq

class PolarimeterData:
	def __init__(self, time, ref, obj):
		"""Object to handle polarimeter data and compute phase
		difference between reference and object beams.

		Arguments:
			time: list of times corresponding to each sample (seconds)
			ref: list of signal measurements (volts) for reference beam
			obj: as for ref but object beam

		Note that ref and obj can be a list of lists, i.e. if repeat
		measurements were made. 

		Attributes:
			self.phase_difference: numpy.array of phase difference
			(radians) between object and reference beam.
		"""

		# zip below requires list of lists, so check
		if not any(isinstance(el, list) for el in ref):
			ref = [ref]

		if not any(isinstance(el, list) for el in obj):
			obj = [obj]

		self.time = time
		self.ref = ref
		self.obj = obj
		self.phase_difference = list()

		for ref, obj in zip(ref, obj):
			self.phase_difference.append(self._calc_phase_difference(time, obj,
																	 ref))

		# if only one PD caluclated, return as number not list of 1
		if len(self.phase_difference) == 1:
			self.phase_difference = self.phase_difference[0]

	def _calc_phase_difference(self, time, obj, ref):
		"""Calculate the phase difference between the reference and object
		signals. Returns phase difference in radians.
		"""
		f = fftfreq(len(ref), time[1]-time[0])

		# low pass filter
		lp_filter = np.ones(len(f)) / (1 + ((f / 6)**2))   
		ref = ifft(fft(ref) * lp_filter)
		obj = ifft(fft(obj) * lp_filter)

		# apodising filter (time domain)
		a0 = 0.355768
		a1 = 0.487396
		a2 = 0.144232
		a3 = 0.012604
		n = np.arange(0,len(time),1)
		apodize_filter =  (a0 - a1*np.cos(2*np.pi*n/len(time))
						  + a2*np.cos(4*np.pi*n/len(time))
						  - a3*np.cos(6*np.pi*n/len(time)))
		ref *= apodize_filter
		obj *= apodize_filter

		# bp filter in freq domain
		sig = 1
		f0 = 7
		bp_filter = np.exp(-(f-f0)**2 / (2*sig*sig))    
		ref = ifft(fft(ref) * bp_filter)
		obj = ifft(fft(obj) * bp_filter)

		delta_phi = np.angle(obj * ref.conjugate()) / 2
		# exclude outer 25% because of edge effects
		return np.mean(delta_phi[len(f)*0.25:len(f)*0.75])