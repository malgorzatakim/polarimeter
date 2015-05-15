from __future__ import division
import unittest
import polarimeter as p
import numpy as np
import time
import os

class Test(unittest.TestCase):
    """Tests for polarimeter.py"""

    def test_simulate_signals(self, repeat=1):
        """Test that simulate_signals, which is later used to test the
        phase difference algorithm, behaves as desired.
        """
        time = np.arange(0, 5, 0.01)
        sigA, sigB = simulate_signals(time)
        self.assertIs(type(sigA), np.ndarray)
        self.assertIs(type(sigB), np.ndarray)
        self.assertEqual(len(sigA), len(time))
        self.assertEqual(len(sigB), len(time))

    """Tests for polarimeter.calc_phase_difference"""
    def test_CPD_simulated_analysis_no_noise(self):
        """Test analysis with a perfect, noiseless signal."""
        phiB = np.pi * 0.33
        time = np.arange(0, 3, 0.001)
        sigA, sigB = simulate_signals(time, phiB=phiB)
        phi = p.calc_phase_difference(time, sigA, sigB)

        self.assertIs(type(phi), np.ndarray)
        self.assertEqual(round(np.mean(np.deg2rad(phi)), 3),
                         round(phiB, 3))

    def test_CPD_simulated_analysis_with_noise(self):
        """Test analysis with a noisy signal."""
        phiB = np.pi * 0.33
        time = np.arange(0, 3, 0.001)
        sigA, sigB = simulate_signals(time, phiB=phiB, noise=0.01)
        phi = p.calc_phase_difference(time, sigA, sigB)

        self.assertIs(type(phi), np.ndarray)
        self.assertTrue(len(phi) > 1)
        self.assertEqual(round(np.mean(np.deg2rad(phi)), 2),
                         round(phiB, 2))

    def test_measure(self):
        """Test p.measure()"""
        start_time = time.time()
        capture_time = 5
        timestamp, phase_difference = p.measure(capture_time)
        end_time = time.time()

        self.assertIsInstance(timestamp, int)
        self.assertIsInstance(phase_difference, float)
        self.assertTrue(end_time - start_time > capture_time)

    def test_write_result(self):
        timestamp, phase_difference = p.measure(1)
        string_written = p.write_result('temp.txt', timestamp,
                                        phase_difference)
        self.assertIsInstance(string_written, str)

	contents = np.loadtxt('temp.txt', delimiter=',', dtype={'names': ('time', 'phi'), 'formats': (np.int32, np.float64)})
        os.remove('temp.txt')
	self.assertEqual(contents['time'], timestamp)
	self.assertAlmostEqual(contents['phi'], phase_difference)


def simulate_signals(t, phiA=0, phiB=0.5, dcA=0.1, dcB=0.2,
                      ampA=1, ampB=1.3, noise=0):
    """Simulate signals.

    Angular rotational frequency f is set to 1.7 Hz as this is roughly
    the frequency in practice. polarimeter.calc_phase_difference expects
    this frequency as the band pass filter is centered there.

    Arguments:
        t: times (1D array)
        phiA and phiB = initial phases (rads)
        dcA and dcB = dc offsets
        ampA and ampB = amplitudes
        noise = noise factor

    Returns:
        sigA, sigB (np arrays)
    """
    f = 1.7
    sigA = (ampA * (np.cos(2 * np.pi * f * t - phiA)) ** 2
        + dcA + np.random.normal(size=len(t)) * noise)
    sigB = (ampA * (np.cos(2 * np.pi * f * t - phiB)) ** 2
        + dcB + np.random.normal(size=len(t)) * noise)
    return sigA, sigB

if __name__ == '__main__':
    unittest.main()
