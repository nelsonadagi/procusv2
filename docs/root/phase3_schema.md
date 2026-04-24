## Phase 3: Escrow + Embedded Finance Layer

**Overview:** This pivotal phase introduces the robust financial infrastructure, transitioning from placeholder payments to a secure, automated escrow system. It focuses on mitigating payment and delivery risks, laying the groundwork for embedded financing, and formalizing dispute resolution.

### Core Entities:

#### 3.1. Escrow Account (`escrow_account`)
Represents a dedicated account where funds are securely held for a specific `Contract` or order, ensuring trust between transacting parties.

```mermaid
classDiagram
    class EscrowAccount {
        +id: UUID
        +contract_id: FK --> Contract
        +buyer_id: FK --> User // The buyer/owner who funded the escrow
        +total_amount_held: Decimal
        +currency: str
        +status: str // ACTIVE, RELEASED, CLOSED, DISPUTED
        +created_at: DateTime
        +updated_at: DateTime
    }
    Contract "1" -- "1" EscrowAccount : manages_funds_for
    User "1" -- "0..*" EscrowAccount : funds
```

#### 3.2. Escrow Transaction (`escrow_transaction`)
Records every movement of funds into, within, or out of an `EscrowAccount`, providing a complete audit trail for financial flows.

```mermaid
classDiagram
    class EscrowTransaction {
        +id: UUID
        +escrow_account_id: FK --> EscrowAccount
        +type: str // DEPOSIT, RELEASE, REFUND, ADJUSTMENT
        +amount: Decimal
        +milestone_id: FK? --> Milestone // Nullable, if transaction not tied to a specific milestone
        +payment_reference: str?
        +created_at: DateTime
        +updated_at: DateTime
    }
    EscrowAccount "1" -- "0..*" EscrowTransaction : has
    Milestone "1" -- "0..1" EscrowTransaction : relates_to
```

#### 3.3. Escrow Release (`escrow_release`)
Documents the approval and release of funds from an `EscrowAccount` upon the successful completion and approval of a `Milestone`.

```mermaid
classDiagram
    class EscrowRelease {
        +id: UUID
        +milestone_id: FK --> Milestone
        +escrow_account_id: FK --> EscrowAccount
        +approved_by: FK --> User // The user (e.g., Project Owner) who approved the release
        +released_amount: Decimal
        +release_status: str // PENDING, COMPLETED, FAILED
        +released_at: DateTime
        +created_at: DateTime
        +updated_at: DateTime
    }
    Milestone "1" -- "0..1" EscrowRelease : triggers
    EscrowAccount "1" -- "0..*" EscrowRelease : handles
    User "1" -- "0..*" EscrowRelease : approved_by
```

#### 3.4. Escrow Dispute Hold (`escrow_hold`)
Captures the state when funds in an `EscrowAccount` are temporarily frozen due to a `Dispute`, awaiting arbitration.

```mermaid
classDiagram
    class EscrowDisputeHold {
        +id: UUID
        +escrow_account_id: FK --> EscrowAccount
        +dispute_id: FK --> Dispute
        +reason: TextField
        +status: str // ACTIVE, RESOLVED
        +created_at: DateTime
        +updated_at: DateTime
    }
    EscrowAccount "1" -- "0..*" EscrowDisputeHold : subject_to
    Dispute "1" -- "0..1" EscrowDisputeHold : initiates
```

---