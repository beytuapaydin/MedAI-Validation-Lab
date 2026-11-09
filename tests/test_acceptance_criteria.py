
import unittest

from medai.validation import analyze
from medai.__main__ import DEFAULTS


def cases(cohort, period, tp, fn, tn=0):
    """Build synthetic cases with known classification outcomes."""
    rows = []

    for prediction, count, reference in [
        (1, tp, 1),
        (0, fn, 1),
        (0, tn, 0),
    ]:
        rows.extend(
            {
                "cohort": cohort,
                "period": period,
                "reference_label": reference,
                "model_prediction": prediction,
            }
            for _ in range(count)
        )

    return rows


def get_check(report, name):
    return next(
        check for check in report["checks"]
        if check["criterion"] == name
    )


class AcceptanceCriteriaTests(unittest.TestCase):

    def test_REQ_001_all_subgroups_checked(self):
        """Verify that every defined subgroup is assessed."""
        rows = (
            cases("A", "baseline", 10, 0, 5)
            + cases("B", "baseline", 7, 3, 5)
            + cases("C", "baseline", 9, 1, 5)
        )

        criteria = {
            **DEFAULTS,
            "cohort_min_positives": 1,
        }

        result = analyze(rows, criteria)

        self.assertEqual(
            set(result["cohorts"]), {"A", "B", "C"}
        )

        self.assertEqual(
            get_check(result, "cohort_A_sensitivity")["status"],
            "PASS"
        )
        self.assertEqual(
            get_check(result, "cohort_B_sensitivity")["status"],
            "FAIL"
        )
        self.assertEqual(
            get_check(result, "cohort_C_sensitivity")["status"],
            "PASS"
        )

    def test_REQ_001_threshold_boundary(self):
        """Exactly 80% sensitivity must meet the example rule."""
        rows = cases("A", "baseline", 4, 1, 5)

        result = analyze(
            rows,
            {**DEFAULTS, "cohort_min_positives": 1},
        )

        check = get_check(
            result, "cohort_A_sensitivity"
        )

        self.assertEqual(check["observed"], 0.8)
        self.assertEqual(check["status"], "PASS")

    def test_REQ_002_degradation_boundary(self):
        """A drop exactly at 8% must meet the example rule."""
        rows = (
            cases("A", "baseline", 25, 0, 5)
            + cases("A", "followup", 23, 2, 5)
        )

        result = analyze(
            rows,
            {**DEFAULTS, "cohort_min_positives": 1},
        )

        check = get_check(
            result, "period_sensitivity_drop"
        )

        self.assertEqual(check["observed"], 0.08)
        self.assertEqual(check["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
