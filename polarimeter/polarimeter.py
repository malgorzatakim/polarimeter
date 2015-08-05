from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
import time
import labview
import os


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


def band_pass_filter(time, signal, sigma=2):
    """Apply band pass filter to signal (positve frequencies only).

    Sigma is the width of the filter. Freq is automatically picked.

    Expects and returns 1-D np.arrays.
    """
    f = fftfreq(len(time), time[1]-time[0])
    sigfft = fft(signal)

    highpass = 5  # Hz, anything below ignored
    
    """
    Note that the maximum is picked from np.abs(sigfft) not just
    sigfft or sigfft**2 and then the bp_filter is applied to sigfft
    (rather than np.abs(sigfft) or sigfft**2).
    """
    freq = f[f>highpass][np.argmax(np.abs(sigfft)[f>highpass])]
    bp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
    return ifft(sigfft * bp_filter)

def measure(capture_time=1, save_data=False):
    """Acquire data (with capture time in seconds) and calculate the phase
    difference.

    Returns:
        Unix timestamp when the capture started
        Phase difference (degrees)

    If save_data is true, the signal is recorded and kept in
    ~/dcb/polarimeter/data/signals.
    """
    timestamp = int(time.time())
    t, a, b  = labview.acquire(capture_time, save_data=save_data)
    phase_difference = calc_phase_difference(t, a, b)
    return timestamp, phase_difference


def write_result(filename, timestamp, phase_difference):
    """Append to filename the timestamp and phase difference.
    Returns line that was written as a string.
    """
    f = open(filename, 'a')
    string = '{}, {:.15f}\n'.format(timestamp, phase_difference)
    f.write(string)
    f.close()
    return string


def pretty_print_result(timestamp, phase_difference):
    line = '{:s}, {:07.3f} degrees'
    print(line.format(time.asctime(time.gmtime(timestamp)),
                      phase_difference))


def run(output_file=None, duration=30, units='s', print_output=True,
        log_signals=False):
    """Repeatedly run measurements for specified duration.
 
    Returns mean and std of phase differences, and number of measurements.

    Parameters
    ----------
    output_file : str, optional
        Filename where to save timestamp and phase difference.
    duration : int
        Time to repeat measurements for
    units: str
        's'(econds), 'm'(inutes), 'h'(ours) or 'd'(ays).
    print_output: bool
        If true, print time and phase difference; default: True.
    log_signals: bool
        Save raw signal data; default: False.
    
    Example
    -------
    run('foo.txt', duration=3, units='s')

    """

    if output_file is None:
        output_file = 'temp.txt'

    # Convert time into seconds
    if units == 's': # seconds
        pass
    elif units == 'm': # minutes
        duration *= 60
    elif units == 'h': # hours
        duration *= 60 * 60
    elif units == 'd': # days
        duration *= 24 * 60 * 60
    else:
        raise ValueError(('Unit must be seconds (s), minutes (m), hours (h)'
                          ' or days (d).'))

    start = time.time()
    
    # repeatedly acquire data
    while time.time() < start + duration:
        t, phi = measure(save_data=log_signals)
        write_result(output_file, t, phi)

        if print_output:
            pretty_print_result(t, phi)
    
    # load all the data to compute stats
    t, phi  = np.loadtxt(output_file, delimiter=',', unpack=True)

    if output_file is 'temp.txt':
        os.remove('temp.txt')

    return np.mean(phi), np.std(phi, ddof=1), len(phi)

if __name__ == '__main__':
    mean, std, n = run()
    print('{:.3f} +/- {:.3f} deg (n = {})'.format(mean, std, n))
