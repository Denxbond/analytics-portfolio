import unittest

import pandas as pd

from funnel_optimization_case.analysis.funnel_analysis import calculate_metrics


class FunnelAnalysisTests(unittest.TestCase):
    def test_conversion_uses_seven_day_window_and_excludes_pre_registration_deposit(self):
        frame = pd.DataFrame([
            (1, "2024-01-01", "2024-01-07", "Search", 100),
            (2, "2024-01-01", "2024-01-08", "Search", 100),
            (3, "2024-01-01", None, "Search", 0),
        ], columns=["user_id", "registration_date", "deposit_date", "marketing_channel", "gross_revenue"])
        result = calculate_metrics(frame).iloc[0]
        self.assertEqual(result["registrations"], 3)
        self.assertEqual(result["first_time_depositors_7d"], 1)
        self.assertAlmostEqual(result["reg_to_dep_conversion_rate"], 1 / 3)


if __name__ == "__main__":
    unittest.main()
