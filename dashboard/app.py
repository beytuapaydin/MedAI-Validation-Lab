
"""Read-only local dashboard for synthetic medical AI evidence.

Educational engineering prototype only.
No clinical validation or deployment authorization.
"""

import json
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent.parent

REPORTS = {
    "original": ROOT / "output/demo/validation_report.json",
    "balanced": ROOT / "output/balanced/validation_report.json",
}


def percent(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def points(value):
    if value is None:
        return "N/A"
    return f"{value * 100:+.1f} percentage points"


def make_bar(label, sensitivity, outcome):
    if sensitivity is None:
        width = 0
        color = "#8498aa"
    else:
        width = max(0, min(100, sensitivity * 100))
        if outcome == "PASS":
            color = "#35d1b4"
        elif outcome == "FAIL":
            color = "#ff9278"
        else:
            color = "#609dcc"

    return (
        '<div class="bar-row">'
        f'<div class="bar-label">{escape(str(label))}</div>'
        '<div class="bar-track">'
        f'<div class="bar-fill" style="width:{width:.1f}%;'
        f'background:{color}"></div>'
        '</div>'
        f'<div class="bar-value">{percent(sensitivity)}'
        f' — {escape(str(outcome))}</div>'
        '</div>'
    )


def render(dataset="original"):
    if dataset not in REPORTS:
        raise ValueError("Unknown dataset")

    report = json.loads(
        REPORTS[dataset].read_text(encoding="utf-8")
    )

    overall = report["overall"]
    status = report["status"]

    checks = {
        item["criterion"]: item
        for item in report["checks"]
    }

    threshold = report["thresholds"][
        "cohort_min_sensitivity"
    ]

    maximum_drop = report["thresholds"][
        "maximum_sensitivity_drop"
    ]

    # Dataset selection
    original_selected = (
        ' selected' if dataset == "original" else ''
    )
    balanced_selected = (
        ' selected' if dataset == "balanced" else ''
    )

    # Subgroup analysis
    subgroup_bars = []
    subgroup_rows = []

    for name, metric in report["cohorts"].items():
        sensitivity = metric["sensitivity"]

        check = checks.get(
            f"cohort_{name}_sensitivity"
        )

        outcome = (
            check["status"]
            if check else "NOT TESTED"
        )

        subgroup_bars.append(
            make_bar(f"Group {name}", sensitivity, outcome)
        )

        subgroup_rows.append(
            "<tr>"
            f"<td>{escape(str(name))}</td>"
            f"<td>{metric['n']}</td>"
            f"<td>{percent(sensitivity)}</td>"
            f"<td class='{outcome.lower()}'>{escape(outcome)}</td>"
            "</tr>"
        )

    # Period analysis
    period_bars = []
    period_rows = []

    for name, metric in report["periods"].items():
        sensitivity = metric["sensitivity"]

        period_bars.append(
            make_bar(name, sensitivity, "OBSERVED")
        )

        period_rows.append(
            "<tr>"
            f"<td>{escape(str(name))}</td>"
            f"<td>{metric['n']}</td>"
            f"<td>{metric['tp']}</td>"
            f"<td>{metric['fn']}</td>"
            f"<td>{percent(sensitivity)}</td>"
            "</tr>"
        )

    drop_check = checks.get("period_sensitivity_drop")
    drop_status = (
        drop_check["status"]
        if drop_check else "NOT TESTED"
    )

    period_change = report.get(
        "period_sensitivity_change"
    )

    # Cohort x period analysis
    cohort_period_rows = []
    cohort_change_rows = []

    cohort_period = report.get("cohort_period", {})
    within_changes = report.get(
        "within_cohort_sensitivity_changes", {}
    )

    for cohort, periods in cohort_period.items():
        for period, metric in periods.items():
            cohort_period_rows.append(
                "<tr>"
                f"<td>{escape(str(cohort))}</td>"
                f"<td>{escape(str(period))}</td>"
                f"<td>{metric['n']}</td>"
                f"<td>{metric['tp']}</td>"
                f"<td>{metric['fn']}</td>"
                f"<td>{percent(metric['sensitivity'])}</td>"
                "</tr>"
            )

    for cohort, change in within_changes.items():
        cohort_change_rows.append(
            "<tr>"
            f"<td>Group {escape(str(cohort))}</td>"
            f"<td>{points(change)}</td>"
            "</tr>"
        )

    if not cohort_period_rows:
        cohort_period_content = (
            "<p>Stratified cohort-period evidence is "
            "not available in this saved report.</p>"
        )
    else:
        cohort_period_content = (
            "<table>"
            "<thead><tr>"
            "<th>Cohort</th><th>Period</th><th>Cases</th>"
            "<th>TP</th><th>FN</th><th>Sensitivity</th>"
            "</tr></thead><tbody>"
            + "".join(cohort_period_rows)
            + "</tbody></table>"
        )

    if cohort_change_rows:
        changes_content = (
            "<table>"
            "<thead><tr>"
            "<th>Subgroup</th><th>Sensitivity change</th>"
            "</tr></thead><tbody>"
            + "".join(cohort_change_rows)
            + "</tbody></table>"
        )
    else:
        changes_content = (
            "<p>No within-cohort change evidence available.</p>"
        )

    missing = report.get(
        "missing_cohort_period_combinations"
    )

    if missing is None:
        coverage_text = "Coverage not assessed in this report."
    elif not missing:
        coverage_text = (
            "All defined cohort-period combinations are represented."
        )
    else:
        coverage_text = (
            "Missing combinations: "
            + ", ".join(
                f"{escape(str(item['cohort']))} / "
                f"{escape(str(item['period']))}"
                for item in missing
            )
        )

    # Acceptance criteria
    check_rows = []

    for check in report["checks"]:
        name = str(check["criterion"])
        observed = check["observed"]
        outcome = str(check["status"])

        if (
            "sensitivity" in name
            or "specificity" in name
        ):
            observed_text = percent(observed)
        else:
            observed_text = escape(str(observed))

        check_rows.append(
            "<tr>"
            f"<td>{escape(name)}</td>"
            f"<td>{observed_text}</td>"
            f"<td class='{escape(outcome.lower())}'>"
            f"{escape(outcome)}</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MedAI Validation Lab</title>
<style>
* {{box-sizing:border-box}}
body {{
  background:#081626;
  color:#e9f3f8;
  font:16px Arial,sans-serif;
  margin:0;
  padding:32px;
}}
main {{max-width:1100px;margin:auto}}
h1 {{color:#53ded7;margin-bottom:8px}}
h2 {{margin-top:38px}}
p {{color:#afc4d1;line-height:1.55}}

.notice {{
  border-left:4px solid #53ded7;
  background:#14283b;
  padding:16px;
  margin:22px 0;
}}
.selector {{
  background:#14283b;
  padding:18px;
  border:1px solid #355367;
  border-radius:10px;
  margin:22px 0;
}}
.selector label {{
  color:#53ded7;
  display:block;
  margin-bottom:10px;
  font-weight:bold;
}}
select {{
  background:#081626;
  color:white;
  border:1px solid #53ded7;
  padding:12px;
  border-radius:6px;
  width:100%;
  max-width:420px;
}}
.cards {{
  display:flex;
  flex-wrap:wrap;
  gap:16px;
}}
.card {{
  background:#14283b;
  border:1px solid #355367;
  border-radius:12px;
  padding:22px;
  flex:1;
  min-width:210px;
}}
.number {{
  font-size:28px;
  font-weight:bold;
  margin-top:12px;
}}
.warning,.fail {{color:#ffad81}}
.pass {{color:#35d1b4}}

table {{
  width:100%;
  border-collapse:collapse;
  margin:20px 0 32px;
}}
th,td {{
  padding:13px;
  border-bottom:1px solid #355367;
  text-align:left;
}}
th {{color:#53ded7}}

.bar-row {{
  display:grid;
  grid-template-columns:100px 1fr 160px;
  gap:16px;
  align-items:center;
  margin:18px 0;
}}
.bar-label {{font-weight:bold}}
.bar-track {{
  background:#24384b;
  border-radius:6px;
  height:26px;
  overflow:hidden;
}}
.bar-fill {{height:100%;border-radius:6px}}
.bar-value {{font-weight:bold;font-size:14px}}

.finding {{
  background:#292a37;
  border-left:4px solid #ff9878;
  padding:18px;
  border-radius:6px;
  margin:22px 0;
}}
.finding strong {{color:#ffad81}}
.small {{font-size:14px}}

@media(max-width:650px) {{
  body {{padding:14px}}
  .bar-row {{
    grid-template-columns:1fr;
    gap:6px;
  }}
  table {{font-size:13px}}
  th,td {{padding:8px}}
}}
</style>
</head>
<body>
<main>

<h1>MedAI Validation Lab</h1>
<p>Medical AI Performance & Safety Evidence | Synthetic Demo</p>

<div class="notice">
Research prototype using synthetic predictions only.
Not clinical validation, regulatory conformity or deployment approval.
</div>

<div class="selector">
<label for="dataset">Evaluation Scenario</label>
<select id="dataset"
        onchange="window.location.href='/?dataset='+this.value">
<option value="original"{original_selected}>
Original Dataset — Confounded Example
</option>
<option value="balanced"{balanced_selected}>
Balanced Dataset — Cohort × Period
</option>
</select>
<p class="small">
Selected dataset: {escape(dataset)}.
The displayed results come from a saved JSON evidence report.
</p>
</div>

<div class="cards">
<div class="card">
Overall Sensitivity
<div class="number">{percent(overall['sensitivity'])}</div>
</div>
<div class="card">
Overall Specificity
<div class="number">{percent(overall['specificity'])}</div>
</div>
<div class="card">
Cases Evaluated
<div class="number">{overall['n']}</div>
</div>
<div class="card">
Evidence Review Status
<div class="number warning">{escape(str(status))}</div>
</div>
</div>

<h2>Subgroup Sensitivity Comparison</h2>
<p>
Illustrative minimum sensitivity: {percent(threshold)}.
Not a clinical acceptance threshold.
</p>

{''.join(subgroup_bars)}

<h2>Subgroup Performance</h2>
<table>
<thead><tr>
<th>Group</th><th>Cases</th>
<th>Sensitivity</th><th>Criterion</th>
</tr></thead>
<tbody>{''.join(subgroup_rows)}</tbody>
</table>

<h2>Performance Monitoring Across Periods</h2>
<p>
Period-specific sensitivity comparison.
A performance change is not proof of data drift.
</p>

{''.join(period_bars)}

<div class="finding">
<strong>Performance Change Assessment</strong>
<p>Observed sensitivity change:
{points(period_change)}</p>
<p>Maximum illustrative allowed drop:
{percent(maximum_drop)}</p>
<p>Criterion status:
<strong>{escape(str(drop_status))}</strong></p>
</div>

<h2>Period Evidence</h2>
<table>
<thead><tr>
<th>Period</th><th>Cases</th>
<th>TP</th><th>FN</th><th>Sensitivity</th>
</tr></thead>
<tbody>{''.join(period_rows)}</tbody>
</table>

<h2>Cohort × Period Analysis</h2>
<p>
Stratified sensitivity assessment for each observed
subgroup-period combination.
</p>

{cohort_period_content}

<h2>Within-Cohort Performance Changes</h2>
{changes_content}

<div class="notice">
<strong>Cohort-Period Coverage</strong>
<p>{coverage_text}</p>
<p>
Descriptive differences do not establish causal effects,
model bias, clinical harm or covariate drift.
</p>
</div>

<h2>Illustrative Acceptance Checks</h2>
<table>
<thead><tr>
<th>Criterion</th><th>Observed</th><th>Status</th>
</tr></thead>
<tbody>{''.join(check_rows)}</tbody>
</table>

<p class="small">
Source: {escape(str(REPORTS[dataset].relative_to(ROOT)))}
</p>
</main>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)

        if parsed.path != "/":
            self.send_error(404)
            return

        dataset = parse_qs(
            parsed.query
        ).get("dataset", ["original"])[0]

        if dataset not in REPORTS:
            self.send_error(400, "Unknown dataset")
            return

        try:
            content = render(dataset).encode("utf-8")
        except (OSError, ValueError, KeyError, TypeError) as error:
            self.send_error(500, str(error))
            return

        self.send_response(200)
        self.send_header(
            "Content-Type", "text/html; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    print("Dashboard: http://127.0.0.1:8766")
    HTTPServer(
        ("127.0.0.1", 8766), Handler
    ).serve_forever()
