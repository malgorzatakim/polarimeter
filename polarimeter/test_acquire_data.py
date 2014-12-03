from __future__ import division
import unittest
import acquire_data
import os

class AcquireDataTestCase(unittest.TestCase):
	"""Tests for acquire_data.py"""

	def test_acquire_returns_as_expected(self):
		samples = 6000
		sample_rate = 1E6
		time, chA, chB = acquire_data.main(samples, sample_rate)

		self.assertTrue(len(time) == len(chA) == len(chB) == samples)
		self.assertTrue(time[-1] == (samples-1) / sample_rate)
		self.assertIsInstance(time, list)
		self.assertIsInstance(chA, list)
		self.assertIsInstance(chB, list)

	def test_high_sample_rate_raises_exception(self):
		self.assertRaises(AssertionError, acquire_data.main, 6000, 1E100)

	def test_too_many_samples_raises_exception(self):
		self.assertRaises(AssertionError, acquire_data.main, 60000, 1E10)

	def test_directory_does_not_change(self):
		initial_dir = os.getcwd()
		time, chA, chB = acquire_data.main(6000, 1E6)
		final_dir = os.getcwd()
		self.assertTrue(initial_dir == final_dir)

if __name__ == '__main__':
	unittest.main()