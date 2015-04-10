from __future__ import division
import unittest
import control

class Test(unittest.TestCase):
	"""Tests for control.py"""

	def test_gimbal(self):
		c = control.Controller('/dev/ttyACM0')
		self.assertIs(c.gimbal(power=True), True)
		self.assertIs(c.gimbal(power=False), False)		

	def test_laser(self):
		c = control.Controller('/dev/ttyACM0')
		self.assertIs(c.laser(power=True), True)
		self.assertIs(c.laser(power=False), False)		

if __name__ == '__main__':
	unittest.main()