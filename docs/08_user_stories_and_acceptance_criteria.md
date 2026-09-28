# User Stories and Acceptance Criteria

## 1. Purpose

This document converts the approved requirements into user stories and testable acceptance criteria.

Acceptance criteria use the Given–When–Then format:

- **Given** describes the starting condition
- **When** describes the user action or event
- **Then** describes the expected result

> **Implementation status:** These are target-state acceptance criteria; they do not mean every feature has been implemented or tested. The current dashboard has Department and Expense Category slicers only. Date and status filters, automated reminders and escalations, and the receipt threshold rule are not implemented in the current prototype. Refer to the completed project guide for the scenarios verified during UAT.

## 2. User Story Summary

| Story ID | User Story Title | Primary User | Priority | Related Requirements |
|---|---|---|---|---|
| US-001 | Submit an expense request | Employee | Must Have | FR-001–FR-010 |
| US-002 | Validate receipt requirements | Employee | Must Have | FR-004–FR-007 |
| US-003 | Receive submission confirmation | Employee | Must Have | FR-034–FR-035 |
| US-004 | Review an expense request | Line Manager | Must Have | FR-011–FR-019 |
| US-005 | Approve a high-value request | Finance Manager | Must Have | FR-013–FR-015 |
| US-006 | Return a request for information | Approver | Must Have | FR-016–FR-020 |
| US-007 | Validate an approved request | Finance Officer | Must Have | FR-021–FR-028 |
| US-008 | Identify potential duplicates | Finance Officer | Should Have | FR-023 |
| US-009 | Receive reminders and escalations | Approver | Should Have | FR-040–FR-041 |
| US-010 | Maintain an audit trail | Finance Manager | Must Have | FR-042–FR-046 |
| US-011 | Monitor expense performance | Management Team | Should Have | RPT-001–RPT-010 |
| US-012 | Maintain workflow rules | System Administrator | Should Have | NFR-009 |

---

## US-001: Submit an Expense Request

### User Story

As an employee, I want to submit an expense request through an online form so that I do not need to send expense information manually by email.

### Acceptance Criteria

```gherkin
Scenario: Submit a complete and valid request
Given the employee has completed all mandatory fields
And the expense amount is greater than £0
And the expense date is not in the future
When the employee submits the form
Then the system creates the expense request
And generates a unique Expense ID
And records the submission date and time
And sets the status to Pending Manager Approval
And stores the request in the central dataset
```

```gherkin
Scenario: Mandatory information is missing
Given at least one mandatory field is blank
When the employee attempts to submit the form
Then the system prevents submission
And displays a clear validation message
And identifies the field that must be completed
```

```gherkin
Scenario: Expense amount is invalid
Given the expense amount is zero or negative
When the employee attempts to submit the form
Then the system prevents submission
And displays an amount validation message
```

```gherkin
Scenario: Expense date is in the future
Given the expense date is later than the current date
When the employee attempts to submit the form
Then the system prevents submission
And displays a date validation message
```

---

## US-002: Validate Receipt Requirements

### User Story

As an employee, I want to know when a receipt is required so that I can provide the correct supporting evidence.

### Acceptance Criteria

```gherkin
Scenario: Receipt is required
Given the expense amount is greater than £25
And no receipt has been provided
When the employee attempts to submit the request
Then the system prevents submission
And displays a message explaining that a receipt is required
```

```gherkin
Scenario: Receipt is optional
Given the expense amount is £25 or less
And no receipt has been provided
When the employee submits all other required information
Then the system accepts the request
```

```gherkin
Scenario: Receipt has been provided
Given the expense amount is greater than £25
And a receipt has been provided
When the employee submits the form
Then the system accepts the receipt information
And continues processing the request
```

---

## US-003: Receive Submission Confirmation

### User Story

As an employee, I want to receive confirmation after submitting an expense request so that I know it has been received.

### Acceptance Criteria

```gherkin
Scenario: Confirmation is sent successfully
Given a valid expense request has been submitted
When the system creates the request
Then the employee receives a confirmation notification
And the notification includes the Expense ID
And the notification includes the submitted amount
And the notification includes the current status
```

```gherkin
Scenario: Notification cannot be delivered
Given a valid request has been recorded
And the confirmation notification fails
When the automation handles the error
Then the request remains stored
And the error is recorded in the error log
And confidential information is not included in the error message
```

---

## US-004: Review an Expense Request

### User Story

As a Line Manager, I want to review and decide on an employee expense request so that only valid business expenses proceed to Finance.

### Acceptance Criteria

```gherkin
Scenario: Manager approves a request of £500 or less
Given the request is Pending Manager Approval
And the expense amount is £500 or less
When the Line Manager approves the request
Then the system records the approver
And records the decision date and time
And sets the status to Pending Finance Review
And sends the request to Finance
```

```gherkin
Scenario: Manager approves a request above £500
Given the request is Pending Manager Approval
And the expense amount is greater than £500
When the Line Manager approves the request
Then the system records the approval
And sets the status to Pending Finance Manager Approval
And notifies the Finance Manager
```

```gherkin
Scenario: Manager rejects a request
Given the request is Pending Manager Approval
When the Line Manager selects Reject
Then the system requires a rejection reason
And sets the status to Rejected
And records the decision
And notifies the employee
And stops the approval workflow
```

```gherkin
Scenario: Rejection reason is missing
Given the Line Manager has selected Reject
And the rejection reason is blank
When the Line Manager submits the decision
Then the system prevents the rejection from being completed
And requests a rejection reason
```

---

## US-005: Approve a High-Value Request

### User Story

As a Finance Manager, I want to review high-value expense requests so that additional financial control is applied.

### Acceptance Criteria

```gherkin
Scenario: High-value request is routed correctly
Given the expense amount is greater than £500
And the Line Manager has approved the request
When the approval is recorded
Then the system sets the status to Pending Finance Manager Approval
And sends the request to the Finance Manager
```

```gherkin
Scenario: Finance Manager approves the request
Given the request is Pending Finance Manager Approval
When the Finance Manager approves the request
Then the system records the approver and timestamp
And sets the status to Pending Finance Review
And notifies Finance
```

```gherkin
Scenario: Finance Manager rejects the request
Given the request is Pending Finance Manager Approval
When the Finance Manager provides a reason and rejects the request
Then the system sets the status to Rejected
And records the decision and reason
And notifies the employee
And stops the workflow
```

```gherkin
Scenario: Expense amount is exactly £500
Given the expense amount is exactly £500
And the Line Manager approves the request
When the approval rule is evaluated
Then Finance Manager approval is not required
And the request proceeds to Pending Finance Review
```

---

## US-006: Return a Request for Information

### User Story

As an approver, I want to return an incomplete request to the employee so that it can be corrected before approval.

### Acceptance Criteria

```gherkin
Scenario: Approver returns a request
Given the request is waiting for approval or Finance review
When the approver selects Return for Information
And provides a return reason
Then the system sets the status to Returned for Information
And records the reason and timestamp
And notifies the employee
```

```gherkin
Scenario: Return reason is missing
Given the approver selects Return for Information
And the reason is blank
When the approver submits the decision
Then the system prevents the action
And requests a return reason
```

```gherkin
Scenario: Employee corrects and resubmits the request
Given the status is Returned for Information
When the employee provides the required information
And resubmits the request
Then the system records the resubmission time
And routes the request to the appropriate approval stage
```

---

## US-007: Validate an Approved Request

### User Story

As a Finance Officer, I want to validate approved expense requests so that only complete and compliant requests proceed to payment.

### Acceptance Criteria

```gherkin
Scenario: Finance validation passes
Given all required approvals have been completed
And the receipt and expense information are valid
When the Finance Officer completes the review
Then the system sets the status to Ready for Payment
And records the Finance Officer and timestamp
```

```gherkin
Scenario: Finance requires additional information
Given Finance identifies missing or unclear information
When the Finance Officer provides a reason and returns the request
Then the status becomes Returned for Information
And the employee receives a notification
```

```gherkin
Scenario: Finance records payment
Given the request status is Ready for Payment
When an authorised Finance Officer records the payment
Then the system sets the status to Paid
And records the payment date
And records the Finance user
And notifies the employee
```

```gherkin
Scenario: Unauthorised user attempts to record payment
Given the user does not have Finance permission
When the user attempts to set the request to Paid
Then the system prevents the action
```

---

## US-008: Identify Potential Duplicates

### User Story

As a Finance Officer, I want potential duplicate requests to be flagged so that duplicate reimbursements can be prevented.

### Acceptance Criteria

```gherkin
Scenario: Potential duplicate is detected
Given an existing request has the same employee
And the same expense date
And the same expense amount
When a new request is submitted
Then the system flags it as a potential duplicate
And allows Finance to investigate it
And does not automatically reject it
```

```gherkin
Scenario: Duplicate is confirmed
Given Finance confirms that the request is a duplicate
When the Finance Officer records the review outcome
Then the request does not proceed to payment
And the decision is recorded in the audit trail
```

---

## US-009: Receive Reminders and Escalations

### User Story

As an approver, I want to receive reminders about outstanding requests so that approvals are completed on time.

### Acceptance Criteria

```gherkin
Scenario: First reminder is sent
Given a request has remained with an approver for one business day
And no decision has been recorded
When the reminder process runs
Then the system sends a reminder to the approver
```

```gherkin
Scenario: Request is escalated
Given a request has remained outstanding for more than three business days
And no decision has been recorded
When the escalation process runs
Then the system sends an escalation notification
And records the escalation in the audit log
```

```gherkin
Scenario: Completed request receives no reminder
Given a decision has already been recorded
When the reminder process runs
Then no reminder is sent for that approval stage
```

---

## US-010: Maintain an Audit Trail

### User Story

As a Finance Manager, I want all important actions to be recorded so that the expense process can be reviewed and audited.

### Acceptance Criteria

```gherkin
Scenario: Approval decision is recorded
Given an approver submits a decision
When the system processes the decision
Then the audit log records the Expense ID
And the action
And the user
And the date and time
And the resulting status
```

```gherkin
Scenario: Status is changed
Given the status of a request changes
When the change is completed
Then the previous status and new status are recorded
```

```gherkin
Scenario: Standard user attempts to change audit history
Given the user does not have authorised administrative access
When the user attempts to edit an audit record
Then the system prevents the change
```

---

## US-011: Monitor Expense Performance

### User Story

As a member of the Management Team, I want to view expense and approval KPIs so that I can monitor spending and process performance.

### Acceptance Criteria

```gherkin
Scenario: Dashboard displays core KPIs
Given expense data is available
When the user opens the dashboard
Then the dashboard displays total expense value
And total number of requests
And requests by status
And expenses by department
And expenses by category
```

```gherkin
Scenario: Dashboard filters are applied
Given the dashboard contains expense data
When the user selects a date, department, category or status filter
Then all relevant visualisations update to reflect the selection
```

```gherkin
Scenario: Outstanding requests are displayed
Given at least one request has not completed the workflow
When the dashboard is refreshed
Then the request is included in the outstanding request analysis
```

---

## US-012: Maintain Workflow Rules

### User Story

As a System Administrator, I want approval thresholds and reference values to be maintainable so that authorised changes can be implemented without rebuilding the entire process.

### Acceptance Criteria

```gherkin
Scenario: Approval threshold is updated
Given an authorised change has been approved
When the administrator updates the approval threshold
Then the new threshold is applied to future requests
And existing completed requests are not changed
And the change is documented
```

```gherkin
Scenario: Expense category is added
Given a new category has been approved
When the administrator updates the category reference list
Then the new category becomes available for future submissions
```

## 3. Definition of Ready

A user story is ready for implementation when:

- The user and business need are clear
- Acceptance criteria are documented
- Relevant business rules are identified
- Dependencies are understood
- Required data fields are known
- The story is prioritised
- The story is small enough to implement and test

## 4. Definition of Done

A user story is complete when:

- The agreed functionality has been implemented
- All acceptance criteria have been tested
- Critical tests have passed
- Errors are handled appropriately
- Documentation has been updated
- No confidential data is exposed
- Evidence has been saved for the portfolio
- The Product Owner or relevant stakeholder has accepted the result
