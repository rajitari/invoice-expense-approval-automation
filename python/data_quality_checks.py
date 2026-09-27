#!/usr/bin/env python3
"""Run non-destructive data-quality checks against the project Excel workbook."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "Expense Requests": {
        "Expense_ID",
        "Employee_ID",
        "Employee_Name",
        "Employee_Email",
        "Department",
        "Line_Manager_Email",
        "Expense_Date",
        "Expense_Category",
        "Amount_GBP",
        "Policy_Exception",
        "Potential_Duplicate",
        "Approval_Rule_ID",
        "Current_Status",
        "Submitted_At",
        "Payment_Date",
        "Last_Updated_At",
    },
    "Employee Directory": {
        "Employee_ID",
        "Employee_Name",
        "Employee_Email",
        "Department",
        "Line_Manager_Email",
        "Active_Flag",
    },
    "Approval Matrix": {
        "Approval_Rule_ID",
        "Minimum_Amount_GBP",
        "Maximum_Amount_GBP",
        "Line_Manager_Required",
        "Finance_Manager_Required",
        "Finance_Review_Required",
        "Policy_Exception_Rule",
        "Active_Flag",
    },
    "Audit Log": {
        "Audit_ID",
        "Expense_ID",
        "Action_Type",
        "Previous_Status",
        "New_Status",
        "Action_By",
        "Action_At",
        "Comments",
        "Automation_Run_ID",
    },
    "Error Log": {
        "Error_ID",
        "Expense_ID",
        "Workflow_Step",
        "Error_Type",
        "Error_Message",
        "Occurred_At",
        "Resolved_Flag",
        "Resolved_By",
        "Resolved_At",
        "Resolution_Notes",
    },
}

ALLOWED_STATUSES = {
    "Submitted",
    "Pending Manager",
    "Pending Manager Approval",
    "Pending Finance Manager",
    "Pending Finance Manager Approval",
    "Pending Finance Review",
    "Ready for Payment",
    "Returned for Information",
    "Rejected",
    "Paid",
    "Cancelled",
}


def as_text(series: pd.Series) -> pd.Series:
    """Return whitespace-trimmed text while treating missing values as empty."""
    return series.fillna("").astype(str).str.strip()


def as_bool(series: pd.Series) -> pd.Series:
    """Normalise Excel logical values and common text representations."""
    return as_text(series).str.upper().isin({"TRUE", "YES", "Y", "1"})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the Invoice & Expense Approval Automation workbook."
    )
    parser.add_argument("workbook", type=Path, help="Path to the .xlsx workbook")
    parser.add_argument(
        "--output",
        type=Path,
        help="CSV report path (default: data_quality_report.csv beside the workbook)",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Return exit code 1 when an ERROR check finds failed rows",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workbook = args.workbook.expanduser().resolve()
    output = (
        args.output.expanduser().resolve()
        if args.output
        else workbook.with_name("data_quality_report.csv")
    )

    if not workbook.exists():
        print(f"Workbook not found: {workbook}", file=sys.stderr)
        return 2

    results: list[dict[str, object]] = []

    def add(check: str, severity: str, failed_rows: int, details: str) -> None:
        results.append(
            {
                "check": check,
                "severity": severity,
                "failed_rows": int(failed_rows),
                "status": "PASS" if int(failed_rows) == 0 else "FAIL",
                "details": details,
            }
        )

    try:
        excel = pd.ExcelFile(workbook, engine="openpyxl")
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"Unable to open workbook: {exc}", file=sys.stderr)
        return 2

    missing_sheets = sorted(set(REQUIRED_COLUMNS) - set(excel.sheet_names))
    add(
        "Required worksheets exist",
        "ERROR",
        len(missing_sheets),
        "Missing: " + ", ".join(missing_sheets) if missing_sheets else "All required worksheets found",
    )

    frames: dict[str, pd.DataFrame] = {}
    structurally_valid = True
    for sheet, required in REQUIRED_COLUMNS.items():
        if sheet not in excel.sheet_names:
            structurally_valid = False
            continue
        frame = pd.read_excel(excel, sheet_name=sheet, dtype=object)
        frame.columns = [str(column).strip() for column in frame.columns]
        frames[sheet] = frame
        missing_columns = sorted(required - set(frame.columns))
        add(
            f"{sheet}: required columns",
            "ERROR",
            len(missing_columns),
            "Missing: " + ", ".join(missing_columns)
            if missing_columns
            else "All required columns found",
        )
        structurally_valid = structurally_valid and not missing_columns

    if not structurally_valid:
        report = pd.DataFrame(results)
        output.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(output, index=False)
        print(report.to_string(index=False))
        print(f"\nReport written to: {output}")
        return 1 if args.fail_on_error else 0

    requests = frames["Expense Requests"].copy()
    employees = frames["Employee Directory"].copy()
    audit = frames["Audit Log"].copy()
    errors = frames["Error Log"].copy()

    # Ignore entirely empty worksheet rows, while keeping partly populated rows for validation.
    def populated_rows(frame: pd.DataFrame) -> pd.DataFrame:
        has_value = frame.astype("string").fillna("").ne("").any(axis=1)
        return frame.loc[has_value].copy()

    requests = populated_rows(requests)
    employees = populated_rows(employees)
    audit = populated_rows(audit)
    errors = populated_rows(errors)

    expense_id = as_text(requests["Expense_ID"])
    employee_id = as_text(requests["Employee_ID"])
    status = as_text(requests["Current_Status"])
    amount = pd.to_numeric(requests["Amount_GBP"], errors="coerce")
    expense_date = pd.to_datetime(requests["Expense_Date"], errors="coerce")
    submitted_at = pd.to_datetime(requests["Submitted_At"], errors="coerce", utc=True)
    payment_date = pd.to_datetime(requests["Payment_Date"], errors="coerce")

    core_fields = {
        "Expense_ID": expense_id,
        "Employee_ID": employee_id,
        "Employee_Name": as_text(requests["Employee_Name"]),
        "Employee_Email": as_text(requests["Employee_Email"]),
        "Department": as_text(requests["Department"]),
        "Expense_Category": as_text(requests["Expense_Category"]),
        "Current_Status": status,
    }
    for field, values in core_fields.items():
        failed = int(values.eq("").sum())
        add(
            f"Expense Requests: {field} populated",
            "ERROR",
            failed,
            f"{failed} row(s) have a blank {field}",
        )

    duplicate_id_rows = int(expense_id.ne("").mul(expense_id.duplicated(keep=False)).sum())
    add(
        "Expense Requests: Expense_ID unique",
        "ERROR",
        duplicate_id_rows,
        f"{duplicate_id_rows} row(s) belong to duplicate Expense_ID values",
    )

    invalid_amount = amount.isna() | amount.le(0)
    add(
        "Expense Requests: Amount_GBP is numeric and positive",
        "ERROR",
        int(invalid_amount.sum()),
        f"{int(invalid_amount.sum())} row(s) have a blank, non-numeric or non-positive amount",
    )

    invalid_status = status.ne("") & ~status.isin(ALLOWED_STATUSES)
    add(
        "Expense Requests: Current_Status is allowed",
        "ERROR",
        int(invalid_status.sum()),
        "Unexpected values: " + ", ".join(sorted(status[invalid_status].unique()))
        if invalid_status.any()
        else "All status values are allowed",
    )

    invalid_date = expense_date.isna()
    add(
        "Expense Requests: Expense_Date is valid",
        "ERROR",
        int(invalid_date.sum()),
        f"{int(invalid_date.sum())} row(s) have a blank or invalid expense date",
    )

    today = pd.Timestamp.now(tz="Europe/London").normalize().tz_localize(None)
    future_date = expense_date.notna() & expense_date.dt.normalize().gt(today)
    add(
        "Expense Requests: Expense_Date is not in the future",
        "ERROR",
        int(future_date.sum()),
        f"{int(future_date.sum())} row(s) contain a future expense date",
    )

    invalid_submitted = submitted_at.isna()
    add(
        "Expense Requests: Submitted_At is valid",
        "ERROR",
        int(invalid_submitted.sum()),
        f"{int(invalid_submitted.sum())} row(s) have a blank or invalid submitted timestamp",
    )

    active_employees = employees.loc[as_bool(employees["Active_Flag"])].copy()
    active_ids = set(as_text(active_employees["Employee_ID"])) - {""}
    unknown_employee = employee_id.ne("") & ~employee_id.isin(active_ids)
    add(
        "Expense Requests: Employee_ID exists and is active",
        "ERROR",
        int(unknown_employee.sum()),
        "Unknown/inactive IDs: " + ", ".join(sorted(employee_id[unknown_employee].unique()))
        if unknown_employee.any()
        else "All request employees are active directory members",
    )

    directory_manager = (
        active_employees.assign(
            _employee_id=as_text(active_employees["Employee_ID"]),
            _manager_email=as_text(active_employees["Line_Manager_Email"]).str.lower(),
        )
        .drop_duplicates("_employee_id")
        .set_index("_employee_id")["_manager_email"]
    )
    expected_manager = employee_id.map(directory_manager).fillna("")
    actual_manager = as_text(requests["Line_Manager_Email"]).str.lower()
    manager_mismatch = expected_manager.ne("") & actual_manager.ne(expected_manager)
    add(
        "Expense Requests: manager matches Employee Directory",
        "ERROR",
        int(manager_mismatch.sum()),
        f"{int(manager_mismatch.sum())} row(s) have an unexpected line-manager email",
    )

    policy_exception = as_bool(requests["Policy_Exception"])
    expected_rule = pd.Series("RULE-001", index=requests.index, dtype="object")
    expected_rule.loc[amount.gt(500)] = "RULE-002"
    expected_rule.loc[policy_exception] = "RULE-003"
    actual_rule = as_text(requests["Approval_Rule_ID"])
    rule_mismatch = amount.notna() & actual_rule.ne(expected_rule)
    add(
        "Expense Requests: Approval_Rule_ID matches routing logic",
        "ERROR",
        int(rule_mismatch.sum()),
        f"{int(rule_mismatch.sum())} row(s) do not match RULE-001/002/003 routing logic",
    )

    duplicate_key = pd.DataFrame(
        {
            "employee": employee_id,
            "date": expense_date.dt.strftime("%Y-%m-%d"),
            "amount": amount.round(2),
        },
        index=requests.index,
    )
    valid_key = (
        duplicate_key["employee"].ne("")
        & duplicate_key["date"].notna()
        & duplicate_key["amount"].notna()
    )
    group_size = pd.Series(0, index=requests.index, dtype="int64")
    group_size.loc[valid_key] = (
        duplicate_key.loc[valid_key]
        .groupby(["employee", "date", "amount"])["employee"]
        .transform("size")
        .astype(int)
    )
    duplicate_candidate = group_size.gt(1)
    duplicate_flag = as_bool(requests["Potential_Duplicate"])
    false_positive = duplicate_flag & ~duplicate_candidate
    add(
        "Expense Requests: duplicate flags have a matching request",
        "WARNING",
        int(false_positive.sum()),
        f"{int(false_positive.sum())} flagged row(s) have no employee/date/amount match",
    )

    duplicate_groups = duplicate_key.loc[duplicate_candidate].copy()
    if duplicate_groups.empty:
        unflagged_duplicate_groups = 0
    else:
        duplicate_groups["flag"] = duplicate_flag.loc[duplicate_groups.index]
        group_flags = duplicate_groups.groupby(["employee", "date", "amount"])["flag"].any()
        unflagged_duplicate_groups = int((~group_flags).sum())
    add(
        "Expense Requests: duplicate groups include a flag",
        "WARNING",
        unflagged_duplicate_groups,
        f"{unflagged_duplicate_groups} duplicate group(s) contain no Potential_Duplicate flag",
    )

    paid = status.eq("Paid")
    paid_without_date = paid & payment_date.isna()
    add(
        "Expense Requests: Paid requests have Payment_Date",
        "ERROR",
        int(paid_without_date.sum()),
        f"{int(paid_without_date.sum())} paid request(s) have no payment date",
    )

    date_without_paid = ~paid & payment_date.notna()
    add(
        "Expense Requests: Payment_Date only appears on Paid requests",
        "WARNING",
        int(date_without_paid.sum()),
        f"{int(date_without_paid.sum())} non-paid request(s) contain a payment date",
    )

    audit_id = as_text(audit["Audit_ID"])
    audit_expense_id = as_text(audit["Expense_ID"])
    add(
        "Audit Log: Audit_ID populated",
        "ERROR",
        int(audit_id.eq("").sum()),
        f"{int(audit_id.eq('').sum())} audit row(s) have no Audit_ID",
    )
    duplicate_audit_rows = int(audit_id.ne("").mul(audit_id.duplicated(keep=False)).sum())
    add(
        "Audit Log: Audit_ID unique",
        "ERROR",
        duplicate_audit_rows,
        f"{duplicate_audit_rows} row(s) belong to duplicate Audit_ID values",
    )
    known_expense_ids = set(expense_id) - {""}
    orphan_audit = audit_expense_id.ne("") & ~audit_expense_id.isin(known_expense_ids)
    add(
        "Audit Log: Expense_ID links to a request",
        "ERROR",
        int(orphan_audit.sum()),
        f"{int(orphan_audit.sum())} audit row(s) reference an unknown Expense_ID",
    )

    action_at = pd.to_datetime(audit["Action_At"], errors="coerce", utc=True)
    add(
        "Audit Log: Action_At is valid",
        "ERROR",
        int(action_at.isna().sum()),
        f"{int(action_at.isna().sum())} audit row(s) have a blank or invalid timestamp",
    )

    error_id = as_text(errors["Error_ID"])
    add(
        "Error Log: Error_ID populated",
        "ERROR",
        int(error_id.eq("").sum()),
        f"{int(error_id.eq('').sum())} error row(s) have no Error_ID",
    )
    occurred_at = pd.to_datetime(errors["Occurred_At"], errors="coerce", utc=True)
    add(
        "Error Log: Occurred_At is valid",
        "ERROR",
        int(occurred_at.isna().sum()),
        f"{int(occurred_at.isna().sum())} error row(s) have a blank or invalid timestamp",
    )

    resolved = as_bool(errors["Resolved_Flag"])
    resolution_missing = resolved & (
        as_text(errors["Resolved_By"]).eq("")
        | as_text(errors["Resolved_At"]).eq("")
        | as_text(errors["Resolution_Notes"]).eq("")
    )
    add(
        "Error Log: resolved errors include resolution evidence",
        "ERROR",
        int(resolution_missing.sum()),
        f"{int(resolution_missing.sum())} resolved error(s) lack by/date/notes evidence",
    )

    report = pd.DataFrame(results)
    output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(output, index=False)

    print(report.to_string(index=False))
    print("\nSummary")
    print(report.groupby(["severity", "status"]).size().to_string())
    print(f"\nReport written to: {output}")

    has_errors = bool(((report["severity"] == "ERROR") & (report["failed_rows"] > 0)).any())
    return 1 if args.fail_on_error and has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
