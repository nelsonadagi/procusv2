## Phase 2: Contractor + Contracts Execution Layer

**Overview:** This phase expands the platform to include a marketplace for construction services and contracts. It introduces new user roles for contractors, mechanisms for posting tenders, bidding, and managing project execution through milestones. The schemas reflect the core entities required to facilitate service-based procurement.

### Core Entities:

#### 2.1. Contractor Profile (`contractors_contractor`)
Represents a professional contractor or construction firm offering services on the platform. It extends the base `User` model with specific contractor details and performance metrics. This is distinct from `VendorProfile` for material suppliers.

```mermaid
classDiagram
    class ContractorProfile {
        +id: UUID
        +user_id: FK --> User
        +company_name: str
        +service_categories: List[str]
        +operating_region: str
        +verified_status: str // PENDING, APPROVED, SUSPENDED
        +rating_avg: Float // Average review score
        +created_at: DateTime
        +updated_at: DateTime
    }
    User "1" -- "1" ContractorProfile : has_profile
```

#### 2.2. Contractor Certification (`contractors_certification`)
Documents specific qualifications, licenses, or industry certifications held by a `ContractorProfile`, crucial for verification and establishing trust.

```mermaid
classDiagram
    class ContractorCertification {
        +id: UUID
        +contractor_id: FK --> ContractorProfile
        +document_type: str // e.g., "License", "ISO 9001"
        +document_url: str // Link to stored document
        +verified: boolean
        +created_at: DateTime
        +updated_at: DateTime
    }
    ContractorProfile "1" -- "0..*" ContractorCertification : has
```

#### 2.3. Contract (`contracts_contract`)
Represents a formal agreement or tender for construction services posted by a project owner. It outlines the scope of work, budget, timeline, and current execution status.

```mermaid
classDiagram
    class Contract {
        +id: UUID
        +owner_id: FK --> User // Project Owner
        +title: str
        +description_scope: TextField
        +location: str
        +budget_min: Decimal
        +budget_max: Decimal
        +status: str // POSTED, BIDDING, AWARDED, IN_PROGRESS, COMPLETED, CANCELLED
        +created_at: DateTime
        +updated_at: DateTime
    }
    User "1" -- "0..*" Contract : posts
```

#### 2.4. Bid (`contracts_bid`)
Captures a contractor's formal offer in response to a `Contract` (tender). It includes the proposed cost, timeline, and a message from the contractor.

```mermaid
classDiagram
    class Bid {
        +id: UUID
        +contract_id: FK --> Contract
        +contractor_id: FK --> ContractorProfile
        +proposed_cost: Decimal
        +proposed_timeline_days: Integer
        +message: TextField?
        +status: str // SUBMITTED, SHORTLISTED, REJECTED, AWARDED
        +created_at: DateTime
        +updated_at: DateTime
    }
    Contract "1" -- "0..*" Bid : receives
    ContractorProfile "1" -- "0..*" Bid : submits
```

#### 2.5. Milestone (`contracts_milestone`)
Divides a `Contract` into smaller, manageable stages with defined deliverables, amounts, and due dates. Used for tracking progress and triggering payments.

```mermaid
classDiagram
    class Milestone {
        +id: UUID
        +contract_id: FK --> Contract
        +title: str
        +description: TextField
        +amount: Decimal
        +due_date: Date
        +status: str // PENDING, COMPLETED, APPROVED, PAID
        +created_at: DateTime
        +updated_at: DateTime
    }
    Contract "1" -- "0..*" Milestone : comprises
```

#### 2.6. Milestone Payment (`payments_milestone_payment`)
Links a specific `Milestone` completion to a payment record. In this phase, it signifies the initiation of a payment process upon milestone approval.

```mermaid
classDiagram
    class MilestonePayment {
        +id: UUID
        +milestone_id: FK --> Milestone
        +payment_id: FK --> Payment // Links to the generic Payment model
        +release_status: str // PENDING, RELEASED, FAILED
        +created_at: DateTime
        +updated_at: DateTime
    }
    Milestone "1" -- "0..*" MilestonePayment : triggers
    Payment "1" -- "0..*" MilestonePayment : linked_to
```

#### 2.7. Contractor Review (`reviews_contractor_rating`)
Allows project owners to provide feedback and ratings on a `ContractorProfile` after a `Contract` is completed, contributing to the contractor's reputation.

```mermaid
classDiagram
    class ContractorReview {
        +id: UUID
        +contract_id: FK --> Contract
        +owner_id: FK --> User // The project owner who submitted the review
        +contractor_id: FK --> ContractorProfile // The contractor being reviewed
        +score: Integer // 1-5 stars
        +comment: TextField?
        +created_at: DateTime
        +updated_at: DateTime
    }
    Contract "1" -- "0..*" ContractorReview : related_to
    User "1" -- "0..*" ContractorReview : submitted_by
    ContractorProfile "1" -- "0..*" ContractorReview : reviewed_for
```

---