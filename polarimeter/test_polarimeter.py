from __future__ import division
import unittest
from polarimeter import Polarimeter
from simulator import simulate_signals


class Test(unittest.TestCase):
    """Tests for polarimeter.py"""

    def test_measure(self):
        """Test p.measure()"""
        phase_difference = 25
        p = Polarimeter(source=simulate_signals,
                        sourceargs={'phase_difference': phase_difference})
        p.measure()
        self.assertIsInstance(p.last_measured, int)
        self.assertIsInstance(p.phase_difference, float)
        self.assertAlmostEqual(p.phase_difference, phase_difference, places=2)

if __name__ == '__main__':
    unittest.main()
