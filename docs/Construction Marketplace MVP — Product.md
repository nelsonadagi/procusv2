# Construction Marketplace MVP — Production-Ready Monorepo Docs

This document defines the **Phase 1 Materials Marketplace MVP** using a **production-ready monorepo** architecture.

---

## Tech Stack (Phase 1)

* **Frontend:** Vue 3 (Vite)
* **Backend:** Django + Django REST Framework
* **Database:** PostgreSQL
* **Async Jobs:** Celery + Redis
* **Infrastructure:** Docker + Docker Compose
* **Backoffice:** Django Admin

---

## Monorepo Structure

```
construction-marketplace/
├── frontend/              # Vue 3 (Vite) app
├── backend/               # Django project
├── infra/                 # Docker + deployment configs
├── docs/                  # All markdown documentation
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## Roles & Permissions

### Buyer

* Browse catalog
* Place orders
* Track fulfillment

### Vendor

* Manage products
* Confirm orders
* Update stock/pricing

### Admin

* Approve vendors
* Moderate listings
* Resolve disputes

---

## Django App Modules

Recommended Django apps:

* `accounts` (auth + roles)
* `vendors` (vendor profiles, verification)
* `catalog` (products, categories)
* `orders` (checkout + fulfillment)
* `payments` (payment intents)
* `logistics` (delivery tracking)
* `reviews` (ratings)

---

## MVP Scope

### Included

* Vendor onboarding + verification
* Product catalog + search
* Order placement workflow
* Notifications (placeholder)
* Basic ratings

### Excluded (Phase 2+)

* Financing
* Full escrow
* Projects marketplace
* Property listings

---

## Core API Endpoints

### Catalog

* GET `/api/products`
* GET `/api/products/{id}`

### Vendors

* POST `/api/vendors/register`

### Orders

* POST `/api/orders`
* GET `/api/orders/{id}`

---

## Async Tasks (Celery)

* Send order confirmation
* Notify vendor of new order
* Generate invoice (later)

---

## Docker Compose Services

* frontend
* backend
* postgres
* redis
* celery-worker
* celery-beat

---

## Customization Principles

Design for configurability:

* Theme + branding variables
* Config-driven categories
* Feature flags per region
* Modular Django apps

---

## Phase 1 Success Metrics

* Active vendors ≥ 20
* Orders/month ≥ 50
* Delivery success ≥ 90%
* Repeat buyers ≥ 30%

---

## Next Required Markdown Docs

Place these under `/docs`:

1. `SYSTEM_REQUIREMENTS.md`
2. `DATABASE_SCHEMA.md`
3. `API_SPEC.md`
4. `DEPLOYMENT_GUIDE.md`
5. `SECURITY_CHECKLIST.md`
6. `CUSTOMIZATION_GUIDE.md`
7. `PHASE1_EXECUTION_PLAN.md`

---

**Monorepo foundation is now defined and ready for implementation.**

---

## Phase 1 Checkout Model

Phase 1 will follow a **Request Quote → Vendor Confirms → Buyer Pays** workflow.

This is the recommended approach for construction materials where:

* Pricing varies by volume and location
* Stock availability changes frequently
* Delivery fees require confirmation

The platform will support:

1. Buyer requests a quote/order
2. Vendor confirms price + availability
3. Buyer completes payment
4. Delivery is scheduled and fulfilled

This workflow will be formalized in `API_SPEC.md` and `PHASE1_EXECUTION_PLAN.md`.
