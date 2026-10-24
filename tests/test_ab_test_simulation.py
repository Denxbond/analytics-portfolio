import unittest

import numpy as np

from ab_test_simulator.analysis.ab_test_simulation import planned_power, summarize_results


class ABTestSimulationTests(unittest.TestCase):
    def test_power_is_design_based_and_increases_with_sample_size(self):
        low = planned_power(500, 0.10, 0.12)
        high = planned_power(2000, 0.10, 0.12)
        self.assertLess(low, high)
        result = summarize_results(np.array([0, 0, 0, 1]), np.array([1, 1, 1, 1]), 0.10, 0.12)
        self.assertAlmostEqual(result["planned_power"], planned_power(4, 0.10, 0.12))
        self.assertNotAlmostEqual(result["planned_power"], planned_power(4, 0.25, 0.99))

    def test_binary_result_reports_rate_difference_and_interval(self):
        result = summarize_results(np.array([0, 0, 1, 0]), np.array([0, 1, 1, 1]), 0.10, 0.12)
        self.assertAlmostEqual(result["absolute_lift"], 0.5)
        self.assertLess(result["ci_low"], result["absolute_lift"])
        self.assertGreater(result["ci_high"], result["absolute_lift"])


if __name__ == "__main__":
    unittest.main()
