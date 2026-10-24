import unittest

import pandas as pd

from retention_cohort_dashboard.analysis.cohort_retention_analysis import calculate_retention


class CohortRetentionTests(unittest.TestCase):
    def test_unobserved_weeks_are_missing_and_duplicate_events_do_not_inflate(self):
        events = pd.DataFrame([
            ("a", "2024-01-01", "2024-01-01"),
            ("a", "2024-01-01", "2024-01-01"),
            ("b", "2024-01-02", "2024-01-02"),
            ("a", "2024-01-01", "2024-01-08"),
        ], columns=["user_id", "registration_date", "event_date"])
        result = calculate_retention(events, "2024-01-14")
        self.assertEqual(result.loc[pd.Timestamp("2024-01-01"), 0], 1.0)
        self.assertEqual(result.loc[pd.Timestamp("2024-01-01"), 1], 0.5)
        self.assertTrue(pd.isna(result.loc[pd.Timestamp("2024-01-01"), 2]))

    def test_rejects_events_before_registration(self):
        events = pd.DataFrame([("a", "2024-01-02", "2024-01-01")],
                              columns=["user_id", "registration_date", "event_date"])
        with self.assertRaises(ValueError):
            calculate_retention(events)


if __name__ == "__main__":
    unittest.main()
