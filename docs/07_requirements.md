# Requirements Catalogue

## 1. Purpose

This document defines the business, functional, data, reporting and non-functional requirements for the Invoice and Expense Approval Automation project.

The requirements are based on the approved project scope, identified pain points, To-Be process and business rules.

## 2. Priority Definitions

The MoSCoW method is used to prioritise requirements.

| Priority | Definition |
|---|---|
| Must Have | Essential for the prototype to operate successfully |
| Should Have | Important but the prototype can operate temporarily without it |
| Could Have | Desirable enhancement if time and resources permit |
| Won't Have | Not included in the current project scope |

## 3. Business Requirements

| ID | Business Requirement | Priority | Business Owner |
|---|---|---|---|
| BUS-001 | The organisation must have a standard process for submitting employee expenses | Must Have | Finance Manager |
| BUS-002 | The process must reduce incomplete expense submissions | Must Have | Finance Manager |
| BUS-003 | The process must reduce manual data entry performed by Finance | Must Have | Finance Officer |
| BUS-004 | Expense requests must be routed according to approved business rules | Must Have | Finance Manager |
| BUS-005 | Employees must receive information about the progress of their requests | Must Have | Finance Manager |
| BUS-006 | The organisation must maintain an audit trail of approval decisions | Must Have | Finance Manager |
| BUS-007 | Management must be able to monitor expense and approval performance | Should Have | Management Team |
| BUS-008 | Public portfolio materials must not contain confidential or personal data | Must Have | Project Owner |

## 4. Functional Requirements

### 4.1 Expense Submission

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-001 | The system shall allow an employee to submit an expense request through an online form | Must Have |
| FR-002 | The system shall capture employee name, employee email and department | Must Have |
| FR-003 | The system shall capture expense date, category, amount and description | Must Have |
| FR-004 | The system shall prevent submission when a mandatory field is blank | Must Have |
| FR-005 | The system shall prevent submission when the expense amount is zero or negative | Must Have |
| FR-006 | The system shall prevent submission when the expense date is in the future | Must Have |
| FR-007 | The system shall require receipt evidence when the amount exceeds £25 | Must Have |
| FR-008 | The system shall generate a unique Expense ID for every valid submission | Must Have |
| FR-009 | The system shall record the submission date and time automatically | Must Have |
| FR-010 | The system shall store valid requests in a central dataset | Must Have |

### 4.2 Approval Workflow

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-011 | The system shall identify the employee's Line Manager | Must Have |
| FR-012 | The system shall route every valid request to the Line Manager | Must Have |
| FR-013 | The system shall route requests above £500 to the Finance Manager after Line Manager approval | Must Have |
| FR-014 | The system shall route policy exceptions to the Finance Manager regardless of value | Should Have |
| FR-015 | The system shall prevent an employee from approving their own request | Must Have |
| FR-016 | An approver shall be able to approve, reject or return a request | Must Have |
| FR-017 | The system shall require a reason when a request is rejected | Must Have |
| FR-018 | The system shall require a reason when a request is returned for information | Must Have |
| FR-019 | The system shall stop the workflow when a request is rejected | Must Have |
| FR-020 | A corrected request shall be returned to the appropriate approval stage | Must Have |

### 4.3 Finance Processing

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-021 | The system shall send an approved request to Finance for validation | Must Have |
| FR-022 | Finance shall be able to record the result of receipt and policy checks | Must Have |
| FR-023 | The system shall flag potential duplicate requests | Should Have |
| FR-024 | Finance shall be able to return a request for additional information | Must Have |
| FR-025 | Only an authorised Finance user shall be able to set a request to Ready for Payment | Must Have |
| FR-026 | Only an authorised Finance user shall be able to set a request to Paid | Must Have |
| FR-027 | The system shall record the payment date | Must Have |
| FR-028 | Paid requests shall not be editable through the standard workflow | Should Have |

### 4.4 Status Management

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-029 | Every request shall have one current status | Must Have |
| FR-030 | The system shall update the status when a workflow action is completed | Must Have |
| FR-031 | Status values shall be selected from the approved status list | Must Have |
| FR-032 | The system shall prevent invalid status transitions | Should Have |
| FR-033 | An authorised user shall be able to cancel an unpaid request | Could Have |

### 4.5 Notifications and Escalations

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-034 | The system shall send a submission confirmation to the employee | Must Have |
| FR-035 | The confirmation shall include the Expense ID | Must Have |
| FR-036 | The system shall notify an approver when action is required | Must Have |
| FR-037 | The system shall notify the employee when a request is returned | Must Have |
| FR-038 | The system shall notify the employee when a request is rejected | Must Have |
| FR-039 | The system shall notify the employee when payment is recorded | Should Have |
| FR-040 | The system shall remind an approver after one business day | Should Have |
| FR-041 | The system shall escalate a request after three business days without action | Could Have |

### 4.6 Audit Trail

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-042 | The system shall record every status change | Must Have |
| FR-043 | The system shall record the user responsible for each approval decision | Must Have |
| FR-044 | The system shall record the date and time of each decision | Must Have |
| FR-045 | The system shall retain rejection and return reasons | Must Have |
| FR-046 | Standard users shall not be able to overwrite audit history | Must Have |

## 5. Reporting Requirements

| ID | Reporting Requirement | Priority |
|---|---|---|
| RPT-001 | The dashboard shall display total expense value | Must Have |
| RPT-002 | The dashboard shall display the number of submitted requests | Must Have |
| RPT-003 | The dashboard shall display requests by status | Must Have |
| RPT-004 | The dashboard shall display expenses by department | Must Have |
| RPT-005 | The dashboard shall display expenses by category | Must Have |
| RPT-006 | The dashboard shall display monthly expense trends | Should Have |
| RPT-007 | The dashboard shall display average approval time | Should Have |
| RPT-008 | The dashboard shall identify overdue requests | Should Have |
| RPT-009 | Users shall be able to filter results by date, department, category and status | Should Have |
| RPT-010 | The dashboard shall display approval and rejection rates | Could Have |

## 6. Data Requirements

| ID | Data Requirement | Priority |
|---|---|---|
| DR-001 | Expense ID must be unique and must not be blank | Must Have |
| DR-002 | Expense amount must be stored as a numeric value | Must Have |
| DR-003 | Expense and decision dates must be stored in a consistent date format | Must Have |
| DR-004 | Status must use an approved status value | Must Have |
| DR-005 | Department and category must use standard values | Must Have |
| DR-006 | Approver email must use a valid email format | Must Have |
| DR-007 | Missing optional information must be distinguishable from incorrect data | Should Have |
| DR-008 | Sample portfolio data must use fictional names and email addresses | Must Have |
| DR-009 | The dataset must support reporting in Power BI | Must Have |
| DR-010 | The dataset should support analysis using SQL and Python | Should Have |

## 7. Non-Functional Requirements

| ID | Non-Functional Requirement | Priority |
|---|---|---|
| NFR-001 | The form shall use clear labels and instructions | Must Have |
| NFR-002 | A typical expense submission should take no more than five minutes | Should Have |
| NFR-003 | The workflow should begin processing a valid submission within one minute | Should Have |
| NFR-004 | Access to request information shall be limited according to user role | Must Have |
| NFR-005 | Passwords, API keys, tokens and webhook URLs shall not be stored in GitHub | Must Have |
| NFR-006 | Public screenshots and datasets shall contain only fictional or anonymised information | Must Have |
| NFR-007 | The solution shall record automation errors for investigation | Must Have |
| NFR-008 | Error messages shall not expose confidential information | Must Have |
| NFR-009 | Approval thresholds and categories should be maintainable without redesigning the entire workflow | Should Have |
| NFR-010 | Project documentation shall be maintained in GitHub | Must Have |
| NFR-011 | Important source files shall have a private backup | Must Have |
| NFR-012 | The form and dashboard should use accessible colours, readable text and clear navigation | Should Have |

## 8. Requirements Traceability Summary

| Business Need | Supporting Requirements |
|---|---|
| Reduce incomplete submissions | FR-002–FR-007 |
| Reduce manual data entry | FR-008–FR-010 |
| Improve approval routing | FR-011–FR-020 |
| Improve Finance controls | FR-021–FR-028 |
| Improve status visibility | FR-029–FR-041 |
| Maintain an audit trail | FR-042–FR-046 |
| Improve management information | RPT-001–RPT-010 |
| Protect project information | DR-008, NFR-004–NFR-006 |

## 9. Dependencies

The requirements depend on:

- An online form tool
- A central spreadsheet or dataset
- An automation platform
- Valid employee and approver email addresses
- Agreed approval thresholds
- Access to Power BI
- Availability of representative sample data

## 10. Excluded Requirements

The current version will not include:

- Actual bank payments
- Payroll processing
- Live accounting-system integration
- Tax calculation
- Foreign currency conversion
- Mobile application development
- Production-level identity management
- Real employee or company data

## 11. Requirements Acceptance

Requirements should be reviewed against the following questions:

- Is the requirement clear?
- Is it necessary?
- Is it within scope?
- Is it testable?
- Is it consistent with the business rules?
- Does it have an owner?
- Has it been prioritised?
- Can it be traced to a business need?

In a real project, formal approval would be obtained from the Finance Manager, Finance Officer, Project Sponsor and relevant system owner.
