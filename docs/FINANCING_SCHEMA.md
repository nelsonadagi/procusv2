# FINANCING_SCHEMA.md

## Phase 3 — Embedded Financing Database Schema

This document defines the target database models required to support financing products.

Phase 3 introduces:

* Material credit
* Contractor working capital
* Invoice factoring

Later phases extend the same financing foundation to:

* property acquisition
* property completion or renovation
* project completion and structured construction finance

---

## 1. Credit Product Types

### Financing Product (`finance_product`)

Fields:

* id
* name (Material Credit, Contractor Loan)
* provider_name
* max_amount
* interest_rate
* active

---

## 2. Financing Applications

### Financing Application (`finance_application`)

Fields:

* id
* applicant_id (buyer/vendor/contractor)
* product_id
* target_type (PROPERTY/PROJECT/MATERIAL_ORDER/CONTRACT/GENERAL_WORKING_CAPITAL)
* property_id (nullable)
* project_id (nullable)
* requested_amount
* purpose_category (ACQUISITION/COMPLETION/RENOVATION/MATERIALS_PROCUREMENT/WORKING_CAPITAL)
* purpose
* status (SUBMITTED/APPROVED/REJECTED/DISBURSED)
* created_at

Rules:

* financing may target either a property or a project
* property finance may cover acquisition of a completed asset
* property finance may also support completion of an in-progress development asset
* project finance may support execution of a linked project after project setup

---

## 3. Loan Account Tracking

### Loan Account (`finance_loan`)

Fields:

* id
* application_id
* principal_amount
* disbursed_amount
* repayment_due_date
* status (ACTIVE/REPAID/DEFAULT)

---

## 4. Repayment Ledger

### Loan Repayment (`finance_repayment`)

Fields:

* id
* loan_id
* amount
* paid_at
* payment_reference

---

## 5. Supply Chain Credit Integration

### Supplier Credit Line (`finance_credit_line`)

Fields:

* id
* vendor_id
* credit_limit
* available_balance
* status

---

**Financing schema foundation is now defined for Phase 3.**
