import argparse
import json
from pathlib import Path
from .validation import load_cases, analyze, write_report

DEFAULTS = {"overall_min_sensitivity":0.85,"overall_min_specificity":0.8,
            "cohort_min_sensitivity":0.80,"cohort_min_positives":15,
            "maximum_sensitivity_drop":0.08}

def main():
    parser=argparse.ArgumentParser(description="Synthetic SaMD prediction validation demonstrator")
    parser.add_argument("--data",default="data/synthetic_predictions.csv")
    parser.add_argument("--criteria",default="data/illustrative_criteria.json")
    parser.add_argument("--output",default="output/demo")
    args=parser.parse_args()
    rows=load_cases(args.data)
    criteria=json.loads(Path(args.criteria).read_text(encoding="utf-8"))
    if (set(criteria) != set(DEFAULTS)
        or not isinstance(criteria["cohort_min_positives"], int)
        or isinstance(criteria["cohort_min_positives"], bool)
        or criteria["cohort_min_positives"] < 1
        or any(not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 1
               for k,v in criteria.items() if k != "cohort_min_positives")):
        raise ValueError("Invalid criteria: rates must be in [0,1] and minimum positives must be a positive integer")
    report=analyze(rows,criteria)
    write_report(report,args.output)
    print(f"Cases: {report['overall']['n']}; sensitivity: {report['overall']['sensitivity']}; specificity: {report['overall']['specificity']}")
    print("Cohort sensitivities:",", ".join(f"{k}={v['sensitivity']}" for k,v in report['cohorts'].items()))
    print(f"Status: {report['status']} (illustrative only)")
    print(f"Reports: {args.output}/validation_report.md and .json")

if __name__=="__main__":main()
