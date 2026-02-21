# PROJECTS_SCHEMA.md

## Phase 4 — Projects Marketplace Database Schema

This document defines the database extensions required for Phase 4 project listings and lifecycle management.

---

## 1. Project Entity

### Project (`projects_project`)

Fields:

* id
* owner_id (FK → accounts_user)
* title
* description
* location
* estimated_budget
* funding_required (boolean)
* status (LISTED/FUNDING_OPEN/EXECUTION_STARTED/COMPLETED)
* created_at

---

## 2. Project Requirements

### Project Requirement (`projects_requirement`)

Defines required inputs.

Fields:

* id
* project_id
* type (MATERIAL/CONTRACTOR/SERVICE)
* description
* quantity

---

## 3. Project Funding Layer (Foundation)

### Investment Commitment (`projects_investment_commitment`)

Fields:

* id
* project_id
* investor_id (FK → accounts_user)
* amount_committed
* status (PLEDGED/CONFIRMED/CANCELLED)
* created_at

---

## 4. Execution Linkage

### Project Contract Link (`projects_project_contract`)

Connects projects to awarded contracts.

Fields:

* id
* project_id
* contract_id

---

## 5. Reporting

### Project Update (`projects_update`)

Fields:

* id
* project_id
* update_text
* posted_by
* created_at

---

**Phase 4 projects schema is now defined.**
