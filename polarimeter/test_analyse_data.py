from __future__ import division
import unittest
import analyse_data
import numpy as np

def simulate_signals(t, f=3, phiA=0, phiB=0, dcA=-0.1, dcB=0.2, ampA=1,
					 ampB=0.7, noise=0):
	random_noise = np.random.normal(size=len(t))
	sigA = (ampA * (np.cos(2 * np.pi * f * t + phiA)) ** 2 + dcA
			+ random_noise * noise)

	random_noise = np.random.normal(size=len(t))
	sigB = (ampB * (np.cos(2 * np.pi * f * t + phiB)) ** 2 + dcB
			+ random_noise * noise)
	return sigA, sigB

class AnalyseDataTestCase(unittest.TestCase):
	"""Tests for analyse_data.py"""

	def test_analysis_no_noise(self):
		"""Test analysis with a perfect, noiseless signal."""
		t = np.arange(0, 1, 0.01)
		phiB = np.pi * 0.33
		sigA, sigB = simulate_signals(t, phiB=phiB, noise=0)
		calc_phiB = analyse_data.calc_phase_difference(t, sigA, sigB)
		self.assertEqual(round(phiB,3), round(calc_phiB,3))

	def test_analysis_with_noise(self):
		"""Test analysis with a noisy simulated signal. Note that this
		is different to no noise test in that it uses more data (longer
		time period) and rounds to just 2 d.p. rather than 3.
		"""
		t = np.arange(0, 10, 0.01)
		phiB = np.pi * 0.33
		sigA, sigB = simulate_signals(t, phiB=phiB, noise=0.02)
		calc_phiB = analyse_data.calc_phase_difference(t, sigA, sigB)
		self.assertEqual(round(phiB,2), round(calc_phiB,2))

if __name__ == '__main__':
	unittest.main()