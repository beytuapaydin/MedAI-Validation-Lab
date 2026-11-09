
"""Read-only local dashboard for synthetic validation evidence."""

import json
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "output" / "demo" / "validation_report.json"


def percent(value):
    return "N/A" if value is None else f"{value * 100:.1f}%"


def render():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    overall = report["overall"]
    status = report["status"]

    subgroup_rows = []
    for name, metrics in report["cohorts"].items():
        criterion = next(
            (
                c for c in report["checks"]
                if c["criterion"] == f"cohort_{name}_sensitivity"
            ),
            None,
        )
        outcome = criterion["status"] if criterion else "NOT TESTED"
        subgroup_rows.append(
            "<tr>"
            f"<td>{escape(str(name))}</td>"
            f"<td>{metrics['n']}</td>"
            f"<td>{percent(metrics['sensitivity'])}</td>"
            f"<td>{escape(outcome)}</td>"
            "</tr>"
        )

    check_rows = []
    for check in report["checks"]:
        check_rows.append(
            "<tr>"
            f"<td>{escape(check['criterion'])}</td>"
            f"<td>{percent(check['observed']) if 'sensitivity' in check['criterion'] or 'specificity' in check['criterion'] else escape(str(check['observed']))}</td>"
            f"<td>{escape(check['status'])}</td>"
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
  background:#081626; color:#e9f3f8;
  font:16px Arial,sans-serif; margin:0; padding:35px;
}}
main {{max-width:1100px; margin:auto}}
h1 {{color:#53ded7}}
p {{color:#afc4d1}}
.cards {{display:flex; flex-wrap:wrap; gap:16px}}
.card {{
  background:#14283b; border:1px solid #355367;
  border-radius:12px; padding:22px; flex:1; min-width:210px;
}}
.number {{font-size:28px; font-weight:bold; margin-top:12px}}
.warning {{color:#ffad81}}
table {{width:100%; border-collapse:collapse; margin:20px 0 36px}}
th,td {{padding:13px; border-bottom:1px solid #355367;
        text-align:left}}
th {{color:#53ded7}}
.notice {{border-left:4px solid #53ded7; padding:12px;
         background:#14283b; margin:24px 0}}
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
<div class="card">Overall Sensitivity
<div class="number">{percent(overall['sensitivity'])}</div></div>
<div class="card">Overall Specificity
<div class="number">{percent(overall['specificity'])}</div></div>
<div class="card">Cases Evaluated
<div class="number">{overall['n']}</div></div>
<div class="card">Evidence Review Status
<div class="number warning">{escape(status)}</div></div>
</div>

<h2>Subgroup Performance</h2>
<table>
<thead><tr><th>Group</th><th>Cases</th>
<th>Sensitivity</th><th>Criterion</th></tr></thead>
<tbody>{''.join(subgroup_rows)}</tbody>
</table>

<h2>Illustrative Acceptance Checks</h2>
<table>
<thead><tr><th>Criterion</th><th>Observed</th>
<th>Status</th></tr></thead>
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
