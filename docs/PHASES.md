# 🏗️ Procus v2 — Platform Development Phases

> This document describes the six development phases that together comprise the full Procus v2 Construction Marketplace platform. Each phase builds on the previous, progressively deepening functionality, regulatory coverage, and intelligence.

---

## Phase Overview at a Glance

```
Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase 4 ──▶ Phase 5 ──▶ Phase 6
Materials   Contracts   Financial   Projects    Regulated   Intelligence
Liquidity   Execution   Infra       & Capital   Investment  & Scale
Engine      Layer       Layer       Pipeline    & Govt      Layer
  ✅            ✅          ✅          ✅           ✅          ✅
```

| Phase | Name | Theme | Status |
|---|---|---|---|
| **1** | Materials Liquidity Engine | Core Marketplace & Payments | ✅ Delivered |
| **2** | Contracts & Execution Layer | Contractor Registry & Bidding | ✅ Delivered |
| **3** | Financial Infrastructure | Escrow, Disputes & Embedded Finance | ✅ Delivered |
| **4** | Projects, Property & Capital | Project Lifecycle & Investment | ✅ Delivered |
| **5** | Regulated Investment & Government | KYC, Compliance & Public Procurement | ✅ Delivered |
| **6** | Full Regulatory Integration & AI | Banking, Reporting & Intelligence | ✅ Delivered |

---

## Phase 1 — Materials Liquidity Engine

> **Theme:** Establish the core marketplace for construction materials — connecting verified vendors with buyers.

### 🎯 Goals
- Create a functional B2B materials marketplace from the ground up
- Enable vendor onboarding, product discovery, and quote-to-order workflows
- Implement basic payment tracking and dispute handling
- Lay the identity and data foundations for all future phases

### 🧩 New Backend Modules
| Module | App | Responsibility |
|---|---|---|
| User Accounts | `accounts` | Authentication, role assignment, user profiles |
| Vendor Profiles | `accounts` | Verified vendor identities with performance metrics |
| Product Catalogue | `catalog` | Material listings with inventory, pricing, and availability |
| Orders | `orders` | Full order lifecycle from placement to delivery |
| Payments | `payments` | Payment transaction records (gateway-ready structure) |
| Disputes | `disputes` | Order conflict management and resolution tracking |
| Reviews | `reviews` | Buyer ratings and vendor reputation engine |
| Taxonomy | `taxonomy` | Category classification for products and services |

### 🔑 Key Data Models

```
User ──▶ VendorProfile ──▶ Product ──▶ Order ──▶ Payment
                                          │
                                          └──▶ Dispute
```

| Model | Key Fields |
|---|---|
| `User` | `email`, `role` (ADMIN, VENDOR, BUYER, CONTRACTOR…), `created_at` |
| `VendorProfile` | `company_name`, `verified_status`, `fulfillment_rate`, `average_rating` |
| `Product` | `name`, `base_price`, `unit_of_measure`, `stock_level`, `status` |
| `Order` | `buyer`, `vendor`, `status` (PLACED → DELIVERED → COMPLETED), `total_amount` |
| `Payment` | `provider` (MPESA/STRIPE), `status` (UNPAID → PAID), `transaction_reference` |
| `Dispute` | `order`, `status` (OPENED → RESOLVED_RELEASE/REFUND), `reason` |

### 🌐 Frontend Views
- `ProductList.vue` — Material catalogue with search & filters
- `ProductDetail.vue` — Product info, stock, and ordering
- `VendorDashboard.vue` — Vendor product and order management
- `BuyerDashboard.vue` — Order history and status tracking
- `Login.vue` / `Register.vue` — Authentication flows

### 🔗 API Endpoints (v1)
```
GET|POST   /api/products/
GET        /api/products/{id}/
GET|POST   /api/orders/
GET|POST   /api/payments/
GET|POST   /api/disputes/
GET|POST   /api/accounts/register/
POST       /api/token/
```

### ➡️ Sets the stage for
Phase 2 — who executes the *work* on the materials? → Contractors.

---

## Phase 2 — Contracts & Execution Layer

> **Theme:** Extend the platform from material procurement into construction services — introducing contractor onboarding, competitive bidding, and milestone-based job execution.

### 🎯 Goals
- Enable project owners to post construction tenders
- Allow contractors to discover, bid on, and win contracts
- Implement milestone-based execution and payment trigger workflow
- Build role-segmented dashboards for owners and contractors

### 🧩 New Backend Modules
| Module | App | Responsibility |
|---|---|---|
| Contractors | `contractors` | Company profiles, capability taxonomy, verification queue |
| Contracts | `contracts` | Tender posting, status workflow, contract lifecycle |
| Bids | `bids` | Bid submission, shortlisting, and award engine |
| Milestones | `milestones` | Execution checkpoints with approval-triggered payment |

### 🔑 Key Data Models

```
Contract (Tender) ◀──── Owner posts
     │
     └──▶ Bids (Contractor submits) ──▶ Award ──▶ Contract IN_PROGRESS
                                                        │
                                                        └──▶ Milestones ──▶ Approve ──▶ Pay
```

| Model | Key Fields |
|---|---|
| `Contractor` | `company_name`, `service_categories`, `is_verified`, `rating_avg` |
| `Contract` | `title`, `budget_min/max`, `status` (POSTED → AWARDED → COMPLETED) |
| `Bid` | `proposed_cost`, `proposed_timeline_days`, `status` (SUBMITTED → AWARDED) |
| `Milestone` | `title`, `amount`, `due_date`, `status` (PENDING → APPROVED → PAID) |

### 🌐 Frontend Views
- `ContractorRegistration.vue` — Contractor onboarding form
- `ViewTenders.vue` — Active tender discovery for contractors
- `ContractList.vue` — Full contract marketplace
- `ContractDetail.vue` — Bid submission, award, and milestone tracking
- `PostContract.vue` — Owner tender creation
- `ContractorDashboard.vue` — Active jobs and milestone tracking

### 🔗 API Endpoints (v2)
```
POST       /api/contractors/register/
GET|POST   /api/contracts/
POST       /api/contracts/{id}/bids/
POST       /api/bids/{id}/award/
POST       /api/contracts/{id}/milestones/
POST       /api/milestones/{id}/approve/
```

### ➡️ Sets the stage for
Phase 3 — milestones need *real* escrow-backed fund releases, not placeholders.

---

## Phase 3 — Financial Infrastructure Layer

> **Theme:** Replace payment placeholders with real escrow mechanics — creating a trustworthy financial backbone with dispute arbitration and embedded credit.

### 🎯 Goals
- Implement full escrow fund holding and release mechanics
- Automate fund release on milestone approval (atomic transactions)
- Build dispute resolution with escrow freeze capability
- Introduce embedded finance (credit/loan products)
- Lay the foundation for contractor reliability scoring

### 🧩 New Backend Modules
| Module | App | Responsibility |
|---|---|---|
| Escrow | `escrow` | Fund holding, ledger, milestone-triggered releases |
| Finance | `finance` | Loan products and credit applications |
| Scoring | `scoring` | Contractor reliability score (0–100) |

### 🔑 Key Data Models

```
Contract ──▶ EscrowAccount ──▶ EscrowTransaction (DEPOSIT / RELEASE / REFUND)
                  │
                  └──▶ EscrowRelease (triggered by Milestone Approval)
                  │
                  └──▶ EscrowHold (triggered by Dispute — freezes funds)
                              │
                              └── Admin resolves ──▶ Release or Refund
```

| Model | Key Fields |
|---|---|
| `EscrowAccount` | `contract`, `total_amount_held`, `currency`, `status` (ACTIVE/RELEASED) |
| `EscrowTransaction` | `type` (DEPOSIT/RELEASE/REFUND), `amount`, `milestone`, `payment_reference` |
| `EscrowRelease` | `milestone`, `approved_by`, `released_amount`, `release_status` |
| `EscrowHold` | `escrow_account`, `dispute`, `reason`, `status` |
| `FinanceProduct` | Credit product definitions |
| `FinanceApplication` | `status` (SUBMITTED → APPROVED → DISBURSED) |
| `ReliabilityScore` | `contractor`, `score` (0–100), `risk_tier` |

### 🔑 Key Workflows
1. **Escrow Funding** → Owner deposits funds against a contract
2. **Milestone Automation** → Approving a milestone atomically releases funds (if escrow active and not frozen)
3. **Dispute Freeze** → Filing a dispute creates an `EscrowHold`, blocking all releases
4. **Arbitration** → Admin resolves dispute, lifting the hold and executing Refund or Release

### 🔗 API Endpoints (v3)
```
POST       /api/escrow/deposit/
POST       /api/escrow-releases/trigger/
POST       /api/disputes/
POST       /api/disputes/{id}/evidence/
POST       /api/disputes/{id}/resolve/
GET        /api/finance/products/
POST       /api/finance/applications/
GET        /api/scoring/
```

### ➡️ Sets the stage for
Phase 4 — escrow-backed projects need *project-level* structure, not just contract-level.

---

## Phase 4 — Projects, Property & Capital Pipeline

> **Theme:** Introduce a connected property and project operating model where property remains a standalone marketplace domain while still linking into financing, procurement, execution, and capital flows.

### 🎯 Goals
- Create a top-level `Project` entity that aggregates all platform activities
- keep property as a standalone marketplace and operating asset module
- enable approved property managers to operate listings on behalf of owners
- allow public discovery, inquiries, and appointment booking for property assets
- Enable investors to discover and pledge capital to construction projects
- allow financing to target either a property or a project
- connect real estate/property listings to upstream project demand
- Provide project owners with a unified execution dashboard

### 🧩 New Backend Modules
| Module | App | Responsibility |
|---|---|---|
| Projects | `projects` | Project lifecycle, requirements, funding status, updates feed |
| Property | `property` | Standalone property listings, development metadata, inquiries, appointments, and project linkage |
| Investments | `investments` | Investor pledge and commitment workflow |

### 🔑 Key Data Models

```
PropertyListing ──▶ PropertyInquiry / Appointment
        │
        ├──▶ FinanceApplication (property-targeted)
        │
        └──▶ Project ──▶ Contract (execution)
                    │
                    ├──▶ ProjectRequirement (materials/services needed)
                    │
                    ├──▶ InvestmentCommitment (investor pledges)
                    │
                    └──▶ ProjectUpdate (progress feed)
```

| Model | Key Fields |
|---|---|
| `Project` | `title`, `location`, `estimated_budget`, `funding_required`, `status` (LISTED → FUNDING_OPEN → EXECUTION_STARTED → COMPLETED) |
| `ProjectRequirement` | `type` (MATERIAL/CONTRACTOR/SERVICE), `description`, `quantity` |
| `InvestmentCommitment` | `investor`, `amount_committed`, `status` (PLEDGED → CONFIRMED) |
| `ProjectContractLink` | Connects `Project` ↔ `Contract` |
| `PropertyListing` | `asset_type`, `listing_type`, `price_estimate`, `status`, `financing_allowed` |
| `DevelopmentMetadata` | `zoning_info`, `build_ready`, `utilities_available` |
| `PropertyInquiry` | lead capture, callback details, chat linkage |
| `PropertyAppointment` | calendar booking with owner/manager-defined availability |
| `PropertyProjectLink` | Connects `Property` ↔ `Project` |

### 🌐 Frontend Views
- `ProjectList.vue` — Project marketplace and investment discovery
- `ProjectDetail.vue` — Full project view with requirements, investment, and updates
- `CreateProject.vue` — Owner project creation flow
- `PropertyListing.vue` — Property discovery and filtering
- `PropertyDetail.vue` — Property hub for inquiries, appointments, financing, linked project context, and suggested materials/services
- `InvestorDashboard.vue` — Portfolio and pledge management
- `PropertyManagerDashboard.vue` — Listing operations, inquiries, appointments, and availability management
- `OwnerDashboard.vue` — Multi-project management

### 🔗 API Endpoints (v4 foundation)
```
GET|POST   /api/projects/
POST       /api/projects/{id}/requirements/
POST       /api/projects/{id}/commit/
POST       /api/projects/{id}/link-contract/
POST       /api/projects/{id}/updates/
GET|POST   /api/property/
POST       /api/property/{id}/link-project/
```

Target property workflow additions build on this foundation with inquiry, appointment, availability, and finance-entry surfaces.

### ➡️ Sets the stage for
Phase 5 — investment must become *regulated* — KYC, legal agreements, government tendering.

---

## Phase 5 — Regulated Investment, Enterprise & Government Layer

> **Theme:** Transform the platform into a fully regulated environment — handling KYC/AML compliance, binding legal investment agreements, enterprise procurement workflows, and government public tenders.

### 🎯 Goals
- Implement KYC (Know Your Customer) for investor onboarding
- Enforce legally-binding investment agreements and accreditation status
- Enable government agencies to post public infrastructure tenders
- Support enterprise-grade approval workflows and supplier SLA tracking
- Implement jurisdiction-aware compliance rules (VAT, currency, data)

### 🧩 New Backend Modules
| Module | App | Responsibility |
|---|---|---|
| Regulation | `regulation` | Investor KYC, accreditation, investment agreements, reporting |
| Enterprise | `enterprise` | Organisations, approval workflows, supplier SLA tracking |
| Government | `government` | Public tender lifecycle, immutable audit logs |
| Compliance | `compliance` | KYC document upload, jurisdiction rules engine |
| Risk | `risk` | Risk scoring engine, compliance alerts |

### 🔑 Key Data Models

| Model | Key Fields |
|---|---|
| `InvestorProfile` | `kyc_status` (PENDING/VERIFIED/REJECTED), `accreditation_status`, `jurisdiction` |
| `InvestmentAgreement` | `agreement_terms_url`, `status` (SIGNED → FUNDED → CANCELLED), `signed_at` |
| `InvestorReport` | `report_period`, `performance_summary` |
| `Organization` | Enterprise account entity |
| `ApprovalWorkflow` | Multi-step enterprise approval chain |
| `SupplierPerformance` | SLA tracking for enterprise suppliers |
| `PublicTender` | Government procurement lifecycle |
| `AuditLog` | Immutable government-grade audit trail |
| `KYCVerification` | Identity document uploads and verification status |
| `JurisdictionRule` | VAT/currency/data rules by jurisdiction |
| `RiskScore` | Composite risk score per entity |
| `ComplianceAlert` | Triggered on rule violations |

### 🌐 Frontend Views
- `ViewTenders.vue` — Public government infrastructure tenders
- `InvestorDashboard.vue` — KYC status, agree to terms, sign binding documents

### 🔗 API Endpoints (v5)
```
POST       /api/investors/onboard/
POST       /api/agreements/{id}/sign/
GET        /api/tenders/
POST       /api/kyc/upload-doc/
POST       /api/organizations/
GET        /api/risk/
GET        /api/compliance/alerts/
```

### ➡️ Sets the stage for
Phase 6 — regulated capital needs real *banking rails*, *AI-driven risk*, and *ERP integrations*.

---

## Phase 6 — Full Regulatory Integration & Advanced Intelligence

> **Theme:** The final phase transforms Procus v2 from a marketplace into institutional-grade financial infrastructure — with real banking settlement, AI-driven risk prediction, a regulated secondary market, and ERP integration.

### 🎯 Goals
- Implement licensed banking settlement for money movement
- Automate regulatory reporting (AML/SAR/Tax filings)
- Deploy AI/ML models for default prediction and underwriting
- Launch a regulated secondary market for project stakes
- Provide ERP connectors (SAP/Oracle scaffolding)

### 🧩 New Backend Modules
| Module | App | Responsibility |
|---|---|---|
| Banking | `banking` | Bank accounts, settlement transactions, licensed money movement |
| Reporting | `reporting` | Regulatory reports, tax filings, AML logs |
| AI Engine | `ai_engine` | Predictive models, underwriting, fraud detection |
| Liquidity | `liquidity` | Secondary market for stakes, trade execution |
| Integrations | `integrations` | ERP connectors, external system sync |

### 🔑 Key Data Models

| Model | Key Fields |
|---|---|
| `BankAccount` | Registered bank account for settlement |
| `SettlementTransaction` | Escrow-backed licensed money movement |
| `RegulatoryReport` | Type (AML/SAR/TAX), report period, filing status |
| `TaxFiling` | Automated tax compliance records |
| `PredictiveModel` | Trained ML model registry |
| `UnderwritingPrediction` | Real-time default risk score per entity |
| `SecondaryTrade` | Buy/sell orders for project investment stakes |
| `StakeTransfer` | Ownership transfer record on secondary market |
| `ERPConnector` | SAP/Oracle integration configuration |
| `ExternalSystemSync` | Data synchronisation event log |

### 🌐 Frontend Views
- `RegulatoryReports.vue` — Admin compliance downloads (AML/SAR/Tax)
- `SecondaryMarket.vue` — Secondary market listings — buy/sell project stakes

### 🔗 API Endpoints (v6)
```
GET        /api/regulatory-reports/
POST       /api/ai-predictions/predict-default/
GET        /api/secondary-trades/
POST       /api/settlements/
POST       /api/erp-connectors/
```

### 🏁 Final Platform Status
After Phase 6, the platform is a **fully integrated, regulated, AI-enhanced construction industry OS** capable of:

| Capability | Phases |
|---|---|
| End-to-end project lifecycle (materials → contracts → milestones) | 1–4 |
| Escrow-backed financial trust layer | 3 |
| Investor onboarding and capital mobilisation | 4–5 |
| Full KYC/AML/compliance coverage | 5 |
| Government procurement integration | 5 |
| Licensed banking and settlement rails | 6 |
| AI-driven default prediction and underwriting | 6 |
| Regulated secondary market for construction finance | 6 |
| Enterprise ERP integration scaffolding | 6 |

---

## Cumulative Module Map

The diagram below shows how all apps were introduced across phases:

```
PHASE 1   accounts · catalog · orders · payments · disputes · reviews · taxonomy
    │
PHASE 2   + contractors · contracts · bids · milestones
    │
PHASE 3   + escrow · finance · scoring
    │
PHASE 4   + projects · property · investments
    │
PHASE 5   + regulation · enterprise · government · compliance · risk
    │
PHASE 6   + banking · reporting · ai_engine · liquidity · integrations
    │
    └──▶  28 backend apps  |  20 frontend views  |  6 API versions
```

---

## Database Schema Reference

For the full consolidated database schema (all models across all phases), see:

- [`consolidated_schema.md`](../consolidated_schema.md) — concise field-level model reference
- [`consolidated_schema_enhanced.md`](../consolidated_schema_enhanced.md) — enhanced schema with relationships
- Phase-specific schemas: `phase1_schema.md` through `phase6_schema.md`

---

*Procus v2 · © 2026 · All rights reserved*
