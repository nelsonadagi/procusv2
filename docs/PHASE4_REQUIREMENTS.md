# PHASE4_REQUIREMENTS.md

## Construction Marketplace — Phase 4 Requirements

Phase 4 introduces the **Projects + Property + Investment Layer**, completing the construction economy ecosystem.

---

## 1. Phase 4 Objective

Enable the platform to support:

* Project owners listing full construction projects
* Developers sourcing contractors + suppliers
* Investors funding construction opportunities
* Property assets feeding project demand
* Full lifecycle construction commerce

## 1.1 Project Module Definition

Projects are the execution hub for construction activity.

* A project is not a tender.
* A project is not a property listing.
* A project may link to one or more awarded contracts.
* A project may link to one or more property records when the asset is part of the development context.
* A project must be usable immediately after creation, even before requirements or contracts are added.

### Project Screens

* `ProjectList.vue` is the discovery and filtering surface.
* `CreateProject.vue` is the minimal shell creation flow.
* `ProjectDetail.vue` is the project management cockpit for summary, requirements, contracts, milestones, funding, documents, updates, risks, and activity.
* `OwnerDashboard.vue` is the owner entry point for project actions.

---

---

## 2. Actors & Permissions

### Developer / Project Sponsor
*   **Permissions**: `projects:create_project`, `projects:update_project`, `contracts:post_contract`, `investments:view`
*   **Actions**: Can define project roadmaps and internal budget allocation.
*   **Enforcement**: Restricted to modifying projects they own.

### Property Owner
*   **Permissions**: `property:list_property`, `property:update_property`, `projects:create_project`
*   **Actions**: List land for development or sites for renovation.

### Investor Guest (Pledge-only)
*   **Permissions**: `projects:view`, `investments:view`, `investments:pledge`
*   **Actions**: Browse projects and express interest (pledge) without full financial commitment.
*   **Forbidden**: Cannot sign binding investment agreements until Phase 5 KYC.

### Projects Admin
*   **Permissions**: `projects:delete_project`, `projects:view`, `risk:view`
*   **Actions**: Global moderation and risk scoring assessment for projects.

---

## 3. Core Functional Requirements

### 2.1 Projects Marketplace

Project owners can publish:

* Project title + description
* Location + timeline
* Budget requirements
* Required materials + contractors
* Funding needs (optional)

Projects become structured pipelines beyond single contracts.

### 2.1.1 Project Behavior

* Creation only stores the project shell.
* Requirements are added after creation.
* Contract links are added after award.
* Updates are posted during execution.
* Funding and pledges are attached to the project record.

---

### 2.2 Investor Participation Layer

Investors can:

* Browse investment-ready projects
* Commit funding (Phase 4 foundation)
* Track milestone-based deployment
* Receive structured reporting

Full securities compliance is Phase 5+.

---

### 2.3 Property Marketplace Integration

Property owners/developers can list:

* Land parcels
* Development-ready sites
* Renovation/build opportunities

Property becomes the upstream demand engine.

---

### 2.4 Project Lifecycle Management

Projects progress through:

* Listed
* Funding Open
* Execution Started
* Completed

Each stage integrates:

* Contractors (Phase 2)
* Escrow + financing (Phase 3)

### 2.4.1 Minimum UI Expectations

* The project list must support browse, search, and filter.
* The project detail page must show linked contracts, requirements, milestones, documents, updates, funding state, and risk/issues.
* The project create form must not force the owner to define every operational detail up front.
* The owner dashboard must provide a direct route into project creation and project review.

### 2.4.2 Project Detail Layout

Project detail should be organized into clear sections or tabs rather than one long form.

Recommended sections:

* Summary
* Requirements
* Contracts
* Milestones
* Funding
* Documents
* Updates
* Risks / Issues
* Activity Log

The summary section should always come first and show:

* project status
* budget
* funding state
* linked contracts
* current blockers or issues

---

### 2.5 Global Expansion Features

Phase 4 requires:

* Multi-currency support
* Region-specific tax/VAT handling
* Cross-border supplier logistics integration
* Local compliance configuration

---

## 3. Phase 4 Exclusions

Not included until Phase 5+:

* Fully regulated investment marketplace
* Secondary markets
* Government procurement compliance

---

## 4. Phase 4 Success Metrics

* ≥ 50 active projects listed/month
* ≥ 20% projects funded or financed
* Increased contract volume via project pipeline
* Property listings feeding execution demand

---

**Phase 4 requirements are now defined.**
