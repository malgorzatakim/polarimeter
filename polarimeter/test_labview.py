from __future__ import division
import unittest
import labview
import numpy as np

class Test(unittest.TestCase):
	"""Tests for labview.py"""

	def test_simulate_signals(self, repeat=1):
		"""Test that labview.acquire returns data as expected."""
		capture_time = 1
		t, a, b = labview.acquire(capture_time)
		print type(t)
		self.assertIs(type(t), np.ndarray)
		self.assertIs(type(a), np.ndarray)
		self.assertIs(type(b), np.ndarray)
		self.assertAlmostEqual(t[-1], capture_time, places=3)

if __name__ == '__main__':
	unittest.main()