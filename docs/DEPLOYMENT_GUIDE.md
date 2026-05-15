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

## 3. Production Variables

Local Docker uses Compose defaults and does not require a `.env` file. For the normal Docker production deployment, provide only these required values through the deployment environment, CI/CD secrets, Docker secrets, or the orchestrator secret store:

```bash
export PUBLIC_DOMAIN=paanguzo.iqsaccodigital.com
export POSTGRES_PASSWORD='<generated-by-scripts-deploy-prod>'
export DJANGO_SECRET_KEY='<generated-by-scripts-deploy-prod>'
```

The production compose file derives the rest from those three values. Override these only when the deployment needs custom infrastructure:

* DATABASE_URL
* REDIS_URL
* ALLOWED_HOSTS
* CORS_ALLOWED_ORIGINS
* CSRF_TRUSTED_ORIGINS
* VITE_API_URL
* VITE_WS_URL
* PAYMENT_PROVIDER_KEYS

For this deployment, the derived values are:

```env
POSTGRES_DB=marketplace
POSTGRES_USER=postgres
DATABASE_URL=postgres://postgres:<POSTGRES_PASSWORD>@postgres:5432/marketplace
ALLOWED_HOSTS=paanguzo.iqsaccodigital.com
CORS_ALLOWED_ORIGINS=https://paanguzo.iqsaccodigital.com
CSRF_TRUSTED_ORIGINS=https://paanguzo.iqsaccodigital.com
VITE_API_URL=https://paanguzo.iqsaccodigital.com/api
VITE_WS_URL=wss://paanguzo.iqsaccodigital.com/ws/notifications/
```

The helper script can generate and persist the required secret values for this Docker deployment:

```bash
scripts/deploy-prod.sh paanguzo.iqsaccodigital.com --config
scripts/deploy-prod.sh paanguzo.iqsaccodigital.com
```

The script does not create a `.env` file. For local Docker deployments, it saves generated secrets in `.deploy/prod-vars.sh`, which is ignored by git, so redeploys reuse the same Postgres password and Django secret. The Postgres image creates the configured database automatically on first boot when the database volume is empty.

During deployment, the helper also runs `scripts/prepare-postgres.sh`. That script starts Postgres, sets the `postgres` user password to the saved deployment password, creates the `marketplace` database if it does not exist, and verifies that Django can connect before the backend is started.

For repeatable production redeploys, generate the exports once and save them in the host or CI/CD secret store:

```bash
scripts/generate-prod-vars.sh paanguzo.iqsaccodigital.com
```

---

## 4. Copy-Paste Production Deployment

Run these commands on the production server from the repository root.

### First Deploy

```bash
git pull
scripts/deploy-prod.sh --config
scripts/deploy-prod.sh
```

### Redeploy Existing Server

The first deploy creates `.deploy/prod-vars.sh`. Keep that file on the server so Postgres and Django reuse the same secrets.

```bash
git pull
scripts/deploy-prod.sh --config
scripts/deploy-prod.sh
```

### Manual Export Alternative

Use this only if the three values are stored by your hosting platform or CI/CD secrets:

```bash
export PUBLIC_DOMAIN=paanguzo.iqsaccodigital.com
export POSTGRES_PASSWORD='<saved-postgres-password>'
export DJANGO_SECRET_KEY='<saved-django-secret-key>'

make prod-config
make prod
```

### Check Logs

```bash
scripts/prod-compose.sh ps
scripts/prod-compose.sh logs -f --tail=150
```

### Backend Stuck Waiting For Postgres

If backend logs repeat this:

```text
Postgres is unavailable - sleeping
```

but `scripts/prod-compose.sh ps` shows Postgres is healthy, run the Postgres preparation script:

```bash
scripts/prepare-postgres.sh
scripts/prod-compose.sh up -d --force-recreate backend celery-worker celery-beat
scripts/prod-compose.sh logs backend --tail=120
```

Only use a volume reset when you intentionally want to delete and recreate the database:

```bash
scripts/prod-compose.sh down -v
scripts/deploy-prod.sh
```

### Stop Production Stack

```bash
scripts/prod-compose.sh down
```

Do not remove volumes unless you intentionally want to delete the database:

```bash
scripts/prod-compose.sh down -v
```

---

## 5. Docker Compose Structure

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

## 6. Local Development Workflow

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

## 7. Production Deployment Notes

Phase 1 production recommendations:

* Keep `.deploy/prod-vars.sh` backed up or move the values into a secret store
* Do not commit `.deploy/`, `.env`, or any secret file
* Point DNS for `paanguzo.iqsaccodigital.com` to the production server
* Terminate HTTPS at the host reverse proxy or load balancer
* Run backend behind a reverse proxy
* Enable HTTPS
* Use managed Postgres and Redis when moving beyond single-server Docker
* Store media assets in S3-compatible storage when moving beyond single-server Docker

---

## 8. CI/CD Readiness

Recommended pipeline steps:

* Lint frontend
* Run Django tests
* Build Docker images
* Deploy to staging
* Promote to production

---

**Deployment foundation is now defined for Phase 1.**
