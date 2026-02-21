# DEPLOYMENT_GUIDE.md

## Construction Marketplace MVP — Deployment Guide (Phase 1)

This document defines the deployment approach for the Vue 3 + Django monorepo using Docker.

---

## 1. Deployment Principles

* One monorepo, multiple services
* Dockerized dev/staging/prod parity
* Stateless backend API
* Externalized config via environment variables

---

## 2. Required Services

Docker Compose will run:

* frontend (Vue 3 + Vite)
* backend (Django + DRF)
* postgres (database)
* redis (queue broker)
* celery-worker (async jobs)
* celery-beat (scheduled tasks)

---

## 3. Environment Variables

Provide `.env.example`:

* DATABASE_URL
* REDIS_URL
* DJANGO_SECRET_KEY
* DEBUG
* ALLOWED_HOSTS
* PAYMENT_PROVIDER_KEYS

---

## 4. Docker Compose Structure

Root `docker-compose.yml` should define:

* network: marketplace-net
* volumes: postgres-data

Services:

### backend

* build: ./backend
* exposes port 8000

### frontend

* build: ./frontend
* exposes port 5173

### postgres

* official Postgres image

### redis

* official Redis image

### celery-worker

* runs Celery worker

### celery-beat

* runs scheduled tasks

---

## 5. Local Development Workflow

1. Clone repo
2. Copy env file:

```bash
cp .env.example .env
```

3. Start stack:

```bash
docker-compose up --build
```

4. Access:

* Frontend: [http://localhost:5173](http://localhost:5173)
* Backend API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
* Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 6. Production Deployment Notes

Phase 1 production recommendations:

* Use managed Postgres (AWS RDS/Supabase)
* Use managed Redis
* Run backend behind Nginx reverse proxy
* Enable HTTPS
* Store media assets in S3

---

## 7. CI/CD Readiness

Recommended pipeline steps:

* Lint frontend
* Run Django tests
* Build Docker images
* Deploy to staging
* Promote to production

---

**Deployment foundation is now defined for Phase 1.**
