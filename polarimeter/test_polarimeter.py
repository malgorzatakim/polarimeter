from __future__ import division
import unittest
from polarimeter import Polarimeter
from data_acquirers import SimulatedDataAcquirer


class Test(unittest.TestCase):
    """Tests for polarimeter.py"""

    def test_measure(self):
        """Test p.measure() with SimulatedDataAcquirer"""
        phase_difference = 14
        acquirer = SimulatedDataAcquirer(phase_difference=phase_difference)
        p = Polarimeter()
        phase_diff, stdev = p.measure(*acquirer.acquire())
        print phase_diff
        print stdev
        self.assertIsInstance(phase_diff, float)
        self.assertAlmostEqual(phase_diff, phase_difference, places=2)

    def test_measure2(self):
        """Test p.measure() with SimulatedDataAcquirer"""
        phase_difference = 60
        acquirer = SimulatedDataAcquirer(phase_difference=phase_difference, time=0.3, amp_A=1, amp_B=0.9)
        p = Polarimeter()
        phase_diff, stdev = p.measure(*acquirer.acquire())
        print phase_diff
        print stdev
        self.assertIsInstance(phase_diff, float)
        self.assertAlmostEqual(phase_diff, phase_difference, places=2)

if __name__ == '__main__':
    unittest.main()
