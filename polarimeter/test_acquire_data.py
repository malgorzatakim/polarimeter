from __future__ import division
import unittest
import polarimeter
import os

class Test(unittest.TestCase):
	"""Tests for acquire_data.py"""

	def test_single_acquire_returns_as_expected(self):
		rate = 50000
		size = 5000
		time, chA, chB = polarimeter.acquire(rate, size)

		self.assertTrue(len(time) == len(chA[0]) == len(chB[0]))
		self.assertAlmostEqual(time[-1] / (size/rate), 1, places=3) # 0.1%
		self.assertIsInstance(time, list)
		self.assertIsInstance(chA, list)
		self.assertIsInstance(chB, list)

	def test_directory_does_not_change(self):
		initial_dir = os.getcwd()
		time, chA, chB = polarimeter.acquire(50000, 5000)
		final_dir = os.getcwd()
		self.assertTrue(initial_dir == final_dir)

	def test_repeat_acquire_works(self):
		repeat = 5
		time, chA, chB = polarimeter.acquire(50000, 5000, repeat)
		self.assertEqual(len(chA), repeat)
		self.assertEqual(len(chB), repeat)
		self.assertEqual(len(chA[0]), len(time))
		self.assertEqual(len(chB[0]), len(time))

if __name__ == '__main__':
	unittest.main()