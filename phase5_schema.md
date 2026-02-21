## Phase 5: Regulated Investment + Enterprise + Government Layer

**Overview:** This critical phase solidifies the platform's role as institutional infrastructure by introducing regulated investment flows, specialized features for enterprise procurement, and compliance-driven modules for government tendering. It emphasizes robust identity verification and financial governance.

### Core Entities:

#### 5.1. Investor Profile (`investor_profile`)
Extends the base `User` model for individuals or entities participating in regulated investment activities. It includes fields for KYC/AML status and accreditation, essential for compliance.

```mermaid
classDiagram
    class InvestorProfile {
        +id: UUID
        +user_id: FK --> User
        +kyc_status: str // PENDING, VERIFIED, REJECTED
        +accreditation_status: str // e.g., ACCREDITED, NON_ACCREDITED
        +jurisdiction: str
        +created_at: DateTime
        +updated_at: DateTime
    }
    User "1" -- "1" InvestorProfile : has_profile
```

#### 5.2. Investment Agreement (`investment_agreement`)
Represents a legally binding contract between an `InvestorProfile` and a `Project`, formalizing the funding commitment initiated in Phase 4.

```mermaid
classDiagram
    class InvestmentAgreement {
        +id: UUID
        +project_id: FK --> Project
        +investor_id: FK --> InvestorProfile
        +amount: Decimal
        +agreement_terms_url: str // Link to legal document
        +status: str // SIGNED, FUNDED, CANCELLED, COMPLETED
        +signed_at: DateTime
        +created_at: DateTime
        +updated_at: DateTime
    }
    InvestorProfile "1" -- "0..*" InvestmentAgreement : enters
    Project "1" -- "0..*" InvestmentAgreement : for
```

#### 5.3. Investment Transaction (`investment_transaction`)
Records the actual movement of capital corresponding to an `InvestmentAgreement`, often linked directly to `EscrowAccount`s for secure deployment.

```mermaid
classDiagram
    class InvestmentTransaction {
        +id: UUID
        +agreement_id: FK --> InvestmentAgreement
        +escrow_account_id: FK --> EscrowAccount // Linked to specific escrow for funding
        +type: str // FUNDING, RELEASE, RETURN
        +amount: Decimal
        +created_at: DateTime
        +updated_at: DateTime
    }
    InvestmentAgreement "1" -- "0..*" InvestmentTransaction : results_in
    EscrowAccount "1" -- "0..*" InvestmentTransaction : involves
```

#### 5.4. Investor Report (`investor_report`)
Provides periodic performance summaries and updates to `InvestorProfile`s regarding their investments in specific `Project`s.

```mermaid
classDiagram
    class InvestorReport {
        +id: UUID
        +project_id: FK --> Project
        +investor_id: FK --> InvestorProfile
        +report_period: str // e.g., "Q1-2026"
        +performance_summary: TextField
        +created_at: DateTime
        +updated_at: DateTime
    }
    InvestorProfile "1" -- "0..*" InvestorReport : receives
    Project "1" -- "0..*" InvestorReport : reports_on
```

---