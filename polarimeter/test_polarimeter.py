from __future__ import division
import unittest
import polarimeter as p
import numpy as np
import time
import os
from random import random

class Test(unittest.TestCase):
    """Tests for polarimeter.py"""

    def test_simulate_signals(self, repeat=1):
        """Test that simulate_signals, which is later used to test the
        phase difference algorithm, behaves as desired.
        """
        time = np.arange(0, 5, 1/125000)
        phase_difference = random() * 360
        sigA, sigB = simulate_signals(time, phase_difference)

        self.assertIs(type(sigA), np.ndarray)
        self.assertIs(type(sigB), np.ndarray)
        self.assertEqual(len(sigA), len(time))
        self.assertEqual(len(sigB), len(time))

    """Tests for polarimeter.calc_phase_difference"""
    def test_calculate_phase_difference(self):
        """Test analysis with a perfect, noiseless signal."""
        phase_difference = 90 * random()
        time = np.arange(0, 5, 1/12500)
        sigA, sigB = simulate_signals(time, phase_difference)

        calc_phase_difference = p.calc_phase_difference(time, sigA, sigB)
        self.assertIs(type(calc_phase_difference), np.float64)
        self.assertEqual(round(phase_difference, 2),
                         round(calc_phase_difference, 2))

    def test_measure(self):
        """Test p.measure()"""
        start_time = time.time()
        capture_time = 1
        timestamp, phase_difference, laser = p.measure(capture_time)
        end_time = time.time()

        self.assertIsInstance(timestamp, int)
        self.assertIsInstance(phase_difference, float)
        self.assertTrue(end_time - start_time > capture_time)
        self.assertIsInstance(laser, float)

    def test_write_result(self):
        timestamp, phase_difference, laser = p.measure(1)
        string_written = p.write_result('temp.txt', timestamp,
                                        phase_difference, laser)
        self.assertIsInstance(string_written, str)

        contents = np.loadtxt('temp.txt', delimiter=',',
                              dtype={'names': ('time', 'phi', 'laser'),
                              'formats': (np.int32, np.float64, np.float64)})
        os.remove('temp.txt')
        self.assertEqual(contents['time'], timestamp)
        self.assertAlmostEqual(contents['phi'], phase_difference)

def simulate_signals(time, phase_difference):
    """
    phase_difference in degrees
    """
    f = 1.7
    A = 1
    # Random initial phase for chA
    phiA = random() * 2 * np.pi
    sigA = A * np.cos(2 * np.pi * f * time + phiA) ** 2
    sigA += np.random.rand(len(sigA)) * 0.01 * A

    # Add the phase difference for chB
    phiB = phiA - (phase_difference * np.pi / 180)
    sigB = A * np.cos(2 * np.pi * f * time + phiB) ** 2
    sigB +=  np.random.rand(len(sigB)) * 0.01 * A
    return sigA, sigB

if __name__ == '__main__':
    unittest.main()
