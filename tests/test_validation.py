import tempfile
import unittest
from pathlib import Path
from medai.validation import metrics, wilson_interval, load_cases, analyze, write_report
from medai.__main__ import DEFAULTS

class ValidationTests(unittest.TestCase):
    def test_confusion_matrix(self):
        rows=[{'reference_label':1,'model_prediction':1},{'reference_label':1,'model_prediction':0},
              {'reference_label':0,'model_prediction':0},{'reference_label':0,'model_prediction':1}]
        m=metrics(rows)
        self.assertEqual((m['tp'],m['fn'],m['tn'],m['fp']),(1,1,1,1))
        self.assertEqual(m['sensitivity'],.5)
        self.assertEqual(m['specificity'],.5)
    def test_zero_denominator_is_unknown(self):
        self.assertIsNone(metrics([{'reference_label':0,'model_prediction':0}])['sensitivity'])
    def test_wilson_bounds(self):
        lo,hi=wilson_interval(8,10)
        self.assertGreaterEqual(lo,0)
        self.assertLessEqual(hi,1)
        self.assertLess(lo,hi)
    def test_sample_detects_hidden_failure(self):
        rows=load_cases('data/synthetic_predictions.csv')
        r=analyze(rows,DEFAULTS)
        self.assertGreaterEqual(r['overall']['sensitivity'],DEFAULTS['overall_min_sensitivity'])
        self.assertLess(r['cohorts']['B']['sensitivity'],DEFAULTS['cohort_min_sensitivity'])
        self.assertEqual(r['status'],'REVIEW_REQUIRED')
        self.assertTrue(any(x['status']=='FAIL' for x in r['checks']))
    def test_report_files(self):
        r=analyze(load_cases('data/synthetic_predictions.csv'),DEFAULTS)
        with tempfile.TemporaryDirectory() as d:
            write_report(r,d)
            self.assertIn('Subgroup metrics',(Path(d)/'validation_report.md').read_text())
            self.assertTrue((Path(d)/'validation_report.json').exists())
    def test_reject_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.csv'
            p.write_text('case_id,cohort,period,reference_label,model_prediction\nX,A,baseline,1,1\nX,A,baseline,0,0\n')
            with self.assertRaisesRegex(ValueError,'duplicate'):
                load_cases(p)
    def test_insufficient_data_is_not_a_pass(self):
        r=analyze([{'cohort':'A','period':'baseline','reference_label':0,'model_prediction':0}],DEFAULTS)
        self.assertEqual(r['status'],'REVIEW_REQUIRED')
        self.assertTrue(any(x['status']=='INSUFFICIENT_DATA' for x in r['checks']))

if __name__=='__main__':unittest.main()
