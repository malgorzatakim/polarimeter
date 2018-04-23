from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
import time
import matplotlib.pyplot as plt
from math import sqrt, ceil
from numpy.fft import rfft, irfft, rfftfreq
from scipy import signal
#from plotter import Plotter

class Polarimeter:
    def measure(self, time, obj, ref, plot = False):
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

        if plot:
            plotter = Plotter()
            plotter.addPlot([time, ref, time, obj, "raw_data"])
            plotter.addPlot([time, np.real(ref1), time, np.real(obj1), "fd;lfdraw_data"])
            plotter.addPlot([time, np.real(ref2), time, np.real(obj2), "raw_daflkdjfldskta"])
            plotter.addPlot([time, np.real(ref3), time, np.real(obj3), "raw_dajklsdfkjlsta"])
            plotter.show()

        """
        np.angle converts complex no. into angle in degrees if deg=True
        .conjugate() returns complex conjugate
        divided by two because optical rotation = phase difference by 2 (?) value given is most probably
        the optical rotation not the phase difference
        """
        delta_phi = np.angle(obj3 * ref3.conjugate(), deg=True) / 2
        delta_phi = delta_phi[int(len(delta_phi)*0.2):int(len(delta_phi)*0.8)]
        delta_phi_std = np.std(delta_phi)
        delta_phi_mean = np.mean(delta_phi)


        # Alternative calculation
        print "\nHIL_B"
        obj_filtered = self.__band_pass_filter2(time, obj2)
        ref_filtered = self.__band_pass_filter2(time, ref2)

        obj_h = signal.hilbert(obj_filtered)
        ref_h = signal.hilbert(ref_filtered)
        phases = np.angle(obj_h / ref_h, deg=True) / 2
        #phases = (np.angle(obj_h, deg=True) - np.angle(ref_h, deg=True)) / 2
        #phases = phases[int(len(phases)*0.2):int(len(phases)*0.8)]
        phases_std = np.std(phases)
        phases_mean = np.mean(phases)
        print phases_mean, phases_std
        print "HIL_E\n"


        return delta_phi_mean, delta_phi_std

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

    def __band_pass_filter2(self, time, signal, min_freq=5, sigma=2):
        # 1. Get frequency domain.
        # Full frequency domain
        freq_real = rfftfreq(len(time), time[1]-time[0])
        # Adjust frequency domain - input signal has only real values
        #freq_real = np.abs(freq_full[0: len(time) // 2 + 1])

        # 2. Do DFT for a real-valued signal.
        sigrfft = rfft(signal)

        # 3. Find freq with max amplitude in the DFT result.
        # Consider only fft values for freqs > min_freq
        sigrfft_above_min = sigrfft[freq_real > min_freq]
        # Get corresponding freqs
        freq_real_above_min = freq_real[freq_real > min_freq]
        # Find freq with max amplitude - np.abs needed for np.argmax to choose
        # complex number from sigrfft_above_min with biggest magnitude
        freq_max_amp = freq_real_above_min[np.argmax(np.abs(sigrfft_above_min))]

        # 4. Prepare filter for filtering out values from our DFT result.
        # Guassian filter
        bp_filter = np.exp(-(freq_real-freq_max_amp)**2 / (2*(sigma**2)))
        # Rectangular filter - bitmask
        #bp_filter = [int(np.abs(f - freq_max_amp) <= sigma) for f in freq_real]


        return irfft(sigrfft * bp_filter)
