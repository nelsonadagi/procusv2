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

**Phase 1 API contract is now defined.**
