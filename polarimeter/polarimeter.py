from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq

def calc_phase_difference(time, obj, ref):
    """Calculate the phase difference between the reference and object
    signals. Returns phase differences in degrees.
    
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

    obj = low_pass_filter(time, obj)
    ref = low_pass_filter(time, ref)

    obj = apodise(time, obj)
    ref = apodise(time, ref)

    obj = band_pass_filter(time, obj)
    ref = band_pass_filter(time, ref)

    delta_phi = np.angle(obj * ref.conjugate()) / 2
    delta_phi = delta_phi[len(delta_phi)*0.2:len(delta_phi)*0.8]
    delta_phi = np.rad2deg(delta_phi)
    return delta_phi

def low_pass_filter(time, signal):
    """Apply a low pass filter to the signal (np.array).

    Returns np.array containing the low-pass filtered signal.
    """ 
    f = fftfreq(len(time), time[1]-time[0])
    lp_filter = np.ones(len(signal)) / (1 + ((f / 6)**2))
    return ifft(fft(signal) * lp_filter)

def apodise(time, signal):
    """Apodise the signal. Expects and returns np.arrays.
    """
    a0 = 0.355768
    a1 = 0.487396
    a2 = 0.144232
    a3 = 0.012604
    n = np.arange(0,len(time))
    apodize_filter =  (a0 - a1*np.cos(2*np.pi*n/len(time))
                      + a2*np.cos(4*np.pi*n/len(time))
                      - a3*np.cos(6*np.pi*n/len(time)))
    return signal * apodize_filter

def band_pass_filter(time, signal, freq=3.4, sigma=0.5):
    """Apply band pass filter to signal.

    Optionally specify the center frequency (freq, default 3.4)
    and width (sigma, default 0.5).

    Expects and returns np.arrays.
    """
    f = fftfreq(len(time), time[1]-time[0])
    bp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
    return ifft(fft(signal) * bp_filter)