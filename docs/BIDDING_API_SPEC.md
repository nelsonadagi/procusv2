# BIDDING_API_SPEC.md

## Phase 2 — Contracts & Bidding API Specification

This document defines the REST API endpoints required for Phase 2.

Base URL:

`/api/v2/`

---

## 1. Contractor APIs

### POST `/contractors/register`

Create contractor profile.

Request:

* company_name
* service_categories
* operating_region

---

### GET `/contractors/{id}`

Retrieve contractor profile.

---

## 2. Contract Posting APIs

### POST `/contracts`

Project owner posts a new contract.

Request:

* title
* description_scope
* location
* budget_min
* budget_max

Response:

* contract_id

---

### GET `/contracts`

List contracts with filters.

Query params:

* location
* status

---

### GET `/contracts/{id}`

Retrieve contract detail.

---

## 3. Bidding APIs

### POST `/contracts/{id}/bids`

Contractor submits bid.

Request:

* proposed_cost
* proposed_timeline_days
* message

Response:

* bid_id

---

### GET `/contracts/{id}/bids`

Owner views submitted bids.

---

### POST `/bids/{id}/shortlist`

Owner shortlists bid.

---

### POST `/bids/{id}/award`

Owner awards contract to contractor.

Response:

* contract_status = AWARDED

---

## 4. Milestones APIs

### POST `/contracts/{id}/milestones`

Owner defines milestones.

Request:

* title
* amount
* due_date

---

### POST `/milestones/{id}/approve`

Owner approves milestone completion.

---

## 5. Reviews

### POST `/contracts/{id}/review`

Owner rates contractor.

Request:

* score
* comment

---

## 6. Permissions

* Only owners can post contracts
* Only contractors can bid
* Only owners can shortlist/award

---

**Phase 2 bidding API contract is now defined.**
