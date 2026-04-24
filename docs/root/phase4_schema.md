## Phase 4: Projects + Property + Capital Pipeline

**Overview:** This phase elevates the platform beyond individual transactions to managing entire construction project lifecycles. It introduces mechanisms for project listing, property asset management, and foundational support for investment commitments, linking all previous phases into a comprehensive project management ecosystem.

### Core Entities:

#### 4.1. Project (`projects_project`)
The central entity for managing a construction initiative, encapsulating its overall scope, budget, timeline, and status. It acts as an umbrella for multiple `Contract`s and `Product` procurements.

```mermaid
classDiagram
    class Project {
        +id: UUID
        +owner_id: FK --> User // The project owner/developer
        +title: str
        +description: TextField
        +location: str
        +estimated_budget: Decimal
        +funding_required: boolean
        +status: str // LISTED, FUNDING_OPEN, EXECUTION_STARTED, COMPLETED, CANCELLED
        +created_at: DateTime
        +updated_at: DateTime
    }
    User "1" -- "0..*" Project : owns
```

#### 4.2. Project Requirement (`projects_requirement`)
Details the specific materials, contractors, or services needed to execute a `Project`, linking directly to the marketplace functionalities established in earlier phases.

```mermaid
classDiagram
    class ProjectRequirement {
        +id: UUID
        +project_id: FK --> Project
        +type: str // MATERIAL, CONTRACTOR, SERVICE
        +description: TextField
        +quantity: Decimal // Relevant for materials
        +created_at: DateTime
        +updated_at: DateTime
    }
    Project "1" -- "0..*" ProjectRequirement : defines
```

#### 4.3. Investment Commitment (`projects_investment_commitment`)
Represents an investor's non-binding pledge of funds towards a `Project`, serving as a preliminary indicator of funding interest before formal agreements.

```mermaid
classDiagram
    class InvestmentCommitment {
        +id: UUID
        +project_id: FK --> Project
        +investor_id: FK --> User // The user making the commitment
        +amount_committed: Decimal
        +status: str // PLEDGED, CONFIRMED, CANCELLED
        +created_at: DateTime
        +updated_at: DateTime
    }
    Project "1" -- "0..*" InvestmentCommitment : attracts
    User "1" -- "0..*" InvestmentCommitment : makes
```

#### 4.4. Project Contract Link (`projects_project_contract`)
Establishes the relationship between an overarching `Project` and the individual `Contract`s executed as part of that project.

```mermaid
classDiagram
    class ProjectContractLink {
        +id: UUID
        +project_id: FK --> Project
        +contract_id: FK --> Contract
        +created_at: DateTime
        +updated_at: DateTime
    }
    Project "1" -- "0..*" ProjectContractLink : manages
    Contract "1" -- "1" ProjectContractLink : belongs_to
```

#### 4.5. Project Update (`projects_update`)
Allows project owners to post progress updates, significant events, or challenges related to a `Project`, providing transparency to stakeholders.

```mermaid
classDiagram
    class ProjectUpdate {
        +id: UUID
        +project_id: FK --> Project
        +update_text: TextField
        +posted_by: FK --> User
        +created_at: DateTime
        +updated_at: DateTime
    }
    Project "1" -- "0..*" ProjectUpdate : has
    User "1" -- "0..*" ProjectUpdate : posts
```

#### 4.6. Property Listing (`property_listing`)
Enables owners to list land or existing structures that are potential sites for new construction or renovation `Project`s. This serves as an upstream demand generator.

```mermaid
classDiagram
    class PropertyListing {
        +id: UUID
        +owner_id: FK --> User // The owner of the property listing
        +title: str
        +description: TextField
        +location: str
        +asset_type: str // LAND, RESIDENTIAL, COMMERCIAL, RENOVATION
        +price_estimate: Decimal?
        +status: str // ACTIVE, SOLD, INACTIVE
        +created_at: DateTime
        +updated_at: DateTime
    }
    User "1" -- "0..*" PropertyListing : lists
```

#### 4.7. Development Metadata (`property_development`)
Provides additional details about the development potential of a `PropertyListing`, such as zoning information or utility availability.

```mermaid
classDiagram
    class DevelopmentMetadata {
        +id: UUID
        +property_id: FK --> PropertyListing
        +zoning_info: TextField?
        +build_ready: boolean
        +utilities_available: boolean
        +created_at: DateTime
        +updated_at: DateTime
    }
    PropertyListing "1" -- "0..1" DevelopmentMetadata : has
```

#### 4.8. Property Project Link (`property_project_link`)
Connects a `PropertyListing` to a `Project`, indicating that the project is being developed on or is related to that specific property.

```mermaid
classDiagram
    class PropertyProjectLink {
        +id: UUID
        +property_id: FK --> PropertyListing
        +project_id: FK --> Project
        +created_at: DateTime
        +updated_at: DateTime
    }
    PropertyListing "1" -- "0..*" PropertyProjectLink : associated_with
    Project "1" -- "0..*" PropertyProjectLink : associated_with
```

---