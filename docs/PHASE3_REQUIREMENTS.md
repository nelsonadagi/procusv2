# PHASE3_REQUIREMENTS.md

## Construction Marketplace — Phase 3 Requirements

Phase 3 introduces the **financial infrastructure layer**:

* Escrow-backed payments
* Embedded construction financing
* Supply chain credit
* Dispute arbitration

Phase 3 is where the platform becomes a defensible construction operating system.

---

## 1. Phase 3 Objective

Enable trusted high-value construction commerce by adding:

* Escrow holding accounts
* Automated milestone releases
* Credit products for materials and contractors
* Financial compliance readiness

---

---

## 2. Actors & Permissions

### Finance Applicant
*   **Permissions**: `finance:apply`, `finance:view`
*   **Actions**: Can apply for material credit or project loans.

### Finance Admin
*   **Permissions**: `finance:view`, `finance:approve_loan`, `finance:disburse`, `audit:view`
*   **Actions**: Review applications, perform credit checks, and approve fund disbursement.
*   **Enforcement**: Requires multi-factor authentication (MFA) for disbursement.

### Arbitration Admin
*   **Permissions**: `disputes:view`, `disputes:arbitrate_dispute`, `escrow:release_funds`, `escrow:refund_funds`
*   **Actions**: Review evidence provided by Project Owners/Contractors and finalize escrow status.

### Audit Viewer
*   **Permissions**: `*:view`, `compliance:role_history`
*   **Actions**: Read-only log access for regulatory compliance checks.

---

## 3. Core Functional Requirements

### 2.1 Escrow System

* Buyer funds held securely
* Release tied to milestone approval
* Admin arbitration controls

### 2.2 Embedded Financing

* Material credit lines
* Contractor working capital
* Invoice factoring

### 2.3 Dispute Resolution

* Structured dispute workflows
* Evidence submission
* Admin resolution + refunds

### 2.4 Credit Scoring Foundation

* Transaction history-based scoring
* Vendor reliability metrics
* Contractor completion metrics

---

## 3. Phase 3 Exclusions

Not included until Phase 4+:

* Investment marketplace
* Property assets marketplace

---

## 4. Phase 3 Success Metrics

* ≥ 30% of contracts using escrow
* Reduced disputes by ≥ 40%
* Financing adoption ≥ 15%

---

**Phase 3 requirements are now defined.**
