# API_SPEC.md

## Construction Marketplace MVP — API Specification (Phase 1)

This document defines the REST API contract for the Phase 1 marketplace.

Workflow:

**Request Quote → Vendor Confirms → Buyer Pays → Fulfillment**

Base URL:

`/api/v1/`

---

## 1. Authentication

### POST `/auth/login`

Login via email/phone.

Response:

* JWT access token

---

## 2. Catalog APIs

### GET `/products`

List products with filters.

Query params:

* category
* location
* search

### GET `/products/{id}`

Retrieve product detail.

---

## 3. Vendor APIs

### POST `/vendors/register`

Register vendor business.

Request:

* business_name
* registration_number
* location

Status:

* PENDING verification

---

## 4. Quote Workflow APIs

### POST `/quotes/request`

Buyer submits quote request.

Request:

* items: [{product_id, quantity}]

Response:

* quote_request_id

---

### GET `/quotes/{id}`

Retrieve quote request status.

---

### POST `/quotes/{id}/confirm`

Vendor confirms quote.

Request:

* confirmed_price
* delivery_fee
* expires_at

Response:

* quote_response_id

---

### POST `/quotes/{id}/reject`

Vendor rejects request.

---

## 5. Orders & Payments

### POST `/orders/create`

Create order after buyer accepts confirmed quote.

Request:

* quote_response_id

Response:

* order_id
* payment_required

---

### POST `/payments/initiate`

Initiate payment.

Request:

* order_id
* provider

Response:

* payment_reference

---

### GET `/orders/{id}`

Retrieve order status.

---

## 6. Logistics

### GET `/orders/{id}/delivery`

Delivery tracking.

---

## 7. Reviews

### POST `/orders/{id}/review`

Buyer rates vendor.

Request:

* score (1–5)
* comment

---

## 8. Admin Backoffice APIs

Admin uses Django Admin for Phase 1:

* Vendor approval
* Product moderation
* Order overrides

---

## 9. API Conventions

* JSON request/response
* JWT authentication
* Role-based permissions
* Pagination for listings

---

## 10. Analytics & Reporting APIs (v6)

Base URL: `/api/v6/analytics/`

Permission: `AdminOnly` (staff, superuser, or role = `ADMIN`)

All endpoints support `?days=N` (default: 30) for time-windowed queries except `geographic`.

### GET `/analytics/summary/`

High-level platform KPIs.

Response:
* users `{total, new}`
* orders `{total, new}`
* revenue `{total, period}`
* vendors `{total, approved}`
* properties `{total, active}`
* disputes `{total, open}`
* projects, contracts, pending_kyc, period_days

### GET `/analytics/financial/`

Revenue and payment analytics.

Response:
* order_trend `[{x: date, y: count}]`
* revenue_trend `[{x: date, y: amount}]`
* payment_status `[{status, count, total}]`
* aov (average order value)

### GET `/analytics/marketplace/`

Marketplace performance metrics.

Response:
* order_funnel_all `{status: count}`
* order_funnel_period `{status: count}`
* top_products `[{name, quantity_sold, revenue}]`
* vendor_leaderboard `[{name, rating, fulfillment_rate, cancellation_rate, delivery_timeliness, orders}]`
* product_status `[{status, count}]`
* low_stock_alerts `[{name, stock_quantity, reorder_level}]`

### GET `/analytics/users/`

User growth and demographics.

Response:
* role_distribution `[{role, count}]`
* signup_trend `[{x: date, y: count}]`
* activation `{active, inactive}`

### GET `/analytics/operations/`

Operational pipeline health.

Response:
* kyc_pipeline `{status: count}`
* dispute_status `{status: count}`
* contract_status `{status: count}`
* project_status `{status: count}`
* contractor_status `{status: count}`

### GET `/analytics/property/`

Real estate analytics.

Response:
* listing_status `{status: count}`
* asset_types `[{type, count}]`
* inquiry_status `{status: count}`
* appointment_status `{status: count}`
* inquiry_trend `[{x: date, y: count}]`

### GET `/analytics/geographic/`

Spatial entity data for mapping.

Response:
* vendors `[{name, lat, lng, status}]`
* projects `[{name, lat, lng, status}]`
* properties `[{name, lat, lng, status, type}]`
* orders `[{lat, lng, status}]`

---

**Phase 1 API contract is now defined.**
