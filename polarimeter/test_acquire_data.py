from __future__ import division
import unittest
import acquire_data
import os

class AcquireDataTestCase(unittest.TestCase):
	"""Tests for acquire_data.py"""

	def test_single_acquire_returns_as_expected(self):
		capture_time = 0.25
		time, chA, chB = acquire_data.main(capture_time)

		self.assertTrue(len(time) == len(chA) == len(chB))
		self.assertAlmostEqual(time[-1] / capture_time, 1, places=3) # 0.1%
		self.assertIsInstance(time, list)
		self.assertIsInstance(chA, list)
		self.assertIsInstance(chB, list)

	def test_directory_does_not_change(self):
		initial_dir = os.getcwd()
		time, chA, chB = acquire_data.main(0.1)
		final_dir = os.getcwd()
		self.assertTrue(initial_dir == final_dir)

	def test_repeat_acquire_works(self):
		repeat = 5
		time, chA, chB = acquire_data.main(0.01, repeat)
		self.assertEqual(len(chA), repeat)
		self.assertEqual(len(chB), repeat)
		self.assertEqual(len(chA[0]), len(time))
		self.assertEqual(len(chB[0]), len(time))

if __name__ == '__main__':
	unittest.main()