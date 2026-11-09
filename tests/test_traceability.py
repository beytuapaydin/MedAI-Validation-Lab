
import unittest

from medai.validation import analyze
from medai.__main__ import DEFAULTS


def make_rows(cohort, period, positives, detected):
    """Create synthetic positive cases with known outcomes."""
    return [
        {
            "cohort": cohort,
            "period": period,
            "reference_label": 1,
            "model_prediction": int(i < detected),
        }
        for i in range(positives)
    ]


class TraceabilityTests(unittest.TestCase):

    def test_TEST_001_subgroup_sensitivity(self):
        """REQ-001 / RISK-001: detect subgroup failure."""
        rows = (
            make_rows("A", "baseline", 4, 4)
            + make_rows("B", "baseline", 4, 3)
        )

        criteria = {
            **DEFAULTS,
            "cohort_min_positives": 1,
        }

        result = analyze(rows, criteria)

        self.assertEqual(
            result["cohorts"]["B"]["sensitivity"], 0.75
        )

        check = next(
            c for c in result["checks"]
            if c["criterion"] == "cohort_B_sensitivity"
        )

        self.assertEqual(check["status"], "FAIL")
        self.assertEqual(
            result["status"], "REVIEW_REQUIRED"
        )

    def test_TEST_002_performance_degradation(self):
        """REQ-002 / RISK-002: detect sensitivity drop."""
        rows = (
            make_rows("A", "baseline", 10, 10)
            + make_rows("A", "followup", 10, 7)
        )

        criteria = {
            **DEFAULTS,
            "cohort_min_positives": 1,
        }

        result = analyze(rows, criteria)

        self.assertEqual(
            result["periods"]["baseline"]["sensitivity"],
            1.0
        )
        self.assertEqual(
            result["periods"]["followup"]["sensitivity"],
            0.7
        )

        self.assertEqual(
            result["period_sensitivity_change"], -0.3
        )

        check = next(
            c for c in result["checks"]
            if c["criterion"] == "period_sensitivity_drop"
        )

        self.assertEqual(check["status"], "FAIL")
        self.assertEqual(
            result["status"], "REVIEW_REQUIRED"
        )


if __name__ == "__main__":
    unittest.main()
