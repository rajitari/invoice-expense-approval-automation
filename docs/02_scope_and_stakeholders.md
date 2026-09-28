# Project Scope and Stakeholders

## 1. Project Purpose

The purpose of this project is to design and demonstrate an automated invoice and employee expense approval process.

The proposed solution will replace a manual email and spreadsheet-based process with a centralised workflow for submission, approval, status tracking and management reporting.

This is a portfolio project based on a fictional medium-sized UK organisation. All names, email addresses and financial data used in the project are fictional.

## 2. Project Objectives

- Standardise the expense submission process
- Reduce incomplete or incorrect submissions
- Automate approval routing based on predefined business rules
- Improve visibility of outstanding requests
- Reduce manual work for the finance team
- Maintain a record of approval decisions
- Provide expense insights through the Excel Desktop dashboard

## 3. In Scope

The following activities are included in the project:

- Employee expense request submission
- Capture of employee and expense information
- Upload or submission of receipt evidence
- Automatic generation of a unique Expense ID
- Data validation
- Approval routing based on expense value
- Manager approval or rejection
- Additional finance approval for high-value expenses
- Automatic status updates
- Email notifications
- Central storage of request information
- Approval audit trail
- UAT testing
- Management reporting and dashboard development
- Analysis using SQL and Python

## 4. Out of Scope

The following activities are not included:

- Actual transfer of money to employees
- Integration with a real banking system
- Integration with a live accounting or ERP system
- Payroll processing
- Corporate credit card reconciliation
- Tax calculation
- Foreign exchange conversion
- Supplier procurement
- Production deployment
- Use of real company or employee data

## 5. Key Assumptions

- Employees have access to an online form
- Employees provide a valid email address
- Each employee has an assigned line manager
- Approvers have access to email
- Supporting receipts are available electronically
- Approval thresholds are agreed by the finance team
- The project uses fictional and anonymised data
- Microsoft Excel in OneDrive for Business acts as the central data source for the current prototype

## 6. Constraints

- The project is a portfolio prototype rather than a production system
- The solution will use free or low-cost software where possible
- The project will not connect to confidential company systems
- Security and access controls will be demonstrated conceptually
- The automation depends on the availability of third-party tools
- Dashboard results depend on the quality of the sample data

## 7. Stakeholders

| Stakeholder | Role in the Process | Main Needs |
|---|---|---|
| Employee | Submits an expense request | Simple submission process and status visibility |
| Line Manager | Reviews normal expense requests | Complete information and an easy approval process |
| Finance Officer | Reviews approved requests | Accurate data and supporting evidence |
| Finance Manager | Approves high-value requests | Spending control and visibility |
| Management Team | Reviews expense performance | Dashboard, trends and KPIs |
| System Administrator | Maintains the workflow | Reliable process and error information |
| Business Analyst | Analyses and documents requirements | Clear requirements and stakeholder agreement |
| Data Analyst | Develops reports and analysis | Complete and structured data |

## 8. Stakeholder Influence and Interest

| Stakeholder | Influence | Interest | Engagement Approach |
|---|---|---|---|
| Employee | Low | High | Gather feedback and provide clear instructions |
| Line Manager | Medium | High | Consult during workflow and approval design |
| Finance Officer | High | High | Involve throughout requirements and testing |
| Finance Manager | High | High | Obtain approval for rules and reporting needs |
| Management Team | High | Medium | Provide progress updates and dashboard results |
| System Administrator | Medium | Medium | Consult on technical feasibility and controls |

## 9. High-Level Responsibilities

| Activity | Employee | Line Manager | Finance Officer | Finance Manager | System Administrator |
|---|---|---|---|---|---|
| Submit request | Responsible | Informed | Informed | Informed | Informed |
| Review normal expense | Informed | Responsible | Consulted | Informed | Informed |
| Review high-value expense | Informed | Consulted | Consulted | Responsible | Informed |
| Update payment status | Informed | Informed | Responsible | Accountable | Informed |
| Maintain workflow | Informed | Informed | Consulted | Accountable | Responsible |
| Review dashboard | Informed | Consulted | Consulted | Responsible | Informed |

## 10. Project Success Criteria

The project will be considered successful when:

- Employees can submit a complete expense request
- Each request receives a unique Expense ID
- Requests are routed to the correct approver
- Approvers can approve or reject requests
- Request status is updated automatically
- Employees receive a decision notification
- Approval actions are recorded in an audit trail
- All critical UAT test cases pass
- The dashboard displays agreed expense KPIs
- No confidential or personally identifiable data is published
