
"""Read-only local dashboard for synthetic validation evidence."""

import json
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "output" / "demo" / "validation_report.json"


def percent(value):
    return "N/A" if value is None else f"{value * 100:.1f}%"


def make_bar(label, sensitivity, outcome):
    """Render an accessible horizontal sensitivity bar."""
    if sensitivity is None:
        width = 0
        color = "#8b9bad"
    else:
        width = max(0, min(sensitivity * 100, 100))
        color = "#37d4b5" if outcome == "PASS" else "#ff9878"

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


def render():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    overall = report["overall"]
    status = report["status"]

    checks_by_name = {
        check["criterion"]: check
        for check in report["checks"]
    }

    threshold = report["thresholds"]["cohort_min_sensitivity"]
    maximum_drop = report["thresholds"]["maximum_sensitivity_drop"]

    subgroup_rows = []
    subgroup_bars = []

    for name, metrics in report["cohorts"].items():
        criterion = checks_by_name.get(
            f"cohort_{name}_sensitivity"
        )
        outcome = criterion["status"] if criterion else "NOT TESTED"
        sensitivity = metrics["sensitivity"]

        subgroup_rows.append(
            "<tr>"
            f"<td>{escape(str(name))}</td>"
            f"<td>{metrics['n']}</td>"
            f"<td>{percent(sensitivity)}</td>"
            f"<td>{escape(outcome)}</td>"
            "</tr>"
        )

        subgroup_bars.append(
            make_bar(f"Group {name}", sensitivity, outcome)
        )

    period_rows = []
    period_bars = []

    for name, metrics in report["periods"].items():
        sensitivity = metrics["sensitivity"]
        outcome = (
            "INSUFFICIENT DATA"
            if sensitivity is None
            else "OBSERVED"
        )

        period_bars.append(
            make_bar(name, sensitivity, outcome)
        )

        period_rows.append(
            "<tr>"
            f"<td>{escape(str(name))}</td>"
            f"<td>{metrics['n']}</td>"
            f"<td>{metrics['tp']}</td>"
            f"<td>{metrics['fn']}</td>"
            f"<td>{percent(sensitivity)}</td>"
            "</tr>"
        )

    drop_check = checks_by_name.get(
        "period_sensitivity_drop"
    )

    drop_status = (
        drop_check["status"]
        if drop_check else "NOT TESTED"
    )

    period_change = report.get("period_sensitivity_change")

    if period_change is None:
        change_text = "N/A"
    else:
        change_text = f"{period_change * 100:+.1f} percentage points"

    check_rows = []

    for check in report["checks"]:
        name = str(check["criterion"])
        observed = check["observed"]

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
            f"<td>{escape(str(check['status']))}</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MedAI Validation Lab</title>
<style>
body {{
  background:#081626;
  color:#e9f3f8;
  font:16px Arial,sans-serif;
  margin:0;
  padding:35px;
}}
main {{max-width:1100px; margin:auto}}
h1 {{color:#53ded7}}
h2 {{margin-top:34px}}
p {{color:#afc4d1}}
.cards {{display:flex; flex-wrap:wrap; gap:16px}}
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
.warning {{color:#ffad81}}
table {{
  width:100%;
  border-collapse:collapse;
  margin:20px 0 36px;
}}
th,td {{
  padding:13px;
  border-bottom:1px solid #355367;
  text-align:left;
}}
th {{color:#53ded7}}
.notice {{
  border-left:4px solid #53ded7;
  padding:12px;
  background:#14283b;
  margin:24px 0;
}}
.bar-row {{
  display:grid;
  grid-template-columns:100px 1fr 155px;
  gap:16px;
  align-items:center;
  margin:18px 0;
}}
.bar-label {{font-weight:bold}}
.bar-track {{
  height:26px;
  background:#24384b;
  border-radius:6px;
  overflow:hidden;
}}
.bar-fill {{
  height:100%;
  border-radius:6px;
}}
.bar-value {{
  font-weight:bold;
  font-size:14px;
}}
.threshold-note {{
  color:#afc4d1;
  font-size:14px;
}}
.finding {{
  background:#292a37;
  border-left:4px solid #ff9878;
  border-radius:5px;
  padding:18px;
  margin:20px 0;
}}
.finding strong {{color:#ffad81}}
@media(max-width:650px) {{
  .bar-row {{
    grid-template-columns:1fr;
    gap:6px;
  }}
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
<p class="threshold-note">
Illustrative minimum sensitivity:
{percent(threshold)} — not a clinical acceptance threshold.
</p>

{''.join(subgroup_bars)}

<h2>Subgroup Performance</h2>
<table>
<thead>
<tr><th>Group</th><th>Cases</th>
<th>Sensitivity</th><th>Criterion</th></tr>
</thead>
<tbody>{''.join(subgroup_rows)}</tbody>
</table>

<h2>Performance Monitoring Across Periods</h2>
<p class="threshold-note">
Period-specific sensitivity comparison.
A performance change is not proof of data drift.
</p>

{''.join(period_bars)}

<div class="finding">
<strong>Performance Change Assessment</strong>
<p>Observed sensitivity change: {change_text}</p>
<p>Maximum illustrative allowed drop:
{percent(maximum_drop)}</p>
<p>Criterion status: <strong>{escape(str(drop_status))}</strong></p>
</div>

<h2>Period Evidence</h2>
<table>
<thead>
<tr><th>Period</th><th>Cases</th>
<th>TP</th><th>FN</th><th>Sensitivity</th></tr>
</thead>
<tbody>{''.join(period_rows)}</tbody>
</table>

<h2>Illustrative Acceptance Checks</h2>
<table>
<thead>
<tr><th>Criterion</th><th>Observed</th>
<th>Status</th></tr>
</thead>
<tbody>{''.join(check_rows)}</tbody>
</table>

<p>Source: output/demo/validation_report.json</p>
</main>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return

        try:
            content = render().encode("utf-8")
        except (OSError, ValueError, KeyError, TypeError) as error:
            self.send_error(500, str(error))
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    print("Dashboard: http://127.0.0.1:8766")
    HTTPServer(("127.0.0.1", 8766), Handler).serve_forever()
