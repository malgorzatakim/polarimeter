from __future__ import division
import unittest
import labview
import numpy as np

class Test(unittest.TestCase):
	"""Tests for labview.py"""

	def test_acquire(self):
		"""Test that labview.acquire returns data as expected."""
		capture_time = 1
		t, a, b = labview.acquire(capture_time)

		for ch in [t, a, b]:
			self.assertIsInstance(ch, np.ndarray)

		self.assertAlmostEqual(t[-1], capture_time, places=2)

if __name__ == '__main__':
	unittest.main()