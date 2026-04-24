# REGULATED_INVESTMENT_SCHEMA.md

## Phase 5 — Regulated Investment Database Schema

This document defines the database structures required for binding, compliant investment flows.

---

## 1. Investor Profile

### Investor (`investor_profile`)

Fields:

* id
* user_id (FK → accounts_user)
* kyc_status (PENDING/VERIFIED/REJECTED)
* accreditation_status
* jurisdiction
* created_at

---

## 2. Binding Investment Agreements

### Investment Agreement (`investment_agreement`)

Fields:

* id
* project_id
* investor_id
* amount
* agreement_terms_url
* status (SIGNED/FUNDED/CANCELLED)
* signed_at

---

## 3. Capital Deployment Ledger

### Investment Transaction (`investment_transaction`)

Fields:

* id
* agreement_id
* escrow_account_id
* type (FUNDING/RELEASE/RETURN)
* amount
* created_at

---

## 4. Investor Reporting

### Investor Report (`investor_report`)

Fields:

* id
* project_id
* investor_id
* report_period
* performance_summary
* created_at

---

**Regulated investment schema is now defined for Phase 5.**
