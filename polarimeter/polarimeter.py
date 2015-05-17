from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
import time
import labview


def calc_phase_difference(time, obj, ref):
    """Calculate the phase difference between the reference and object
    signals. Returns phase difference in degrees.

    Arguments (1D arrays or lists):
        time: sampling times
        obj: object beam signal
        ref: reference beam signal
    """

    obj = low_pass_filter(time, obj)
    ref = low_pass_filter(time, ref)

    obj = apodise(time, obj)
    ref = apodise(time, ref)

    obj = band_pass_filter(time, obj)
    ref = band_pass_filter(time, ref)

    delta_phi = np.angle(obj * ref.conjugate(), deg=True) / 2
    delta_phi = delta_phi[len(delta_phi)*0.2:len(delta_phi)*0.8]
    delta_phi = np.mean(delta_phi)
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
    return signal * np.blackman(len(time))


def band_pass_filter(time, signal, sigma=0.8, freq=None):
    """Apply band pass filter to signal.

    Sigma is the width of the filter. Center frequency automatically
    found by the max in the FFT, but you can override this by specifying
    freq (Hz).

    Expects and returns 1-D np.arrays.
    """
    f = fftfreq(len(time), time[1]-time[0])
    sigfft = fft(signal)

    if freq is None:
        freq = f[f>1][np.argmax(sigfft[f>1])]
        
    bp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
    return ifft(sigfft * bp_filter)

def measure(capture_time=5):
    """Acquire data (capture time in seconds) then calculate the phase
    difference.

    Returns Unix timestamp (when the capture started, int) and
    phase difference in degrees.
    """
    timestamp = int(time.time())
    t, a, b = labview.acquire(capture_time)
    phase_difference = calc_phase_difference(t, a, b)
    return timestamp, phase_difference


def write_result(filename, timestamp, phase_difference):
    """Append the timestamp and phase_difference to filename."""
    f = open(filename, 'a')
    string = '{}, {:.15f}\n'.format(timestamp, phase_difference)
    f.write(string)
    f.close()
    return string


def pretty_print_result(timestamp, phase_difference):
    print('{:s}, {:07.3f} degrees'.format(time.asctime(time.gmtime(timestamp)),
                                          phase_difference))
