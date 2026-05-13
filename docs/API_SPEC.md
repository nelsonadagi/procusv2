# API_SPEC.md

## Construction Marketplace — Full API Specification

This document defines the REST API contracts across all platform phases.

---

## Base URLs by Version

| Version | Base Path | Scope |
|---------|-----------|-------|
| v1 | `/api/v1/` | Catalog & marketplace (legacy) |
| v2 | `/api/v2/` | Contractors, contracts, bids, milestones |
| v3 | `/api/v3/` | Escrow, finance, disputes, scoring |
| v4 | `/api/v4/` | Projects, property |
| v5 | `/api/v5/` | Regulation, investors, compliance, risk |
| v6 | `/api/v6/` | Banking, analytics, liquidity, ERP |
| accounts | `/api/accounts/` | User management, profiles, addresses |
| orders | `/api/orders/` | Quote requests, orders, checkout |
| chat | `/api/chat/` | Real-time messaging rooms |

---

## 1. Authentication

### POST `/api/accounts/login/`

Login via email/password.

**Response:**
- JWT access token
- Refresh token
- User profile summary

### POST `/api/accounts/register/`

Register new account.

**Request:**
- email, first_name, last_name, password

**Response:**
- User object
- Default role: `PROJECT_OWNER`

### GET `/api/accounts/profile/`

Retrieve current user profile.

### PATCH `/api/accounts/profile/`

Update profile fields.

---

## 2. Catalog APIs (v1)

### GET `/api/v1/products/`

List products with filters.

**Query params:**
- category__slug, region, search, ordering

### GET `/api/v1/products/{id}/`

Retrieve product detail.

---

## 3. Vendor APIs (v1)

### POST `/api/vendors/register/`

Register vendor business.

**Request:**
- business_name, registration_number, location, categories

**Status:** `PENDING` until admin approval.

---

## 4. Quote & Order Workflow APIs (orders)

### POST `/api/orders/quote-requests/`

Buyer submits quote request.

**Request:**
- items: `[{product_id, quantity}]`

### POST `/api/orders/quote-requests/{id}/respond/`

Vendor responds with pricing.

**Request:**
- items: `[{id, unit_price, availability_notes}]`
- delivery_fee, valid_until

### POST `/api/orders/quote-requests/{id}/checkout/`

Buyer accepts quote and creates order.

**Request:**
- response_id

**Side effects:**
- Creates `Order` with `status: PLACED`, `payment_status: UNPAID`
- Creates `Payment` intent with `provider: MODERN_CHECKOUT`
- Reserves inventory via atomic transaction

### GET `/api/orders/orders/`

List orders for authenticated user.

**Permissions:** Buyers see own orders; vendors see orders assigned to them.

### POST `/api/orders/orders/{id}/update_fulfillment/`

Vendor updates order status.

**Request:**
- status: `CONFIRMED`, `PACKING`, `SHIPPED`, `DELIVERED`, `CANCELLED`
- tracking_number (if `SHIPPED`)
- carrier_code (if `SHIPPED`)

### POST `/api/orders/orders/{id}/confirm_delivery/`

Buyer confirms receipt. Order status → `COMPLETED`.

### POST `/api/orders/orders/{id}/cancel_order/`

Cancel order (only if `PLACED` or `CONFIRMED`). Restocks inventory.

### POST `/api/orders/orders/{id}/initiate_dispute/`

Open dispute. Request: reason.

---

## 5. Payments APIs

### Model-Only (No Direct Endpoints)

The `payments` app currently has no dedicated viewset. Payments are created implicitly during checkout.

**Payment Status Flow:**
```
UNPAID → PENDING → PAID
           ↓
         FAILED
```

**Planned Integrations:** M-Pesa Daraja, Stripe Checkout, Flutterwave.

---

## 6. Contract & Contractor APIs (v2)

### GET `/api/v2/contracts/`

List contracts with filters.

**Query params:**
- search, location, status, budget_min, budget_max, sort_by

### POST `/api/v2/contracts/`

Create new contract/tender.

**Request:**
- title, description_scope, location, budget_min, budget_max
- currency, category_uuid, bid_deadline
- project_start_date, project_end_date
- payment_terms, eligibility_criteria
- featured_image (file)

### GET `/api/contracts/{id}/`

Retrieve contract detail.

### POST `/api/contracts/{id}/publish/`

Publish contract to marketplace.

### POST `/api/contracts/{id}/bids/`

Submit bid (contractor only).

**Request:**
- proposed_cost, proposed_timeline_days, message

### GET `/api/contracts/{id}/bids/`

List bids.

**Permissions:** Owner sees all bids; contractors see only their own.

### POST `/api/contracts/{id}/milestones/`

Add milestone (owner/admin).

**Request:**
- title, description, amount, due_date

### GET `/api/contracts/{id}/milestones/`

List milestones.

### POST `/api/milestones/{id}/complete/`

Contractor marks milestone complete.

### POST `/api/milestones/{id}/approve/`

Owner approves milestone. Triggers escrow release if applicable.

### POST `/api/bids/{id}/award/`

Owner awards contract to bidder.

### POST `/api/bids/{id}/shortlist/`

Owner shortlists a bid.

---

## 7. Project APIs (v4)

### GET `/api/v4/projects/`

List projects with filters.

**Query params:**
- search, location, status, budget_min, budget_max, owner=me, sort_by
- latitude, longitude, radius_km (GIS proximity)

### POST `/api/v4/projects/`

Create project.

### GET `/api/v4/projects/{id}/`

Retrieve project detail with nested requirements, updates, commitments, linked contracts.

### PATCH `/api/v4/projects/{id}/`

Update project. Status transitions validated.

### DELETE `/api/v4/projects/{id}/`

Delete project (owner/admin).

### POST `/api/v4/projects/{id}/requirements/`

Add requirement.

### DELETE `/api/v4/projects/{id}/requirements/{req_id}/`

Remove requirement.

### POST `/api/v4/projects/{id}/commit/`

Pledge investment commitment.

**Request:**
- amount_committed

**Validation:**
- Amount > 0
- funding_required must be true
- Total committed + amount ≤ estimated_budget

### POST `/api/v4/projects/{id}/link-contract/`

Link an awarded contract to project.

### DELETE `/api/v4/projects/{id}/linked-contracts/{link_id}/`

Unlink contract.

### POST `/api/v4/projects/{id}/updates/`

Post project update.

### DELETE `/api/v4/projects/{id}/updates/{upd_id}/`

Remove update.

---

## 8. Escrow APIs (v3)

### POST `/api/v3/escrow/deposit/`

Deposit funds into contract escrow.

**Request:**
- contract_id, amount

**Permissions:** `escrow:deposit_funds`

**Validation:** Caller must be contract owner.

**Response:**
- status, balance

### POST `/api/v3/escrow-releases/trigger/`

Release funds for an approved milestone.

**Request:**
- milestone_id

**Permissions:** `escrow:release_funds`

**Validation:**
- Escrow account must exist
- No active dispute holds
- Sufficient balance ≥ milestone.amount

**Side effects:**
- Deducts from escrow balance
- Creates `EscrowTransaction` (type: RELEASE)
- Creates `EscrowRelease` record
- Milestone status → `PAID`

### GET `/api/v3/escrow/`

List escrow accounts (owner sees own; admin sees all).

### GET `/api/v3/escrow-releases/`

List release records.

---

## 9. Finance APIs (v3)

### GET `/api/v3/finance/products/`

List active finance products (public).

**Response:**
- id, name, provider_name, max_amount, interest_rate, active

### GET `/api/v3/finance/applications/`

List your finance applications.

**Permissions:** `finance:view`

### POST `/api/v3/finance/applications/`

Submit finance application.

**Request:**
- product_id, target_type, requested_amount
- purpose_category, purpose
- property_id (optional), project_id (optional)

**Permissions:** `finance:apply`

**Target Types:**
- `PROPERTY`, `PROJECT`, `MATERIAL_ORDER`, `CONTRACT`, `GENERAL_WORKING_CAPITAL`

**Purpose Categories:**
- `ACQUISITION`, `COMPLETION`, `RENOVATION`, `MATERIALS_PROCUREMENT`, `WORKING_CAPITAL`

### PATCH `/api/v3/finance/applications/{id}/`

Update application (before approval).

---

## 10. Investor & Agreement APIs (v5)

### GET `/api/v5/investors/`

Retrieve investor profile.

**Permissions:** `investments:view`

### POST `/api/v5/investors/onboard/`

Create investor profile.

**Request:**
- kyc_status, accreditation_status, jurisdiction

**Permissions:** `investments:onboard`

### GET `/api/v5/agreements/`

List investment agreements.

### POST `/api/v5/agreements/`

Create agreement (typically by project owner).

### POST `/api/v5/agreements/{id}/sign/`

Sign agreement as investor.

**Validation:** Caller must be agreement.investor.

**Side effects:**
- status → `SIGNED`
- signed_at timestamp set

---

## 11. Banking APIs (v6)

### GET `/api/v6/bank-accounts/`

List your registered bank accounts.

**Permissions:** `banking:view`

### POST `/api/v6/bank-accounts/`

Add bank account.

**Request:**
- bank_name, account_number_last4, routing_number, currency

**Permissions:** `banking:manage_accounts`

### GET `/api/v6/settlements/`

List settlement transactions.

---

## 12. Secondary Market APIs (v6)

### GET `/api/v6/secondary-trades/`

List trade requests.

**Permissions:** `investments:view`

**Query:**
- status: `REQUESTED`, `APPROVED`, `COMPLETED`, `REJECTED`

### POST `/api/v6/secondary-trades/`

Create trade listing (sell stake).

**Request:**
- investment_agreement_id, amount, price

**Permissions:** `investments:transfer_stake`

---

## 13. Analytics & Reporting APIs (v6)

Base URL: `/api/v6/analytics/`

Permission: `AdminOnly`

All endpoints support `?days=N` (default: 30).

### GET `/api/v6/analytics/summary/`

High-level platform KPIs.

### GET `/api/v6/analytics/financial/`

Revenue and payment analytics.

**Response:**
- order_trend `[{x: date, y: count}]`
- revenue_trend `[{x: date, y: amount}]`
- payment_status `[{status, count, total}]`
- aov (average order value)

### GET `/api/v6/analytics/marketplace/`

Marketplace performance metrics.

### GET `/api/v6/analytics/users/`

User growth and demographics.

### GET `/api/v6/analytics/operations/`

Operational pipeline health.

### GET `/api/v6/analytics/property/`

Real estate analytics.

### GET `/api/v6/analytics/geographic/`

Spatial entity data for mapping.

---

## 14. Chat APIs

### POST `/api/chat/rooms/get-or-create/`

Get or create chat room.

**Request:**
- contract (optional), order (optional), user_id (optional)

### WebSocket

Real-time messaging via WebSocket connection to chat room.

---

## 15. API Conventions

- **Format**: JSON request/response
- **Auth**: JWT Bearer token in `Authorization` header
- **Permissions**: RBAC via `HasRequiredPermission` with action-level permission maps
- **Pagination**: Default page size for list endpoints
- **Errors**: Standard DRF error format with `detail` or field-level messages
- **Throttling**: `payment_gateway` scope for escrow/financial endpoints

---

*API Spec v2.0 — Covers Phases 1–6*
