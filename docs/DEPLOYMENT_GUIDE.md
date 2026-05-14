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

Local Docker uses Compose defaults and does not require a `.env` file. For the normal Docker production deployment, provide only these required values through the deployment environment, CI/CD secrets, Docker secrets, or the orchestrator secret store:

* PUBLIC_DOMAIN
* POSTGRES_PASSWORD
* DJANGO_SECRET_KEY

The production compose file derives the rest from those three values. Override these only when the deployment needs custom infrastructure:

* DATABASE_URL
* REDIS_URL
* ALLOWED_HOSTS
* CORS_ALLOWED_ORIGINS
* CSRF_TRUSTED_ORIGINS
* VITE_API_URL
* VITE_WS_URL
* PAYMENT_PROVIDER_KEYS

The helper script can generate the required secret values for a Docker deployment run:

```bash
scripts/deploy-prod.sh your-domain.example --config
scripts/deploy-prod.sh your-domain.example
```

The script does not create a `.env` file. For local Docker deployments, it saves generated secrets in `.deploy/prod-vars.sh`, which is ignored by git, so redeploys reuse the same Postgres password and Django secret. The Postgres image creates the configured database automatically on first boot when the database volume is empty.

For repeatable production redeploys, generate the exports once and save them in the host or CI/CD secret store:

```bash
scripts/generate-prod-vars.sh your-domain.example
```

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
2. Start stack:

```bash
docker-compose up --build
```

3. Access:

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
