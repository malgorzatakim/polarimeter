from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
import time
import labview


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
    return signal * np.blackman(len(time))


def band_pass_filter(time, signal, freq=3.4, sigma=0.8):
    """Apply band pass filter to signal.

    Optionally specify the center frequency (freq, default 3.4)
    and width (sigma, default 0.5).

    Expects and returns np.arrays.
    """
    f = fftfreq(len(time), time[1]-time[0])
    bp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
    return ifft(fft(signal) * bp_filter)


def measure(capture_time=5):
    """Acquire data (capture time in seconds) then calculate the phase
    difference.

    Returns Unix timestamp (when the capture started) and phase
    difference in degrees.
    """
    timestamp = time.time()
    t, a, b = labview.acquire(capture_time)
    phase_difference = np.mean(calc_phase_difference(t, a, b))
    return timestamp, phase_difference


def write_result(filename, timestamp, phase_difference):
    """Append the timestamp and phase_difference to filename."""
    f = open(filename, 'a')
    string = '{}, {}\n'.format(timestamp, phase_difference)
    f.write(string)
    f.close()
    return string


def pretty_print_result(timestamp, phase_difference):
    print('{:s}, {:07.3f} degrees'.format(time.asctime(time.gmtime(timestamp)),
                                          phase_difference))
