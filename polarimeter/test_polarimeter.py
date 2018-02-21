from __future__ import division
import unittest
from polarimeter_fortest import Polarimeter
from simulator import simulate_signals, simulate_signals_j


class Test(unittest.TestCase):
    """Tests for polarimeter.py"""

    def test_measure(self):
        """Test p.measure() with simulate_signals"""
        phase_difference = 14
        p = Polarimeter(source=simulate_signals,
                        sourceargs={'phase_difference': phase_difference})
        p.measure()
        print p.phase_difference
        print p.stdeviation
        self.assertIsInstance(p.last_measured, int)
        self.assertIsInstance(p.phase_difference, float)
        self.assertAlmostEqual(p.phase_difference, phase_difference, places=5)

    def test_measure_j(self):
        """Test p.measure() with simulate_signals_j"""
        phase_difference = 60
        p = Polarimeter(source=simulate_signals_j,
                        sourceargs={'phase_difference': phase_difference})
        p.measure()
        print p.phase_difference
        print p.stdeviation
        self.assertIsInstance(p.last_measured, int)
        self.assertIsInstance(p.phase_difference, float)
        self.assertAlmostEqual(p.phase_difference, phase_difference, places=5)

if __name__ == '__main__':
    unittest.main()
