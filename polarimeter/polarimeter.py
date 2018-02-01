from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
from labview import acquire
import time


class Polarimeter:
    def __init__(self, acq_time=1):
        """
        data_source: function that returns (t, chA, chB)
        """
        self.t = acq_time
        self.last_measured = None
        self.phase_difference = None

    def measure(self):
        timestamp = int(time.time())

        data = acquire(self.t)

        self.phase_difference = self.__calc_phase_difference(*data)
        self.last_measured = timestamp

    def __calc_phase_difference(self, time, obj, ref):
        """Calculate the phase difference between the reference and object
        signals. Returns phase difference in degrees.

        Arguments (1D arrays or lists):
            time: sampling times
            obj: object beam signal
            ref: reference beam signal
        """
        obj = self.__low_pass_filter(time, obj)
        ref = self.__low_pass_filter(time, ref)

        obj = self.__apodise(time, obj)
        ref = self.__apodise(time, ref)

        obj = self.__band_pass_filter(time, obj)
        ref = self.__band_pass_filter(time, ref)

        delta_phi = np.angle(obj * ref.conjugate(), deg=True) / 2
        delta_phi = delta_phi[int(len(delta_phi)*0.2):int(len(delta_phi)*0.8)]
        delta_phi = np.mean(delta_phi)
        return delta_phi

    def __low_pass_filter(self, time, signal, fwhm=100):
        """Apply a low pass filter to the signal (np.array).

        Returns np.array containing the low-pass filtered signal.
        """
        f = fftfreq(len(time), time[1]-time[0])
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        freq = 0
        lp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
        return ifft(fft(signal) * lp_filter)

    def __apodise(self, time, signal):
        """__Apodise the signal. Expects and returns np.arrays.
        """
        return signal * np.blackman(len(time))

    def __band_pass_filter(self, time, signal, sigma=2):
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
