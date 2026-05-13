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

Side effects:

* Awarded bid status → `AWARDED`
* All other bids on this contract → auto-rejected (`REJECTED`)
* Contract status → `AWARDED`

Response:

* status = "Bid awarded"
* contract_status = "AWARDED"

---

## 4. Milestones APIs

### POST `/contracts/{id}/milestones`

Owner defines milestones.

Request:

* title
* amount
* due_date

---

### POST `/milestones/{id}/complete`

Contractor marks milestone as completed.

* Only the awarded contractor can complete milestones.
* Milestone must be in `PENDING` state.
* Side effect: if contract status is `AWARDED`, it auto-progresses to `IN_PROGRESS`.

Response:

* status = "Milestone marked complete"
* contract_status (may be "IN_PROGRESS" if first completion)

---

### POST `/milestones/{id}/approve`

Owner approves milestone completion.

* Milestone must be in `COMPLETED` state.
* Side effect: if all milestones on the contract are `APPROVED`, contract auto-progresses to `COMPLETED`.

Response:

* status = "Milestone approved"
* payment_status = "PENDING_RELEASE"
* contract_status (may be "COMPLETED" if final milestone)

---

## 5. Contract Status Lifecycle

```
PENDING → POSTED → BIDDING → AWARDED → IN_PROGRESS → COMPLETED
   ↑         ↑         ↑          ↑            ↑
  draft   publish   1st bid   bid award   1st milestone
                               (auto-reject   complete
                                others)
```

* `PENDING` — Owner draft, not visible to public
* `POSTED` — Published to marketplace, accepting bids
* `BIDDING` — Bids received (set manually or via first bid)
* `AWARDED` — Contractor selected, owner defines milestones
* `IN_PROGRESS` — Contractor marked first milestone complete
* `COMPLETED` — All milestones approved by owner

## 6. Reviews

### POST `/contracts/{id}/review`

Owner rates contractor.

Request:

* score
* comment

---

## 7. Permissions

* Only owners can post, publish, and manage their contracts
* Only contractors can bid
* Only owners can shortlist/award
* Only the awarded contractor can complete milestones
* Only the contract owner can approve milestones

---

**Phase 2 bidding API contract is now defined.**
