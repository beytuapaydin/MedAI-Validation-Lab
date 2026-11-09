
import unittest
from dashboard.app import render


class DashboardTests(unittest.TestCase):

    def test_dashboard_displays_validation_evidence(self):
        html = render()

        self.assertIn("MedAI Validation Lab", html)
        self.assertIn("85.6%", html)
        self.assertIn("92.5%", html)
        self.assertIn("REVIEW_REQUIRED", html)
        self.assertIn("cohort_B_sensitivity", html)
        self.assertIn("FAIL", html)
        self.assertIn("Synthetic Demo", html)

    def test_dashboard_contains_safety_disclaimer(self):
        html = render()

        self.assertIn("Not clinical validation", html)
        self.assertIn("regulatory conformity", html)
        self.assertIn("deployment approval", html)


if __name__ == "__main__":
    unittest.main()
