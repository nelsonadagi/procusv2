# CONTRACTS_SCHEMA.md

## Phase 2 — Contracts & Services Database Schema

This document defines the database extensions required for Phase 2.

Phase 2 introduces:

* Contractors
* Contracts/Tenders
* Bidding
* Milestones

---

## 1. Contractor Entities

### Contractor Profile (`contractors_contractor`)

Fields:

* id
* user_id (FK → accounts_user)
* company_name
* service_categories
* operating_region
* verified_status
* rating_avg
* created_at

---

### Contractor Certifications (`contractors_certification`)

Fields:

* id
* contractor_id
* document_type
* document_url
* verified

---

## 2. Contract Posting

### Contract (`contracts_contract`)

Fields:

* id
* owner_id (FK → accounts_user)
* title
* description_scope
* location
* budget_min
* budget_max
* status (POSTED/BIDDING/AWARDED/IN_PROGRESS/COMPLETED)
* created_at

---

## 3. Bidding System

### Bid (`contracts_bid`)

Fields:

* id
* contract_id
* contractor_id
* proposed_cost
* proposed_timeline_days
* message
* status (SUBMITTED/SHORTLISTED/REJECTED/AWARDED)
* created_at

---

## 4. Milestones

### Milestone (`contracts_milestone`)

Fields:

* id
* contract_id
* title
* description
* amount
* due_date
* status (PENDING/APPROVED/PAID)

---

## 5. Milestone Payments (Placeholder)

### Milestone Payment (`payments_milestone_payment`)

Fields:

* id
* milestone_id
* payment_id (FK → payments_payment)
* release_status

---

## 6. Reputation Expansion

### Contractor Review (`reviews_contractor_rating`)

Fields:

* id
* contract_id
* owner_id
* contractor_id
* score
* comment
* created_at

---

**Phase 2 contracts schema is now defined.**
