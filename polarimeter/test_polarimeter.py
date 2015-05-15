from __future__ import division
import unittest
import polarimeter
import numpy as np

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
        phi = polarimeter.calc_phase_difference(time, sigA, sigB)

        self.assertIs(type(phi), np.ndarray)
        self.assertEqual(round(np.mean(np.deg2rad(phi)), 3),
                         round(phiB, 3))

    def test_CPD_simulated_analysis_with_noise(self):
        """Test analysis with a noisy signal."""
        phiB = np.pi * 0.33
        time = np.arange(0, 3, 0.001)
        sigA, sigB = simulate_signals(time, phiB=phiB, noise=0.01)
        phi = polarimeter.calc_phase_difference(time, sigA, sigB)

        self.assertIs(type(phi), np.ndarray)
        self.assertTrue(len(phi) > 1)
        self.assertEqual(round(np.mean(np.deg2rad(phi)), 2),
                         round(phiB, 2))

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
