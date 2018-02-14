from __future__ import division
import numpy as np
from random import random


def simulate_signals(time=1, phase_difference=60, samplingrate=125000):
    """
    capture_time (s)
    phase_difference (degrees)
    samplingrate (Hz)
    """
    t = np.arange(0, time, 1/samplingrate)
    f = 10
    A = 1
    # Random initial phase for chA
    phiA = random() * 2 * np.pi
    sigA = A * np.cos(2 * np.pi * f * t + phiA) ** 2
    sigA += np.random.rand(len(sigA)) * 0.01 * A

    # Add the phase difference for chB
    phiB = phiA - (phase_difference * np.pi / 180)
    sigB = A * np.cos(2 * np.pi * f * t + phiB) ** 2
    sigB += np.random.rand(len(sigB)) * 0.01 * A
    return t, sigA, sigB
