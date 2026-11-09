
"""Medical AI validation on synthetic binary classification data.

Research and educational prototype only.
All thresholds are illustrative, not clinically validated.
Uses only the Python standard library.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

REQUIRED = (
    "case_id",
    "cohort",
    "period",
    "reference_label",
    "model_prediction",
)


def load_cases(path: str | Path) -> list[dict]:
    """Load and validate synthetic prediction records."""
    with open(path, encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)

        if not reader.fieldnames or any(
            field not in reader.fieldnames for field in REQUIRED
        ):
            raise ValueError(
                f"CSV requires columns: {', '.join(REQUIRED)}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("Input dataset is empty")

    ids = set()

    for number, row in enumerate(rows, 2):
        case_id = row["case_id"].strip()

        if not case_id or case_id in ids:
            raise ValueError(
                f"Missing or duplicate case_id on CSV row {number}"
            )

        ids.add(case_id)

        for key in ("cohort", "period"):
            if not row[key].strip():
                raise ValueError(
                    f"Missing {key} on CSV row {number}"
                )

        for key in ("reference_label", "model_prediction"):
            if row[key] not in ("0", "1"):
                raise ValueError(
                    f"{key} must be 0 or 1 on CSV row {number}"
                )

            row[key] = int(row[key])

    return rows


def wilson_interval(
    successes: int,
    total: int,
    z: float = 1.96,
):
    """Calculate an approximate 95% Wilson confidence interval."""
    if total == 0:
        return None

    p = successes / total
    d = 1 + z * z / total

    mid = (p + z * z / (2 * total)) / d

    half = (
        z
        * math.sqrt(
            p * (1 - p) / total
            + z * z / (4 * total * total)
        )
        / d
    )

    return [
        round(max(0.0, mid - half), 4),
        round(min(1.0, mid + half), 4),
    ]


def metrics(rows: list[dict]) -> dict:
    """Calculate binary classification performance metrics."""
    tp = sum(
        r["reference_label"] == 1
        and r["model_prediction"] == 1
        for r in rows
    )

    fn = sum(
        r["reference_label"] == 1
        and r["model_prediction"] == 0
        for r in rows
    )

    tn = sum(
        r["reference_label"] == 0
        and r["model_prediction"] == 0
        for r in rows
    )

    fp = sum(
        r["reference_label"] == 0
        and r["model_prediction"] == 1
        for r in rows
    )

    positive = tp + fn
    negative = tn + fp

    def ratio(a, b):
        return None if not b else round(a / b, 4)

    return {
        "n": len(rows),
        "tp": tp,
        "fn": fn,
        "tn": tn,
        "fp": fp,
        "sensitivity": ratio(tp, positive),
        "specificity": ratio(tn, negative),
        "false_negative_rate": ratio(fn, positive),
        "positive_predictive_value": ratio(tp, tp + fp),
        "sensitivity_ci_95_wilson": wilson_interval(
            tp, positive
        ),
        "specificity_ci_95_wilson": wilson_interval(
            tn, negative
        ),
    }


def cohort_period_analysis(rows: list[dict]) -> dict:
    """Calculate performance for each cohort-period combination.

    This is a descriptive stratified analysis.
    It does not establish causation or prove data drift.
    """
    grouped = defaultdict(list)

    for row in rows:
        key = (row["cohort"], row["period"])
        grouped[key].append(row)

    result = {}

    for (cohort, period), records in sorted(grouped.items()):
        result.setdefault(cohort, {})
        result[cohort][period] = metrics(records)

    return result


def analyze(rows: list[dict], thresholds: dict) -> dict:
    """Evaluate synthetic performance against illustrative criteria."""
    overall = metrics(rows)

    groups = defaultdict(list)
    windows = defaultdict(list)

    for row in rows:
        groups[row["cohort"]].append(row)
        windows[row["period"]].append(row)

    by_group = {
        key: metrics(value)
        for key, value in sorted(groups.items())
    }

    by_window = {
        key: metrics(value)
        for key, value in sorted(windows.items())
    }

    by_cohort_period = cohort_period_analysis(rows)

    checks = []

    def check(name, value, comparison, threshold):
        if value is None:
            status = "INSUFFICIENT_DATA"
        elif comparison == ">=":
            status = "PASS" if value >= threshold else "FAIL"
        else:
            status = "PASS" if value <= threshold else "FAIL"

        checks.append({
            "criterion": name,
            "observed": value,
            "operator": comparison,
            "threshold": threshold,
            "status": status,
        })

    check(
        "overall_sensitivity",
        overall["sensitivity"],
        ">=",
        thresholds["overall_min_sensitivity"],
    )

    check(
        "overall_specificity",
        overall["specificity"],
        ">=",
        thresholds["overall_min_specificity"],
    )

    for cohort, value in by_group.items():
        check(
            f"cohort_{cohort}_sensitivity",
            value["sensitivity"],
            ">=",
            thresholds["cohort_min_sensitivity"],
        )

        check(
            f"cohort_{cohort}_minimum_positives",
            value["tp"] + value["fn"],
            ">=",
            thresholds["cohort_min_positives"],
        )

    keys = sorted(by_window)

    if len(keys) >= 2:
        baseline = by_window[keys[0]]
        latest = by_window[keys[-1]]

        if (
            baseline["sensitivity"] is None
            or latest["sensitivity"] is None
        ):
            delta = None
        else:
            delta = round(
                latest["sensitivity"]
                - baseline["sensitivity"],
                4,
            )

        observed_drop = (
            None if delta is None
            else round(max(0, -delta), 4)
        )

        check(
            "period_sensitivity_drop",
            observed_drop,
            "<=",
            thresholds["maximum_sensitivity_drop"],
        )
    else:
        delta = None

    # Check whether every cohort is represented in every period.
    all_cohorts = sorted(by_group)
    all_periods = sorted(by_window)

    missing_combinations = [
        {
            "cohort": cohort,
            "period": period,
        }
        for cohort in all_cohorts
        for period in all_periods
        if period not in by_cohort_period.get(cohort, {})
    ]

    # Descriptive changes within each cohort.
    within_cohort_changes = {}

    for cohort, periods in by_cohort_period.items():
        if len(all_periods) < 2:
            within_cohort_changes[cohort] = None
            continue

        first = periods.get(all_periods[0])
        last = periods.get(all_periods[-1])

        if (
            first is None
            or last is None
            or first["sensitivity"] is None
            or last["sensitivity"] is None
        ):
            within_cohort_changes[cohort] = None
        else:
            within_cohort_changes[cohort] = round(
                last["sensitivity"] - first["sensitivity"],
                4,
            )

    if any(c["status"] == "FAIL" for c in checks):
        status = "REVIEW_REQUIRED"
    elif any(
        c["status"] == "INSUFFICIENT_DATA"
        for c in checks
    ):
        status = "EVIDENCE_INCOMPLETE"
    else:
        status = "CRITERIA_MET"

    return {
        "disclaimer": (
            "Synthetic portfolio demonstration; "
            "not clinical validation or regulatory conformity."
        ),
        "decision": (
            "Illustrative evidence review only; "
            "never a deployment authorization."
        ),
        "status": status,
        "thresholds": thresholds,
        "overall": overall,
        "cohorts": by_group,
        "periods": by_window,
        "cohort_period": by_cohort_period,
        "missing_cohort_period_combinations": missing_combinations,
        "within_cohort_sensitivity_changes": within_cohort_changes,
        "period_sensitivity_change": delta,
        "checks": checks,
    }


def write_report(
    report: dict,
    destination: str | Path,
) -> None:
    """Write JSON and Markdown evidence reports."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    json_path = destination / "validation_report.json"
    md_path = destination / "validation_report.md"

    json_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# MedAI Validation Evidence Report",
        "",
        f"**Status:** `{report['status']}`",
        "",
        "> Synthetic demonstration only. Not clinical validation, "
        "release approval, or regulatory conformity.",
        "",
        "## Overall confusion matrix and metrics",
        "",
        "```json",
        json.dumps(report["overall"], indent=2),
        "```",
        "",
        "## Subgroup metrics",
        "",
        "| Cohort | N | TP | FN | Sensitivity | 95% Wilson CI |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for cohort, value in report["cohorts"].items():
        lines.append(
            f"| {cohort} | {value['n']} | "
            f"{value['tp']} | {value['fn']} | "
            f"{value['sensitivity']} | "
            f"{value['sensitivity_ci_95_wilson']} |"
        )

    lines.extend([
        "",
        "## Cohort x Period Analysis",
        "",
        "| Cohort | Period | N | TP | FN | Sensitivity |",
        "|---|---|---:|---:|---:|---:|",
    ])

    for cohort, periods in report["cohort_period"].items():
        for period, value in periods.items():
            lines.append(
                f"| {cohort} | {period} | {value['n']} | "
                f"{value['tp']} | {value['fn']} | "
                f"{value['sensitivity']} |"
            )

    lines.extend([
        "",
        "## Within-Cohort Sensitivity Changes",
        "",
        "| Cohort | Sensitivity change |",
        "|---|---:|",
    ])

    for cohort, delta in report[
        "within_cohort_sensitivity_changes"
    ].items():
        lines.append(
            f"| {cohort} | "
            f"{'N/A' if delta is None else f'{delta * 100:+.2f} percentage points'} |"
        )

    lines.extend([
        "",
        "## Cohort-Period Coverage",
        "",
    ])

    missing = report["missing_cohort_period_combinations"]

    if not missing:
        lines.append(
            "Every defined cohort is represented in every "
            "defined evaluation period."
        )
    else:
        lines.append(
            "**Missing combinations detected:**"
        )
        for item in missing:
            lines.append(
                f"- Cohort {item['cohort']}, "
                f"period {item['period']}"
            )

    lines.extend([
        "",
        "## Predefined illustrative criteria",
        "",
        "| Criterion | Observed | Rule | Result |",
        "|---|---:|---|---|",
    ])

    for check in report["checks"]:
        lines.append(
            f"| {check['criterion']} | {check['observed']} | "
            f"{check['operator']} {check['threshold']} | "
            f"**{check['status']}** |"
        )

    lines.extend([
        "",
        "## Interpretation and limits",
        "",
        "- A failure triggers human investigation; it does "
        "not diagnose a patient or authorize deployment.",
        "- A change in sensitivity is not proof of "
        "feature or covariate drift.",
        "- Complete cohort-period coverage does not "
        "establish causal independence.",
        "- Small subgroup denominators can produce "
        "wide confidence intervals.",
        "- Acceptance thresholds are illustrative.",
        "- No clinical data, clinical validation, or "
        "formal standards compliance is claimed.",
        "",
    ])

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
