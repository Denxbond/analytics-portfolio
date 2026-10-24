import unittest

import pandas as pd

from revenue_forecast_model.analysis.revenue_forecast import rolling_origin_backtest


class RevenueForecastTests(unittest.TestCase):
    def test_rolling_origin_evaluates_only_future_values(self):
        values = pd.Series(range(100, 124), index=pd.date_range("2022-01-01", periods=24, freq="MS"))
        detail, summary = rolling_origin_backtest(values, horizon=3)
        self.assertEqual(len(detail), 24)  # 4 origins x 3 months x 2 methods
        self.assertEqual(set(summary["method"]), {"holt_damped_trend", "seasonal_naive_12m"})
        self.assertTrue((detail["month"] > detail["origin"]).all())


if __name__ == "__main__":
    unittest.main()
