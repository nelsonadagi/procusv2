# MONOREPO_BOOTSTRAP.md

## Construction Marketplace MVP — Monorepo Bootstrap Guide

This document defines the exact steps to initialize the production-ready Vue 3 + Django monorepo.

---

## 1. Repository Structure

```
construction-marketplace/
├── frontend/
├── backend/
├── infra/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 2. Frontend Bootstrap (Vue 3 + Vite)

Run:

```bash
cd frontend
npm create vite@latest . -- --template vue
npm install
npm run dev
```

Add dependencies:

* axios
* vue-router
* pinia

---

## 3. Backend Bootstrap (Django + DRF)

Run:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework psycopg2-binary celery redis

django-admin startproject config .
python manage.py startapp accounts
python manage.py startapp catalog
python manage.py startapp orders
```

Enable DRF in `INSTALLED_APPS`.

---

## 4. Database Setup (Postgres)

Use Docker Postgres.

Update Django settings:

* DATABASES via env var

---

## 5. Celery Setup

Create `config/celery.py`:

* Connect Redis broker
* Autodiscover tasks

Run worker:

```bash
celery -A config worker -l info
```

---

## 6. Docker Compose Baseline

Root `docker-compose.yml` should include:

* frontend
* backend
* postgres
* redis
* celery-worker

---

## 7. First Working API Endpoint

In `catalog/views.py`:

* GET /api/v1/products

Test:

```bash
curl http://localhost:8000/api/v1/products
```

---

## 8. First Frontend Integration

In Vue:

* Fetch products via axios
* Render product list

Deliverable:

Frontend displays backend product API results.

---

## 9. Immediate Next Implementation Steps

1. Vendor registration flow
2. Quote request endpoint
3. Vendor confirm quote UI
4. Payment placeholder

---

**Monorepo bootstrap is now defined. Ready to start coding Phase 1.**
