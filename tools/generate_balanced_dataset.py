
"""Generate a balanced synthetic medical AI evaluation dataset.

Each subgroup appears in both evaluation periods.
All records are fictional. No patient data is used.
"""

import csv
from pathlib import Path

OUTPUT = Path("data/synthetic_predictions_balanced.csv")

# Each cell contains 40 positive and 40 negative examples.
# TP and TN values are deliberately selected to demonstrate
# subgroup differences and period performance changes.
SCENARIOS = [
    {"cohort": "A", "period": "baseline", "tp": 38, "tn": 37},
    {"cohort": "A", "period": "current",  "tp": 36, "tn": 37},
    {"cohort": "B", "period": "baseline", "tp": 34, "tn": 37},
    {"cohort": "B", "period": "current",  "tp": 28, "tn": 37},
]


def generate():
    rows = []
    case_number = 1

    for scenario in SCENARIOS:
        cohort = scenario["cohort"]
        period = scenario["period"]

        # 40 positive reference cases
        for i in range(40):
            rows.append({
                "case_id": f"SYN-{case_number:04d}",
                "cohort": cohort,
                "period": period,
                "reference_label": 1,
                "model_prediction": int(i < scenario["tp"]),
            })
            case_number += 1

        # 40 negative reference cases
        for i in range(40):
            rows.append({
                "case_id": f"SYN-{case_number:04d}",
                "cohort": cohort,
                "period": period,
                "reference_label": 0,
                "model_prediction": 0 if i < scenario["tn"] else 1,
            })
            case_number += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_id",
                "cohort",
                "period",
                "reference_label",
                "model_prediction",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} synthetic cases")
    print(f"Output: {OUTPUT}")
    print("Subgroups: A, B")
    print("Periods: baseline, current")
    print("Cases per subgroup-period combination: 80")


if __name__ == "__main__":
    generate()
