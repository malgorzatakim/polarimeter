from __future__ import division
import unittest
import analyse_data
import numpy as np

class AnalyseDataTestCase(unittest.TestCase):
	"""Tests for analyse_data.py"""
	def test_simulate_signals(self):
		t, a, b = simulate_signals(np.arange(100))
		self.assertIs(type(t), list)
		self.assertIs(type(a), list)
		self.assertIs(type(b), list)

	def test_analysis_no_noise(self):
		"""Test analysis with a perfect, noiseless signal."""
		phiB = np.pi * 0.33
		t, sigA, sigB = simulate_signals(np.arange(0, 1, 0.01), phiB=phiB)
		p = analyse_data.PolarimeterData(t, sigA, sigB)
		self.assertEqual(round(phiB, 3), round(p.phase_difference, 3))

	def test_analysis_with_noise(self):
		"""Test analysis with a noisy simulated signal. Note that this
		is different to no noise test in that it uses more data (longer
		time period) and rounds to just 1 d.p. rather than 3.
		"""
		phiB = np.pi * 0.33
		t, sigA, sigB = simulate_signals(np.arange(0, 10, 0.01), phiB=phiB,
										 noise=0.02)
		p = analyse_data.PolarimeterData(t, sigA, sigB)
		self.assertEqual(round(phiB, 1), round(p.phase_difference, 1))

	def test_multiple_signals(self):
		"""Test analysis with multiple perfect signals to check
		analyse_data handles input correctly.
		"""
		chAs = list()
		chBs = list()
		phiB = np.pi * 0.33
		repeats = 3

		# Generate signals and get into format acquire_data does
		for i in range(repeats):
			t, chA, chB = simulate_signals(np.arange(0, 1, 0.01), phiB=phiB)
			chAs.append(chA) # list of lists of values
			chBs.append(chB)

		p = analyse_data.PolarimeterData(t, chAs, chBs)

		for i in range(repeats):
			self.assertEqual(round(phiB, 3), round(p.phase_difference[i], 3))

		self.assertIs(type(p.phase_difference), list)

def simulate_signals(t, f=3, phiA=0, phiB=0, dcA=-0.1, dcB=0.2,
					  ampA=1, ampB=0.7, noise=0):
	"""Simulate signals. Returns lists as this is what the
	acquire_data module does.
	"""
	t = np.array(t)
	random_noise = np.random.normal(size=len(t))
	sigA = (ampA * (np.cos(2 * np.pi * f * t + phiA)) ** 2 + dcA
			+ random_noise * noise)

	random_noise = np.random.normal(size=len(t))
	sigB = (ampB * (np.cos(2 * np.pi * f * t + phiB)) ** 2 + dcB
			+ random_noise * noise)
	return list(t), list(sigA), list(sigB)

if __name__ == '__main__':
	unittest.main()