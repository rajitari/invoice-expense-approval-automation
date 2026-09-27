-- Portfolio analytics queries for the Invoice & Expense Approval Automation.
-- Dialect: SQLite. Each query can be run independently.

-- 1. Executive KPI summary
SELECT
    COUNT(*) AS total_requests,
    ROUND(SUM(amount_gbp), 2) AS total_expense_gbp,
    SUM(CASE
            WHEN current_status LIKE 'Pending%'
              OR current_status IN ('Submitted', 'Returned for Information')
            THEN 1 ELSE 0
        END) AS open_requests,
    SUM(CASE WHEN current_status = 'Paid' THEN 1 ELSE 0 END) AS paid_requests,
    SUM(CASE WHEN policy_exception = 1 THEN 1 ELSE 0 END) AS policy_exceptions,
    SUM(CASE WHEN potential_duplicate = 1 THEN 1 ELSE 0 END) AS flagged_duplicates
FROM expense_requests;

-- 2. Request volume and value by current status
SELECT
    current_status,
    COUNT(*) AS request_count,
    ROUND(SUM(amount_gbp), 2) AS amount_gbp,
    ROUND(AVG(amount_gbp), 2) AS average_request_gbp
FROM expense_requests
GROUP BY current_status
ORDER BY request_count DESC, current_status;

-- 3. Expense value by category
SELECT
    expense_category,
    COUNT(*) AS request_count,
    ROUND(SUM(amount_gbp), 2) AS amount_gbp,
    ROUND(100.0 * SUM(amount_gbp) / SUM(SUM(amount_gbp)) OVER (), 1) AS percentage_of_total
FROM expense_requests
GROUP BY expense_category
ORDER BY amount_gbp DESC;

-- 4. Department demand and approval outcomes
SELECT
    department,
    COUNT(*) AS request_count,
    ROUND(SUM(amount_gbp), 2) AS amount_gbp,
    SUM(CASE WHEN current_status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_count,
    SUM(CASE WHEN current_status = 'Paid' THEN 1 ELSE 0 END) AS paid_count
FROM expense_requests
GROUP BY department
ORDER BY amount_gbp DESC;

-- 5. Risk and control indicators
SELECT 'Policy Exceptions' AS indicator, COUNT(*) AS indicator_count
FROM expense_requests
WHERE policy_exception = 1
UNION ALL
SELECT 'Potential Duplicates', COUNT(*)
FROM expense_requests
WHERE potential_duplicate = 1
UNION ALL
SELECT 'Rejected Requests', COUNT(*)
FROM expense_requests
WHERE current_status = 'Rejected';

-- 6. Routing rule distribution and value
SELECT
    approval_rule_id,
    COUNT(*) AS request_count,
    ROUND(SUM(amount_gbp), 2) AS amount_gbp,
    ROUND(AVG(amount_gbp), 2) AS average_request_gbp
FROM expense_requests
GROUP BY approval_rule_id
ORDER BY approval_rule_id;

-- 7. Open-request ageing for operational follow-up
SELECT
    expense_id,
    employee_name,
    department,
    current_status,
    current_approver_email,
    amount_gbp,
    submitted_at,
    CAST(julianday('now') - julianday(substr(submitted_at, 1, 10)) AS INTEGER) AS days_open
FROM expense_requests
WHERE current_status NOT IN ('Paid', 'Rejected', 'Cancelled')
ORDER BY days_open DESC, amount_gbp DESC;

-- 8. Duplicate candidates based on employee, date and amount
SELECT
    employee_id,
    date(expense_date) AS expense_date,
    ROUND(amount_gbp, 2) AS amount_gbp,
    COUNT(*) AS matching_records,
    GROUP_CONCAT(expense_id, ', ') AS expense_ids
FROM expense_requests
GROUP BY employee_id, date(expense_date), ROUND(amount_gbp, 2)
HAVING COUNT(*) > 1
ORDER BY matching_records DESC;

-- 9. End-to-end audit trail for one request
-- Replace the parameter with an Expense ID in a SQL client that does not support named parameters.
SELECT
    a.expense_id,
    a.action_at,
    a.action_type,
    a.previous_status,
    a.new_status,
    a.action_by,
    a.comments,
    a.automation_run_id
FROM audit_log AS a
WHERE a.expense_id = :expense_id
ORDER BY a.action_at, a.audit_id;

-- 10. Current approver workload
SELECT
    current_approver_email,
    current_status,
    COUNT(*) AS open_requests,
    ROUND(SUM(amount_gbp), 2) AS open_amount_gbp
FROM expense_requests
WHERE current_status LIKE 'Pending%'
GROUP BY current_approver_email, current_status
ORDER BY open_requests DESC, open_amount_gbp DESC;

-- 11. Average completion time for paid requests
SELECT
    ROUND(AVG(julianday(payment_date) - julianday(substr(submitted_at, 1, 10))), 2)
        AS average_days_to_payment,
    MIN(julianday(payment_date) - julianday(substr(submitted_at, 1, 10)))
        AS minimum_days_to_payment,
    MAX(julianday(payment_date) - julianday(substr(submitted_at, 1, 10)))
        AS maximum_days_to_payment
FROM expense_requests
WHERE current_status = 'Paid'
  AND payment_date IS NOT NULL;

