# DATABASE_SCHEMA.md

## Construction Marketplace MVP — Database Schema (Phase 1)

This document defines the core **PostgreSQL relational schema** for the Phase 1 materials marketplace.

Focus: **Quote → Confirm → Pay → Fulfill** ordering.

---

## 1. Design Principles

* Strong relational integrity
* Clear separation of vendor vs buyer data
* Support for future expansion (financing, projects)
* Auditability of all transactions

---

## 2. Core Entities

### 2.1 Users (`accounts_user`)

Stores all authenticated users.

Fields:

* id (UUID)
* email / phone
* password_hash
* role (BUYER | VENDOR | ADMIN)
* created_at

---

### 2.2 Vendors (`vendors_vendor`)

Represents supplier businesses.

Fields:

* id
* user_id (FK → accounts_user)
* business_name
* registration_number
* verified_status (PENDING/APPROVED/REJECTED)
* location
* created_at

---

### 2.3 Product Categories (`catalog_category`)

Config-driven categories.

Fields:

* id
* name (Cement, Steel, Tiles)
* active

---

### 2.4 Products (`catalog_product`)

Vendor-listed materials.

Fields:

* id
* vendor_id (FK → vendors_vendor)
* category_id (FK → catalog_category)
* name
* description
* unit (bag, ton, piece)
* base_price
* stock_quantity
* is_active
* created_at

---

## 3. Quote + Order Workflow Tables

### 3.1 Quote Request (`orders_quote_request`)

Initiated by buyer.

Fields:

* id
* buyer_id (FK → accounts_user)
* status (REQUESTED/CONFIRMED/REJECTED)
* requested_at

---

### 3.2 Quote Items (`orders_quote_item`)

Line items in quote.

Fields:

* id
* quote_request_id (FK)
* product_id (FK → catalog_product)
* quantity

---

### 3.3 Vendor Quote Response (`orders_quote_response`)

Vendor confirms pricing.

Fields:

* id
* quote_request_id (FK)
* vendor_id (FK)
* confirmed_price
* delivery_fee
* expires_at
* confirmed_at

---

### 3.4 Orders (`orders_order`)

Created only after buyer payment.

Fields:

* id
* buyer_id
* vendor_id
* quote_response_id
* status (PENDING_PAYMENT/PAID/FULFILLING/DELIVERED/CANCELLED)
* total_amount
* created_at

---

### 3.5 Order Items (`orders_order_item`)

Snapshot of purchased products.

Fields:

* id
* order_id
* product_name_snapshot
* unit_price_snapshot
* quantity

---

## 4. Payments (`payments_payment`)

Tracks buyer payments.

Fields:

* id
* order_id
* provider (Stripe/Mpesa)
* amount
* status (INITIATED/SUCCESS/FAILED)
* transaction_reference
* paid_at

---

## 5. Logistics (`logistics_delivery`)

Delivery tracking.

Fields:

* id
* order_id
* delivery_status (PENDING/DISPATCHED/DELIVERED)
* delivery_address
* delivered_at

---

## 6. Reviews (`reviews_rating`)

Buyer trust feedback.

Fields:

* id
* order_id
* buyer_id
* vendor_id
* score (1–5)
* comment
* created_at

---

## 7. Future Expansion Reserved Tables

Phase 2+ may introduce:

* Financing applications
* Escrow accounts
* Project listings
* Property assets

Schema is designed to extend cleanly.

---

**Phase 1 schema is complete and production-ready.**
