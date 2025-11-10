# Financial Dashboard Helper Notes

Use these instructions whenever you want to revisit or regenerate the sample financial dashboard derived from `05-07_sample-financial-output.csv`.

---

## Key Files

| File | Role | Notes |
| :--- | :--- | :--- |
| `docs/05_supporting_materials/05-07_sample-financial-output.csv` | Sample dataset | Edit or replace with live scenario data (keep headers intact). |
| `tools/build_financial_dashboard.py` | Generator script | Reads the CSV, aggregates metrics, and writes a Markdown dashboard. |
| `outputs/financial_dashboard.md` | Generated summary | Safe to delete and regenerate on demand. |

---

## Regenerate the Dashboard

```bash
python tools/build_financial_dashboard.py
```

* The command prints the full path of the updated Markdown file.
* No environment variables or extra dependencies are required (Python 3.9+ recommended).

---

## Customise or Extend

1. **Update data**: add rows or new scenarios to the CSV; keep column names consistent.
2. **Modify calculations**: edit the `aggregate` or `build_markdown` functions in the script (e.g., add EBITDA, ROI, or project grouping).
3. **Change format**: currently Markdown; convert to CSV/JSON/HTML by swapping the writer section.
4. **Integrate elsewhere**: the Markdown output can be copied into Notion, Base44, Power BI, or other tooling as a quick snapshot.

---

## Parking the Dashboard

- If the dashboard is not needed, simply ignore `outputs/financial_dashboard.md` or delete it—the script can recreate it later.
- `.gitignore` already excludes `.env`, Notion sync artefacts, and local transcripts; no further cleanup is required.
- Keep the sample CSV and script as a ready-made template for future projects.

---

## Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| Command reports missing CSV | Ensure `05-07_sample-financial-output.csv` exists and paths are unchanged. |
| Unicode/encoding issues | Save the CSV in UTF-8 and run the script in a UTF-8-friendly environment. |
| Need richer visuals | Feed the output or source CSV into Base44, Power BI, or another BI tool for charts. |

---

**Tip:** When you are ready to generate real dashboards, duplicate the script and CSV into a project-specific folder so samples remain untouched. !*** End Patch

