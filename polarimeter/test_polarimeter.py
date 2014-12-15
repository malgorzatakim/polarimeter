from __future__ import division
import unittest
import polarimeter
import os
import numpy as np

class Test(unittest.TestCase):
	"""Tests for polarimeter.py"""

	def test_simulate_signals(self, repeat=1):
		"""Test that simulate_signals, which is later used to test the
		phase difference algorithm, behaves exactly as
		polarimeter.acquire() does. Single measurement (no repeat).
		"""
		n = 100
		t, a, b = simulate_signals(np.arange(n), repeat=repeat)
		self.assertIs(type(t), list)
		self.assertIs(type(a), list)
		self.assertIs(type(b), list)

		self.assertEqual(len(t), n)
		self.assertEqual(len(a), repeat)
		self.assertEqual(len(b), repeat)

		self.assertEqual(len(a[0]), n)
		self.assertEqual(len(b[0]), n)

	def test_simulate_multiple_signals(self):
		"""Test that simulate_signals returns multiple signals for
		"repeat" measurements.
		"""
		self.test_simulate_signals(repeat=3)

	def test_simulated_analysis_no_noise(self):
		"""Test analysis with a perfect, noiseless signal."""
		phiB = np.pi * 0.33
		t, sigA, sigB = simulate_signals(np.arange(0, 1, 0.01), phiB=phiB)
		phi = polarimeter.calc_phase_difference(t, sigA, sigB)
		self.assertEqual(round(phiB, 3), round(phi, 3))

	def test_simulated_analysis_with_noise(self):
		"""Test analysis with a noisy simulated signal. Note that this
		is different to no noise test in that it uses more data (longer
		time period) and rounds to just 1 d.p. rather than 3.
		"""
		phiB = np.pi * 0.33
		t, sigA, sigB = simulate_signals(np.arange(0, 10, 0.01), phiB=phiB,
										 noise=0.02)
		phi = polarimeter.calc_phase_difference(t, sigA, sigB)
		self.assertEqual(round(phiB, 1), round(phi, 1))

	def test_simulated_multiple_signal_analysis(self):
		"""Test analysis with multiple perfect signals to check
		analyse_data handles input correctly.
		"""
		phiB = np.pi * 0.33
		t, chA, chB = simulate_signals(np.arange(0, 1, 0.01), repeat=5,
									   phiB=phiB)
		phi = polarimeter.calc_phase_difference(t, chA, chB)

		for i in phi:
			self.assertEqual(round(phiB, 3), round(i, 3))

def simulate_signals(t, f=3, phiA=0, phiB=0, dcA=-0.1, dcB=0.2,
					  ampA=1, ampB=0.7, noise=0, repeat=1):
	"""Simulate signals. Returns exactly as acquire does.
	"""
	t = np.array(t)

	sigA = []
	sigB = []

	while len(sigA) < repeat:
		random_noise = np.random.normal(size=len(t))
		sigA.append(list(ampA * (np.cos(2 * np.pi * f * t - phiA)) ** 2 + dcA
				+ random_noise * noise))

		random_noise = np.random.normal(size=len(t))
		sigB.append(list(ampB * (np.cos(2 * np.pi * f * t - phiB)) ** 2 + dcB
				+ random_noise * noise))
	return list(t), sigA, sigB

if __name__ == '__main__':
	unittest.main()