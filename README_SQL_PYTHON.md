# SQL and Python Portfolio Files

These files demonstrate the SQL and Python components of a portfolio prototype for an expense approval process. Use synthetic or sanitised data only.

## Folder contents

- `sql/01_schema.sql` — relational database design for the five workbook tables.
- `sql/02_analytics_queries.sql` — management KPIs, operational monitoring, duplicate analysis and audit-trail queries.
- `sql/03_data_quality_queries.sql` — exception queries that should normally return zero rows.
- `python/data_quality_checks.py` — read-only validation of the sanitised Excel workbook.
- `python/requirements.txt` — Python dependencies.

## Run the Python checks

Use only a sanitised copy of the workbook with personal, organisational and confidential data removed. Do not use or publish the live operational workbook.

From Terminal, change into the `python` folder and create an isolated environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```
Run the checks against the sanitised workbook:

```bash
python3 data_quality_checks.py "/path/to/sanitised_workbook.xlsx" \
  --output "/path/to/data_quality_report.csv"
```

The script does not modify the workbook. It writes the CSV report to the path specified with `--output`. Add `--fail-on-error` if the command should return a non-zero exit code when a critical check fails.
## Use the SQL files

The SQL uses SQLite syntax so it can be demonstrated with DB Browser for SQLite or the `sqlite3` command-line tool. Run `01_schema.sql` first, import sanitised workbook data into the matching tables, and then execute queries from `02_analytics_queries.sql` and `03_data_quality_queries.sql`.

The Excel workbook remains the operational data store for the automated prototype. The SQL model demonstrates how the solution could be migrated to a governed relational database at production scale.
