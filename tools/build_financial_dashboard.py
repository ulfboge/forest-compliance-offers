import csv
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "docs" / "05_supporting_materials" / "05-07_sample-financial-output.csv"
OUTPUT_FILE = REPO_ROOT / "outputs" / "financial_dashboard.md"


def read_records():
    records = []
    with DATA_FILE.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            numeric = {}
            for key in ["year", "revenue_usd", "opex_usd", "compliance_cost_usd", "capex_usd", "net_cashflow_usd"]:
                numeric[key] = float(row[key])
            row.update(numeric)
            records.append(row)
    return records


def aggregate(records):
    per_project = defaultdict(lambda: {"revenue": 0.0, "net": 0.0, "capex": 0.0, "compliance": 0.0})
    per_year = defaultdict(lambda: {"revenue": 0.0, "net": 0.0})

    scenarios = defaultdict(lambda: defaultdict(lambda: {"revenue": 0.0, "net": 0.0}))

    for rec in records:
        key = f"{rec['project_id']} | {rec['scenario']}"
        per_project[key]["revenue"] += rec["revenue_usd"]
        per_project[key]["net"] += rec["net_cashflow_usd"]
        per_project[key]["capex"] += rec["capex_usd"]
        per_project[key]["compliance"] += rec["compliance_cost_usd"]

        per_year[int(rec["year"])]["revenue"] += rec["revenue_usd"]
        per_year[int(rec["year"])]["net"] += rec["net_cashflow_usd"]

        scenarios[rec["project_id"]][rec["scenario"]]["revenue"] += rec["revenue_usd"]
        scenarios[rec["project_id"]][rec["scenario"]]["net"] += rec["net_cashflow_usd"]

    return per_project, per_year, scenarios


def format_currency(value):
    return f"${value:,.0f}"


def build_markdown(records, per_project, per_year, scenarios):
    years = sorted(per_year.keys())
    total_revenue = sum(r["revenue_usd"] for r in records)
    total_net = sum(r["net_cashflow_usd"] for r in records)
    total_capex = sum(r["capex_usd"] for r in records)
    total_compliance = sum(r["compliance_cost_usd"] for r in records)

    lines = []
    lines.append("# Financial Dashboard (Sample Data)")
    lines.append("")
    lines.append("This dashboard summarises the dummy financial outputs generated for tooling experiments.")
    lines.append("")
    lines.append("## Portfolio Snapshot")
    lines.append("")
    lines.append("| Metric | Amount |")
    lines.append("| --- | --- |")
    lines.append(f"| Total Revenue (2025-2027) | {format_currency(total_revenue)} |")
    lines.append(f"| Total Net Cashflow | {format_currency(total_net)} |")
    lines.append(f"| Total Capex | {format_currency(total_capex)} |")
    lines.append(f"| Total Compliance Spend | {format_currency(total_compliance)} |")
    lines.append("")

    lines.append("## Performance by Project & Scenario")
    lines.append("")
    lines.append("| Project & Scenario | Revenue | Net Cashflow | Capex | Compliance Cost |")
    lines.append("| --- | --- | --- | --- | --- |")
    for key, metrics in sorted(per_project.items()):
        lines.append(
            f"| {key} | {format_currency(metrics['revenue'])} | "
            f"{format_currency(metrics['net'])} | {format_currency(metrics['capex'])} | "
            f"{format_currency(metrics['compliance'])} |"
        )
    lines.append("")

    lines.append("## Yearly Portfolio Trend")
    lines.append("")
    lines.append("| Year | Revenue | Net Cashflow |")
    lines.append("| --- | --- | --- |")
    for year in years:
        metrics = per_year[year]
        lines.append(
            f"| {year} | {format_currency(metrics['revenue'])} | {format_currency(metrics['net'])} |"
        )
    lines.append("")

    lines.append("## Scenario Highlights")
    lines.append("")
    for project_id, project_scenarios in sorted(scenarios.items()):
        lines.append(f"### {project_id}")
        lines.append("")
        lines.append("| Scenario | Revenue | Net Cashflow | Signal |")
        lines.append("| --- | --- | --- | --- |")
        for scenario, metrics in sorted(project_scenarios.items()):
            signal = "Improved viability" if metrics["net"] > 0 else "Review assumptions"
            lines.append(
                f"| {scenario} | {format_currency(metrics['revenue'])} | "
                f"{format_currency(metrics['net'])} | {signal} |"
            )
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- The dataset covers three projects with base vs enhanced scenarios.")
    lines.append("- Compliance and capex lines are tracked explicitly to showcase where monitoring and certification investments land.")
    lines.append("- Replace this sample with live outputs when integrating with tools such as Base44 or Power BI.")
    lines.append("")

    return "\n".join(lines)


def main():
    records = read_records()
    per_project, per_year, scenarios = aggregate(records)
    markdown = build_markdown(records, per_project, per_year, scenarios)
    OUTPUT_FILE.write_text(markdown, encoding="utf-8")
    print(f"Wrote dashboard summary to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

