# Software Requirements Specification (SRS)

## Procus v2 — Construction Marketplace Platform

| Field | Value |
|---|---|
| **Document Version** | 2.0 |
| **Status** | Approved |
| **Date** | 21 February 2026 |
| **Prepared by** | Engineering Team |
| **Repository** | https://github.com/nelsonadagi/procusv2 |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Stakeholders & User Classes](#3-stakeholders--user-classes)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [System Constraints](#6-system-constraints)
7. [External Interface Requirements](#7-external-interface-requirements)
8. [Data Requirements](#8-data-requirements)
9. [Security Requirements](#9-security-requirements)
10. [Compliance & Regulatory Requirements](#10-compliance--regulatory-requirements)
11. [Appendix — Glossary](#11-appendix--glossary)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for **Procus v2**, a comprehensive, multi-role construction industry marketplace platform. The document serves as the contractual reference between stakeholders, business analysts, and the engineering team throughout the development lifecycle.

### 1.2 Product Scope

Procus v2 is a web-based B2B and B2C platform that manages the full lifecycle of construction projects — from raw material procurement, through contractor tendering, contract execution, milestone-based escrow payments, all the way to regulatory reporting and secondary investment markets.

The system is designed to serve **six primary user roles** operating across a single, multi-tenanted platform backed by a RESTful API and a Vue 3 single-page application.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|---|---|
| **SRS** | Software Requirements Specification |
| **SDD** | Software Design Document |
| **SPA** | Single-Page Application |
| **DRF** | Django REST Framework |
| **RBAC** | Role-Based Access Control |
| **KYC** | Know Your Customer — identity verification process |
| **AML** | Anti-Money Laundering |
| **SAR** | Suspicious Activity Report |
| **ERP** | Enterprise Resource Planning |
| **SLA** | Service Level Agreement |
| **BoQ** | Bill of Quantities |
| **MVP** | Minimum Viable Product |
| **JWT** | JSON Web Token |
| **API** | Application Programming Interface |
| **CORS** | Cross-Origin Resource Sharing |

### 1.4 References

- `docs/PHASES.md` — Platform development phase descriptions
- `consolidated_schema.md` — Database schema reference
- `docker-compose.yml` — Infrastructure configuration
- `backend/requirements.txt` — Python dependencies
- `frontend/package.json` — Node.js dependencies
- `frontend/FRONTEND_STYLE_GUIDE.md` — UI design system reference

### 1.5 Document Overview

Section 2 provides a high-level system overview. Section 3 identifies stakeholders. Section 4 details all functional requirements, grouped by user role and domain. Section 5 covers non-functional requirements. Sections 6–10 address constraints, interfaces, data, security, and compliance.

---

## 2. Overall Description

### 2.1 Product Perspective

Procus v2 is a standalone, full-stack web application. It is not a replacement or module of any existing system but operates as an independent platform. It communicates with external payment gateways (M-Pesa, Stripe), ERP systems (SAP, Oracle), and identity verification services (SumSub, Onfido) via adapters.

```
External World
│
├── Payment Gateways (M-Pesa, Stripe)
├── KYC Providers (SumSub / Onfido)
├── ERP Systems (SAP / Oracle)
│
▼
┌──────────────────────────────────┐
│           Procus v2               │
│  Vue 3 SPA ◄──► Django REST API  │
│         PostgreSQL + Redis        │
└──────────────────────────────────┘
```

### 2.2 Product Functions (Summary)

| Domain | Core Functions |
|---|---|
| **Identity & Access** | Registration, authentication (JWT), RBAC, KYC verification |
| **Materials Commerce** | Vendor listings, product catalogue, quote-to-order, inventory management |
| **Contractor Services** | Contractor onboarding, verification, tender discovery, bidding |
| **Contract Lifecycle** | Tender posting, bid evaluation, contract award, milestone tracking |
| **Financial Layer** | Escrow fund management, milestone-triggered releases, dispute arbitration |
| **Project Management** | Project creation, BoQ, updates feed, cross-module linkages |
| **Investment** | Investor KYC, pledge workflow, binding agreements, secondary market |
| **Compliance** | KYC/AML checks, jurisdiction rules, risk scoring, audit log |
| **Government** | Public procurement tendering, immutable audit trail |
| **Intelligence** | AI risk prediction, underwriting automation |
| **Banking & Reporting** | Bank settlement, regulatory reports, tax filings |
| **Administration** | Platform config, user management, roles, countries, master data |

### 2.3 User Characteristics

The platform serves a mixed user base ranging from non-technical buyers and contractors to compliance officers and system administrators. The UI must be accessible to users with minimal technical background while providing advanced controls for power users.

### 2.4 Assumptions and Dependencies

1. Users have access to a modern web browser (Chrome 120+, Firefox 120+, Safari 17+, Edge 120+).
2. Internet connectivity is available; the platform does not support offline operation.
3. Payment integrations (M-Pesa, Stripe) require valid API credentials configured in the environment.
4. Email notifications depend on a configured SMTP provider.
5. The AI engine requires a trained predictive model loaded at startup.
6. PostgreSQL 15 and Redis 7 are required infrastructure components.

---

## 3. Stakeholders & User Classes

### 3.1 User Roles

| Role | Description | Primary Actions |
|---|---|---|
| **Admin** | Platform superuser with full system access | Manage users, settings, verifications, compliance, reporting |
| **Vendor** | Company supplying construction materials | List products, manage inventory, process orders |
| **Buyer** | Individual or company purchasing materials | Browse catalogue, place orders, track deliveries, raise disputes |
| **Contractor** | Licensed construction service provider | Register capabilities, bid on tenders, execute milestones |
| **Project Owner** | Individual or company commissioning construction | Create projects, post tenders, award contracts, release payments |
| **Investor** | Financial entity funding projects | Complete KYC, pledge capital, sign agreements, trade stakes |
| **Staff** | Internal platform operators | Support functions, compliance monitoring |

### 3.2 External Actors

| Actor | Interaction |
|---|---|
| **Payment Gateways** | Fund collection, settlement, refunds |
| **KYC Providers** | Identity document verification |
| **ERP Systems** | Enterprise procurement data sync |
| **Government Agencies** | Public tender management |

---

## 4. Functional Requirements

Requirements are identified with unique IDs in the format `FR-[DOMAIN]-[NUMBER]`.

---

### 4.1 Authentication & Identity Management

#### FR-AUTH-001 — User Registration
The system SHALL allow new users to register with an email address, password, first name, last name, and a selected role (VENDOR, BUYER, CONTRACTOR, PROJECT_OWNER, INVESTOR).

#### FR-AUTH-002 — JWT Authentication
The system SHALL issue a JSON Web Token (access + refresh) upon successful login. Access tokens SHALL expire after a configurable duration. Refresh tokens SHALL allow silent renewal.

#### FR-AUTH-003 — Role Assignment
Each user SHALL be assigned exactly one primary role. The Admin MAY reassign roles via the Admin Console. Role changes SHALL be recorded in the audit log.

#### FR-AUTH-004 — Password Security
Passwords SHALL be hashed using Django's default PBKDF2-SHA256 algorithm with a minimum length of 8 characters.

#### FR-AUTH-005 — Account Deactivation
Admins SHALL be able to deactivate any user account. Deactivated users SHALL be denied API access. The system SHALL NOT delete user records.

---

### 4.2 Materials Catalogue (Phase 1)

#### FR-CAT-001 — Product Listing
Vendors SHALL be able to create product listings containing: name, description, category, base price, unit of measure, minimum order quantity, stock level, delivery regions, and status.

#### FR-CAT-002 — Product Status Management
Products SHALL have statuses: `ACTIVE`, `INACTIVE`, `OUT_OF_STOCK`. Vendors SHALL be able to update product status.

#### FR-CAT-003 — Product Discovery
Buyers SHALL be able to browse and search the product catalogue. Search SHALL support filtering by category, price range, vendor, delivery region, and availability.

#### FR-CAT-004 — Inventory Tracking
The system SHALL decrement `stock_level` when an order is placed. The system SHALL automatically mark a product `OUT_OF_STOCK` when `stock_level` reaches zero.

#### FR-CAT-005 — Product Categories
Products SHALL be categorised using a hierarchical taxonomy (parent/child categories). Categories SHALL be managed by Admins.

---

### 4.3 Orders & Payments (Phase 1)

#### FR-ORD-001 — Order Placement
Buyers SHALL be able to place orders against one or more products from a single vendor. The system SHALL capture ordered quantity, unit price, and delivery address.

#### FR-ORD-002 — Order Lifecycle
Orders SHALL progress through statuses: `PLACED → CONFIRMED → PACKING → SHIPPED → DELIVERED → COMPLETED`. Vendors SHALL update status. Status regression SHALL NOT be permitted.

#### FR-ORD-003 — Payment Recording
Each order SHALL have an associated payment record capturing: provider (M-PESA, STRIPE), amount, status, and transaction reference.

#### FR-ORD-004 — Vendor Performance Metrics
The system SHALL automatically update vendor `fulfillment_rate`, `cancellation_rate`, and `delivery_timeliness` metrics after each order completion.

---

### 4.4 Disputes & Reviews (Phase 1)

#### FR-DISP-001 — Dispute Filing
Buyers OR Vendors SHALL be able to open a dispute on any non-completed order by providing a reason.

#### FR-DISP-002 — Dispute Workflow
Disputes SHALL follow the workflow: `OPENED → UNDER_REVIEW → RESOLVED_RELEASE | RESOLVED_REFUND | CLOSED`. Only Admins SHALL move disputes to a resolved state.

#### FR-REV-001 — Contractor & Vendor Reviews
After order/contract completion, the counterparty SHALL be able to submit a rating (1–5 stars) and optional comment. The system SHALL update the entity's `average_rating` automatically.

---

### 4.5 Contractor Registry (Phase 2)

#### FR-CON-001 — Contractor Registration
Contractors SHALL submit a registration form including: company name, service categories, operating region, and supporting documents (certifications).

#### FR-CON-002 — Contractor Verification Queue
Pending contractor registrations SHALL appear in the Admin verification queue. Admins SHALL be able to approve or reject registrations. Approved contractors SHALL receive a `is_verified = true` flag.

#### FR-CON-003 — Capability Classification
Contractor service capabilities SHALL be classified using the platform's taxonomy (e.g., CONTRACTOR taxonomy type).

---

### 4.6 Contracts & Bidding (Phase 2)

#### FR-BID-001 — Tender Posting
Project Owners SHALL be able to post tenders containing: title, scope of work, location, budget range (min/max), and required timeline.

#### FR-BID-002 — Tender Discovery
Verified Contractors SHALL be able to browse active tenders filtered by location, category, and budget.

#### FR-BID-003 — Bid Submission
Contractors SHALL submit bids containing: proposed cost, proposed timeline in days, and a message to the owner. Each contractor SHALL submit at most one bid per contract.

#### FR-BID-004 — Bid Evaluation
Project Owners SHALL view all received bids on their contract. Owners MAY shortlist bids and SHALL award exactly one bid per contract.

#### FR-BID-005 — Contract Award
Awarding a bid SHALL update the contract status to `AWARDED` and the winning bid status to `AWARDED`. All other bids SHALL be marked `REJECTED`.

#### FR-BID-006 — Milestone Definition
After contract award, the Project Owner SHALL define milestones (title, description, amount, due date) for the contract.

#### FR-BID-007 — Milestone Approval
Project Owners SHALL approve completed milestones. Approval SHALL trigger fund release from escrow (if funded).

---

### 4.7 Escrow & Financial Layer (Phase 3)

#### FR-ESC-001 — Escrow Account Creation
Upon contract award, the system SHALL create an associated EscrowAccount to hold funds for that contract.

#### FR-ESC-002 — Escrow Deposit
Project Owners SHALL deposit funds into the EscrowAccount. Depositing SHALL create an `EscrowTransaction` of type `DEPOSIT`.

#### FR-ESC-003 — Milestone-Triggered Release
When a milestone is approved, the system SHALL atomically: (a) check the EscrowAccount is ACTIVE and un-frozen, (b) deduct the milestone amount, (c) create an `EscrowTransaction` of type `RELEASE`, and (d) create an `EscrowRelease` record.

#### FR-ESC-004 — Dispute Freeze
Opening a dispute related to a contract SHALL create an `EscrowHold` record, setting the associated EscrowAccount to a frozen state. No releases SHALL be permitted while frozen.

#### FR-ESC-005 — Dispute Resolution
Admin dispute resolution SHALL: (a) lift the `EscrowHold`, and (b) execute either a `RELEASE` (to contractor) or `REFUND` (to owner) transaction.

#### FR-FIN-001 — Finance Products
The system SHALL maintain a catalogue of finance/credit products available to eligible users.

#### FR-FIN-002 — Finance Applications
Users SHALL be able to apply for finance products. Applications SHALL progress through `SUBMITTED → APPROVED → DISBURSED`.

#### FR-SCO-001 — Reliability Scoring
The system SHALL compute and maintain a `ReliabilityScore` (0–100) for contractors based on milestone completion, dispute history, and review ratings.

---

### 4.8 Projects, Property & Investment (Phase 4)

#### FR-PRJ-001 — Project Creation
Project Owners SHALL create projects containing: title, description, location, estimated budget, and funding requirement flag.

#### FR-PRJ-002 — Bill of Quantities
Project Owners SHALL add requirements to a project, each specifying type (MATERIAL, CONTRACTOR, SERVICE), description, and quantity.

#### FR-PRJ-003 — Project Status Lifecycle
Projects SHALL progress through: `LISTED → FUNDING_OPEN → EXECUTION_STARTED → COMPLETED`.

#### FR-PRJ-004 — Project-Contract Linkage
Project Owners SHALL link awarded contracts to a project, enabling unified execution tracking.

#### FR-PRJ-005 — Project Updates Feed
Project Owners SHALL post text updates to a project's progress feed, visible to linked investors.

#### FR-INV-001 — Investment Pledge
Investors SHALL be able to commit a specified amount to a project in `FUNDING_OPEN` status. Pledges SHALL have status `PLEDGED → CONFIRMED → CANCELLED`.

#### FR-PROP-001 — Property Listing
Users SHALL be able to list real estate assets with: title, description, location, asset type (LAND, RESIDENTIAL, COMMERCIAL, RENOVATION), and price estimate.

#### FR-PROP-002 — Property-Project Linkage
Property listings SHALL be linkable to a project to represent upstream demand generation.

---

### 4.9 Regulated Investment & Government (Phase 5)

#### FR-KYC-001 — Investor KYC Onboarding
Investors SHALL complete a KYC onboarding process: uploading identity documents and providing jurisdiction information. KYC status SHALL be `PENDING → VERIFIED → REJECTED`.

#### FR-KYC-002 — Accreditation
The system SHALL record investor accreditation status. Only accredited investors SHALL access certain high-value investment instruments.

#### FR-AGR-001 — Investment Agreement
Investors SHALL sign a legally binding investment agreement (stored as a document URL) before capital is committed. Agreement status: `SIGNED → FUNDED → CANCELLED`.

#### FR-COMP-001 — Jurisdiction Rules
The system SHALL enforce jurisdiction-specific rules including applicable VAT rate, permitted currencies, and data residency constraints.

#### FR-COMP-002 — Compliance Alerts
The system SHALL generate `ComplianceAlert` records when a transaction or entity violates a `JurisdictionRule`.

#### FR-ENT-001 — Enterprise Accounts
Enterprise users SHALL create Organisations within the platform. Organisations SHALL have configurable multi-step `ApprovalWorkflow` for procurement actions.

#### FR-GOV-001 — Public Tender Listing
Government agencies SHALL publish public tenders. Public tenders SHALL be visible to all verified contractors.

#### FR-GOV-002 — Immutable Audit Log (Government)
All government procurement actions SHALL be recorded in an immutable `AuditLog`. Records SHALL NOT be modifiable after creation.

#### FR-RISK-001 — Risk Scoring
The system SHALL compute a `RiskScore` for entities (contractors, investors) based on configurable risk parameters.

---

### 4.10 Banking, Reporting & Intelligence (Phase 6)

#### FR-BANK-001 — Bank Account Registration
Users SHALL register bank accounts (account number, sort code, bank name) for settlement purposes.

#### FR-BANK-002 — Settlement Transactions
The system SHALL execute escrow-backed bank settlement transactions, creating `SettlementTransaction` records tied to `BankAccount` entries.

#### FR-REP-001 — Regulatory Reports
The system SHALL auto-generate regulatory compliance reports (AML, SAR, Tax) on a scheduled basis. Reports SHALL be downloadable by Admins.

#### FR-REP-002 — Tax Filings
The system SHALL maintain `TaxFiling` records per jurisdiction, linked to transaction data.

#### FR-AI-001 — Default Prediction
The AI Engine SHALL accept a request containing entity and transaction features and return a real-time default prediction probability (0.0–1.0).

#### FR-AI-002 — Underwriting Automation
The system SHALL use the AI Engine's predictions to auto-approve or flag finance applications for manual review.

#### FR-LIQ-001 — Secondary Market Listings
Investors SHALL list their confirmed investment stakes for sale on the secondary market.

#### FR-LIQ-002 — Secondary Trade Execution
Other investors SHALL be able to purchase listed stakes. Trade execution SHALL atomically transfer stake ownership and update investment records.

#### FR-INT-001 — ERP Integration
The system SHALL expose an ERP connector configuration interface supporting SAP and Oracle schemas. Sync events SHALL be logged in `ExternalSystemSync`.

---

### 4.11 Platform Administration

#### FR-ADM-001 — Platform Identity Configuration
Admins SHALL configure: platform name, tagline, support email, support phone, website URL, physical address, default region code, and brand colours.

#### FR-ADM-002 — Currency Management
Admins SHALL add, enable/disable, and set exchange rates for supported currencies relative to the platform default (KES).

#### FR-ADM-003 — Country Management
Admins SHALL configure active countries including: ISO code, name, flag emoji, phone prefix, default currency, and active/default status.

#### FR-ADM-004 — Role (Group) Management
Admins SHALL create and delete Django permission groups used as platform roles. Admins SHALL assign groups to users.

#### FR-ADM-005 — Taxonomy Category Management
Admins SHALL create, enable/disable, and delete taxonomy categories classified by type (MATERIAL, SERVICE, PROJECT, PROPERTY, FINANCE, GOVERNMENT, COMPLIANCE).

#### FR-ADM-006 — Audit Log Stream
Admins SHALL view a real-time, paginated stream of all system actions logged by the RBAC audit layer, including actor, action, resource type, and timestamp.

#### FR-ADM-007 — Contractor Verification
Admins SHALL see a queue of pending contractor registrations and SHALL approve or reject them individually.

---

## 5. Non-Functional Requirements

### 5.1 Performance

| ID | Requirement |
|---|---|
| NFR-PERF-001 | API endpoints SHALL return responses within **500ms** at p95 under normal load |
| NFR-PERF-002 | The system SHALL support at least **500 concurrent users** without degradation |
| NFR-PERF-003 | Page load time (SPA initial load) SHALL be under **3 seconds** on a 10 Mbps connection |
| NFR-PERF-004 | Database queries SHALL be optimised with appropriate indexes; ORM N+1 queries SHALL be eliminated via `select_related` / `prefetch_related` |
| NFR-PERF-005 | Celery async tasks (e.g. email, reports) SHALL not block the request-response cycle |

### 5.2 Scalability

| ID | Requirement |
|---|---|
| NFR-SCAL-001 | The backend SHALL be stateless and horizontally scalable (multiple Django workers) |
| NFR-SCAL-002 | The database connection pool SHALL be configurable to support load balancing |
| NFR-SCAL-003 | Redis SHALL be used as a distributed cache to reduce database read pressure |
| NFR-SCAL-004 | The Celery task queue SHALL support multiple workers for async job parallelism |

### 5.3 Availability & Reliability

| ID | Requirement |
|---|---|
| NFR-AVAIL-001 | The system SHALL target **99.5% uptime** measured monthly |
| NFR-AVAIL-002 | The PostgreSQL database SHALL have automated daily backups with a 30-day retention period |
| NFR-AVAIL-003 | All financial transactions (escrow, settlement) SHALL be **atomic** — partial commits SHALL be rolled back |
| NFR-AVAIL-004 | The system SHALL implement health-check endpoints for all services (`/health/`) |

### 5.4 Usability

| ID | Requirement |
|---|---|
| NFR-USE-001 | The SPA SHALL be fully responsive across screen widths from 320px (mobile) to 1920px (desktop) |
| NFR-USE-002 | All interactive elements SHALL have unique, descriptive IDs for accessibility and automated testing |
| NFR-USE-003 | Error messages SHALL be user-friendly and actionable (not raw stack traces) |
| NFR-USE-004 | Forms SHALL provide inline validation feedback |
| NFR-USE-005 | Loading states SHALL be indicated with visual feedback on all async operations |

### 5.5 Maintainability

| ID | Requirement |
|---|---|
| NFR-MAINT-001 | Backend code SHALL follow PEP 8 Python style conventions |
| NFR-MAINT-002 | Frontend components SHALL use `<script setup>` SFCs and `<style scoped>` |
| NFR-MAINT-003 | All Django apps SHALL be independently testable with unit tests |
| NFR-MAINT-004 | API versioning SHALL be maintained (`/api/v1/` through `/api/v6/`) to ensure backward compatibility |
| NFR-MAINT-005 | Environment-specific configuration SHALL live exclusively in `.env` files (no hardcoded secrets) |

### 5.6 Portability

| ID | Requirement |
|---|---|
| NFR-PORT-001 | The application SHALL be fully containerised using Docker and deployable via `docker-compose up --build` |
| NFR-PORT-002 | The system SHALL run on any Linux-based container host (Ubuntu 22.04+, Alpine) |

---

## 6. System Constraints

| ID | Constraint |
|---|---|
| CON-001 | The backend MUST use Django 5.2 and Django REST Framework 3.16 |
| CON-002 | The frontend MUST use Vue 3 with Vite as the build tool |
| CON-003 | The primary database MUST be PostgreSQL 15 |
| CON-004 | The message broker MUST be Redis 7 |
| CON-005 | The task queue MUST be Celery 5.6 |
| CON-006 | Styling MUST use a custom Vanilla CSS design system — no utility frameworks (Tailwind/Bootstrap) |
| CON-007 | Authentication MUST use JWT tokens; session-based auth is NOT permitted on the API |
| CON-008 | All financial operations MUST be wrapped in database transactions to ensure atomicity |
| CON-009 | `.env` files MUST NOT be committed to the repository (enforced via `.gitignore`) |

---

## 7. External Interface Requirements

### 7.1 User Interface

- Delivered as a Vue 3 SPA served by Vite dev server (port 5173) or a production static host.
- Uses a custom Vanilla CSS design system with CSS custom properties (design tokens).
- Responsive design: mobile-first, breakpoints at 768px and 1024px.
- No third-party CSS frameworks.

### 7.2 API Interface

- RESTful JSON API served by Django REST Framework (port 8000).
- Base URL: `/api/`
- Versioning: `/api/v1/` through `/api/v6/` (namespace-based).
- Authentication: `Authorization: Bearer <access_token>` header on all protected endpoints.
- Pagination: All list endpoints return `{ "count": N, "results": [...] }`.
- Error format: `{ "detail": "message" }` or `{ "field": ["error"] }`.

### 7.3 Payment Gateway Interface

| Gateway | Integration Type | Use Case |
|---|---|---|
| M-Pesa | REST API (Daraja 2.0) | Mobile money collection and disbursement |
| Stripe | REST API + Webhooks | Card-based payments and payouts |

### 7.4 KYC Provider Interface

| Provider | Integration Type | Use Case |
|---|---|---|
| SumSub | REST API + Webhook | Investor identity document verification and AML screening |
| Onfido | REST API + Webhook | Fallback identity verification |

### 7.5 ERP Interface

| System | Integration Type | Use Case |
|---|---|---|
| SAP | REST / SOAP adapter | Enterprise procurement data sync |
| Oracle | REST adapter | Enterprise supplier and PO data sync |

### 7.6 Database Interface

- ORM: Django ORM (abstraction over PostgreSQL).
- Connection: `dj-database-url` via `DATABASE_URL` environment variable.
- Connection pooling: Configurable via Django's `CONN_MAX_AGE`.

### 7.7 Cache / Message Broker Interface

- Redis accessed via `django-redis` for caching and `Celery` for async task brokering.
- Connection via `REDIS_URL` environment variable.

---

## 8. Data Requirements

### 8.1 Data Retention

| Data Type | Retention Period |
|---|---|
| User accounts | Indefinite (soft delete only) |
| Transaction records (Orders, Payments, Escrow) | Minimum 7 years (financial compliance) |
| Audit logs | Minimum 5 years |
| Government procurement audit logs | Immutable — permanent |
| Regulatory reports (AML/SAR/Tax) | Minimum 7 years |
| Dispute records | Minimum 5 years |

### 8.2 Data Integrity

- All ForeignKey relationships SHALL use `on_delete=PROTECT` for financial records to prevent orphaned transactions.
- All monetary amounts SHALL use `DecimalField` with precision `(15, 2)`.
- UUIDs SHALL be used as primary keys across all financial models.
- `created_at` and `updated_at` timestamps SHALL be present on all models.

### 8.3 Data Privacy

- Passwords SHALL never be stored in plaintext.
- PII (Personally Identifiable Information) fields SHALL be encrypted at rest where required by jurisdiction.
- The system SHALL support data export and deletion requests per GDPR Article 17 and equivalent local regulations.

---

## 9. Security Requirements

| ID | Requirement |
|---|---|
| SEC-001 | All API endpoints SHALL be protected by JWT authentication unless explicitly marked public |
| SEC-002 | RBAC SHALL enforce that users can only access resources appropriate to their role |
| SEC-003 | CORS SHALL be configured to allow only whitelisted origins in production |
| SEC-004 | The `DJANGO_SECRET_KEY` SHALL be at least 50 characters, randomly generated, and stored in `.env` |
| SEC-005 | `DEBUG` SHALL be set to `False` in production deployments |
| SEC-006 | `ALLOWED_HOSTS` SHALL list only valid production domain(s) — wildcards are forbidden in production |
| SEC-007 | All HTTP traffic SHALL be redirected to HTTPS in production |
| SEC-008 | SQL injection SHALL be prevented via Django ORM parameterised queries (raw SQL is forbidden unless explicitly reviewed) |
| SEC-009 | File uploads (KYC documents, evidence) SHALL be validated for type and size before storage |
| SEC-010 | Sensitive actions (role changes, account deactivation, escrow operations) SHALL be recorded in the RBAC audit log |
| SEC-011 | Rate limiting SHALL be applied to authentication endpoints to mitigate brute-force attacks |
| SEC-012 | Payment webhook endpoints SHALL validate provider signatures before processing |

---

## 10. Compliance & Regulatory Requirements

| ID | Requirement |
|---|---|
| COMP-001 | Investor onboarding SHALL comply with KYC/AML requirements in the investor's jurisdiction |
| COMP-002 | Investment agreements SHALL be legally binding and stored as auditable documents |
| COMP-003 | Government procurement records SHALL maintain an immutable, tamper-evident audit trail |
| COMP-004 | The platform SHALL generate AML Suspicious Activity Reports (SARs) for transactions exceeding configurable thresholds |
| COMP-005 | Tax filings SHALL be computed and stored per applicable jurisdiction tax rules |
| COMP-006 | Data residency rules defined in `JurisdictionRule` SHALL be enforced for data storage decisions |
| COMP-007 | Accreditation status SHALL be verified before allowing access to regulated investment instruments |
| COMP-008 | The platform SHALL maintain a complete, paginated audit log of all user and system actions |

---

## 11. Appendix — Glossary

| Term | Definition |
|---|---|
| **Tender** | A public invitation for contractors to submit bids for construction work |
| **Bid** | A contractor's proposal (cost + timeline) in response to a tender |
| **Milestone** | A defined checkpoint in contract execution linked to a payment amount |
| **Escrow** | Funds held by a neutral third party (the platform) until conditions are met |
| **EscrowHold** | A freeze on escrow funds triggered by an open dispute |
| **Stake** | An investor's ownership share in a funded construction project |
| **Secondary Market** | A marketplace where investors can buy and sell project stakes |
| **BoQ** | Bill of Quantities — a detailed list of materials and services required for a project |
| **KYC** | Know Your Customer — the regulatory process of verifying investor identity |
| **AML** | Anti-Money Laundering — detection and prevention of financial crime |
| **SAR** | Suspicious Activity Report — a mandatory report filed with regulators |
| **Taxonomy** | A hierarchical classification system for products, services, projects, etc. |
| **RBAC** | Role-Based Access Control — permission management tied to user roles |
| **Reliability Score** | A 0–100 score representing a contractor's historical performance |
| **Jurisdiction Rule** | A configurable rule defining VAT, currency, and data constraints per country |

---

*End of SRS — Procus v2 v2.0 · 21 February 2026*
