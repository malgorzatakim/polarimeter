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
    obj = apodise(time, obj)
    ref = apodise(time, ref)

    obj = band_pass_filter(time, obj)
    ref = band_pass_filter(time, ref)

    delta_phi = np.angle(obj * ref.conjugate(), deg=True) / 2
    delta_phi = delta_phi[len(delta_phi)*0.2:len(delta_phi)*0.8]
    delta_phi = np.mean(delta_phi)
    return delta_phi


def low_pass_filter(time, signal, fwhm=100):
    """Apply a low pass filter to the signal (np.array).

    Returns np.array containing the low-pass filtered signal.
    """
    f = fftfreq(len(time), time[1]-time[0])
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    freq = 0
    lp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
    return ifft(fft(signal) * lp_filter)


def apodise(time, signal):
    """Apodise the signal. Expects and returns np.arrays.
    """
    return signal * np.blackman(len(time))


def band_pass_filter(time, signal, sigma=0.43, freq=3.4):
    """Apply band pass filter to signal (positve frequencies only).

    Sigma is the width of the filter. Freq is the position.

    Expects and returns 1-D np.arrays.
    """
    f = fftfreq(len(time), time[1]-time[0])
    bp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
    bp_filter[f <= 0] = 0
    return ifft(fft(signal) * bp_filter)

def measure(capture_time=5, save_data=False):
    """Acquire data (with capture time in seconds) and calculate the phase
    difference.

    Returns:
        Unix timestamp when the capture started
        Phase difference (degrees)
        Mean laser intensity over the capture time.

    If save_data is true, the signal is recorded and kept in
    ~/dcb/polarimeter/data/signals.
    """
    timestamp = int(time.time())
    t, a, b, laser = labview.acquire(capture_time, save_data=save_data)
    phase_difference = calc_phase_difference(t, a, b)
    return timestamp, phase_difference, np.mean(laser)


def write_result(filename, timestamp, phase_difference, laser):
    """Append to filename the timestamp, phase difference, and laser
    intensity. Returns line that was written as a string.
    """
    f = open(filename, 'a')
    string = '{}, {:.15f}, {:.15f}\n'.format(timestamp, phase_difference, laser)
    f.write(string)
    f.close()
    return string


def pretty_print_result(timestamp, phase_difference, laser):
    line = '{:s}, {:07.3f} degrees, laser intensity: {:.3f} V'
    print(line.format(time.asctime(time.gmtime(timestamp)),
                      phase_difference, laser))
