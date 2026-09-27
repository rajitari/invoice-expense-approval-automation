-- Data-quality and control queries.
-- A well-controlled dataset should return zero rows for most queries below.

-- 1. Missing core request information
SELECT expense_id, employee_id, amount_gbp, current_status, submitted_at
FROM expense_requests
WHERE TRIM(COALESCE(expense_id, '')) = ''
   OR TRIM(COALESCE(employee_id, '')) = ''
   OR amount_gbp IS NULL
   OR amount_gbp <= 0
   OR TRIM(COALESCE(current_status, '')) = ''
   OR TRIM(COALESCE(submitted_at, '')) = '';

-- 2. Duplicate business keys
SELECT expense_id, COUNT(*) AS duplicate_count
FROM expense_requests
GROUP BY expense_id
HAVING COUNT(*) > 1;

-- 3. Employees missing from the active directory
SELECT r.expense_id, r.employee_id
FROM expense_requests AS r
LEFT JOIN employee_directory AS e
    ON e.employee_id = r.employee_id
   AND e.active_flag = 1
WHERE e.employee_id IS NULL;

-- 4. Manager email does not match the employee directory
SELECT
    r.expense_id,
    r.employee_id,
    r.line_manager_email AS request_manager_email,
    e.line_manager_email AS directory_manager_email
FROM expense_requests AS r
JOIN employee_directory AS e
    ON e.employee_id = r.employee_id
WHERE LOWER(TRIM(r.line_manager_email)) <> LOWER(TRIM(e.line_manager_email));

-- 5. Approval rule does not match the business routing rules
SELECT
    expense_id,
    amount_gbp,
    policy_exception,
    approval_rule_id,
    CASE
        WHEN policy_exception = 1 THEN 'RULE-003'
        WHEN amount_gbp > 500 THEN 'RULE-002'
        ELSE 'RULE-001'
    END AS expected_rule_id
FROM expense_requests
WHERE approval_rule_id <>
    CASE
        WHEN policy_exception = 1 THEN 'RULE-003'
        WHEN amount_gbp > 500 THEN 'RULE-002'
        ELSE 'RULE-001'
    END;

-- 6. Paid requests without a payment date
SELECT expense_id, current_status, payment_date
FROM expense_requests
WHERE current_status = 'Paid'
  AND TRIM(COALESCE(payment_date, '')) = '';

-- 7. Payment date recorded for a request that is not Paid
SELECT expense_id, current_status, payment_date
FROM expense_requests
WHERE current_status <> 'Paid'
  AND TRIM(COALESCE(payment_date, '')) <> '';

-- 8. Potential duplicate flags with no matching business key
WITH duplicate_keys AS (
    SELECT employee_id, date(expense_date) AS expense_date, ROUND(amount_gbp, 2) AS amount_gbp
    FROM expense_requests
    GROUP BY employee_id, date(expense_date), ROUND(amount_gbp, 2)
    HAVING COUNT(*) > 1
)
SELECT r.expense_id, r.employee_id, r.expense_date, r.amount_gbp
FROM expense_requests AS r
LEFT JOIN duplicate_keys AS d
    ON d.employee_id = r.employee_id
   AND d.expense_date = date(r.expense_date)
   AND d.amount_gbp = ROUND(r.amount_gbp, 2)
WHERE r.potential_duplicate = 1
  AND d.employee_id IS NULL;

-- 9. Audit records that do not link to a request
SELECT a.audit_id, a.expense_id, a.action_type, a.action_at
FROM audit_log AS a
LEFT JOIN expense_requests AS r
    ON r.expense_id = a.expense_id
WHERE r.expense_id IS NULL;

-- 10. Resolved errors missing resolution evidence
SELECT error_id, expense_id, workflow_step, resolved_by, resolved_at, resolution_notes
FROM error_log
WHERE resolved_flag = 1
  AND (
        TRIM(COALESCE(resolved_by, '')) = ''
     OR TRIM(COALESCE(resolved_at, '')) = ''
     OR TRIM(COALESCE(resolution_notes, '')) = ''
  );

