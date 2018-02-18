from __future__ import division
import numpy as np
from random import random


def simulate_signals(time=0.3, phase_difference=60, samplingrate=16000):
    """
    capture_time (s)
    phase_difference (degrees)
    samplingrate (Hz)
    """
    t = np.arange(0, time, 1/samplingrate)
    f = 10
    A = 0.6
    B = 0.7
    T0 = 0.2
    # Random initial phase for chA
    phiA = 0
    sigA = A * np.cos(2 * np.pi * f * t + phiA) ** 2 + T0
    sigA += np.random.rand(len(sigA)) * 0.01

    # Add the phase difference for chB
    phiB = phiA - np.pi * (1/3)
    sigB = B * np.cos(2 * np.pi * f * t + phiB) ** 2 +T0
    sigB += np.random.rand(len(sigB)) * 0.01
    return t, sigA, sigB