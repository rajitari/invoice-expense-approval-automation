-- Invoice & Expense Approval Automation
-- Logical relational model implemented in SQLite for portfolio demonstration.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS employee_directory (
    employee_id          TEXT PRIMARY KEY,
    employee_name        TEXT NOT NULL,
    employee_email       TEXT NOT NULL UNIQUE,
    department           TEXT NOT NULL,
    line_manager_id      TEXT,
    line_manager_email   TEXT NOT NULL,
    active_flag          INTEGER NOT NULL DEFAULT 1 CHECK (active_flag IN (0, 1)),
    effective_from       TEXT,
    effective_to         TEXT,
    FOREIGN KEY (line_manager_id) REFERENCES employee_directory(employee_id)
);

CREATE TABLE IF NOT EXISTS approval_rules (
    approval_rule_id              TEXT PRIMARY KEY,
    minimum_amount_gbp            NUMERIC NOT NULL CHECK (minimum_amount_gbp >= 0),
    maximum_amount_gbp            NUMERIC,
    line_manager_required         INTEGER NOT NULL CHECK (line_manager_required IN (0, 1)),
    finance_manager_required      INTEGER NOT NULL CHECK (finance_manager_required IN (0, 1)),
    finance_review_required       INTEGER NOT NULL CHECK (finance_review_required IN (0, 1)),
    policy_exception_rule         INTEGER NOT NULL CHECK (policy_exception_rule IN (0, 1)),
    reminder_after_days           INTEGER NOT NULL CHECK (reminder_after_days >= 0),
    escalation_after_days         INTEGER NOT NULL CHECK (escalation_after_days >= 0),
    active_flag                   INTEGER NOT NULL DEFAULT 1 CHECK (active_flag IN (0, 1)),
    effective_from                TEXT,
    effective_to                  TEXT,
    CHECK (maximum_amount_gbp IS NULL OR maximum_amount_gbp >= minimum_amount_gbp)
);

CREATE TABLE IF NOT EXISTS expense_requests (
    expense_id                    TEXT PRIMARY KEY,
    employee_id                   TEXT NOT NULL,
    employee_name                 TEXT NOT NULL,
    employee_email                TEXT NOT NULL,
    department                    TEXT NOT NULL,
    line_manager_email            TEXT NOT NULL,
    expense_date                  TEXT NOT NULL,
    expense_category              TEXT NOT NULL,
    amount_gbp                    NUMERIC NOT NULL CHECK (amount_gbp > 0),
    description                   TEXT,
    receipt_link                  TEXT,
    policy_exception              INTEGER NOT NULL DEFAULT 0 CHECK (policy_exception IN (0, 1)),
    potential_duplicate           INTEGER NOT NULL DEFAULT 0 CHECK (potential_duplicate IN (0, 1)),
    approval_rule_id              TEXT NOT NULL,
    current_approver_email        TEXT,
    current_status                TEXT NOT NULL CHECK (
        current_status IN (
            'Submitted',
            'Pending Manager',
            'Pending Manager Approval',
            'Pending Finance Manager',
            'Pending Finance Manager Approval',
            'Pending Finance Review',
            'Ready for Payment',
            'Returned for Information',
            'Rejected',
            'Paid',
            'Cancelled'
        )
    ),
    submitted_at                  TEXT NOT NULL,
    manager_decision              TEXT,
    manager_email                 TEXT,
    manager_decision_at           TEXT,
    manager_comments              TEXT,
    finance_manager_decision      TEXT,
    finance_manager_email         TEXT,
    finance_manager_decision_at   TEXT,
    finance_manager_comments      TEXT,
    finance_review_result         TEXT,
    finance_officer_email         TEXT,
    ready_for_payment_at          TEXT,
    payment_date                  TEXT,
    rejection_reason              TEXT,
    return_reason                 TEXT,
    last_updated_at               TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee_directory(employee_id),
    FOREIGN KEY (approval_rule_id) REFERENCES approval_rules(approval_rule_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    audit_id              TEXT PRIMARY KEY,
    expense_id            TEXT NOT NULL,
    action_type           TEXT NOT NULL,
    previous_status       TEXT,
    new_status            TEXT NOT NULL,
    action_by             TEXT NOT NULL,
    action_at             TEXT NOT NULL,
    comments              TEXT,
    automation_run_id     TEXT,
    FOREIGN KEY (expense_id) REFERENCES expense_requests(expense_id)
);

CREATE TABLE IF NOT EXISTS error_log (
    error_id              TEXT PRIMARY KEY,
    expense_id            TEXT,
    workflow_step         TEXT NOT NULL,
    error_type            TEXT NOT NULL,
    error_message         TEXT NOT NULL,
    occurred_at           TEXT NOT NULL,
    resolved_flag         INTEGER NOT NULL DEFAULT 0 CHECK (resolved_flag IN (0, 1)),
    resolved_by           TEXT,
    resolved_at           TEXT,
    resolution_notes      TEXT,
    FOREIGN KEY (expense_id) REFERENCES expense_requests(expense_id)
);

CREATE INDEX IF NOT EXISTS idx_expense_employee_date
    ON expense_requests(employee_id, expense_date);

CREATE INDEX IF NOT EXISTS idx_expense_status
    ON expense_requests(current_status);

CREATE INDEX IF NOT EXISTS idx_expense_category
    ON expense_requests(expense_category);

CREATE INDEX IF NOT EXISTS idx_audit_expense_action_at
    ON audit_log(expense_id, action_at);

