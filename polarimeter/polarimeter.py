from __future__ import division
import numpy as np
from scipy.fftpack import ifft, fft, fftfreq
import time
import matplotlib.pyplot as plt
from math import sqrt, ceil
from numpy.fft import rfft, irfft, rfftfreq
from scipy import signal
from plotter import Plotter

class Polarimeter:
    def measure(self, time, obj, ref, plot = False):
        """Calculate the phase difference between the reference and object
        signals. Returns phase difference in degrees.

        Arguments (1D arrays or lists):
            time: sampling times
            obj: object beam signal
            ref: reference beam signal
        """
        obj2 = self.__apodise(time, obj)
        ref2 = self.__apodise(time, ref)

        freq, obj_filtered, objfft3, objfft3_bp = self.__band_pass_filter(time, obj2)
        freq, ref_filtered, reffft3, reffft3_bp = self.__band_pass_filter(time, ref2)

        obj_h = signal.hilbert(obj_filtered)
        ref_h = signal.hilbert(ref_filtered)
        phases = np.angle(obj_h / ref_h, deg=True) / 2
        phases_std = np.std(phases)
        phases_mean = np.mean(phases)

        if plot:
            plotter = Plotter()
            plotter.addPlot([time, obj, time, ref], [0, 0.8, 0, 1.4], "raw_data")
            plotter.addPlot([time, obj2, time, ref2], [0, 0.8, 0, 1.4], "windowed")
            plotter.addPlot([freq, objfft3, freq, reffft3], [0, 2000, -100, 150], "FFTed")
            plotter.addPlot([freq, objfft3_bp, freq, reffft3_bp], [0, 2000, -100, 150], "band_passed")
            plotter.addPlot([time, obj_filtered, time, ref_filtered], [0, 0.8, -0.6, 0.6], "IFFT")
            plotter.addPlot([time, phases], [0, 0.8, 0, 90], "Phase Diff")
            plotter.show()

        return phases_mean, phases_std

    def __apodise(self, time, signal):
        """__Apodise the signal. Expects and returns np.arrays.
        """
        return signal * np.hanning(len(time))

    def __band_pass_filter(self, time, signal, min_freq=5, sigma=0.5):
        # 1. Get frequency domain.
        # Full frequency domain adjusted as input signal has only real values
        freq_real = rfftfreq(len(time), time[1]-time[0])

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

        return freq_real, irfft(sigrfft * bp_filter), abs(sigrfft), abs(sigrfft * bp_filter)