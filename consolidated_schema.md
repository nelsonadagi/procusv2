# Consolidated Construction Marketplace Database Schema

This document provides a consolidated view of the database schema across all phases of the Construction Marketplace platform.

---

## Phase 1: Materials Liquidity Engine (Core Marketplace & Payments)

### Payment Model
```python
class Payment:
    order: ForeignKey
    provider: str  # 'MODERN_CHECKOUT', 'MPESA', 'STRIPE'
    amount: Decimal
    status: UNPAID | PENDING | PAID | FAILED
    transaction_reference: str
    paid_at: DateTime
```

### Dispute Model
```python
class Dispute:
    opened_by: User
    order: Order
    status: OPENED | UNDER_REVIEW | RESOLVED_RELEASE | RESOLVED_REFUND | CLOSED
    reason: TextField
    created_at: DateTime
```

### Vendor Performance & Trust Signals (Part of Vendor Profile)
```python
class Vendor:
    fulfillment_rate: Float  # % of completed orders
    cancellation_rate: Float  # % of cancelled orders
    delivery_timeliness: Float  # % on-time deliveries
    average_rating: Float  # Average buyer rating (1-5)
    total_reviews: Integer  # Number of ratings
```

---

## Phase 2: Contractor + Contracts Execution Layer

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

### Contractor Certifications (`contractors_certification`)
Fields:
* id
* contractor_id
* document_type
* document_url
* verified

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

### Milestone (`contracts_milestone`)
Fields:
* id
* contract_id
* title
* description
* amount
* due_date
* status (PENDING/APPROVED/PAID)

### Milestone Payment (`payments_milestone_payment`)
Fields:
* id
* milestone_id
* payment_id (FK → payments_payment)
* release_status

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

## Phase 3: Escrow + Embedded Finance Layer

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

### Escrow Release (`escrow_release`)
Approval-based release record.
Fields:
* id
* milestone_id
* approved_by (owner/admin)
* released_amount
* release_status (PENDING/COMPLETED)
* released_at

### Escrow Dispute Hold (`escrow_hold`)
Freeze funds during disputes.
Fields:
* id
* escrow_account_id
* dispute_id
* reason
* status

---

## Phase 4: Projects + Property + Capital Pipeline

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

### Project Requirement (`projects_requirement`)
Defines required inputs.
Fields:
* id
* project_id
* type (MATERIAL/CONTRACTOR/SERVICE)
* description
* quantity

### Investment Commitment (`projects_investment_commitment`)
Fields:
* id
* project_id
* investor_id (FK → accounts_user)
* amount_committed
* status (PLEDGED/CONFIRMED/CANCELLED)
* created_at

### Project Contract Link (`projects_project_contract`)
Connects projects to awarded contracts.
Fields:
* id
* project_id
* contract_id

### Project Update (`projects_update`)
Fields:
* id
* project_id
* update_text
* posted_by
* created_at

### Property Listing (`property_listing`)
Fields:
* id
* owner_id (FK → accounts_user)
* title
* description
* location
* asset_type (LAND/RESIDENTIAL/COMMERCIAL/RENOVATION)
* price_estimate
* status (ACTIVE/SOLD/INACTIVE)
* created_at

### Development Metadata (`property_development`)
Fields:
* id
* property_id
* zoning_info
* build_ready (boolean)
* utilities_available

### Property Project Link (`property_project_link`)
Fields:
* id
* property_id
* project_id

---

## Phase 5: Regulated Investment + Enterprise + Government Layer

### Investor (`investor_profile`)
Fields:
* id
* user_id (FK → accounts_user)
* kyc_status (PENDING/VERIFIED/REJECTED)
* accreditation_status
* jurisdiction
* created_at

### Investment Agreement (`investment_agreement`)
Fields:
* id
* project_id
* investor_id
* amount
* agreement_terms_url
* status (SIGNED/FUNDED/CANCELLED)
* signed_at

### Investment Transaction (`investment_transaction`)
Fields:
* id
* agreement_id
* escrow_account_id
* type (FUNDING/RELEASE/RETURN)
* amount
* created_at

### Investor Report (`investor_report`)
Fields:
* id
* project_id
* investor_id
* report_period
* performance_summary
* created_at
