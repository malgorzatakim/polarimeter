import simulator
import unittest
import numpy as np


class Test(unittest.TestCase):
    def test_simulate_signals(self, repeat=1):
        t, sigA, sigB = simulator.simulate_signals()
        self.assertIs(type(sigA), np.ndarray)
        self.assertIs(type(sigB), np.ndarray)
        self.assertIs(type(t), np.ndarray)
        self.assertEqual(len(sigA), len(t))
        self.assertEqual(len(sigB), len(t))

if __name__ == '__main__':
    unittest.main()
