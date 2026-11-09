
import json
import tempfile
import unittest
from pathlib import Path

from medai.validation import load_cases, analyze, write_report
from medai.__main__ import DEFAULTS


class ReportEvidenceTests(unittest.TestCase):

    def test_failed_subgroup_is_reported(self):
        """Check that a failed subgroup appears in both reports."""

        rows = load_cases("data/synthetic_predictions.csv")
        report = analyze(rows, DEFAULTS)

        self.assertEqual(report["status"], "REVIEW_REQUIRED")

        subgroup_check = next(
            check for check in report["checks"]
            if check["criterion"] == "cohort_B_sensitivity"
        )

        self.assertEqual(subgroup_check["status"], "FAIL")

        with tempfile.TemporaryDirectory() as folder:
            write_report(report, folder)

            json_path = Path(folder) / "validation_report.json"
            md_path = Path(folder) / "validation_report.md"

            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())

            saved = json.loads(
                json_path.read_text(encoding="utf-8")
            )

            self.assertEqual(
                saved["status"], "REVIEW_REQUIRED"
            )

            saved_check = next(
                check for check in saved["checks"]
                if check["criterion"] == "cohort_B_sensitivity"
            )

            self.assertEqual(saved_check["status"], "FAIL")

            markdown = md_path.read_text(encoding="utf-8")

            self.assertIn("cohort_B_sensitivity", markdown)
            self.assertIn("FAIL", markdown)
            self.assertIn("REVIEW_REQUIRED", markdown)
            self.assertIn("Not clinical validation", markdown)


if __name__ == "__main__":
    unittest.main()
