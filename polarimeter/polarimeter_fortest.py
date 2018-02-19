from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
from labview import acquire
import time
from plotting import plot
import matplotlib.pyplot as plt

class Polarimeter:
    def __init__(self, source, sourceargs=None):
        """
        data_source: function that returns (t, chA, chB)
        """
        self.source = source
        self.sourceargs = sourceargs
        self.last_measured = None
        self.phase_difference = None

    def measure(self):
        timestamp = int(time.time())

        if self.sourceargs is not None:
            data = self.source(**self.sourceargs)
        else:
            data = self.source()

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
        obj1 = self.__low_pass_filter(time, obj)
        ref1 = self.__low_pass_filter(time, ref)

        obj2 = self.__apodise(time, obj1)
        ref2 = self.__apodise(time, ref1)

        obj3 = self.__band_pass_filter(time, obj2)
        ref3 = self.__band_pass_filter(time, ref2)

        """
        np.angle converts complex no. into angle in degrees if deg=True
        .conjugate() returns complex conjugate
        divided by two because optical rotation = phase difference by 2 (?) value given is most probably
        the optical rotation not the phase difference
        """

        delta_phi = np.angle(obj3 * ref3.conjugate(), deg=True) / 2
        delta_phi_crop = delta_phi[int(len(delta_phi)*0.25):int(len(delta_phi)*0.75)]
        delta_phi_st = np.std(delta_phi_crop)
        delta_phi_mean = np.mean(delta_phi_crop)
        print delta_phi_st
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        ax1.plot(time, np.real(ref), time, np.real(obj))
        plt.title('raw data')
        ax2 = fig.add_subplot(222)
        ax2.plot(time, np.real(ref1), time, np.real(obj1))
        plt.title('after low pass')
        ax3 = fig.add_subplot(223)
        #ax3.plot(time, np.real(ref2), time, np.real(obj2))
        #plt.title('after apodise')
        ax3.plot(time, delta_phi)
        plt.title('delta_phi')
        ax4 = fig.add_subplot(224)
        ax4.plot(time, np.real(ref3), time, np.real(obj3))
        plt.title('after band pass')
        plt.show()
        """
        """
        data_obj = [obj, obj1, obj2, obj3]
        data_ref = [ref, ref1, ref2, ref3]
        titles = ["raw data", "after low pass", "after apodise", "after band pass"]
        plot(time, data_obj, data_ref, titles)
        """
        return delta_phi_mean

    def __low_pass_filter(self, time, signal, fwhm=100):
        """Apply a low pass filter to the signal (np.array).

        Returns np.array containing the low-pass filtered signal.
        """
        f = fftfreq(len(time), time[1]-time[0])
        #lp_filter = 1 /(1 + (f / 100) ** 2)
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        freq = 0
        lp_filter = np.exp(-(f-freq)**2 / (2*(sigma**2)))
        return ifft(fft(signal) * lp_filter)

    def __apodise(self, time, signal):
        """__Apodise the signal. Expects and returns np.arrays.
        """
        return signal * np.blackman(len(time)) #why blackman

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
