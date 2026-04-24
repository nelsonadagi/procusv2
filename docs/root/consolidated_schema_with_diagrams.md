# Consolidated Construction Marketplace Database Schema

This document provides a consolidated view of the database schema across all phases of the Construction Marketplace platform.

---

## Phase 1: Materials Liquidity Engine (Core Marketplace & Payments)

### Payment Model
```mermaid
classDiagram
    class Payment {
        order: ForeignKey
        provider: str
        amount: Decimal
        status: str
        transaction_reference: str
        paid_at: DateTime
    }
```

### Dispute Model
```mermaid
classDiagram
    class Dispute {
        opened_by: User
        order: Order
        status: str
        reason: TextField
        created_at: DateTime
    }
```

### Vendor Performance & Trust Signals (Part of Vendor Profile)
```mermaid
classDiagram
    class Vendor {
        fulfillment_rate: Float
        cancellation_rate: Float
        delivery_timeliness: Float
        average_rating: Float
        total_reviews: Integer
    }
```

---

## Phase 2: Contractor + Contracts Execution Layer

### Contractor Profile (`contractors_contractor`)
```mermaid
classDiagram
    class ContractorProfile {
        id
        user_id: FK --> accounts_user
        company_name
        service_categories
        operating_region
        verified_status
        rating_avg
        created_at
    }
```

### Contractor Certifications (`contractors_certification`)
```mermaid
classDiagram
    class ContractorCertification {
        id
        contractor_id: FK
        document_type
        document_url
        verified
    }
    ContractorProfile "1" -- "0..*" ContractorCertification : has
```

### Contract (`contracts_contract`)
```mermaid
classDiagram
    class Contract {
        id
        owner_id: FK --> accounts_user
        title
        description_scope
        location
        budget_min
        budget_max
        status: str
        created_at
    }
```

### Bid (`contracts_bid`)
```mermaid
classDiagram
    class Bid {
        id
        contract_id: FK
        contractor_id: FK
        proposed_cost
        proposed_timeline_days
        message
        status: str
        created_at
    }
    Contract "1" -- "0..*" Bid : has
    ContractorProfile "1" -- "0..*" Bid : submits
```

### Milestone (`contracts_milestone`)
```mermaid
classDiagram
    class Milestone {
        id
        contract_id: FK
        title
        description
        amount
        due_date
        status: str
    }
    Contract "1" -- "0..*" Milestone : has
```

### Milestone Payment (`payments_milestone_payment`)
```mermaid
classDiagram
    class MilestonePayment {
        id
        milestone_id: FK
        payment_id: FK --> payments_payment
        release_status
    }
    Milestone "1" -- "0..*" MilestonePayment : triggers
```

### Contractor Review (`reviews_contractor_rating`)
```mermaid
classDiagram
    class ContractorReview {
        id
        contract_id: FK
        owner_id: FK
        contractor_id: FK
        score
        comment
        created_at
    }
    Contract "1" -- "0..*" ContractorReview : reviewed_in
    ContractorProfile "1" -- "0..*" ContractorReview : gets_reviewed
```

---

## Phase 3: Escrow + Embedded Finance Layer

### Escrow Account (`escrow_account`)
```mermaid
classDiagram
    class EscrowAccount {
        id
        contract_id: FK
        buyer_id: FK
        total_amount_held
        currency
        status: str
        created_at
    }
    Contract "1" -- "1" EscrowAccount : manages_funds_for
```

### Escrow Transaction (`escrow_transaction`)
```mermaid
classDiagram
    class EscrowTransaction {
        id
        escrow_account_id: FK
        type: str
        amount
        milestone_id: FK?
        payment_reference
        created_at
    }
    EscrowAccount "1" -- "0..*" EscrowTransaction : has
    Milestone "1" -- "0..1" EscrowTransaction : via
```

### Escrow Release (`escrow_release`)
```mermaid
classDiagram
    class EscrowRelease {
        id
        milestone_id: FK
        approved_by: str
        released_amount
        release_status: str
        released_at
    }
    Milestone "1" -- "0..1" EscrowRelease : approved_by
```

### Escrow Dispute Hold (`escrow_hold`)
```mermaid
classDiagram
    class EscrowDisputeHold {
        id
        escrow_account_id: FK
        dispute_id: FK
        reason
        status
    }
    EscrowAccount "1" -- "0..*" EscrowDisputeHold : has
    Dispute "1" -- "0..1" EscrowDisputeHold : triggers
```

---

## Phase 4: Projects + Property + Capital Pipeline

### Project (`projects_project`)
```mermaid
classDiagram
    class Project {
        id
        owner_id: FK --> accounts_user
        title
        description
        location
        estimated_budget
        funding_required: boolean
        status: str
        created_at
    }
```

### Project Requirement (`projects_requirement`)
```mermaid
classDiagram
    class ProjectRequirement {
        id
        project_id: FK
        type: str
        description
        quantity
    }
    Project "1" -- "0..*" ProjectRequirement : has
```

### Investment Commitment (`projects_investment_commitment`)
```mermaid
classDiagram
    class InvestmentCommitment {
        id
        project_id: FK
        investor_id: FK --> accounts_user
        amount_committed
        status: str
        created_at
    }
    Project "1" -- "0..*" InvestmentCommitment : receives
```

### Project Contract Link (`projects_project_contract`)
```mermaid
classDiagram
    class ProjectContractLink {
        id
        project_id: FK
        contract_id: FK
    }
    Project "1" -- "0..*" ProjectContractLink : links_to
    Contract "1" -- "0..*" ProjectContractLink : linked_by
```

### Project Update (`projects_update`)
```mermaid
classDiagram
    class ProjectUpdate {
        id
        project_id: FK
        update_text
        posted_by
        created_at
    }
    Project "1" -- "0..*" ProjectUpdate : has
```

### Property Listing (`property_listing`)
```mermaid
classDiagram
    class PropertyListing {
        id
        owner_id: FK --> accounts_user
        title
        description
        location
        asset_type: str
        price_estimate
        status: str
        created_at
    }
```

### Development Metadata (`property_development`)
```mermaid
classDiagram
    class DevelopmentMetadata {
        id
        property_id: FK
        zoning_info
        build_ready: boolean
        utilities_available
    }
    PropertyListing "1" -- "0..1" DevelopmentMetadata : has
```

### Property Project Link (`property_project_link`)
```mermaid
classDiagram
    class PropertyProjectLink {
        id
        property_id: FK
        project_id: FK
    }
    PropertyListing "1" -- "0..*" PropertyProjectLink : associated_with
    Project "1" -- "0..*" PropertyProjectLink : associated_with
```

---

## Phase 5: Regulated Investment + Enterprise + Government Layer

### Investor (`investor_profile`)
```mermaid
classDiagram
    class InvestorProfile {
        id
        user_id: FK --> accounts_user
        kyc_status: str
        accreditation_status
        jurisdiction
        created_at
    }
```

### Investment Agreement (`investment_agreement`)
```mermaid
classDiagram
    class InvestmentAgreement {
        id
        project_id: FK
        investor_id: FK
        amount
        agreement_terms_url
        status: str
        signed_at
    }
    InvestorProfile "1" -- "0..*" InvestmentAgreement : enters
    Project "1" -- "0..*" InvestmentAgreement : for
```

### Investment Transaction (`investment_transaction`)
```mermaid
classDiagram
    class InvestmentTransaction {
        id
        agreement_id: FK
        escrow_account_id: FK
        type: str
        amount
        created_at
    }
    InvestmentAgreement "1" -- "0..*" InvestmentTransaction : results_in
    EscrowAccount "1" -- "0..*" InvestmentTransaction : involves
```

### Investor Report (`investor_report`)
```mermaid
classDiagram
    class InvestorReport {
        id
        project_id: FK
        investor_id: FK
        report_period
        performance_summary
        created_at
    }
    InvestorProfile "1" -- "0..*" InvestorReport : receives
    Project "1" -- "0..*" InvestorReport : reports_on
```
