# MILESTONE_PAYMENT_WORKFLOW.md

## Phase 2 — Milestone Payment Workflow (Bridge to Escrow)

This document defines how Phase 2 implements milestone-based payments with automatic contract status progression.

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

* `PENDING` — Defined by owner, waiting for contractor
* `COMPLETED` — Contractor claims work is done
* `APPROVED` — Owner confirms completion, payment triggered
* `PAID` — Payment released (Phase 3: wired via escrow)

---

## 3. Phase 2 Workflow

### Step 0 — Owner Publishes Contract

Owner creates contract (status: `PENDING`), then publishes it:

```
POST /contracts/{id}/publish
```

Status moves: `PENDING` → `POSTED`

---

### Step 1 — Contractors Bid

Contractors discover `POSTED` contracts and submit bids.

Owner reviews bids, shortlists, and awards one:

```
POST /bids/{id}/award
```

Side effects:
* Awarded bid → `AWARDED`
* All other bids → auto-rejected (`REJECTED`)
* Contract → `AWARDED`

---

### Step 2 — Owner Defines Milestones

Owner sets payment stages:

```
POST /contracts/{id}/milestones
```

Request:
* title
* amount
* due_date

---

### Step 3 — Contractor Executes Work

Contractor finishes work for a milestone and marks it complete:

```
POST /milestones/{id}/complete
```

* Only the awarded contractor can call this.
* Milestone status: `PENDING` → `COMPLETED`
* **Auto-progress**: If contract was `AWARDED`, it moves to `IN_PROGRESS`

---

### Step 4 — Owner Approves

Owner inspects deliverables and approves:

```
POST /milestones/{id}/approve
```

* Milestone must be `COMPLETED`.
* Milestone status: `COMPLETED` → `APPROVED`
* **Auto-progress**: If all milestones on the contract are `APPROVED`, contract moves to `COMPLETED`

---

### Step 5 — Payment Trigger

Platform initiates payment release.

Phase 2 returns:

```json
{
  "status": "Milestone approved",
  "payment_status": "PENDING_RELEASE",
  "contract_status": "COMPLETED"
}
```

Actual payment gateway integration is a Phase 3 upgrade.

---

## 4. Contract Auto-Progression Rules

| Event | From Status | To Status | Condition |
|-------|-------------|-----------|-----------|
| Owner publishes | `PENDING` | `POSTED` | Explicit `publish` action |
| Owner awards bid | `POSTED` / `BIDDING` | `AWARDED` | Bid awarded |
| Contractor completes 1st milestone | `AWARDED` | `IN_PROGRESS` | Any milestone → `COMPLETED` |
| Owner approves last milestone | `IN_PROGRESS` | `COMPLETED` | All milestones → `APPROVED` |

---

## 5. Data Requirements

Milestones must store:

* Amount locked
* Completion timestamp (set when contractor marks complete)
* Approval timestamp (set when owner approves)
* Payment reference

---

## 6. Phase 3 Escrow Upgrade Path

Phase 3 will extend this into:

* Escrow holding accounts
* Automatic milestone releases upon approval
* Dispute arbitration
* Financing overlays

---

**Milestone payment workflow is now defined for Phase 2.**
