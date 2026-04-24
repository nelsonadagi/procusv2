# MILESTONE_PAYMENT_WORKFLOW.md

## Phase 2 — Milestone Payment Workflow (Bridge to Escrow)

This document defines how Phase 2 introduces milestone-based payments.

Phase 2 does NOT implement full escrow, but establishes the workflow foundation.

---

## 1. Payment Philosophy

Construction work is executed in stages.

Payments must align with:

* Contract award
* Progress delivery
* Final completion

---

## 2. Milestone Lifecycle

Each contract contains milestones:

* Deposit milestone (award)
* Progress milestones
* Final milestone

Milestone states:

* PENDING
* COMPLETED (contractor claims done)
* APPROVED (owner confirms)
* PAID

---

## 3. Phase 2 Workflow

### Step 1 — Owner Defines Milestones

Owner sets:

* Amount
* Due date
* Deliverable description

---

### Step 2 — Contractor Executes Work

Contractor marks milestone as completed.

---

### Step 3 — Owner Approves

Owner approves completion.

---

### Step 4 — Payment Trigger

Platform initiates payment release.

Phase 2 uses placeholder provider integration.

---

## 4. Data Requirements

Milestones must store:

* Amount locked
* Approval timestamp
* Payment reference

---

## 5. Phase 3 Escrow Upgrade Path

Phase 3 will extend this into:

* Escrow holding accounts
* Automatic milestone releases
* Dispute arbitration
* Financing overlays

---

**Milestone payment workflow is now defined for Phase 2.**
