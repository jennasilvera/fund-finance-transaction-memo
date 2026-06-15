# Analyst Walkthrough Guide

## Purpose

This guide explains how to review the Fund Finance Transaction Memo & Credit Request Package as a recruiter, banker, or credit analyst.

The project is a simulated fund finance case study using synthetic data only. It is designed to demonstrate analyst-level understanding of transaction analysis, credit request preparation, borrowing base analysis, NAV / LTV monitoring, term sheet support, closing memo support, and portfolio monitoring.

---

## Recommended Review Order

### 1. Start with the README

File: `README.md`

The README explains the transaction, repository structure, technical stack, outputs, methodology, and controls.

---

### 2. Review the Transaction Memo

File: `docs/transaction_memo.md`

This is the core banker-style memo. It includes:

- Executive summary
- Sponsor overview
- Fund overview
- Facility request
- Transaction rationale
- Sources and uses
- Repayment analysis
- Borrowing base summary
- NAV / LTV analysis
- Key risks and mitigants
- Recommendation
- Monitoring requirements

---

### 3. Review the Credit Request Package

File: `docs/credit_request_package.md`

This document frames the transaction as an internal credit approval request. It includes the requested facility terms, credit strengths, credit concerns, covenant package, conditions precedent, and final recommendation.

---

### 4. Open the Excel Model

File: `model/fund_finance_model.xlsx`

The Excel workbook includes:

- Assumptions
- Investor commitments
- Borrowing base
- NAV collateral
- Facility summary
- Covenant monitoring
- Output tables

This is the main quantitative model supporting the written documents.

---

### 5. Review the Monitoring Outputs

Files:

- `outputs/reports/borrowing_base_summary_formatted.md`
- `outputs/reports/covenant_monitoring_report.md`
- `outputs/reports/sql_monitoring_outputs.md`

These reports show the automated analysis layer behind the transaction package.

---

### 6. Review the Term Sheet and Closing Memo

Files:

- `docs/term_sheet.md`
- `docs/closing_memo.md`

These documents demonstrate awareness of transaction structuring, documentation, conditions precedent, and closing support.

---

### 7. Review the Lender Presentation Outline

File: `deck/lender_presentation_outline.md`

This is a 16-slide outline that summarizes the transaction in presentation format.

---

## Key Transaction Metrics

| Metric | Value |
|---|---:|
| Facility Size | $150.0mm |
| Initial Outstanding | $110.0mm |
| Total Commitments | $1,200.0mm |
| Eligible Unfunded Commitments | $627.0mm |
| Subscription Borrowing Base | $484.1mm |
| Eligible NAV | $584.1mm |
| Current LTV | 18.8% |
| Maximum LTV Covenant | 35.0% |
| Excess Availability | $40.0mm |
| Current Unfunded Coverage | 5.70x |

---

## Key Credit Strengths

- Meaningful eligible unfunded commitments
- Conservative opening LTV
- Positive excess availability
- Diversified investor base
- Clear covenant package
- Monthly borrowing base monitoring
- Quarterly NAV monitoring
- SQL-based portfolio monitoring outputs

---

## Key Risks Considered

- LP funding risk
- NAV deterioration
- Fund-level leverage
- Investor concentration
- Documentation / closing risk
- Liquidity risk
- Watchlist asset deterioration

---

## What This Project Demonstrates

This project demonstrates the ability to:

- Build a structured transaction memo
- Prepare an internal-style credit request package
- Analyze borrowing base availability
- Calculate NAV / LTV and facility capacity
- Identify credit risks and mitigants
- Create a monitoring framework
- Build a synthetic Excel model
- Automate reporting with Python and pandas
- Query monitoring data using SQL
- Present a transaction in banker-style materials

---

## Important Disclaimer

This is a simulated portfolio project using synthetic data only. It does not represent real transaction experience, real client work, legal advice, credit approval, or proprietary bank information.
