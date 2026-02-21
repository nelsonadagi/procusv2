# SYSTEM_REQUIREMENTS.md

## Construction Marketplace MVP — System Requirements (Phase 1)

This document defines the **functional** and **non-functional** requirements for Phase 1 of the Construction Materials Marketplace.

---

## 1. Objective

Phase 1 delivers a production-ready marketplace enabling:

* Vendor onboarding and verification
* Materials listing and discovery
* Quote-based ordering workflow
* Admin operational control

Primary transaction model:

**Request Quote → Vendor Confirms → Buyer Pays → Delivery Fulfilled**

---

## 2. Core User Roles

### Buyer

* Browse and search materials
* Request quotes
* Confirm payment after vendor approval
* Track order fulfillment

### Vendor

* Register and complete verification
* Upload products and manage stock
* Respond to quote requests
* Fulfill confirmed orders

### Admin (Backoffice)

* Approve vendors
* Moderate listings
* Override order states
* Resolve disputes

---

## 3. Functional Requirements

### 3.1 Vendor Management

* Vendor registration
* Verification workflow (manual Phase 1)
* Vendor storefront/profile

### 3.2 Product Catalog

* Structured categories (cement, steel, tiles)
* Unit-based pricing
* Stock availability
* Product moderation

### 3.3 Buyer Discovery

* Search and filtering
* Location-aware results
* Product detail pages

### 3.4 Quote-Based Ordering

* Buyer submits quote request
* Vendor confirms price + availability
* Buyer completes payment
* Order moves to fulfillment

### 3.5 Notifications

* Vendor notified of new quote request
* Buyer notified of vendor confirmation
* Order status updates

### 3.6 Backoffice Operations

* Admin dashboards via Django Admin
* Order dispute and override controls

### 3.7 Configurable Platform Layer (Global Customization)

* **Platform Branding**: Centralized management of names, logos, and support details.
* **Localization**: Regional defaults for currency, language, and compliance rules.
* **Gateway Orchestration**: Hot-swappable payment and messaging configurations.
* **Modular features**: Feature flags to enable/disable specific hubs (Financing, Tenders) without code changes.

---

## 4. Non-Functional Requirements

### 4.1 Scalability

* Support city-by-city expansion
* Modular Django apps
* Stateless API services

### 4.2 Reliability

* > 99% uptime target
* Transaction-safe order processing

### 4.3 Security

* Role-based access control
* Vendor verification
* Secure payment handling

### 4.4 Maintainability

* Monorepo structure
* Dockerized environments
* Clear separation of concerns

### 4.5 Customizability

* Config-driven categories
* Feature flags by region
* Branding and theme variables

---

## 5. Phase 1 Success Criteria

* Active vendors ≥ 20
* Transactions/month ≥ 50
* Delivery success ≥ 90%
* Repeat buyers ≥ 30%

---

**Phase 1 requirements are now defined and ready for implementation.**
