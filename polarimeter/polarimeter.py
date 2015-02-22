from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
import bitscope

def measure(filename=None, repeat=30):
    """
    Acquire signal with default of 30 repeats. Calculate phase difference
    and write to filename, if provided. Return list of phase differences.
    All in radians.
    """
    t, a, b = bitscope.acquire(repeat=repeat)
    delta_phi = calc_phase_difference(t, a, b)

    if filename is not None:
        np.savetxt(filename, delta_phi, delimiter=',')

    return delta_phi

def calc_phase_difference(time, obj, ref):
    """Calculate the phase difference between the reference and object
    signals. Returns phase difference in radians.
    
    Arguments:
        time: sampling times
        obj: object beam signal
        ref: reference beam signal

    Obj and ref can be list of lists of voltages at each sample or a
    numpy array of size (n, m) where n is the number of repeats and m is
    the number of samples.

    Returns:
        numpy array of size (n, 1) with each phase difference
    """

    time = np.array(time)
    obj = np.array(obj)
    ref = np.array(ref)

    f = fftfreq(ref.shape[1], time[1]-time[0])

    # low pass filter
    lp_filter = np.ones(obj.shape) / (1 + ((f / 6)**2))
    ref = ifft(fft(ref) * lp_filter)
    obj = ifft(fft(obj) * lp_filter)

    # apodising filter (time domain)
    a0 = 0.355768
    a1 = 0.487396
    a2 = 0.144232
    a3 = 0.012604
    n = np.tile(np.arange(0,len(time),1), (ref.shape[0], 1))
    apodize_filter =  (a0 - a1*np.cos(2*np.pi*n/len(time))
                      + a2*np.cos(4*np.pi*n/len(time))
                      - a3*np.cos(6*np.pi*n/len(time)))
    ref *= apodize_filter
    obj *= apodize_filter

    # bp filter in freq domain
    sig = 1
    f0 = 7
    bp_filter = np.tile(np.exp(-(f-f0)**2 / (2*sig*sig)), (ref.shape[0], 1))
    ref = ifft(fft(ref) * bp_filter)
    obj = ifft(fft(obj) * bp_filter)

    delta_phi = np.angle(obj * ref.conjugate()) / 2
    # exclude outer 25% because of edge effects
    return np.mean(delta_phi[:,delta_phi.shape[1]*0.25:delta_phi.shape[1]*0.75],
                   axis=1)
