# Construction Marketplace MVP (POC → Production-Ready)

This document set defines the **Phase 1 Materials Marketplace MVP** using:

- **Frontend:** Nuxt 3 (Vue 3)
- **Backend:** Django + Django REST Framework
- **DB:** PostgreSQL
- **Async:** Celery + Redis
- **Infra:** Docker Compose
- **Backoffice:** Django Admin

The goal is a **production-grade foundation** that is highly customizable.

---

## 1. Product Vision (Phase 1)

Build a marketplace where:

- Vendors upload construction materials
- Buyers search and place orders
- Admins verify vendors and manage disputes

Phase 1 focuses only on **materials liquidity**.

---

## 2. Roles & Permissions

### Buyer
- Browse catalog
- Place orders
- Track fulfillment

### Vendor
- Manage products
- Confirm orders
- Update stock/pricing

### Admin (Backoffice)
- Approve vendors
- Moderate listings
- Resolve disputes

---

## 3. MVP Scope

### Included
- Vendor onboarding + verification
- Product catalog + search
- Order placement workflow
- Notifications (email/SMS placeholder)
- Basic ratings

### Excluded (Later)
- Financing
- Full escrow
- Projects marketplace
- Property listings

---

## 4. System Architecture

```
Nuxt 3 Frontend
      |
REST API (DRF)
      |
PostgreSQL  + Redis
      |
Celery Workers
      |
Django Admin Backoffice
```

---

## 5. Django App Modules

Recommended Django apps:

- `accounts` (auth + roles)
- `vendors` (vendor profiles, verification)
- `catalog` (products, categories)
- `orders` (checkout + fulfillment)
- `payments` (payment intents)
- `logistics` (delivery tracking)
- `reviews` (ratings)

---

## 6. Core Data Models (Simplified)

### Vendor
- name
- business_registration
- verified_status

### Product
- vendor
- category
- unit_price
- stock_qty

### Order
- buyer
- status
- total_amount

### OrderItem
- product
- quantity

---

## 7. API Endpoints (Phase 1)

### Auth
- POST `/api/auth/login`

### Catalog
- GET `/api/products`
- GET `/api/products/{id}`

### Vendor
- POST `/api/vendors/register`

### Orders
- POST `/api/orders`
- GET `/api/orders/{id}`

---

## 8. Backoffice Operations

Use Django Admin for:

- Vendor approval
- Product moderation
- Order overrides
- Dispute resolution

---

## 9. Async Tasks (Celery)

Background jobs:

- Send order confirmation
- Notify vendor of new order
- Generate invoice PDF (later)

---

## 10. Docker Compose Baseline

Services:

- frontend
- backend
- postgres
- redis
- celery-worker
- celery-beat

---

## 11. Customization Principles

Design for configurability:

- Theme + branding variables
- Config-driven categories
- Feature flags per region
- Modular Django apps

---

## 12. Phase 1 Success Metrics

- Active vendors ≥ 20
- Orders/month ≥ 50
- Delivery success ≥ 90%
- Repeat buyers ≥ 30%

---

## Next Document Suggestions

You should add separate markdown files for:

- `DATABASE_SCHEMA.md`
- `DEPLOYMENT_GUIDE.md`
- `SECURITY_CHECKLIST.md`
- `ROADMAP_PHASE2.md`

---

**Ready to begin implementation.**

