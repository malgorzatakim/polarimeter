import numpy as np
from scipy.fftpack import ifft, fft, fftfreq

def calc_delta_phi(t, ref, obj):
	f = fftfreq(len(ref), t[1]-t[0])

	# low pass filter
	lp_filter = np.ones(len(f)) / (1 + ((f / 6)**2))   
	ref = ifft(fft(ref) * lp_filter)
	obj = ifft(fft(obj) * lp_filter)

	# apodising filter (time domain)
	a0 = 0.355768
	a1 = 0.487396
	a2 = 0.144232
	a3 = 0.012604
	n = np.arange(0,len(t),1)
	apodize_filter =  (a0 - a1*np.cos(2*np.pi*n/len(t))
					  + a2*np.cos(4*np.pi*n/len(t))
					  - a3*np.cos(6*np.pi*n/len(t)))
	ref *= apodize_filter
	obj *= apodize_filter

	# bp filter in freq domain
	sig = 1
	f0 = 3.5
	bp_filter = np.exp(-(f-f0)**2 / (2*sig*sig))    
	ref = ifft(fft(ref) * bp_filter)
	obj = ifft(fft(obj) * bp_filter)

	delta_phi = np.angle(ref * obj.conjugate())

	# exclude outer 25% because of edge effects
	return np.mean(delta_phi[len(f)*0.25:len(f)*0.75])