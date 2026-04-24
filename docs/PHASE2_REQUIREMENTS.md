# PHASE2_REQUIREMENTS.md

## Construction Marketplace — Phase 2 Requirements

Phase 2 expands the platform from a **materials procurement marketplace** into a **contracts + services execution marketplace**.

---

## 1. Phase 2 Objective

Enable construction work execution by introducing:

* Contractor marketplace
* Tender/contract posting
* Bidding workflows
* Milestone-based project tracking
* Expanded trust and reputation

---

---

## 2. Actors & Permissions

### Contractor
*   **Permissions**: `contracts:view`, `bids:submit_bid`, `bids:view`, `milestones:view`, `disputes:raise_dispute`
*   **Enforcement**: Restricted to submitting bids on `OPEN` contracts. Cannot view competing bids.

### Contractor Staff
*   **Permissions**: `milestones:view`, `contracts:view`
*   **Actions**: Can update progress on an active contract milestone.

### Project Owner (Contract Publisher)
*   **Permissions**: `contracts:post_contract`, `contracts:award_contract`, `contracts:view`, `projects:create_project`, `bids:view`, `milestones:manage_milestones`
*   **Actions**: Post job scopes, select winning bidders, and define milestones.
*   **Forbidden**: Cannot bid on their own contracts.

### Contracts Admin
*   **Permissions**: `contracts:view`, `contracts:award_contract` (override), `disputes:arbitrate_dispute`
*   **Actions**: Override awards in case of corruption/error and resolve contractor-owner disputes.

---

## 3. New Core Roles (Business Definitions)

### Contractor

* Create verified service profile
* Bid on contracts
* Execute awarded work
* Receive milestone payments

---

## 3. Functional Requirements

### 3.1 Contractor Marketplace

* Contractor onboarding
* Service categories
* Credential verification
* Portfolio and ratings

### 3.2 Contract Posting

Project owners can post:

* Work scope
* Location
* Budget range
* Timeline
* Qualification requirements

### 3.3 Bidding System

Contractors can:

* Submit bids with cost + timeline
* Attach references

Owners can:

* Shortlist bids
* Award contracts

### 3.4 Execution Tracking

Contracts move through:

* Posted → Bidding → Awarded → In Progress → Completed

Milestones define progress checkpoints.

### 3.5 Milestone Payments (Placeholder)

* Deposit on award
* Progress payments
* Final payment on completion

### 3.6 Reputation Expansion

* Contractor-specific ratings
* Completion history
* Dispute rate scoring

---

## 4. Phase 2 Exclusions

Not included until Phase 3+:

* Embedded financing products
* Full escrow compliance
* Investment marketplace

---

## 5. Phase 2 Success Metrics

* ≥ 100 active contractors
* ≥ 30 contracts posted/month
* ≥ 10 completed contracts/month
* Dispute rate < 10%

---

**Phase 2 requirements are now defined.**
