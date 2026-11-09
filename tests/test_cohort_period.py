
"""Tests for cohort-by-period validation analysis."""

import unittest

from medai.validation import (
    analyze,
    load_cases,
    cohort_period_analysis,
)
from medai.__main__ import DEFAULTS


class CohortPeriodTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rows = load_cases(
            "data/synthetic_predictions.csv"
        ) if False else None

        from tools.generate_balanced_dataset import SCENARIOS

        cls.rows = []

        for scenario in SCENARIOS:
            cohort = scenario["cohort"]
            period = scenario["period"]

            for i in range(40):
                cls.rows.append({
                    "cohort": cohort,
                    "period": period,
                    "reference_label": 1,
                    "model_prediction": int(
                        i < scenario["tp"]
                    ),
                })

            for i in range(40):
                cls.rows.append({
                    "cohort": cohort,
                    "period": period,
                    "reference_label": 0,
                    "model_prediction": int(
                        i >= scenario["tn"]
                    ),
                })

    def test_all_four_combinations_exist(self):
        result = cohort_period_analysis(self.rows)

        self.assertEqual(
            set(result.keys()), {"A", "B"}
        )

        for cohort in ("A", "B"):
            self.assertEqual(
                set(result[cohort].keys()),
                {"baseline", "current"},
            )

    def test_expected_cell_sensitivities(self):
        result = cohort_period_analysis(self.rows)

        expected = {
            ("A", "baseline"): 0.95,
            ("A", "current"): 0.90,
            ("B", "baseline"): 0.85,
            ("B", "current"): 0.70,
        }

        for (cohort, period), value in expected.items():
            self.assertEqual(
                result[cohort][period]["sensitivity"],
                value,
            )

    def test_within_cohort_changes(self):
        result = analyze(self.rows, DEFAULTS)

        self.assertEqual(
            result["within_cohort_sensitivity_changes"]["A"],
            -0.05,
        )

        self.assertEqual(
            result["within_cohort_sensitivity_changes"]["B"],
            -0.15,
        )

    def test_complete_cohort_period_coverage(self):
        result = analyze(self.rows, DEFAULTS)

        self.assertEqual(
            result["missing_cohort_period_combinations"],
            [],
        )


if __name__ == "__main__":
    unittest.main()
