# ESCROW_SCHEMA.md

## Phase 3 — Escrow Database Schema

This document defines the database structures required to support escrow-backed milestone payments.

---

## 1. Escrow Account Model

### Escrow Account (`escrow_account`)

Represents held funds for a contract/order.

Fields:

* id
* contract_id (FK)
* buyer_id (FK)
* total_amount_held
* currency
* status (ACTIVE/RELEASED/CLOSED)
* created_at

---

## 2. Escrow Ledger

### Escrow Transaction (`escrow_transaction`)

Tracks all movements in escrow.

Fields:

* id
* escrow_account_id
* type (DEPOSIT/RELEASE/REFUND)
* amount
* milestone_id (nullable)
* payment_reference
* created_at

---

## 3. Milestone Release Link

### Escrow Release (`escrow_release`)

Approval-based release record.

Fields:

* id
* milestone_id
* approved_by (owner/admin)
* released_amount
* release_status (PENDING/COMPLETED)
* released_at

---

## 4. Admin Arbitration Overrides

### Escrow Dispute Hold (`escrow_hold`)

Freeze funds during disputes.

Fields:

* id
* escrow_account_id
* dispute_id
* reason
* status

---

**Escrow schema foundation is now defined for Phase 3.**
