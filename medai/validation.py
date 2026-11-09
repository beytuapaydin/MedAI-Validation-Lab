"""Transparent binary-classification validation on synthetic labels.

All thresholds are illustrative portfolio acceptance criteria, NOT regulatory or
clinical requirements. Uses only Python standard library.
"""
from __future__ import annotations
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

REQUIRED = ("case_id", "cohort", "period", "reference_label", "model_prediction")


def load_cases(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or any(field not in reader.fieldnames for field in REQUIRED):
            raise ValueError(f"CSV requires columns: {', '.join(REQUIRED)}")
        rows = list(reader)
    if not rows:
        raise ValueError("Input dataset is empty")
    ids = set()
    for number, row in enumerate(rows, 2):
        case_id = row["case_id"].strip()
        if not case_id or case_id in ids:
            raise ValueError(f"Missing or duplicate case_id on CSV row {number}")
        ids.add(case_id)
        for key in ("cohort", "period"):
            if not row[key].strip():
                raise ValueError(f"Missing {key} on CSV row {number}")
        for key in ("reference_label", "model_prediction"):
            if row[key] not in ("0", "1"):
                raise ValueError(f"{key} must be 0 or 1 on CSV row {number}")
        row["reference_label"] = int(row["reference_label"])
        row["model_prediction"] = int(row["model_prediction"])
    return rows


def wilson_interval(successes: int, total: int, z: float = 1.96):
    if total == 0:
        return None
    p = successes / total
    d = 1 + z * z / total
    mid = (p + z*z/(2*total))/d
    half = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total))/d
    return [round(max(0., mid-half), 4), round(min(1., mid+half), 4)]


def metrics(rows: list[dict]) -> dict:
    tp = sum(r["reference_label"] == 1 and r["model_prediction"] == 1 for r in rows)
    fn = sum(r["reference_label"] == 1 and r["model_prediction"] == 0 for r in rows)
    tn = sum(r["reference_label"] == 0 and r["model_prediction"] == 0 for r in rows)
    fp = sum(r["reference_label"] == 0 and r["model_prediction"] == 1 for r in rows)
    positive = tp + fn
    negative = tn + fp
    def ratio(a, b): return None if not b else round(a/b, 4)
    return {"n":len(rows), "tp":tp, "fn":fn, "tn":tn, "fp":fp,
            "sensitivity":ratio(tp, positive), "specificity":ratio(tn, negative),
            "false_negative_rate":ratio(fn, positive),
            "positive_predictive_value":ratio(tp, tp+fp),
            "sensitivity_ci_95_wilson":wilson_interval(tp, positive),
            "specificity_ci_95_wilson":wilson_interval(tn, negative)}


def analyze(rows: list[dict], thresholds: dict) -> dict:
    # Gate is based on explicit example criteria, not clinical clearance.
    overall = metrics(rows)
    groups = defaultdict(list)
    windows = defaultdict(list)
    for row in rows:
        groups[row["cohort"]].append(row)
        windows[row["period"]].append(row)
    by_group = {key:metrics(value) for key,value in sorted(groups.items())}
    by_window = {key:metrics(value) for key,value in sorted(windows.items())}
    checks = []
    def check(name, value, comparison, threshold):
        status = "INSUFFICIENT_DATA" if value is None else (
            "PASS" if (value >= threshold if comparison == ">=" else value <= threshold) else "FAIL")
        checks.append({"criterion":name, "observed":value, "operator":comparison,
                       "threshold":threshold, "status":status})
    check("overall_sensitivity",overall["sensitivity"],">=",thresholds["overall_min_sensitivity"])
    check("overall_specificity",overall["specificity"],">=",thresholds["overall_min_specificity"])
    for cohort, value in by_group.items():
        check(f"cohort_{cohort}_sensitivity",value["sensitivity"],">=",thresholds["cohort_min_sensitivity"])
        check(f"cohort_{cohort}_minimum_positives",value["tp"]+value["fn"],">=",thresholds["cohort_min_positives"])
    # Note that period sensitivity difference is PERFORMANCE CHANGE, not proof of data drift.
    keys = sorted(by_window)
    if len(keys) >= 2:
        baseline, latest = by_window[keys[0]], by_window[keys[-1]]
        delta = None if baseline["sensitivity"] is None or latest["sensitivity"] is None else round(latest["sensitivity"]-baseline["sensitivity"],4)
        check("period_sensitivity_drop",None if delta is None else round(max(0,-delta),4),"<=",thresholds["maximum_sensitivity_drop"])
    else:
        delta = None
    status = "REVIEW_REQUIRED" if any(c["status"]=="FAIL" for c in checks) else (
        "EVIDENCE_INCOMPLETE" if any(c["status"]=="INSUFFICIENT_DATA" for c in checks) else "CRITERIA_MET")
    return {"disclaimer":"Synthetic portfolio demonstration; not clinical validation or regulatory conformity.",
            "decision":"Illustrative evidence review only; never a deployment authorization.",
            "status":status, "thresholds":thresholds, "overall":overall,
            "cohorts":by_group, "periods":by_window,
            "period_sensitivity_change":delta, "checks":checks}


def write_report(report: dict, destination: str | Path) -> None:
    destination = Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    (destination/"validation_report.json").write_text(json.dumps(report, indent=2)+"\n",encoding="utf-8")
    lines = ["# MedAI Validation Evidence Report", "",f"**Status:** `{report['status']}`", "",
             "> Synthetic demonstration only. Not clinical validation, release approval, or regulatory conformity.","",
             "## Overall confusion matrix and metrics", "", "```json", json.dumps(report['overall'],indent=2), "```", "",
             "## Subgroup metrics", "", "| Cohort | N | TP | FN | Sensitivity | 95% Wilson CI |", "|---|---:|---:|---:|---:|---|"]
    for k,v in report["cohorts"].items():
        lines.append(f"| {k} | {v['n']} | {v['tp']} | {v['fn']} | {v['sensitivity']} | {v['sensitivity_ci_95_wilson']} |")
    lines.extend(["", "## Predefined illustrative criteria", "", "| Criterion | Observed | Rule | Result |", "|---|---:|---|---|"])
    for c in report["checks"]:
        lines.append(f"| {c['criterion']} | {c['observed']} | {c['operator']} {c['threshold']} | **{c['status']}** |")
    lines.extend(["", "## Interpretation and limits", "",
                  "- A failure triggers human investigation; it does not diagnose a patient or automatically authorize/block deployment.",
                  "- A change in sensitivity over time is **performance degradation**, not proof of feature/covariate drift.",
                  "- Small subgroup denominators create wide confidence intervals; illustrative cutoffs are not clinical requirements.",
                  "- No clinical data, patient identifiers, clinical validation, or formal standards compliance is claimed.", ""])
    (destination/"validation_report.md").write_text("\n".join(lines),encoding="utf-8")
