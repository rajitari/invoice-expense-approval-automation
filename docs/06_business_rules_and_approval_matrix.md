# Business Rules and Approval Matrix

## 1. Purpose

This document defines the business rules used to validate, route, approve and monitor employee expense requests.

The rules are based on a fictional medium-sized UK organisation and are used for portfolio demonstration purposes.

## 2. General Assumptions

- The prototype uses GBP as its only currency
- Every employee has an assigned Line Manager
- Finance maintains the approval rules
- All employee and financial data is fictional
- Payment processing takes place outside the automated workflow
- Finance records the payment result in the system

> **Implementation status:** This document includes proposed business rules. The current prototype implements the £500 approval routes, policy-exception routing, future-date validation, duplicate flagging for human review, and payment eligibility control. Receipt requirements above £25, the 90-day submission limit, alternative approver routing, reminders and escalations are proposed requirements and are not implemented in the current prototype.

## 3. Approval Matrix

| Expense Amount | Line Manager Approval | Finance Manager Approval | Finance Review |
|---:|---|---|---|
| £0.01–£500.00 | Required | Not required | Required |
| Above £500.00 | Required | Required | Required |
| Any policy exception | Required | Required | Required |
| Employee's own approval request | Alternative approver required | May be required | Required |

Finance Review is a validation control and does not replace the required management approval.

## 4. Submission Rules

| Rule ID | Business Rule | System Response |
|---|---|---|
| BR-001 | Every request must have a unique Expense ID | Generate an ID when the form is submitted |
| BR-002 | Employee name is mandatory | Prevent submission if blank |
| BR-003 | Employee email is mandatory and must use a valid format | Display a validation message |
| BR-004 | Department is mandatory | Prevent submission if blank |
| BR-005 | Expense date is mandatory | Prevent submission if blank |
| BR-006 | Expense date cannot be in the future | Display a validation message |
| BR-007 | Expense amount must be greater than £0 | Display a validation message |
| BR-008 | Expense category is mandatory | Prevent submission if blank |
| BR-009 | Expense description is mandatory | Prevent submission if blank |
| BR-010 | Expenses above £25 require a receipt | Prevent submission or return for evidence |
| BR-011 | Expenses should be submitted within 90 days of the expense date | Flag late submissions for Finance review |
| BR-012 | The system must record the submission date and time | Add an automatic timestamp |

## 5. Expense Categories

The employee must select one of the following categories:

- Travel
- Accommodation
- Meals and Subsistence
- Office Supplies
- Training and Professional Development
- Client Entertainment
- Software and Subscriptions
- Mileage
- Other

If `Other` is selected, the employee must provide additional details.

## 6. Duplicate Detection Rules

| Rule ID | Business Rule | System Response |
|---|---|---|
| BR-013 | The system should check for an existing request with the same employee, expense date and amount | Flag the request as a potential duplicate |
| BR-014 | A potential duplicate must be reviewed by Finance | Do not automatically reject the request |
| BR-015 | A confirmed duplicate must not proceed to payment | Set the request to Rejected or Cancelled |

## 7. Approval Routing Rules

| Rule ID | Business Rule | System Response |
|---|---|---|
| BR-016 | Every valid request must first be sent to the employee's Line Manager | Set status to Pending Manager Approval |
| BR-017 | Requests of £500 or less require Line Manager approval | Route approved request to Finance Review |
| BR-018 | Requests above £500 require Line Manager and Finance Manager approval | Route to Finance Manager after Line Manager approval |
| BR-019 | A policy exception requires Finance Manager approval regardless of value | Route to Finance Manager |
| BR-020 | An employee cannot approve their own expense request | Route to an alternative authorised approver |
| BR-021 | An approver must record a reason when rejecting a request | Prevent rejection if the reason is blank |
| BR-022 | An approver must provide a reason when returning a request for information | Prevent return if the reason is blank |
| BR-023 | A rejected request cannot proceed to Finance Review or payment | End the approval workflow |
| BR-024 | A corrected request must be submitted for approval again | Restart the appropriate approval stage |

## 8. Finance Review Rules

| Rule ID | Business Rule | System Response |
|---|---|---|
| BR-025 | Finance must verify the receipt and request information | Keep status as Pending Finance Review |
| BR-026 | Finance must investigate potential duplicates | Record the review outcome |
| BR-027 | Finance can return a request for additional information | Set status to Returned for Information |
| BR-028 | Only a Finance user can set a request to Ready for Payment | Restrict the action by role |
| BR-029 | Only a Finance user can record a request as Paid | Record the payment date and user |
| BR-030 | A Paid request cannot be edited through the normal workflow | Lock the record from standard editing |

## 9. Notification and Service-Level Rules

| Rule ID | Business Rule | System Response |
|---|---|---|
| BR-031 | The employee must receive confirmation after submission | Send the Expense ID and submitted details |
| BR-032 | The approver must be notified when a request requires action | Send an approval notification |
| BR-033 | The approver should receive a reminder after one business day | Send an automatic reminder |
| BR-034 | A request outstanding for more than three business days should be escalated | Notify Finance or the next authorised approver |
| BR-035 | The employee must be notified when a request is returned | Include the return reason |
| BR-036 | The employee must be notified when a request is rejected | Include the rejection reason |
| BR-037 | The employee must be notified when payment is recorded | Send payment confirmation |

## 10. Status Rules

| Current Status | Permitted Next Status |
|---|---|
| Submitted | Pending Manager Approval |
| Pending Manager Approval | Returned for Information, Rejected, Pending Finance Manager Approval or Pending Finance Review |
| Pending Finance Manager Approval | Returned for Information, Rejected or Pending Finance Review |
| Returned for Information | Pending Manager Approval or Cancelled |
| Pending Finance Review | Returned for Information, Rejected or Ready for Payment |
| Ready for Payment | Paid |
| Paid | No standard status change permitted |
| Rejected | No standard status change permitted |
| Cancelled | No standard status change permitted |

## 11. Audit Trail Rules

| Rule ID | Business Rule |
|---|---|
| BR-038 | Every request must record its creation date and time |
| BR-039 | Every approval decision must record the approver and timestamp |
| BR-040 | Every rejection or return must record a reason |
| BR-041 | Every status change must be recorded |
| BR-042 | Payment confirmation must record the Finance user and payment date |
| BR-043 | Audit records must not be overwritten through the normal user workflow |

## 12. Data and Security Rules

| Rule ID | Business Rule |
|---|---|
| BR-044 | Users should only access information required for their role |
| BR-045 | Published portfolio data must be fictional or anonymised |
| BR-046 | Passwords, tokens and webhook URLs must not be stored in GitHub |
| BR-047 | Receipt files must not be publicly available |
| BR-048 | Personal information must not be included in screenshots |
| BR-049 | Access to the central dataset should be restricted |
| BR-050 | Error logs must not expose confidential information |

## 13. Approval Logic

The system should apply approval rules in the following order:

1. Validate the submitted information
2. Check whether a receipt is required
3. Check for a potential duplicate
4. Identify the employee's Line Manager
5. Check that the employee is not the approver
6. Obtain Line Manager approval
7. Check whether the amount exceeds £500
8. Check whether the request is a policy exception
9. Obtain Finance Manager approval where required
10. Send the request to Finance Review
11. Mark the request as Ready for Payment after validation
12. Allow Finance to record the request as Paid

## 14. Rule Ownership

| Rule Area | Business Owner |
|---|---|
| Submission requirements | Finance Officer |
| Approval thresholds | Finance Manager |
| Expense categories | Finance Manager |
| Payment status | Finance Officer |
| User access | System Administrator |
| Audit requirements | Finance Manager |
| Data protection | Data Protection or Security Representative |

## 15. Rule Changes

Any change to approval thresholds, receipt requirements or approval responsibilities should:

1. Be approved by the Finance Manager
2. Be documented with an effective date
3. Be tested before implementation
4. Be communicated to affected users
5. Be recorded in the project change log
